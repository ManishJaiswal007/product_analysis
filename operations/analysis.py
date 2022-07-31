from pyspark.sql.functions import col, rank, window, sum, count
from pyspark.sql.window import Window
from pyspark.sql import DataFrame


class Analysis:
    """
    This class contains diffrent insight
    """

    def get_slow_query(cls, df: DataFrame) -> DataFrame:
        """
        This method will return slow running query project wise.

        @Parameters
        ----------
        df : Dataframe object, which will be used for computation

        Returns
        -------
        DataFrame
            A DataFrame with the transformed column and details of slow running query
        """
        windowPartition = Window.partitionBy(
            "project_id").orderBy(col("runtime").desc())
        # Apply the window specification
        slow_query = df.withColumn("rank", rank().over(windowPartition)).filter(
            "rank==1").select("project_id", "name", "runtime")
        return slow_query

    def get_usage(cls, df: DataFrame, time_win: str, agg_col: str) -> DataFrame:
        """
        This method will calculate usage project wise in given time window.

        @Parameters
        ----------
        df : Dataframe object, which will be transformed
        time_win : string object, duration of time window
        agg_col : column containing usage data.

        Returns
        -------
        DataFrame
            A DataFrame with the transformed column 
        """
        df2 = df.groupBy("project_id", window(col("timestamp"), time_win)).agg(sum(agg_col).alias(
            "aggregate_sum")).select("project_id", "window.start", "window.end", "aggregate_sum")

        return df2

    def get_query_mt(cls, df: DataFrame):
        """

        @Parameters
        ----------
        df : Dataframe object, which will be used for computation

        Returns
        -------
        DataFrame
            A DataFrame with the transformed column and details diffrent type of failure
        """
        pivotDF = df.groupBy("project_id").pivot(
            "http_status").agg(count("request_id"))
        query_mt = pivotDF.select(col("project_id"), col("200").alias("Sucusess(200)"), col("500").alias(
            "Internal Error(500)"), col("501").alias("Not implemented(501)"), col("502").alias("Overloaded(502)"))
        return query_mt
