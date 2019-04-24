#!usr/bin/python3

import os
import json

from src import the_path

DIRECTORY = "data"


def get_measure_directories():
    return [file for file in os.listdir(os.path.join(the_path, DIRECTORY))
            if os.path.isdir(os.path.join(the_path, DIRECTORY, file))]


def extract_position_from_directory(sample_directory: str):
    if sample_directory.startswith('sample_'):
        positions = sample_directory[len("sample_"):]
        x, y = positions.split("_")
        return x, y
    else:
        return None


def get_realistic_data():
    measures = []
    print(os.getcwd())
    for i in range(20):
        with open(os.path.join(the_path, 'data', "sample_-1000_1100", "data_" + str(i) + ".json"), "r") as f:
            data = json.load(f)
            measures.append([[float(k) for k in j] for j in data])
    return measures


if __name__ == "__main__":
    print(get_measure_directories())
    print(extract_position_from_directory("sample_-1000_1100"))
    get_realistic_data()