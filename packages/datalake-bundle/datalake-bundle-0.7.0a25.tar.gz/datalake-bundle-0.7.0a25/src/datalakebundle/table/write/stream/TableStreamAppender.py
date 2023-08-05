from logging import Logger
from pyspark.sql.dataframe import DataFrame
from datalakebundle.table.create.TableDefinition import TableDefinition
from datalakebundle.table.schema.SchemaChecker import SchemaChecker
from datalakebundle.table.write.stream.DataStreamWriter import DataStreamWriter


class TableStreamAppender:
    def __init__(
        self,
        logger: Logger,
        schema_checker: SchemaChecker,
        data_stream_writer: DataStreamWriter,
    ):
        self.__logger = logger
        self.__schema_checker = schema_checker
        self.__data_stream_writer = data_stream_writer

    def append(self, result: DataFrame, table_definition: TableDefinition, checkpoint_location: str, options: dict):
        output_table_name = table_definition.full_table_name

        self.__schema_checker.check(result, output_table_name, table_definition)

        self.__logger.info(f"Writing data to table: {output_table_name}")

        self.__data_stream_writer.append(result, output_table_name, table_definition.schema, checkpoint_location, options)

        self.__logger.info(f"Data successfully written to: {output_table_name}")
