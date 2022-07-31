import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType

TEST_SCHEMA = StructType([StructField('project_id', StringType(), True),
                         StructField('timestamp', TimestampType(), True),
                         StructField('name', StringType(), True),
                         StructField('runtime', DoubleType(), True),
                         StructField('request_id', StringType(), True),
                         StructField('response_size', IntegerType(), True),
                         StructField('request_size', IntegerType(), True),
                         StructField('http_status', IntegerType(), True)

                          ])


TEST_QUERY_DATA = [{"project_id": "a4b98e52-5a16-4737-a3de-87b97be3ccd3", "timestamp": "2022-07-30T10:29:06.54525634+05:30", "name": "delete_crayon", "runtime": 0.7045121418055498, "request_id": "e57a5318-5f13-469a-8679-80793d8d426d", "response_size": 25, "request_size": 365, "http_status": 200},
                   {"project_id": "30c4f1f8-d99d-4a86-9393-2c3689365a8b", "timestamp": "2022-07-30T10:31:53.27232506+05:30", "name": "delete_football", "runtime": 0.8741727555734353, "request_id": "50bf86e9-f2f6-4afc-a002-221e069da16f", "response_size": 4, "request_size": 675, "http_status": 200}]


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    spark = SparkSession.builder.master("local[2]").appName(
        'test').getOrCreate()
