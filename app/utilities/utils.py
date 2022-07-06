import json


def print_json(data):
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)


def byte_to_json(my_bytes_value, replace=True):
    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON
    if replace:
        my_json = my_bytes_value.decode('utf8').replace("'", '"')
    else:
        my_json = my_bytes_value.decode('utf8')
    # print(my_json)
    # print('- ' * 20)

    # Load the JSON to a Python list & dump it back out as formatted JSON
    return json.loads(my_json)
