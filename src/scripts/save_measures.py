#! /usr/bin/python3

import os
import time
import json
from src.main.data_retrieval import LidarThread


def store_data():
    for i in range(20):
        with open(os.path.join("lidar-process", "src", "samples", "data_"+str(i)+".json"), "w") as f:
            data = t.get_measures()
            json.dump(data, f)
        time.sleep(2)


if __name__ == "__main__":
    t = LidarThread()
    t.start()
    time.sleep(2)
    store_data()
    # print(t.get_measures())
    # time.sleep(3)
    t.close_connection()
    time.sleep(3)
    print(t.is_alive())
    # sys.exit(0)
    
