"""This module provide classes and functions for reading/writing DataFrameDirectory."""
import os
from pathlib import Path
from typing import Union

import pandas as pd
from pandas.core.dtypes.common import is_categorical_dtype

from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.error import (DirectoryEmptyError, InvalidDirectoryError)
from azureml.studio.core.io.any_directory import (AnyDirectory, DirectoryLoadError, DirectorySaveError, Meta,
                                                  os_io_error_handler)
from azureml.studio.core.io.data_frame_utils import (_get_arrow_index_names, _remove_arrow_bug_columns,
                                                     data_frame_from_parquet, data_frame_to_csv, data_frame_to_parquet)
from azureml.studio.core.io.data_frame_visualizer import DataFrameVisualizer
from azureml.studio.core.schema import ElementTypeName
from azureml.studio.core.utils.jsonutils import load_json_file

_DEFAULT_DATA_PATH = '_data.parquet'
PARQUET_FORMAT = 'Parquet'
CSV_FORMAT = 'CSV'
_DEFAULT_FORMAT = PARQUET_FORMAT

_DUMPERS = {
    PARQUET_FORMAT: data_frame_to_parquet,
    CSV_FORMAT: data_frame_to_csv,
}
_LOADERS = {
    PARQUET_FORMAT: data_frame_from_parquet,
}


