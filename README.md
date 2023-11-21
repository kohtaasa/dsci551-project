# Note
## Storage System
- Save database in several files as chunks
- File name should be {database_name}_{collection_name}_number.json
  - if one file exceeds a certain size the data will be saved in a new file
    - {database_name}_{collection_name}_1.json
    - {database_name}_{collection_name}_2.json
    
## Query Execution
### Sort
External sort

### Group by (aggregation)
- 2 step aggregation
- partial aggregation on each chunk
- final aggregation on partial results
- **does not support COUNT DISTINCT**


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
GET season, tm, COUNT(player), AVG(age) FROM players FILTER season = '2024' GROUP season, tm SORT age_avg DESC

### Aggregation Function
- GROUP
- new column name 






