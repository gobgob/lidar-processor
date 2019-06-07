#!/home/pi/lidar-processor/lidar_env/bin/python

import datetime
import os
import time
import json
from lidarproc.main.data_retrieval import LidarThread, EncoderThread


def store_lidar_data(t):
    for i in range(5):
        with open(os.path.join("samples", "data_"+datetime.datetime.today().ctime().replace(":", "")+".json"), "w")\
                as f:
            data = t.get_measures()
            json.dump(data, f)
        time.sleep(2)


def store_lidar_and_encoder_data(lidar_thread: LidarThread, encoder_thread: EncoderThread):
    """
    Script 28/04/2019

    :param lidar_thread:
    :param encoder_thread:
    :return:
    """
    measureing_duration = 10
    start_time = time.time()
    now = time.time()
    while now - start_time < measureing_duration:

        with open(os.path.join("samples", "lidar_data_" + str(now) + ".json"), "w") as f:
            lidar_turn_data = lidar_thread.get_measures()
            json.dump(lidar_turn_data, f)
            print("lidar")

        # with open(os.path.join("samples", "encoder_data_" + str(now) + ".json"), "w") as f:
        #     encoder_data = encoder_thread.get_measures()
        #     json.dump(encoder_data, f)
        #     print("encoder")

        time.sleep(1)
        now = time.time()


def take_lidar_measure():
    t = LidarThread()
    t.start()
    time.sleep(2)
    store_lidar_data(t)
    # print(t.get_measures())
    # time.sleep(3)
    t.close_connection()
    time.sleep(3)
    print(t.is_alive())
    # sys.exit(0)


def take_lidar_and_encoder_measures():
    t_lidar = LidarThread()
    # t_encoder = EncoderThread()
    t_lidar.start()
    # t_encoder.start()
    time.sleep(2)
    store_lidar_and_encoder_data(t_lidar, None)
    # print(t.get_measures())
    # time.sleep(3)
    t_lidar.close_connection()
    # t_encoder.close_connection()
    time.sleep(3)
    print(t_lidar.is_alive())
    # print(t_encoder.is_alive())
    # sys.exit(0)


if __name__ == "__main__":
    # take_lidar_and_encoder_measures()
    take_lidar_measure()
