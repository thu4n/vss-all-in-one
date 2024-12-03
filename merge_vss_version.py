from deepmerge import Merger
import json
import os
import argparse

parser = argparse.ArgumentParser(
                    prog='VSS-Merger (beta)',
                    description='A Python program to merge COVESA-VSS versions. Datatypes and other metadata will be taken from the first vss.json in the list')

parser.add_argument('-s', '--slim', action='store_true', help='Output file will not contain uuid and comment.')
parser.add_argument('-t', '--target-directory', type=str, default='./vss_releases', help="Target directory to read vss.json files from")

my_merger = Merger(
    [
        (list, ["append_unique"]),
        (dict, ["merge"]),
        (set, ["union"])
    ],
    ["use_existing"],  # Fallback Strategies
    ["use_existing"] # Type conflict Strategies
)

def merge_vss_files(vss_folder):
    merged_vss = {}
    vss_files = os.listdir(vss_folder)
    vss_files.sort(reverse=True)
    for vss_file in vss_files:
        file_path = os.path.join(vss_folder, vss_file)
        print(vss_file)
        with open(file_path, 'r') as f:
            vss_data = json.load(f)
            merged_vss = my_merger.merge(merged_vss, vss_data)
        
    return merged_vss

def filter_dict(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = filter_dict(value)
        elif key != "uuid" and key != "comment":
            result[key] = value
    return result

if __name__ == '__main__':
    args = parser.parse_args()
    vss_folder = args.target_directory
    slim_mode = args.slim
    merged_vss = merge_vss_files(vss_folder=vss_folder)

    if slim_mode:
        suffix = "_slim"
        merged_vss_slim = filter_dict(merged_vss)
        with open(f'merged_vss{suffix}.json', 'w') as f:
            json.dump(merged_vss_slim, f, indent=2)

    with open(f'merged_vss.json', 'w') as f:
        json.dump(merged_vss, f, indent=2)