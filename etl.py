import os
import glob
import psycopg2
import numpy
import pandas as pd
from sql_queries import *
from psycopg2.extensions import register_adapter, AsIs

def process_song_file(cur, filepath):
    '''
    -This function takes a filepath and reads each json file within it
    -With these files it creates a song record and artist record
    -Both records are then inserted into their respective tables
    '''
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = artist_data = df[
        ['artist_id',
         'artist_name',
         'artist_location',
         'artist_latitude',
         'artist_longitude']
    ].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    '''
    -This function takes a filepath and reads each json file within it
    -It then filters the data and converts some columns into proper datatypes
    -The data is then ready to be loaded into multiple different tables
    '''
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query('page == "NextSong"')

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour,
             t.dt.day, t.dt.week, t.dt.year,
             t.dt.month, t.dt.weekday)
    column_labels = ('timestamp', 'hour',
                 'day', 'week', 'year',
                 'month', 'weekday')
    time_df = pd.DataFrame.from_dict((dict(zip(column_labels, time_data))))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
        
    # Fixes datatype incompatibilities
    register_adapter(numpy.int64, addapt_numpy_int64)
    
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
        songplay_data = [
            time_df['timestamp'][index],
            user_df['userId'][index],
            user_df['level'][index],
            songid,
            artistid,
            df['sessionId'][index],
            df['location'][index],
            df['userAgent'][index]]
        cur.execute(songplay_table_insert, songplay_data)
        
def process_data(cur, conn, filepath, func):
    '''
    -Creates a for loop so every file in a filepath can be used
    '''
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
        
def addapt_numpy_int64(numpy_int64):
    '''        
    -Fixes np and psycopg2 datatype incompatibilities
    '''
    return AsIs(numpy_int64)

def main():
    '''
    -Uses all of the previous functions to populate the database
    '''
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()
    
if __name__ == "__main__":
    '''
    -calls the main function
    '''
    main()