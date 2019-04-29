#! /usr/bin/python3

# import sys
import os
import json

the_path = os.path.dirname(os.path.abspath(__file__))


def get_data():
    measures = []
    for i in range(20):

        with open(os.path.join(the_path, "samples", "data_" + str(i) + ".json"), "r") as f:
            data = json.load(f)
            measures.append([[float(k) for k in j] for j in data])
    return measures


if __name__ == "__main__":
    get_data()
