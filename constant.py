from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType

LOG_FILE_PATH = "input/test_data.csv"
CONF_FILE_PATH = "config/config.json"
LOG_SCHEMA = StructType([StructField('project_id', StringType(), True),
                         StructField('timestamp', TimestampType(), True),
                         StructField('operation', StructType([
                             StructField('name', StringType(), True),
                             StructField('runtime', DoubleType(), True),
                             StructField('request_id', StringType(), True),
                             StructField('response_size', IntegerType(), True),
                             StructField('request_size', IntegerType(), True),
                             StructField('http_status', IntegerType(), True)
                         ]))
                         ])
OUTPUT_DIR = "output/report/"
