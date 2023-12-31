from query import *
import shlex
import re


METADATA_FILE = 'metadata.json'


def parse_query(query):
    parts = shlex.split(query, posix=False)
    parts_lower = [part.lower() for part in parts]
    try:
        get_index = parts_lower.index("get")
        from_index = parts_lower.index("from")
        if from_index <= get_index:
            return None, None, None, None, None, None, None
    except ValueError:
        return None, None, None, None, None, None, None

    filter_index = parts_lower.index("filter") if "filter" in parts_lower else None
    group_index = parts_lower.index("group") if "group" in parts_lower else None
    sort_index = parts_lower.index("sort") if "sort" in parts_lower else None
    limit_index = parts_lower.index("limit") if "limit" in parts_lower else None

    # Ensure the order of keywords
    keyword_indices = [index for index in [filter_index, group_index, sort_index, limit_index] if index is not None]
    if any(keyword_indices[i] <= keyword_indices[i - 1] for i in range(1, len(keyword_indices))):
        return None, None, None, None, None, None, None

    conditions = []
    group_by = []
    sort_by = []
    limit = None
    reverse = False

    # Extracting GET clause
    columns = ' '.join(parts[get_index + 1:from_index]).replace(',', '').split()

    # Extracting FROM clause
    table = parts[from_index + 1]

    # Function to process individual filter values
    def process_filter_value(value):
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return value.strip('"') if value.startswith('"') and value.endswith('"') else value

    # Custom function to process the FILTER clause
    def custom_filter_parser(filter_parts):
        in_list = False
        parsed_conditions = []
        current_condition = []

        for part in filter_parts:
            if '[' in part:
                in_list = True
                current_condition.append(part.replace('[', ''))
            elif ']' in part:
                in_list = False
                part = part.replace(']', '')
                if part:  # Append the last part before the closing bracket, if it exists
                    current_condition.append(process_filter_value(part))
                parsed_conditions.append('[' + ''.join(map(str, current_condition)) + ']')
                current_condition = []
            elif in_list and part != ',':
                current_condition.append(process_filter_value(part))
            elif not in_list:
                parsed_conditions.append(process_filter_value(part))

        return parsed_conditions

    # Extracting FILTER clause
    if filter_index:
        filter_end = group_index or sort_index or limit_index or len(parts)
        filter_parts = parts[filter_index + 1:filter_end]
        conditions = custom_filter_parser(filter_parts)

    # Extracting GROUP clause
    if group_index:
        group_end = sort_index or limit_index or len(parts)
        group_by = ' '.join(parts[group_index + 1:group_end]).replace(',', '').split()

    # Extracting SORT clause
    if sort_index:
        sort_end = limit_index or len(parts)
        sort_by = ' '.join(parts[sort_index + 1:sort_end]).replace(',', '').split()
        sort_by_lower = [item.lower() for item in sort_by]
        reverse = "desc" in sort_by_lower

        if "desc" in sort_by_lower:
            sort_by.remove("DESC") if "DESC" in sort_by else sort_by.remove("desc")
        elif "asc" in sort_by_lower:
            sort_by.remove("ASC") if "ASC" in sort_by else sort_by.remove("asc")

    # Extracting LIMIT clause
    if limit_index:
        limit = int(parts[limit_index + 1])

    return columns, table, conditions, group_by, sort_by, reverse, limit


