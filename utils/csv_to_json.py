import csv
import json


def csv_to_json(csv_file_path, json_file_path, skip_conversion_columns=None):
    if skip_conversion_columns is None:
        skip_conversion_columns = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        data = []
        for row in csv_reader:
            processed_row = {}
            for key, value in row.items():
                # Skip conversion for specified columns
                if key in skip_conversion_columns:
                    processed_row[key] = value
                else:
                    try:
                        processed_row[key] = int(value)  # Try converting to integer
                    except ValueError:
                        try:
                            processed_row[key] = float(value)  # Try converting to float
                        except ValueError:
                            processed_row[key] = value  # Keep as string
            data.append(processed_row)

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Example usage:
csv_file_path = '/Users/kohtaasakura/Documents/DSCI551/Player Totals.csv'
json_file_path = '../data/nba_players.json'
skip_columns = ['seas_id', 'season', 'player_id', 'birth_year']
csv_to_json(csv_file_path, json_file_path, skip_columns)
