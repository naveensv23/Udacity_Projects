import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Creates song dataframe by reading data from provided JSON file.
    
    - Selects required song data from the dataframe.
    - Inserts selected data into songs dimension table in the database.
    
    - Selects required artist data from the dataframe.
    - Inserts selected data into artists dimension table in the database.
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_longitude", "artist_latitude"]].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Creates log dataframe by reading data from provided JSON file.
    
    - Filters data by NextSong action.
    
    - Converts timestamp data into datetime data.
    
    - Selects and extract required time data from the dataframe.
    - Inserts selected data into time dimension table in the database.
    
    - Selects required user data from the dataframe.
    - Inserts selected data into users dimension table in the database.
    
    - Selects required songplay data from the dataframe and tables.
    - Inserts selected data into songplays fact table in the database.
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit="ms")
    df['week'] = t.dt.isocalendar().week
    df['year'] = t.dt.year
    df['weekOfYear'] = t.dt.isocalendar().week
    df['weekday'] = t.dt.strftime('%A')
    
    # insert time data records
    time_data = [t.tolist(), t.dt.hour.tolist(), t.dt.day.tolist(), t.dt.isocalendar().week.tolist(), t.dt.month.tolist(), t.dt.year.tolist(), t.dt.weekday.tolist()]
    column_labels = ["timestamp", "hour", "day", "weekOfYear", "month", "year", "weekday"]
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [pd.to_datetime(row.ts, unit="ms"), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Get absolute path to all the JSON files present in the given directory and sub-directories.  
    
    - Prints the number of files found in the current directory and sub-directories.  
    
    - Iterate over all the files and pass it to the relevant functions to process.  
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets cursor to it.  
    
    - Processes song data and inserts into the relevant tables in the database.  
    
    - Processes log data and inserts into the relevant tables in the database.  
    
    - Finally, closes the connection to the database. 
    """
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()