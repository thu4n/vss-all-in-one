import json
from collections import defaultdict

def merge_dicts(d1, d2):
    dd = defaultdict(list)

    for d in (d1, d2):
        for key, value in d.items():
            if isinstance(value, list):
                dd[key].extend(value)
            else:
                dd[key].append(value)
    return dict(dd)

def merge_multiple_json(json_files):
    merged_dict = {}
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            merged_dict = merge_dicts(merged_dict, data)
    return merged_dict

# Example usage with file paths
json_files = ['vss_releases/vss_rel_3.0.json', 'vss_releases/vss_rel_3.1.1.json', 'vss_releases/vss_rel_4.0.json']
merged_json = merge_multiple_json(json_files)

with open('test.json', 'w') as f:
    json.dump(merged_json, f, indent=2)