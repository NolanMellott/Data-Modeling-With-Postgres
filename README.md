# Reflection
Below is the ReadMe for the project itself, this section is simply a reflection on what I did/learned during this project.
This was my second time data modeling with postgresql inside of python.
I mainly learned how to model data based on multiple input data files while creating a data schema.
previously I just needed to make a data model for one input file.
I laern a lot of transoformation within this project while working through the jupyter notebook and the etl script.
I also learned more about incorporating unit tests into my code to help identify answers to possible questions.
Overall I feel more comfortable in my ability to model data with one or more input data files and imputing data to create fact tables.

### Purpose
This database exists to give the startup Sparkify the ability to query their datasets.
Their data was original contained in json files which cannot be searched/queried easiy.
The database will allow Sparkify to perform analysis on song listenings.
Whether it is finding the number of songs one individual listened to or how many people listned to a particular artist.
Sparkify will have the ability to perform SQL queries to find (most of) the information they may need for analysis.
### How to Use Python Scripts
To run the python scripts you must understand a few things:
* The create_tables.py script **MUST ALWAYS ** run first before any other files (that aren't the data json files).
* create_tables.py essentially "resets" the database by dropping all previous data and repopulating the database with all data files using the SQL statements in sql_queries.py.
* The script executes all of the SQL statements required for the database to be created.
* etl.py contains all of the ETL processes required to populate the database.
* It contains some data cleaning, data transformation, and data loading using pandas dataframes.
* sql_queries.py contains all of the SQL statements used to create and populate the the database.
Now that we understand what our python scripts are and what they do we can finally use them.
First, the user must open a python terminal with access to the scripts, afterwards you will type "python (insert script file)" then press enter.
For example, you would want to do:
```
python create_tables.py
python etl.py
```
As stated before the first script will reset the database to be empty, then the second script will populate the database and the third script does not need to be run by a human as create_tables reads from it to execute SQL statements.
After these two scripts are run, the user can use the test.ipynb notebook to run unit tests.
### Files Explained
This project contains six files including this one, and a folder.
* The folder contains all of the data that is used to populate the database
* test.ipynb is a jupyter notebook which contains unit tests which test:
> If the database is populated.
> If certain tables have the correct datatypes.
> If those tables have constraints on specific columns.
> If the insert SQL statements have upserts on conflicts.
* create_tables.py as stated before is a python script which executes the SQL statements inside of sql_queries.py which will reset and rebuild the structure of the database.
* etl.ipynb is a jupyter notebook which was used to test the ETL processes on single files before using the processes on all of the files.
* etl.py as stated before is a python script which contains the ETL processes to populate the database.
* sql_queries.py contains all of the SQL statements that the previous three files use to drop, rebuild, and populate the database.
### Scheme Design
This database uses a star schema, which means there is one fact table and multiple dimension tables, in this case there are four dimension tables.
Each dimension table has a primary key which references a value inside of the fact table.
### ETL Process
The ETL process is fairly simple for this database.
All of the neccessary data comes from two sets of files:
The Song dataset is a subset of a real dataset [Million Song Dataset](http://millionsongdataset.com)
it contains multiple json files which will contain information that looks like this:
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```
The second set of data comes from an [event simulator](https://github.com/Interana/eventsim) which creates logs based on the above songs.
The json files will contain information that looks like this:
```
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
```
The json files are loaded into the etl.py script where they undergo a few transformations before being loaded into the different tables.
The etl.py file is full of comments so I reccomend reading that for further information on the ETL process.
