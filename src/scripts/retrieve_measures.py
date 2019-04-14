#! /usr/bin/python3

# import sys
import os
import json

from src import the_path


def get_data():
    measures = []
    for i in range(20):

        with open(os.path.join(the_path, "samples", "data_" + str(i) + ".json"), "r") as f:
            data = json.load(f)
            measures.append([[float(k) for k in j] for j in data])
    return measures


def get_realistic_data():
    measures = []
    print(os.getcwd())
    for i in range(20):
        with open(os.path.join('C:\\Users\\Clément\\PycharmProjects\\lidar-processor', 'data', "sample--1000-1100", "data_" + str(i) + ".json"), "r") as f:
            data = json.load(f)
            measures.append([[float(k) for k in j] for j in data])
    return measures


if __name__ == "__main__":
    # get_data()
    get_realistic_data()
