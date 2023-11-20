import json
import os


def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


def calculate_data_size(data):
    json_string = json.dumps(data)
    byte_data = json_string.encode('utf-8')
    return len(byte_data)


def get_next_file_number(base_file_name):
    # Get a list of files that match the base file path
    matching_files = [file for file in os.listdir("../data") if file.startswith(base_file_name)]

    # Return the count of matching files plus 1
    return len(matching_files)


def split_json_by_size(base_file_name, input_json, max_size):
    # Convert input JSON string to a Python object (assuming it's an array)
    with open(input_json, 'r') as file:
        json_data = json.load(file)

    current_size = 0
    current_data = []

    for item in json_data:
        # Calculate the size of the current item
        data_size = calculate_data_size(item)
        # Check if adding the current item exceeds the maximum size
        if current_size + data_size > max_size:
            # If it does, write the current data to a new file
            file_number = get_next_file_number(base_file_name)
            output_filename = f'../data/{base_file_name}_{file_number}.json'
            write_json_to_file(current_data, output_filename)

            # Reset current data and size
            current_data = []
            current_size = 0

        # Add the current item to the current data
        current_data.append(item)
        current_size += data_size

    # Write any remaining data to a new file
    if current_data:
        file_number = get_next_file_number(base_file_name)
        output_filename = f'../data/{base_file_name}_{file_number}.json'
        write_json_to_file(current_data, output_filename)


if __name__ == '__main__':
    split_json_by_size('nba_teams', '../data/nba_teams.json', 4000000)