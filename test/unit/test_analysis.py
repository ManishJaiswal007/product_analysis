import pytest
from operations.analysis import Analysis
from pyspark.sql import SparkSession
from test.constant import TEST_QUERY_DATA, TEST_SCHEMA


class TestAnalysis:

    @pytest.mark.usefixtures("spark_session")
    def perfom_test(spark: SparkSession):

        df = spark.read.json(data=TEST_QUERY_DATA, schema=TEST_SCHEMA)
        sq_df = Analysis().get_slow_query(df)
        us_df = Analysis().get_usage(df=df, time_win="1 day", agg_col="response_size")

        assert sq_df.select('runtime').first()[0] == 0.7045121418055498
        assert us_df.select('aggregate_sum').first()[0] == 25
