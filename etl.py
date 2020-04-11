# Standard library imports
import configparser
import glob
import os
from datetime import datetime

# Related third part imports
import boto3
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, year, month, dayofmonth, dayofweek
from pyspark.sql.functions import hour, weekofyear, date_format, from_unixtime

def create_spark_session():
    """Create a Spark session."""
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Write songs table and artists table to parquet files on S3.
    Keyword arguments:
    spark -- a spark session
    input_data -- the script reads song_data from S3
    output_data -- the script writes tables to partitioned parquet on S3
    """
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'

    # read song data file
    song_data_df = spark.read.json(song_data)
    song_data_df = song_data_df.dropDuplicates()
    song_data_df.createOrReplaceTempView("song_data_view")

    # extract columns to create songs table
    songs_table = spark.sql(
        "SELECT DISTINCT \
              song_id, \
              title, \
              artist_id, \
              MAX(year) AS year, \
              duration \
          FROM song_data_view \
          WHERE \
              ISNOTNULL(song_id) \
          GROUP BY \
              song_id, \
              title, \
              artist_id, \
              duration \
          ORDER BY \
              song_id ASC"
        )

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy('year','artist_id') \
        .parquet(output_data + 'songs_table')

    # extract columns to create artists table
    artists_table = spark.sql(
        "SELECT DISTINCT \
            artist_id, \
            artist_name, \
            artist_location, \
            artist_latitude, \
            artist_longitude \
         FROM song_data_view \
         WHERE \
            ISNOTNULL(artist_id)"
        )

    # write artists table to parquet files
    artists_table.write.mode('overwrite').partitionBy('artist_id') \
        .parquet(output_data + 'artists_table')


def process_log_data(spark, input_data, output_data):
    """
    Write users, time and songplays tables to parquet files on S3.
    Keyword arguments:
    spark -- a spark session
    input_data -- the script reads log_data from S3
    output_data -- the script writes tables to partitioned parquet on S3
    """

    # get filepath to log data files
    log_data = input_data + 'log_data/*.json'

    # read log data files
    log_data_df = spark.read.json(log_data)
 
    # filter by actions for song plays
    log_data_df = log_data_df.filter(log_data_df.page == 'NextSong') \
        .dropDuplicates()
    log_data_df.createOrReplaceTempView("log_data_view")

    # extract columns for users table
    users_table = spark.sql(
        "SELECT DISTINCT \
            userid, \
            firstname, \
            lastname, \
            gender, \
            level \
        FROM log_data_view \
        WHERE \
            ISNOTNULL(userid)"
    )
    
    # write users table to parquet files
    users_table.write.mode('overwrite').partitionBy('userid') \
        .parquet(output_data + 'users_table')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: x // 1000)
    ts_df = log_data_df.select(log_data_df.ts)
    ts_df = ts_df.withColumn('timestamp', get_timestamp('ts'))
    
    # create datetime column from original timestamp column
    ts_df = ts_df.withColumn('start_time', from_unixtime('timestamp'))
    ts_df = ts_df.withColumn('hour', hour('start_time'))
    ts_df = ts_df.withColumn('day', dayofmonth('start_time'))
    ts_df = ts_df.withColumn('week', weekofyear('start_time'))
    ts_df = ts_df.withColumn('month', month('start_time'))
    ts_df = ts_df.withColumn('year', year('start_time'))
    ts_df = ts_df.withColumn('week_day', dayofweek('start_time'))
    ts_df.dropDuplicates()
    
    # extract columns to create time table
    ts_df.createOrReplaceTempView("ts_df_view")
    time_table = spark.sql(
        "SELECT DISTINCT \
            start_time, \
            hour, \
            day, \
            week, \
            month, \
            year, \
            week_day \
        FROM ts_df_view"
    )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy('year', 'month') \
    .parquet(output_data + 'time_table')

    # read in song data to use for songplays table
    songplays_df = log_data_df.filter(log_data_df.page == 'NextSong') \
        .dropDuplicates()
    songplays_df = songplays_df.withColumn('timestamp', get_timestamp('ts'))
    songplays_df = songplays_df.withColumn('start_time', \
        from_unixtime('timestamp'))
    songplays_df.createOrReplaceTempView("songplays_view")

    # extract columns from song + log datasets to create songplays table 
    songplays_table = spark.sql(
            "SELECT \
                row_number() over (order by 'start_time', 'user_id', \
                'song_id', 'artist_id') as songplay_id, \
                plays.start_time as start_time, \
                plays.userid as user_id, \
                plays.level, \
                song.song_id, \
                song.artist_id, \
                plays.sessionid as session_id, \
                plays.location, \
                plays.userAgent as user_agent, \
                time.year, \
                time.month \
            FROM \
                songplays_view plays \
                left join song_data_view song \
                on song.artist_name = plays.artist \
                left join ts_df_view time \
                on time.start_time = plays.start_time"
    )

    # write songplays table to parquet files partitioned by year + month
    songplays_table.write.mode('overwrite').partitionBy('year', 'month'). \
        parquet(output_data + 'songplays_table')


def main():
    input_data = "s3a://sparkfy-input/data/"
    output_data = "s3a://sparkfy-output/spark-datalake/"

    #Create a spark session
    spark = create_spark_session()
    
    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()