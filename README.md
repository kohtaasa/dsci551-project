# HoboDB

## Get Started
1. **Enter the CLI**: Run `honodb.sh` to start the command-line interface.
2. **Select the database**: This is crucial as all operations are contextually based on the active database.

## File Structure
- cli.py: handle operations related to CLI (call function.py to query_executor.py to perform CRUD operations)
- functions.py: handle CRUD operations except for query (insertion, deletion, modification)
- query_executor.py: parse query given by users and process it (call query.py)
- query.py: handles query operations (projection, filtering, grouping, aggregation, and sorting)
- data directory: store dataset in JSON format
- metadata.json: store metadata of the database system

## Storage System
- Save database in several files as chunks (5 MB)
- File name should be {database_name}_{collection_name}_number.json
  - if one file exceeds a certain size the data will be saved in a new file
    - {database_name}_{collection_name}_1.json
    - {database_name}_{collection_name}_2.json

## CRUD Operations
### Create Database
``create db <database_name>``
### Create collection
``create collection <collection_name>``

### Insert data to a collection
#### Insert a single item  
``insert <collection> <data>``  
Example: ``insert students {"id": "s100", "name": "foo"}``

#### Insert multiple items
``insertMany <collection> [list of data]`` 

### Read
List databases: ``list db``  
List collections: ``list collection``  
Run queries: ``query <query>``

### Update
#### Update a single item
``modify <collection> <condition> <new_data>``

#### Update multiple items
``modifyMany <collection> <condition> <new_data>``

### Delete
#### Delete database
``drop db <database_name>``
#### Delete collection
``drop collection <collection_name>``

#### Delete a single item
``remove <collection> <condition> ``

#### Delete multiple items
``removeMany <collection> <condition>``

## Query Language
``query GET season, tm, COUNT(player), AVG(age) FROM players FILTER season = '2024' GROUP season, tm SORT age_avg DESC``

### Aggregation Function
- MIN
- MAX
- AVG
- COUNT
- SUM






