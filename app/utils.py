import json
from pathlib import Path
from datetime import datetime
import hashlib


def load_json_data(path: Path, category: str) -> list:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            contents = json.load(f)
    except Exception as e:
        contents = []
        print(f'Error loading {category}: {e}')
    return contents


def format_date(created_at):
    now = datetime.now()
    post_time = datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S GMT')
    delta = now - post_time
    
    seconds = delta.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:  
        minutes = int(seconds // 60)
        return f"{minutes}m ago"
    elif seconds < 86400:  
        hours = int(seconds // 3600)
        return f"{hours}h ago"
    elif seconds < 604800:  
        days = int(seconds // 86400)
        return f"{days}d ago"
    elif now.year == post_time.year:  
        return post_time.strftime("%b %d")  
    else:
        return post_time.strftime("%b %d, %Y")

def get_gravatar_profile(email):
    hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    return f'https://gravatar.com/avatar/{hash}'