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

def metadata_tree_to_dict(tree):
    def add_children(flattened_tree, path, value):
        if "children" in value:
            for child_path, value in value["children"].items():
                add_children(flattened_tree, f"{path}.{child_path}", value)
        else:
            flattened_tree[path] = value

    flattened_tree = {}

    for key, value in tree.items():
        add_children(flattened_tree, key, value)

    return flattened_tree

def merge_vss_files(vss_folder):
    vss_files = os.listdir(vss_folder)
    for vss_file in vss_files:
        file_path = os.path.join(vss_folder, vss_file)
        
        with open(file_path, 'r') as f:
            vss_data = json.load(f)
            merged_vss = merge_dicts(merged_vss, vss_data)
        
    return merged_vss

vss_folder = "vss_releases/"
merged_vss = merge_vss_files(vss_folder=vss_folder)