class DataFrameDirectory(AnyDirectory):
    """A DataFrameDirectory should store pandas.DataFrame data and related meta data in the directory."""
    TYPE_NAME = 'DataFrameDirectory'

    _SCHEMA_FILE_PATH = 'schema/_schema.json'

    def __init__(self, data: pd.DataFrame = None, schema=None, meta: Meta = None):
        super().__init__(meta)
        self._schema = schema
        self._data = data
        self._schema_instance = None

    @classmethod
    def create(cls,
               data: pd.DataFrame = None,
               file_path=_DEFAULT_DATA_PATH,
               file_format=_DEFAULT_FORMAT,
               schema=None,
               compute_schema_if_not_exist=True,
               compute_visualization=True,
               compute_stats_in_visualization=False,
               visualizers=None,
               extensions=None):
        """A DataFrameDirectory is created by a pandas DataFrame, the schema of the DataFrame and other metas.

        :param data: A pandas DataFrame.
        :param file_path: The relative path to store the data.
        :param file_format: The format to dump the data.
        :param schema: The schema is a jsonable dict to describe the detailed info in data.
        :param compute_schema_if_not_exist: Compute schema with data when schema is missing.
        :param compute_visualization: Compute visualization with data and schema when visualizer is missing.
        :param compute_stats_in_visualization: Compute statistics when computing visualization.
        :param visualizers: See AnyDirectory
        :param extensions: See AnyDirectory
        """
        if not schema and compute_schema_if_not_exist and data is not None:
            schema = DataFrameSchema.data_frame_to_dict(data)

        if schema and not isinstance(schema, dict):
            raise TypeError(f"Input argument 'schema' has invalid type {type(schema)}, expected: dict.")

        # fix bug 828135: remove arrow index names like '__index_level_0__' from df and schema
        # because such a column name is the same as the index generated by arrow.
        if isinstance(data, pd.DataFrame) and isinstance(schema, dict):
            schema_instance = DataFrameSchema.from_dict(schema)
            data, rebuilt_schema_instance = cls.remove_arrow_bug_columns_from_data_frame_and_schema(
                df=data, schema=schema_instance)
            schema = rebuilt_schema_instance.to_dict()
        if not visualizers and compute_visualization and data is not None and schema is not None:
            visualizers = [DataFrameVisualizer(data, schema, compute_stats=compute_stats_in_visualization)]
        meta = cls.create_meta(visualizers, extensions, file_format, file_path)
        return cls(data, schema, meta)

    @classmethod
    def remove_arrow_bug_columns_from_data_frame_and_schema(cls, df: pd.DataFrame, schema: DataFrameSchema):
        invalid_columns = [name for name in _get_arrow_index_names(df) if name in df.columns]
        # Remove invalid columns in meta data by selecting valid ones.
        # Do not delete columns in meta data using schema.column_attributes.remove, because score or label column
        # indexes will not be adjusted accordingly.
        # TODO: add method remove_column to class DataFrameSchema.
        selected_columns = [col for col in df.columns if col not in invalid_columns]
        schema_new = schema.select_columns(selected_columns)

        # Remove invalid columns in data frame.
        df = _remove_arrow_bug_columns(df)
        return df, schema_new

    @classmethod
    def create_meta(
            cls,
            visualizers: list = None,
            extensions: dict = None,
            file_format=_DEFAULT_FORMAT,
            file_path=_DEFAULT_DATA_PATH,
    ):
        meta = super().create_meta(visualizers, extensions)
        meta.update_field('format', file_format)
        meta.update_field('data', file_path)
        return meta

    @property
    def file_format(self):
        return self.meta.format

    @property
    def schema_data(self):
        return self._schema

    @property
    def schema(self):
        return self._schema

    @property
    def data(self):
        return self._data

    @classmethod
    def create_from_data(cls, data, schema):
        if schema:
            if isinstance(schema, dict):
                schema = DataFrameSchema.from_dict(schema)
            return cls.create(pd.DataFrame(data, columns=schema.column_attributes.names), schema)
        return cls.create(pd.DataFrame(data))

    def __len__(self):
        if self.data is None:
            return 0
        return self.data.shape[0]

    def get_item(self, idx):
        row = self.data.iloc[idx]

        # In some corner cases, DataFrame.iloc is not a series, need to be handled properly.
        if not isinstance(row, pd.Series):
            # 1. A DataFrame with only one categorical column will return a single value.
            if self.data.shape[1] == 1 and self.schema_instance.get_element_type(0) == ElementTypeName.CATEGORY:
                return {self.get_column_name(0): row}

        # For the normal case, we try to return row.to_dict
        return row.to_dict()

    def dump(self, save_to, meta_file_path=None, overwrite_if_exist=True, validate_if_exist=False):
        """Dump the DataFrame to the directory and and store the yaml file for meta.

        :param save_to: See AnyDirectory
        :param meta_file_path: See AnyDirectory
        :param overwrite_if_exist: If overwrite_if_exist, overwrite the data if the file already exists.
        :param validate_if_exist: If validate_if_exist, make sure the exist file at file_path is a valid DataFrame.
        """

        with os_io_error_handler():
            full_path = self.full_data_path(save_to)
            if overwrite_if_exist or not os.path.exists(full_path):
                DataFrameDirectory.dump_data(self.data, full_path, self.file_format)
            elif validate_if_exist:
                # When the file doesn't exist,
                # if validate_if_exist, try loading data to guarantee the directory is valid,
                DataFrameDirectory.load_data(full_path, self.file_format)
                # otherwise we trust that the file is a valid DataFrame file.

            super().dump(save_to, meta_file_path=meta_file_path)

    def full_data_path(self, folder):
        if hasattr(self._meta, 'data'):
            return os.path.join(folder, self._meta.data)
        # For compatibility of the DFD in alghost-core<=0.0.16
        elif hasattr(self._meta, 'file_path'):
            return os.path.join(folder, self._meta.file_path)
        raise ValueError(f"File path is not provided in meta file.")

    def get_column_index(self, col_name):
        return self.data.columns.get_loc(col_name)

    def get_column_type(self, col_key):
        return self.schema_instance.get_column_type(col_key)

    def get_element_type(self, col_key):
        return self.schema_instance.get_element_type(col_key)

    def get_underlying_element_type(self, col_key):
        elm_type = self.schema_instance.get_underlying_element_type(col_key)
        # This is for backward compatibility that in old meta_data, underlying element type doesn't exist.
        # So we need to infer the element type and update the meta_data.
        if elm_type == ElementTypeName.CATEGORY and elm_type is None:
            self.schema_instance.infer_underlying_element_type(self.data)
            elm_type = self.schema_instance.get_underlying_element_type(col_key)
        return elm_type

    def get_column_name(self, col_index):
        return self.data.columns[col_index]

    @property
    def schema_instance(self):
        if not self._schema_instance:
            if self.schema is not None:
                self._schema_instance = DataFrameSchema.from_dict(self.schema)
            elif self.data is not None:
                self._schema_instance = DataFrameSchema.from_data_frame(self.data)
            else:
                raise ValueError("Neither schema nor data is provided, schema_instance cannot be computed.")
        return self._schema_instance

    @staticmethod
    def dump_data(data, full_path, file_format=_DEFAULT_FORMAT):
        """Dump the data to the specified full_path with file_format."""
        dumper = _DUMPERS.get(file_format, None)
        if not dumper:
            raise NotImplementedError(f"The dumper of file format '{file_format}' is not supported now.")
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"{pd.DataFrame.__name__} is required, got {data.__class__.__name__}")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        dumper(data, full_path)

    @staticmethod
    def load_data(full_path, file_format=_DEFAULT_FORMAT, schema=None):
        """Load the data with the specified full_path with file_format."""
        loader = _LOADERS.get(file_format, None)
        if not loader:
            raise NotImplementedError(f"The loader of file format {file_format} is not supported now.")
        df = loader(full_path)
        if schema:
            DataFrameDirectory.update_schema_according_to_data(df, schema)
        return df

    @staticmethod
    def update_schema_according_to_data(data: pd.DataFrame, schema: Union[dict, DataFrameSchema]):
        for col_index, col_name in enumerate(data):
            column = data[col_name]
            # This is to update column type in schema according to dataframe.
            if column.dtype == ElementTypeName.FLOAT:
                if isinstance(schema, dict):
                    if schema["columnAttributes"][col_index]["elementType"]["typeName"] == ElementTypeName.INT:
                        schema["columnAttributes"][col_index]["elementType"]["typeName"] = ElementTypeName.FLOAT

                elif isinstance(schema, DataFrameSchema):
                    if schema.get_element_type(col_name) == ElementTypeName.INT:
                        schema.column_attributes[col_name].element_type = ElementTypeName.FLOAT

    @classmethod
    def load_raw_parquet(cls, load_from_dir):
        try:
            return cls(data=pd.read_parquet(load_from_dir))
        except Exception as e:
            raise InvalidDirectoryError("Input file/directory is not a valid parquet file/directory.") from e

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None, load_data=True):
        """Load the directory as a DataFrameDirectory.

        :param load_from_dir: See AnyDirectory
        :param meta_file_path: See AnyDirectory
        :param load_data: If load_data=True, the DataFrame and the schema will be loaded to the directory instance.
        :return: See AnyDirectory
        """
        if not Meta.exists(load_from_dir, meta_file_path):
            if os.path.isdir(load_from_dir) and not list(Path(load_from_dir).iterdir()):
                raise DirectoryEmptyError(load_from_dir)
            return cls.load_raw_parquet(load_from_dir)

        # Call super().load to assert type
        directory = super().load(load_from_dir, meta_file_path)
        meta = directory.meta
        if not hasattr(meta, 'format'):
            raise ValueError(f"File format is not provided in meta file.")

        schema = None
        if hasattr(meta, 'schema'):
            schema = load_json_file(os.path.join(load_from_dir, meta.schema))

        data = None
        if load_data:
            data_path = getattr(meta, 'data', None) or getattr(meta, 'file_path', None)
            full_data_path = os.path.join(load_from_dir, data_path)
            data = cls.load_data(
                full_data_path,
                meta.format,
                schema,
            )
        directory = cls(data=data, schema=schema, meta=meta)
        directory.basedir = load_from_dir
        # In pyarrow 0.16.0, if a categorical column is not a string column,
        # the categorical info will be lost after reloaded from parquet,
        # So we need to recover the categorical information to make sure the dataframe works well.
        directory.recover_categorical_columns()
        return directory

    def recover_categorical_columns(self):
        """Recover the categorical columns after loading the parquet file."""
        if not self.schema_data or self.data is None:
            return
        for attr in self.schema_instance.column_attributes:
            col = self.data[attr.name]
            if attr.element_type == ElementTypeName.CATEGORY and not is_categorical_dtype(col):
                self.data[attr.name] = col.astype('category')


