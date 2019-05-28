#!/home/pi/lidar-processor/lidar_env/bin/python

import os
import json

DIRECTORY = "data"

the_path = os.path.dirname(os.path.abspath(__file__))


def get_05_05_2019_encoder_measures(directory_name: str):
    """

    :param directory_name:
    :return:
    """
    if os.path.exists(os.path.join("samples", "05_05_2019", directory_name)):
        measures = []
        for filename in os.listdir(os.path.join("samples", "05_05_2019", directory_name)):
            if filename.startswith("encoder"):
                with open(os.path.join("samples", "05_05_2019", directory_name, filename), "r") as f:
                    data = json.load(f)
                    measures.append([[float(k) for k in j] for j in data])
        return measures
    else:
        return None


def get_05_05_2019_lidar_measures(directory_name: str):
    """

    :param directory_name:
    :return:
    """
    if os.path.exists(os.path.join("samples", "05_05_2019", directory_name)):
        measures = []
        for filename in os.listdir(os.path.join("samples", "05_05_2019", directory_name)):
            if filename.startswith("lidar"):
                with open(os.path.join("samples", "05_05_2019", directory_name, filename), "r") as f:
                    data = json.load(f)
                    measures.append([[float(k) for k in j] for j in data])
        return measures
    else:
        return None


def get_table_measures(directory_name: str):
    """

    :param directory_name:
    :return:
    """
    if os.path.exists(os.path.join("samples", directory_name)):
        measures = []
        for filename in os.listdir(os.path.join("samples", directory_name)):
            with open(os.path.join("samples", directory_name, filename), "r") as f:
                data = json.load(f)
                measures.append([[float(k) for k in j] for j in data])
        return measures
    else:
        return None


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
