import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def compare_values(data1, data2, value_type):
    keys1 = set(data1.keys())
    keys2 = set(data2.keys())
    all_keys = keys1.union(keys2)
    diff_count = 0

    for key in all_keys:
        value1 = data1.get(key, {}).get(value_type)
        value2 = data2.get(key, {}).get(value_type)
        if (value1 != value2) and value1 is not None and value2 is not None:
            diff_count += 1
            print(f"{value_type.capitalize()} mismatch for {key}: {value1} (file 1) != {value2} (file 2)")
        else:
            pass
            # print(f"{value_type.capitalize()} match for {key}: {value1}")
    return diff_count

file_path1 = 'vss_releases_qu/vss_rel_4.2.yaml'
file_path2 = 'vss_releases_qu/vss.yaml'
yaml_data1 = read_yaml(file_path1)
yaml_data2 = read_yaml(file_path2)


# Compare datatype values
datatype_count = compare_values(yaml_data1, yaml_data2, 'datatype')
print(datatype_count)
# Compare unit values
unit_count = compare_values(yaml_data1, yaml_data2, 'unit')
print(unit_count)