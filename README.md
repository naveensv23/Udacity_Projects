Project 1: Song Play Analysis with RDBMS
About The Project

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs their users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity as well as a directory with JSON metadata on the songs in their app.

The startup wants their logs and songs data to be loaded into a Postgres database with tables designed to optimize queries for song play analysis. This project designs a data model by creating a database schema and an ETL pipeline for this analysis using Python and SQL. The project defines dimension and fact tables for a star schema and creates an ETL pipeline that transforms data from JSON files present in two local directories into these tables in the Postgres database for a particular analytic focus.

------------------------------------------------------------
###
##File Structure
1: Dataset available in data folder:
     Song Dataset: Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by      the first three letters of each song's track ID. For example, here are file paths to two files in this dataset.

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

##Log Dataset: These files are also in JSON format and contains user activity data from a music streaming app. The log files are partitioned by year and month. For example, here are filepaths to two files in this dataset.

2. test.ipynb displays the first few rows of each table to let you check the database.

3. create_tables.py drops and creates tables. You run this file to reset your tables before each time you run your ETL scripts.

4.etl.ipynb reads and processes a single file from song_data and log_data and loads the data into the tables. This notebook contains detailed instructions on the ETL process for each of the tables.

5. etl.py reads and processes all files from song_data and log_data and loads them into the tables.

6.sql_queries.py contains all sql queries, and is imported into the last three files above.

7.README.md provides details on the project.

##How To Run

Prepare the Python environment by typing the following command into the Terminal
  In order to work with the project you first need to run the create_tables.py at least once to create the sparkifydb database.
  You can execute the one of the following command inside a python environment to run the create_tables.py
!python create_tables.py
You can only work with test.ipynb, etl.ipynb, or etl.py after running the create_tables.py
Files with extension .ipynb will run inside a Jupyter Notebook environment.
You can execute the one of the following command inside a python environment to run the etl.py

##Database Schema Design
Database schema consist five tables with the following fact and dimension tables:
Fact Table

1. songplays: records in log data associated with song plays filter by NextSong page value. The table contains songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location and user_agent columns.

##Dimension Tables
    users: stores the user data available in the app. The table contains user_id, first_name, last_name, gender and level columns.

    songs: contains songs data. The table consist of the following columns song_id, title, artist_id, year and duration.

    artists: artists in the database. The table contains artist_id, name, location, latitude and longitude columns.

    time: timestamps of records in songplays broken down into specific units with the following columns start_time, hour, day, week, month, year and weekday.
    
##ETL Pipeline

The ETL pipeline follows the following procedure:

Establish connection with the sparkify database and get a cursor to it.

Process song data and insert the data into the relevant tables in the database.

    1.Get absolute path to all the song JSON files present in the given directory and sub-directories.

    2.Iterate over all the song data files one by one and create a dataframe by reading the data from JSON files.

   3.Select the required song data from the dataframe and insert it into the songs dimension table in the database.

    4.Select required artist data from the dataframe and insert it into the artists dimension table in the database.

Process log data and insert the data into the relevant tables in the database.

    1.Get absolute path to all the log JSON files present in the given directory and sub-directories.

    2.Iterate over all the log data files one by one and create a dataframe by reading the data from JSON files.

    3.Filter data by NextSong action.

    4.Converts timestamp data into datetime data as timestamp data is available in miliseconds.

    5.Select and extract required time data from the dataframe and insert it into the time dimension table in the database.

    6.Select the required user data from the dataframe and insert it into the users dimension table in the database.

    7.Select required songplay data from the dataframe and tables and insert it into the songplays fact table in the database.

    8.Finally, close the connection to the database.
