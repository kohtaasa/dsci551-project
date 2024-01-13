# HoboDB

## Introduction
This project aimed to design and implement a document-oriented NoSQL database, named HonoDB, that supports JSON data models. 
The motivation behind the project was to create a simple database system that allows users to interact with data through a Command-Line Interface (CLI). 

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

## System Structure
The database system is structured as follows:
- **User**: This represents the end user who interacts with the database system.
- **CLI (Command Line Interface)**: This is the interface through which the user sends commands to the database system. It processes user input and can perform CRUD (Create, Read, Update, Delete) operations other than queries directly on the database.
- **Query**: The user sends a database query via the CLI. This query is a structured request for data retrieval.
- **Query Parser**: Once the CLI receives a query, it's sent to the Query Parser. The Query Parser's role is to interpret and validate the syntax of the query. It ensures that the query is correctly formatted and can be understood by the database system.
- **Query Engine**: After parsing, the query is processed by the Query Engine. This engine is responsible for the logical and efficient execution of the query.
- **Database Engine**: This component is responsible for the actual manipulation and management of the database. It executes the CRUD operations except for queries on the data stored in File Storage.
- **File Storage**: This is where the actual data is stored in JSON format. The Query Engine and Database Engine may retrieve data from or store data in this File Storage as per the command's requirements.

![system](https://github.com/kohtaasa/dsci551-project/blob/main/system_structure.png?raw=true)


This database is designed to run on a main memory with approximately 5MB. The dataset (https://www.kaggle.com/datasets/nathanlauga/nba-games) is stored in chunks of 5MB in JSON format. When inserting data, the system checks if a file exceeds 5MB and creates a new file if it does. When processing queries, the system loads one file at a time to make sure it does not load the entire dataset. Furthermore, we implemented an external sorting algorithm for sorting and aggregation operations by computing local aggregation in each chunk first and then merging them.



## CRUD Operations
The language supports all fundamental CRUD (Create, Read, Update, Delete) operations, structured as follows:

### Create Operations
- Database Creation: `create db <database_name>`
  - Example: `create db nba`
- Collection Creation: `create collection <collection_name>`
  - Example: `create collection coaches`

### Insert Operations
- Single Item Insertion: `insert <collection> <data>`
  - Example: `insert coaches {"id": 1, "name": "john", "age": 50, "team": "LAL"}`
- Bulk Item Insertion: `insertMany <collection> [list of data]`
  - Example: `insertMany coaches [{"id": 2, "name": "sam", "age": 61, "team": "GSW"}, {"id": 3, "name": "steve", "age": 49, "team": "BRN"}]`

### Read Operations
- Listing Databases: `list db`
- Listing Collections: `list collection`
- Executing Queries: `query <query>`
  - Example: explained in the next section

### Update Operations
- Single Item Update: `modify <collection> <condition> <new_data>`
  - Example: `modify coaches {"name": "john"} {"position": "HC"}`
- Bulk Update: `modifyMany <collection> <condition> <new_data>`
  - Example: `modifyMany coaches {"gender": "M"} {"position": "HC"}`

### Delete Operations
- Deleting a Database: `drop db <database_name>`
  - Example: `drop db nba`
- Deleting a Collection: `drop collection <collection_name>`
  - Example: `drop collection coaches`
- Single Item Deletion: `remove <collection> <condition>`
  - Example: `remove coaches {"age": 50}`
- Bulk Item Deletion: `removeMany <collection> <condition>`
  - Example: `removeMany coaches {"gender": "M"}`

## Example Query
``query GET season, tm, COUNT(player), AVG(age) FROM players FILTER season = '2024' GROUP season, tm SORT age_avg DESC``

### Supported Aggregation Function
- MIN
- MAX
- AVG
- COUNT
- SUM






