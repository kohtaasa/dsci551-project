from functions import *
from query_executor import *
import json
import re
import readline

METADATA_FILE = 'metadata.json'


def validate_command(command: str):
    global selected_db
    # Splitting only on the first two spaces to get the command and collection name
    parts = command.split(' ', 2)
    for_query = command.split(' ', 1)

    if not parts or len(parts) < 2:
        print("Invalid command. Please enter a valid command.")
        return

    command_type = parts[0]

    if command_type == 'select':
        if len(parts) != 2:
            print("Invalid command. Usage: select <database_name>")
        else:
            selected_db = parts[1]
            db_exists = False
            with open(METADATA_FILE, 'r') as file:
                metadata = json.load(file)
                for db in metadata['databases']:
                    if db['name'] == selected_db:
                        print(f"Selected database: {selected_db}")
                        db_exists = True
                        break
                if not db_exists:
                    print(f"Database '{selected_db}' does not exist.")

    elif command_type == 'list' and parts[1] == 'db':
        if len(parts) != 2:
            print("Invalid command. Usage: list db")
        else:
            show_databases()

    elif not selected_db:
        print("No database selected. Please select a database using 'select <database_name>'")

    else:
        if command_type == 'list' and parts[1] == 'collection':
            if len(parts) != 2:
                print("Invalid command. Usage: list collection")
            else:
                show_collections(selected_db)

        elif command_type == 'create':
            if len(parts) != 3:
                print("Invalid command. Usage: create collection/db <collection_name/db_name>")
            else:
                if parts[1] == 'collection':
                    res = create_collection(selected_db, parts[2])
                    if res:
                        print("Collection created successfully.")
                elif parts[1] == 'db':
                    res = create_database(parts[2])
                    if res:
                        print("Database created successfully.")
                else:
                    print("Invalid command. Usage: create collection/db <collection_name/db_name>")

        elif command_type == 'drop':
            if len(parts) != 3:
                print("Invalid command. Usage: drop collection/db <collection_name/db_name>")
            else:
                # Ask for confirmation before dropping
                confirm = input(
                    f"Are you sure you want to drop the {parts[1]} '{parts[2]}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    if parts[1] == 'collection':
                        res = drop_collection(selected_db, parts[2])
                        if res:
                            print("Collection dropped successfully.")
                    elif parts[1] == 'db':
                        res = drop_database(parts[2])
                        if res:
                            print("Database dropped successfully.")
                    else:
                        print("Invalid command. Usage: drop collection/db <collection_name/db_name>")
                else:
                    print(f"Drop operation for {parts[1]} '{parts[2]}' canceled.")

        elif command_type == 'insert':
            if len(parts) != 3:
                print("Invalid command. Usage: insert <collection_name> <data>")
            else:
                collection_name = parts[1]
                data = parts[2]
                res = insert_one(selected_db, collection_name, data)
                if res:
                    print("Insertion successful.")

        elif command_type == 'insertMany':
            if len(parts) != 3:
                print("Invalid command. Usage: insert_many <collection_name> <data>")
            else:
                collection_name = parts[1]
                data = parts[2]
                res = insert_many(selected_db, collection_name, data)
                if res:
                    print("Insertion successful.")

        elif command_type == 'modify':
            # Splitting the third part to get the condition and data
            condition_and_data = re.findall(r'\{.*?\}', parts[2])
            if len(condition_and_data) != 2:
                print("Invalid command. Usage: update <collection_name> <condition> <data>")
            else:
                collection_name = parts[1]
                condition = condition_and_data[0]
                data = condition_and_data[1]
                update_one(selected_db, collection_name, condition, data)

        elif command_type == 'modifyMany':
            # Splitting the third part to get the condition and data
            condition_and_data = re.findall(r'\{.*?\}', parts[2])
            if len(condition_and_data) != 2:
                print("Invalid command. Usage: update <collection_name> <condition> <data>")
            else:
                collection_name = parts[1]
                condition = condition_and_data[0]
                data = condition_and_data[1]
                update_many(selected_db, collection_name, condition, data)

        elif command_type == 'remove':
            if len(parts) != 3:
                print("Invalid command. Usage: delete <collection_name> <condition>")
            else:
                collection_name = parts[1]
                condition = parts[2]
                delete_one(selected_db, collection_name, condition)

        elif command_type == 'removeMany':
            if len(parts) != 3:
                print("Invalid command. Usage: delete_many <collection_name> <condition>")
            else:
                collection_name = parts[1]
                condition = parts[2]
                delete_many(selected_db, collection_name, condition)

        elif command_type == 'query':
            if len(for_query) != 2:
                print("Invalid command. Usage: query <query>")
            else:
                query = for_query[1]
                execute_query(selected_db, query)
        else:
            print("Invalid command. Please try again.")


def print_help_message():
    help_message = """
Exit the app
    Command: exit

Select a database
    Command: select <database_name>

CRUD Operations
---------------    
Create Operations
    Create Database
        Command: create db <database_name>
        Description: Creates a new database with the specified name.
    
    Create Collection
        Command: create collection <collection_name>
        Description: Creates a new collection within the current database.
    
    Insert Data to a Collection
        Insert a single item
            Command: insert <collection> <data>
            Example: insert students {"id": "s100", "name": "foo"}
    
        Insert multiple items
            Command: insertMany <collection> [list of data]

Read Operations
    List databases
        Command: list db

    List collections
        Command: list collection

    Run queries
        Command: query <query>

Update Operations
    Update a single item
        Command: modify <collection> <condition> <new_data>

    Update multiple items
        Command: modifyMany <collection> <condition> <new_data>

Delete Operations
    Delete database
        Command: drop db <database_name>

    Delete collection
        Command: drop collection <collection_name>

    Delete a single item
        Command: remove <collection> <condition>

    Delete multiple items
        Command: removeMany <collection> <condition>

Query Language
--------------
    Example Query: 
    GET season, tm, COUNT(player), AVG(age) 
    FROM players 
    FILTER season = '2024' 
    GROUP season, tm 
    SORT age_avg DESC
"""
    print(help_message)


def main():
    ascii_art = """
    __  __                  ____  ____ 
   / / / /___  ____  ____  / __ \/ __ )
  / /_/ / __ \/ __ \/ __ \/ / / / __  |
 / __  / /_/ / / / / /_/ / /_/ / /_/ / 
/_/ /_/\____/_/ /_/\____/_____/_____/  
    """
    print(ascii_art)
    print("Welcome to HonoDB!")
    print("Type 'help' for a list of commands.")

    while True:
        command = input("HonoDB>> ").strip()
        if command == "exit":
            print("Goodbye!")
            break
        elif command == "help":
            print_help_message()
        else:
            validate_command(command)


if __name__ == '__main__':
    selected_db = None
    main()
