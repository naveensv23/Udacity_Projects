

<!-- PROJECT HEADER -->
<br />
<div align="center">
  <a href="#">
    <img src="images/udacity.svg" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Data Modeling with Postgres using Python & SQL</h3>

  <p align="center">
    Database Schema & ETL pipeline for Song Play Analysis 
    <br />
    <br />
    -----------------------------------------------
    <br />
    <br />
    Data Engineer for AI Applications Nanodegree
    <br />
    Bosch AI Talent Accelerator Scholarship Program
  </p>
</div>

<br />

<!-- TABLE OF CONTENTS -->
<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#file-structure">File Structure</a>
    </li>
    <li><a href="#how-to-run">How To Run</a></li>
    <li><a href="#database-schema-design">Database Schema Design</a></li>
    <li><a href="#etl-pipeline">ETL Pipeline</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br/>

<!-- ABOUT THE PROJECT -->

## About The Project

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs their users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity as well as a directory with JSON metadata on the songs in their app.

The startup wants their `logs` and `songs` data to be loaded into a Postgres database with tables designed to optimize queries for song play analysis. This project designs a data model by creating a database schema and an ETL pipeline for this analysis using Python and SQL. The project defines dimension and fact tables for a star schema and creates an ETL pipeline that transforms data from JSON files present in two local directories into these tables in the Postgres database for a particular analytic focus.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

-   [![Python][python-shield]][python-url]
-   [![PostgreSQL][postgresql-shield]][postgresql-url]
-   [![Jupyter][jupyter-shield]][jupyter-url]
-   [![VSCode][vscode-shield]][vscode-url]

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- FILE STRUCTURE -->

## File Structure

1. Dataset available in data folder:

    - `Song Dataset`: Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are file paths to two files in this dataset.

        ```
        song_data/A/B/C/TRABCEI128F424C983.json
        song_data/A/A/B/TRAABJL12903CDCF1A.json
        ```

        And below is an example of what a single song file looks like.

        ![Song Data][song-dataset]

    <br />

    - `Log Dataset`: These files are also in JSON format and contains user activity data from a music streaming app. The log files are partitioned by year and month. For example, here are filepaths to two files in this dataset.

        ```
        log_data/2018/11/2018-11-12-events.json
        log_data/2018/11/2018-11-13-events.json
        ```

        And below is an example of what the data in a log file looks like.

        ![Log Data][log-dataset]

    <br />

2. `test.ipynb` displays the first few rows of each table to let you check the database.

3. `create_tables.py` drops and creates tables. You run this file to reset your tables before each time you run your ETL scripts.

4. `etl.ipynb` reads and processes a single file from `song_data` and `log_data` and loads the data into the tables. This notebook contains detailed instructions on the ETL process for each of the tables.

5. `etl.py` reads and processes all files from `song_data` and `log_data` and loads them into the tables.

6. `sql_queries.py` contains all sql queries, and is imported into the last three files above.

7. `README.md` provides details on the project.

<p align="right">(<a href="#top">back to top</a>)</p>

## How To Run

### Prerequisite

-   Prepare the Python environment by typing the following command into the Terminal

    ```
    $ pip install -r requirements.txt
    ```

### Running scripts

-   In order to work with the project you first need to run the `create_tables.py` at least once to create the sparkifydb database.

-   You can execute the one of the following command inside a python environment to run the `create_tables.py`

    ```
    $ python create_tables.py
    or
    $ python3 create_tables.py
    ```

-   You can only work with `test.ipynb`, `etl.ipynb`, or `etl.py` after running the `create_tables.py`

-   Files with extension `.ipynb` will run inside a Jupyter Notebook environment.

-   You can execute the one of the following command inside a python environment to run the `etl.py`

    ```
    $ python etl.py
    or
    $ python3 etl.py
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- DATABASE SCHEMA & ETL PIPELINE -->

## Database Schema Design

Database schema consist five tables with the following fact and dimension tables:

-   Fact Table

    1. `songplays`: records in log data associated with song plays filter by `NextSong` page value.
       The table contains songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location and user_agent columns.

<br/>

-   Dimension Tables

    2. `users`: stores the user data available in the app. The table contains user_id, first_name, last_name, gender and level columns.

    3. `songs`: contains songs data. The table consist of the following columns song_id, title, artist_id, year and duration.

    4. `artists`: artists in the database. The table contains artist_id, name, location, latitude and longitude columns.

    5. `time`: timestamps of records in `songplays` broken down into specific units with the following columns start_time, hour, day, week, month, year and weekday.

    <br/>

    ![Sparkifydb ERD][sparkifydb-erd]

<p align="right">(<a href="#top">back to top</a>)</p>

## ETL Pipeline

The ETL pipeline follows the following procedure:

-   Establish connection with the `sparkify` database and get a cursor to it.

-   Process song data and insert the data into the relevant tables in the database.

    -   Get absolute path to all the song JSON files present in the given directory and sub-directories.

    -   Iterate over all the song data files one by one and create a dataframe by reading the data from JSON files.

    -   Select the required song data from the dataframe and insert it into the `songs` dimension table in the database.

    -   Select required artist data from the dataframe and insert it into the `artists` dimension table in the database.

-   Process log data and insert the data into the relevant tables in the database.

    -   Get absolute path to all the log JSON files present in the given directory and sub-directories.

    -   Iterate over all the log data files one by one and create a dataframe by reading the data from JSON files.

    -   Filter data by `NextSong` action.

    -   Converts `timestamp` data into `datetime` data as timestamp data is available in miliseconds.

    -   Select and extract required time data from the dataframe and insert it into the `time` dimension table in the database.

    -   Select the required user data from the dataframe and insert it into the `users` dimension table in the database.

    -   Select required songplay data from the dataframe and tables and insert it into the `songplays` fact table in the database.

-   Finally, close the connection to the database.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

-   [Udacity](https://www.udacity.com/)
-   [Bosch AI Talent Accelerator](https://www.udacity.com/scholarships/bosch-ai-talent-accelerator)
-   [Img Shields](https://shields.io)
-   [Best README Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[postgresql-shield]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[jupyter-shield]: https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter
[vscode-shield]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[linkedin-url]: https://www.linkedin.com/in/arfat-mateen
[python-url]: https://www.python.org/
[postgresql-url]: https://www.postgresql.org/
[jupyter-url]: https://jupyter.org/
[vscode-url]: https://code.visualstudio.com/
[song-dataset]: images/song_data.png
[log-dataset]: images/log_data.png
[sparkifydb-erd]: images/sparkifydb_erd.png
