import json 

def get_url_by_name(collection_json, target_name):
    items = collection_json.get("item", [])
    if not isinstance(items, list):
        return None
    
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if name == target_name:
            # Navigate safely to 'raw' url string
            request = item.get("request")
            if not isinstance(request, dict):
                return None
            url = request.get("url")
            if not isinstance(url, dict):
                return None
            raw_url = url.get("raw")
            return raw_url
    return None


def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)