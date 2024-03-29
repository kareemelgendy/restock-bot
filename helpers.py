import json
import sys


# Reads data from JSON file
def read_data(file: str) -> dict or list:
    try:
        with open(f'data/{file}.json') as f:
            data = json.load(f)
        f.close()
        return data
    except FileNotFoundError:
        print('File not found.')
        sys.exit(1)


# Formats letter size to readable size
def format_size(size: str) -> str:
    size = size.replace('-', '').lower()
    return size[0:2] if size[0] == 'x' else size[0]
