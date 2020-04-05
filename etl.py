import boto3
import configparser
import glob
import numpy as np
import os
import pandas as pd

from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format

config = configparser.ConfigParser()
#config.read('dl.cfg')

#os.environ['AWS_ACCESS_KEY_ID']=config['aws']['AWS_ACCESS_KEY_ID']
#os.environ['AWS_SECRET_ACCESS_KEY']=config['aws']['AWS_SECRET_ACCESS_KEY']


print('step_01 spark session')

def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

print('step_02 create song_data')

def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data + 'song_data/A/A/A/*.json'
    
    # read song data file

    df = spark.read.json(song_data)
    df.createOrReplaceTempView("df_song_data")

    # extract columns to create songs table
    songs_table = spark.sql("SELECT \
              song_id, \
              title, \
              artist_id, \
              MAX(year) AS year, \
              duration \
          FROM df_song_data \
          WHERE \
              ISNOTNULL(song_id) \
          GROUP BY \
              song_id, \
              title, \
              artist_id, \
              duration \
          ORDER BY \
              song_id ASC")

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy('year','artist_id').parquet(output_data + 'songs_table')
    #songs_table.write.parquet( output_data)

    print('step 3 output song_data')


    # extract columns to create artists table
    artists_table = spark.sql("SELECT DISTINCT \
                artist_id, \
                artist_name, \
                artist_location, \
                artist_latitude, \
                artist_longitude \
             FROM df_song_data \
             WHERE ISNOTNULL(artist_id)")

    print('fim select artists')

    # write artists table to parquet files
    artists_table.write.mode('overwrite').partitionBy('artist_id').parquet(output_data + 'artists_table')
'''

def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data =

    # read log data file
    df = 
    
    # filter by actions for song plays
    df = 

    # extract columns for users table    
    artists_table = 
    
    # write users table to parquet files
    artists_table

    # create timestamp column from original timestamp column
    get_timestamp = udf()
    df = 
    
    # create datetime column from original timestamp column
    get_datetime = udf()
    df = 
    
    # extract columns to create time table
    time_table = 
    
    # write time table to parquet files partitioned by year and month
    time_table

    # read in song data to use for songplays table
    song_df = 

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = 

    # write songplays table to parquet files partitioned by year and month
    songplays_table
'''

def main():
    spark = create_spark_session()
    input_data = "s3a://sparkfy-input/data/"
    output_data = "s3a://sparkfy-output/"
    
    #input_data = './data/'
    #output_data = './sparkfy-warehouse'

    process_song_data(spark, input_data, output_data)    
    #process_log_data(spark, input_data, output_data)

    # spark = create_spark_session()
    #log_file = spark.read.json(input_data+'data/log_data/2018-11-01-events.json')
    #log_df = spark.read.load(input_data+'data/log_data/', format='json')
    #print(log_df.count())
    
    #song_file = input_data+'data/song_data/A/A/A/*.json'
    #print(song_file)
    #df_t = spark.read.json(song_file)

    #log_df.filter(log_df.gender == 'F').select('userId', 'gender').show()
    #song_df.select('songId', 'title').show()
    #print(song_df.count())

    

if __name__ == "__main__":
    main()
