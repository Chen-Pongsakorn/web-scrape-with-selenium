import json

def read_json(local_file):
    with open(local_file) as json_file:
        data = json.load(json_file)

    return data

def write_json(data, path):
    with open(path, 'w') as json_file:
        json.dump(data, json_file)