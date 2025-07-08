import json
from pathlib import Path

def load_json_data(path: Path, category: str) -> list:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            contents = json.load(f)
    except Exception as e:
        contents = []
        print(f'Error loading {category}: {e}')
    return contents
