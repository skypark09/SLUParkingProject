import csv
from constants import NEW_CSV, ORIGINAL_CSV, TARGET_INDEX, TARGET_VALUE, ELEMKEY


def read_header(file_path):
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
    return header

def read_from_csv(file_path, index, target_value):
    rows = []
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if len(row) == 0:
                pass
            elif row[index] == target_value:
                rows.append(row)
    return rows

def write_to_csv(read_from_file_path, write_to_file_path):
    header = read_header(read_from_file_path)
    lines = read_from_csv(read_from_file_path, TARGET_INDEX, TARGET_VALUE)
    with open(write_to_file_path, "w") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        csvwriter.writerows(lines)


def read_csv_keys(file_path):
    keys = []
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if len(row) > 0:
                keys.append(row[ELEMKEY])
    return keys


def write_csv_keys(read_from_path, write_to_path):
    keys = read_csv_keys(read_from_path)
    with open(write_to_path, "w") as file:
        for key in keys:
            file.writelines(key)


def read_txt_keys(file_path):
    keys = []
    with open(file_path, "r") as file:
        for key in file:
            key = int(key)
            keys.append(str(key))
    return keys


def read_csv_element(file_path, element_index):
    with open(file_path, "r") as file:
        for line in file:
            pass
