from collections import Callable
from logging import Logger
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StructType


class DataStreamWriter:
    def __init__(
        self,
        logger: Logger,
    ):
        self.__logger = logger

    def append(self, df: DataFrame, full_table_name: str, schema: StructType, checkpoint_location: str, options: dict):
        options['checkpointLocation'] = checkpoint_location

        df.select([field.name for field in schema.fields]).writeStream.format("delta").outputMode("append").options(**options).trigger(once=True).table(full_table_name)

    def update(self, df: DataFrame, full_table_name: str, schema: StructType, checkpoint_location: str, callback: Callable, options: dict):
        options['checkpointLocation'] = checkpoint_location

        df.select([field.name for field in schema.fields]).writeStream.format("delta").outputMode("update").options(**options).foreachBatch(callback).trigger(once=True).table(full_table_name)