def convert_to_nested_format(condition_list):
    operator_mapping = {
        '>': 'gt',
        '<': 'lt',
        '>=': 'gte',
        '<=': 'lte',
        '=': 'eq',
        '!=': 'ne',
        'in': 'in',
        'IN': 'in',
        'nin': 'nin',
        'NIN': 'nin',
    }
    operator_flip = {
        '>': '<',
        '<': '>',
        '>=': '<=',
        '<=': '>=',
    }

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def handle_condition(sublist):
        first, operator_symbol, second = sublist

        if is_number(first):
            # Flip the operator if number/string precedes the column name
            operator_symbol = operator_flip.get(operator_symbol, operator_symbol)
            target, value = second, first
        else:
            target, value = first, second

        if isinstance(value, str):
            value = value.strip('\'"')

        operator = operator_mapping[operator_symbol]
        return {'target': target, 'condition': operator, 'value': value}

    conditions = []
    current_operator = None
    i = 0

    while i < len(condition_list):
        if condition_list[i].upper() in ['AND', 'OR']:
            if current_operator and conditions:
                conditions = [{'operator': current_operator, 'conditions': conditions}]
            current_operator = condition_list[i].upper()
            i += 1
            continue

        condition = handle_condition(condition_list[i:i + 3])
        conditions.append(condition)
        i += 3

    if current_operator:
        return {'operator': current_operator, 'conditions': conditions}
    else:
        return conditions[0]


def parse_aggregation_query(input_list):
    group_key = []
    targets = {}

    # Regular expression pattern to match aggregation functions
    agg_pattern = re.compile(r'(\w+)\((\w+)\)')  # Matches 'COUNT(field)' or 'AVG(field)'

    for item in input_list:
        match = agg_pattern.match(item)
        if match:
            # If the item is an aggregation function, extract the function and field
            func, field = match.groups()
            targets[field] = func.lower()  # Convert function to lowercase ('count', 'avg', etc.)
        else:
            # If the item is not an aggregation function, add it to group keys
            group_key.append(item)

    return group_key, targets


def execute_query(database, query):
    try:
        columns, table, conditions, group_by, sort_by, reverse, limit = parse_query(query)
    except ValueError:
        print("Invalid query")
        return

    if not columns:
        print("Invalid query")
        return

    file_number = get_last_file_number(METADATA_FILE, database, table)
    if not file_number:
        print(f'Collection {table} does not exist')
        return
    input_files = [f'data/{database}_{table}_{i}.json' for i in range(1, file_number + 1)]
    intermediate_results = [save_json_items_to_tempfile(input_file) for input_file in input_files]

    try:
        if conditions:
            converted_conditions = convert_to_nested_format(conditions)
            intermediate_results = [filter_by_values(temp_file, converted_conditions) for temp_file in intermediate_results]

        if group_by:
            for column in group_by:
                if column not in columns:
                    print(f"Column '{column}' need to be selected")
                    return

            group_key, targets = parse_aggregation_query(columns)
            partial_agg = [partial_aggregate(temp_file, group_key, targets) for temp_file in intermediate_results]
            final_agg = final_aggregate(partial_agg, targets)

            if sort_by:
                sorted_file = sort_and_write_chunk(final_agg, sort_by, reverse)
                with open(sorted_file, 'r') as file:
                    for i, line in enumerate(file):
                        if limit is not None and i == limit:
                            break
                        print(line.strip())
                os.remove(sorted_file)
            else:
                with open(final_agg, 'r') as file:
                    for i, line in enumerate(file):
                        if limit is not None and i == limit:
                            break
                        print(line.strip())

        elif not group_by:
            if sort_by:
                sorted_file = execute_external_sort(intermediate_results, sort_by, reverse=reverse)
                with open(sorted_file, 'r') as file:
                    for i, line in enumerate(file):
                        if limit is not None and i == limit:
                            break
                        print(json.dumps(select_record_fields(json.loads(line), columns)))
                os.remove(sorted_file)
            else:
                results = [select_fields(temp_file, columns) for temp_file in intermediate_results]
                count = 0
                for result in results:
                    for item in result:
                        if limit is not None and count == limit:
                            break
                        count += 1
                        print(json.dumps(item))

    except Exception as e:
        print(f"Error during query execution: {e}")

    finally:
        # Clean up all intermediate files
        for temp_file in intermediate_results:
            if os.path.exists(temp_file):
                os.remove(temp_file)
