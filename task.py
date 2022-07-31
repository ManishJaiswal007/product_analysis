import json
from constant import LOG_FILE_PATH, CONF_FILE_PATH, LOG_SCHEMA, OUTPUT_DIR
from operations.analysis import Analysis

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import from_json, instr, col


class AnalysisProcess:
    """
    ETLProcess class define task that needs to be perform to complete Analysis process.

    @Parameters
    ----------
    file_name   : name of file to be processed.
    time_window : time_window for calculting usage
    agg_col     : column used for calculation of usgae
    """

    def __init__(self, file: str, time_window: str, agg_col: str) -> None:
        self._filename = file
        self._time_window = time_window
        self._agg_col = agg_col

    def perform_task(self) -> None:
        """
        This methods call methods to complete nesscary steps to complete Analysis process.
        """
        spark_ses = self.create_spark_session()
        log_df = self.read_data(spark_ses)

        slow_qry = Analysis().get_slow_query(log_df)
        usage = Analysis().get_usage(log_df, self._time_window, self._agg_col)
        query_mt = Analysis().get_query_mt(log_df)

        self.write_data(slow_qry, "slow_performing_query")
        self.write_data(usage, "usage_data")
        self.write_data(query_mt, "query_mt")

    def create_spark_session(self) -> SparkSession:
        """
        This method create spark session

        Returns
        -------
        SparkSession
            A SparkSession instance.
        """
        spark = SparkSession.builder.master("local[1]").appName(
            'Product_analysis').getOrCreate()
        return spark

    def read_data(self, spark: SparkSession) -> DataFrame:
        """
        This method read log data and format it in simple manner by unpacking nested json data.

        @Parameters
        ----------
        SparkSession : SparkSession instance use to read data.

        Returns
        -------
        DataFrame
            A DataFrame with simplified nested json data.

        """
        df = spark.read.text(self._filename)
        jdf = df.select(from_json(df.value.substr(
            instr(df.value, '{'), instr(df.value, '}')), LOG_SCHEMA).alias("json"))
        ap_df = jdf.select(col("json.project_id"), col("json.timestamp"), col("json.operation.name"), col("json.operation.runtime"), col(
            "json.operation.request_id"), col("json.operation.response_size"), col("json.operation.request_size"), col("json.operation.http_status"))
        return ap_df

    def write_data(self, df: DataFrame, name: str) -> None:
        """
        This methods writes data to output dir. Currently only csv supported.
        @Parameters
        ----------
        df : Dataframe object, which will be transformed
        name : name of subfloder to identify data.
        """
        # future work -- add support for diffrent writre format and diffrent write mode
        df.coalesce(1).write.mode("overwrite").csv(
            OUTPUT_DIR+name, header='true')


if __name__ == "__main__":

    with open(CONF_FILE_PATH, 'r') as f:
        data = json.load(f)
        time_win = data.get("time_window")
        agg_col = data.get("agg_col")
    AnalysisProcess(LOG_FILE_PATH, time_win, agg_col).perform_task()
