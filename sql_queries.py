# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES


songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id SERIAL, 
start_time TIMESTAMP NOT NULL, 
user_id INT NOT NULL,
level VARCHAR NOT NULL, 
song_id VARCHAR NULL,
artist_id VARCHAR NULL, 
session_id VARCHAR NOT NULL, 
location VARCHAR NOT NULL, 
user_agent VARCHAR NOT NULL,
PRIMARY KEY (songplay_id))
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id INT, 
first_name VARCHAR NOT NULL,
last_name VARCHAR NOT NULL, 
gender VARCHAR NOT NULL,
level VARCHAR NOT NULL,
PRIMARY KEY (user_id))
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id VARCHAR, 
title VARCHAR NOT NULL,
artist_id VARCHAR NOT NULL, 
year INT, 
duration NUMERIC NOT NULL,
PRIMARY KEY (song_id))
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id VARCHAR, 
name VARCHAR NOT NULL,
location VARCHAR, 
latitude FLOAT, 
longitude FLOAT,
PRIMARY KEY (artist_id))
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time TIMESTAMP,
hour INT NOT NULL,
day INT NOT NULL,
week INT NOT NULL,
month INT NOT NULL,
year INT NOT NULL,
weekday INT NOT NULL,
PRIMARY KEY (start_time))
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level = users.level
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO UPDATE SET name = artists.name, location = artists.location, latitude = artists.latitude, longitude = artists.longitude
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id 
FROM songs s
JOIN artists a
ON s.artist_id = a.artist_id
WHERE s.title = (%s) AND a.name = (%s) AND s.duration = (%s)
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]