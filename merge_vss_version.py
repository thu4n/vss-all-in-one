import os
import json
from collections import defaultdict

def merge_dicts(dict1, dict2):
    merged_dict = defaultdict(list)

    for d in (dict1, dict2):
        for key, value in d.items():
            if isinstance(value, list):
                # If it is a list, extend the list in merged_dict with the current list
                merged_dict[key].extend(value)
            else:
                # If it is not a list, append the value to the list in merged_dict
                merged_dict[key].append(value)
    return dict(merged_dict)

def merge_vss_files(vss_folder):
    merged_vss = {}
    vss_files = os.listdir(vss_folder)
    vss_files.sort(reverse=True)
    for vss_file in vss_files:
        file_path = os.path.join(vss_folder, vss_file)
        print(vss_file)
        with open(file_path, 'r') as f:
            vss_data = json.load(f)
            merged_vss = merge_dicts(merged_vss, vss_data)
        
    return merged_vss

vss_folder = "vss_releases/"
merged_vss = merge_vss_files(vss_folder=vss_folder)

with open('test3.json', 'w') as f:
    json.dump(merged_vss, f, indent=2)