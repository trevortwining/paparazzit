import json
import os

def parse_manifest(file_path):
    """
    Parses a JSON manifest file containing a list of URLs.
    Supports:
    - ["https://google.com", "https://github.com"]
    - [{"url": "https://google.com"}, {"url": "https://github.com"}]
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Manifest file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        raise ValueError("Manifest must be a JSON array")
    
    urls = []
    for item in data:
        if isinstance(item, str):
            urls.append(item)
        elif isinstance(item, dict) and 'url' in item:
            urls.append(item['url'])
        else:
            # Skip or raise error? Spec says handles JSON arrays (strings or objects with 'url')
            # For now, let's skip invalid items but maybe log them
            continue
            
    return urls
