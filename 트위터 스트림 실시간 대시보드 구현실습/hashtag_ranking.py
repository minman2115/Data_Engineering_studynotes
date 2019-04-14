import requests

import findspark
findspark.init()
import pyspark

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

from pyspark.sql.types import *
from pyspark.sql.functions import *

spark.sparkContext.setLogLevel("ERROR")

kafka_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "test").load()
kafka_df_string = kafka_df.select(col("key").cast("STRING").alias("key"),col("value").cast("STRING").alias("value"))

kafka_df_string_2 = kafka_df_string.select(col("value"))

kafka_df_tags = kafka_df_string_2.select(explode(split('value', ' ')).alias('tag')).filter(col('tag').startswith('#'))
kafka_df_tag_count = kafka_df_tags.groupBy('tag').count().withColumnRenamed('count', 'tag_count').orderBy(col('count').desc())

output = kafka_df_tag_count.writeStream.outputMode("complete").format("console").option("truncate", "false").trigger(processingTime="3 seconds").start()

def send_df_to_dashboard(df, id):
	tag = [str(t.tag) for t in df.select("tag").take(10)]
	tag_count = [str(t.tag_count) for t in df.select("tag_count").take(10)]
	url = 'http://localhost:8050/update_data'
	request_data = {'tag': str(tag), 'tag_count': str(tag_count)}
	print('update dashboard')
	response = requests.post(url, data=request_data)

kafka_df_tag_count.writeStream.outputMode("complete").foreachBatch(send_df_to_dashboard).trigger(processingTime="3 seconds").start()

output.awaitTermination()
