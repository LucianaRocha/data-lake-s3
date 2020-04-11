[//]: # (Image References)

[image1]: ./images/star_schema_model_songplays.png "Model"
[image2]: ./images/filepaths.png "Filepaths songdata"
[image3]: ./images/song_file_example.png "Song file example"
[image4]: ./images/filepaths_logdata.png "Filepaths logdata"
[image5]: ./images/log_file_example.png "Log file example"
[image6]: ./images/notebook.png "Notebook"
[image7]: ./images/run_notebook.png "Run notebook"
[image8]: ./images/star_schema_model_songplays.png "Star Schema"
[image9]: ./images/result_1.png "Result"
[image10]: ./images/result_null.png "Result null"
[image11]: ./images/result_count.png "Result count"
[image12]: ./images/dwh_cfg.png "config"
[image13]: ./images/ssh_windows.png "ssh_windows"
[image14]: ./images/ssh_linux.png "ssh_linux"



# Project: Data Warehouse hosted on Amazon S3
This project is part of the [Data Engineering Nanodegree Program](https://www.udacity.com/course/data-engineer-nanodegree--nd027), by [Udacity](https://www.udacity.com/).  

## Introduction  

A music streaming startup, Sparkify, has grown its user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, I was tasked with building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights into what songs their users are listening to.

It is possible to test the database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

### Project Description  

In this project, I applied what I have learned on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3. To complete the project, I needed to load data from S3, process the data into analytics tables using Spark, and load them back into S3. I deployed this Spark process on a cluster using AWS.

# Star Schema for Song Play Analysis
For this project, I used the song and log datasets and created a [star-schema model](https://en.wikipedia.org/wiki/Star_schema) optimized for queries on song play analysis. 

Star and snowflake schemas use the concepts of **fact** and **dimension** tables to make getting value out of the data easier.  

- **Fact table** consists of measurements, metrics or facts a business process.
- **Dimension table** a structure that categorizes facts and measures in order to enable users to answer business questions.

**Benefits of star-schema:**  

- Star-schemas are denormalized. Denormalization increases performance by reducing the number of joins between tables. Data integrity will take a bit of a potential hit, as there will be more copies of the data (to reduce JOINS). The benefits of star-schema denormalization are:  

	- Simpler queries
	- Simplified business reporting logic
	- Query performance gains
	- Fast aggregations
	- Feed cubes
	- Fast aggregations
	
         
## Data modeling

For this project, I modeled a star-schema that includes one fact table and four dimension tables. See the descriptions below:

**Fact Table**  

- **songplays:** records in log data associated with song plays. The log data was filtered with page = 'NextSong'.  

	- Columns: songplay\_id, start\_time, user\_id, level, song\_id, artist\_id, session\_id, location, user\_agent.  
	- Distribution strategy: partitioned parquet files by **year and month** in table directories on S3

**Dimension Tables**  

- **users:** users in the app.  
	- Columns: user\_id, first\_name, last\_name, gender, level.
	- Distribution strategy: partitioned parquet files by **user\_id** in table directories on S3

- **songs:** songs in music database.  
	- Columns: song\_id, title, artist\_id, year, duration  
	- Distribution strategy: partitioned parquet files by **year and artist\_id** in table directories on S3

- **artists:** artists in music database.
	- Columns: artist\_id, name, location, latitude, longitude  
	- Distribution strategy: partitioned parquet files by **artist\_id** in table directories on S3

- **time:** timestamps of records in songplays broken down into specific units.
	- Columns: start\_time, hour, day, week, month, year, weekday  
	- Distribution strategy: partitioned parquet files by **year and month** in table directories on S3
	
![Data Modeling][image8]  
	
# Project Datasets  

## Datasets

I worked with two datasets that reside in S3. Here are the S3 links for each:  
	- Song data: s3://udacity-dend/song\_data  
	- Log data: s3://udacity-dend/log\_data  


### Song Dataset

The first dataset is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

![Filepaths][image2]

And below is an example of what a single song file, TRAAAAW128F429D538.json, looks like.

![Song file example][image3]  

### Log Dataset  
 
The second dataset consists of log files in JSON format generated by this [event simulator](https://github.com/Interana/eventsim) based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

![Filepaths logdata][image4]

And below is an example of what the data in a log file, 2018-11-01-events.json, looks like.  

![Log file example][image5]


# ETL pipeline

I created the **etl.py** that can be run by Anaconda Prompt (Windows) or Terminal (Linux) without the help of a graphic interface. The file is organized as below:  

- **etl.py file:**  
	- imports the necessary packages
	- creates a spark session
	- defines functions to:
		- read the data files (log\_data and song\_data)
		- extract columns to create tables
		- write the tables on S3
	

# Getting Started
## Files included in this repository  
The project includes six files:  

 1.  **etl.py:** reads and processes files from song\_data and log\_data and loads them into your tables. 
 2. **README.md:** provides discussion about this project. 
 3. I did not use a 'dl.cfg' with my AWS credentials because I ran the 'etl.py' into own my AWS environment

## Preparing the environment to run the project

**1.** On [AWS Console](https://aws.amazon.com/) it is necessary:  

- Create a [AWS account](https://aws.amazon.com/pt/premiumsupport/knowledge-center/create-and-activate-aws-account/)  
- Create a SSH key pair to connect on cluster AWS EMR
	+ [Create key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
	+ Download this key pair to your local environment  
- Go to EMR and create a cluster 
	+ [Create a EMR cluster](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs-launch-sample-cluster.html)
- Go to S3 and Create an S3 Buckets (input and output)  
	+ [Create S3 Buckets](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)
- Connect to the Master Node Using SSH
	+ **Windows:**  
		* Download PuTTY.exe to your computer from [Windows](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
		* Start PuTTY and follow the orientations on AWS platform
![Windows][image13]
	+ **Linux:**  
![Linux][image14]

- On EMR you will need install
	+ pip3 install boto3  
	+ pip3 install pandas  
	+ pip3 install pyspark

- In my environment I needed set a few paths like below. Check if this is necessary in your environment:
	+ sudo alternatives --set python /usr/bin/python3.6  
	+ curl -O https://bootstrap.pypa.io/get-pip.py  
	+ python3 get-pip.py --user  
	+ sudo sed -i -e '$a\export PATH=/home/hadoop/.local/bin:$PATH' /home/hadoop/.bash_profile  
	+ sudo sed -i -e '$a\export PYSPARK_PYTHON=/usr/bin/python3' /etc/spark/conf/spark-env.sh  
	+ sudo sed -i -e '$a\export PYSPARK_DRIVER_PYTHON=/usr/bin/python3' /etc/spark/conf/spark-env.sh  
	+ source .bash_profile 
	+ sudo yum install git -y  
	+ I shared **sparkfy.sh** in my GitHub to you use it weather necessary. It has all commands above and you can use him to run in your EMR.


## Getting the code 
There are two options to get this project:

- Download it as a zip file

	- Do the download in this [link](https://github.com/LucianaRocha/data-lake-s3/archive/master.zip).
	- Unzip the file in a folder of your choice.  

- Clone this repository using Git version control system

	- Open Anaconda Prompt (Windows) or Terminal (Linux), navigate to the folder of your choice, and type the command below:  

	```
	git clone https://github.com/LucianaRocha/data-lake-s3.git
	```

# Running the project  

To run this project:  

- Run the etl.py in your EMR environment and write the command bellow:
	+ python etl.py

# References
- Data Warehouse and Business Intelligence Resources [Kimball Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/)
- Spark SQL [Dataframe API](http://spark.apache.org/docs/latest/sql-programming-guide.html)
- Pyspark [functions](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#module-pyspark.sql.functions)
- Boto3 Docs [documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
- AWS Documentation [documentation](https://docs.aws.amazon.com/index.html)
- SQL [Kickstarter SQL Style Guide](https://gist.github.com/fredbenenson/7bb92718e19138c20591)  
- Doctring Conventions [PEP 257](https://www.python.org/dev/peps/pep-0257/)
- PEP8 [style guidelines](https://www.python.org/dev/peps/pep-0008/)