def save_data_frame_to_directory(
        save_to,
        data: pd.DataFrame = None,
        file_path=_DEFAULT_DATA_PATH,
        file_format=_DEFAULT_FORMAT,
        schema=None,
        compute_schema_if_not_exist=True,
        compute_visualization=True,
        compute_stats_in_visualization=False,
        visualizers=None,
        extensions=None,
        meta_file_path=None,
        overwrite_if_exist=True,
        validate_if_exist=False,
):
    """Save a DataFrame object to folder.

    :param save_to: Directory path to which DataFrame object is dumped.
    :type save_to: str
    :param data: DataFrame object to be dumped.
    :type data: DataFrame
    :param file_path: Data file path relative to save_to. The default value is '_data.parquet'.
    :type file_path: str
    :param file_format: The format in which DataFrame is dumped. The default value is 'Parquet'.
    :type file_path: str
    :param schema: Json-serializable dict which describes the detailed info in data.
    :type schema: dict
    :param compute_schema_if_not_exist: Whether to compute and dump schema when schema is missing.
    :type compute_schema_if_not_exist: bool
    :param compute_visualization: Whether to compute and dump visualization when visualizer is missing.
    :type compute_visualization: bool
    :param compute_stats_in_visualization: Whether to compute statistics when computing visualization.
    :type compute_stats_in_visualization: bool
    :param visualizers: A list of Visualizer object to compute and dump visualization info.
    :type visualizers: list
    :param extensions: A dictionary to store extension info.
    :type visualizers: dict
    :param meta_file_path: Path of the meta file relative to save_to. The default value is '_meta.yaml'.
    :type meta_file_path: str
    :param overwrite_if_exist: Whether to dump DataFrame to file_path if the file already exists.
    :type overwrite_if_exist: bool
    :param validate_if_exist: Whether to validate the existed file at file_path is a valid DataFrame
                              if overwrite_if_exist is True.
    :type validate_if_exist: bool
    """
    try:
        DataFrameDirectory.create(
            data,
            file_path,
            file_format,
            schema,
            compute_schema_if_not_exist,
            compute_visualization,
            compute_stats_in_visualization,
            visualizers,
            extensions,
        ).dump(
            save_to,
            meta_file_path=meta_file_path,
            overwrite_if_exist=overwrite_if_exist,
            validate_if_exist=validate_if_exist,
        )
    except BaseException as e:
        raise DirectorySaveError(dir_name=save_to, original_error=e) from e


def load_data_path_from_directory(load_from_dir, meta_file_path=None):
    """Load a full data path in the specific folder."""
    try:
        return DataFrameDirectory.load(load_from_dir, meta_file_path, load_data=False).full_data_path(load_from_dir)
    except BaseException as e:
        raise DirectoryLoadError(dir_name=load_from_dir, original_error=e) from e


def load_data_frame_from_directory(load_from_dir, meta_file_path=None):
    """Load a DataFrameDirectory object from folder.

    :param load_from_dir: Directory path from which DataFrameDirectory object is loaded.
    :type load_from_dir: str
    :param meta_file_path: Path of meta data file relative to load_from_dir. The default value is '_meta.yaml'.
    :type load_from_dir: str
    :return: A DataFrameDirectory object.
    :rtype: DataFrameDirectory
    """
    try:
        return DataFrameDirectory.load(load_from_dir, meta_file_path=meta_file_path)
    # DataFrameDirectory.load occasionally fails due to OSError or IOError caused by
    # "Transport endpoint is not connected".
    # This error is due to transient network issue. Retry might make it work.
    except (OSError, IOError) as e:
        raise InvalidDirectoryError(f"Failed to load dataframe from {load_from_dir}. Please retry later.") from e
    except BaseException as e:
        raise DirectoryLoadError(dir_name=load_from_dir, original_error=e) from e
