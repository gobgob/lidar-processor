#!/home/pi/lidar-processor/lidar_env/bin/python

"""
LiADR and encoder measures 05/05/2019.
"""

import os
import sys
import time
import json
from main.data_retrieval import LidarThread, EncoderThread


def store_lidar_data_05_05_2019(thread_lidar, i_measure: int):
    folder = os.path.join("samples", "05_05_2019")
    if not os.path.exists(os.path.join(folder, str(i_measure))):
        os.mkdir(os.path.join(folder, str(i_measure)))
    for i in range(20):
        with open(os.path.join(folder, str(i_measure), "data_"+str(i)+".json"), "w") as f:
            data = thread_lidar.get_measures()
            json.dump(data, f)
        time.sleep(2)


def store_lidar_and_encoder_data_05_05_2019(lidar_thread: LidarThread, encoder_thread: EncoderThread, i_measure: int):
    """
    Script 05/05/2019

    :param lidar_thread:
    :param encoder_thread:
    :param i_measure:
    :return:
    """

    measuring_duration = 30
    start_time = time.time()
    now = time.time()
    folder = os.path.join("samples", "05_05_2019")
    if not os.path.exists(os.path.join(folder, str(i_measure))):
        os.mkdir(os.path.join(folder, str(i_measure)))

    while now - start_time < measuring_duration:
        with open(os.path.join("samples", "05_05_2019", str(i_measure), "lidar_data_"+str(now)+".json"), "w") as f:
            lidar_turn_data = lidar_thread.get_measures()
            json.dump(lidar_turn_data, f)
            print("lidar")

        with open(os.path.join("samples", "05_05_2019", str(i_measure), "encoder_data_"+str(now)+".json"), "w") as f:
            encoder_data = encoder_thread.get_measures()
            json.dump(encoder_data, f)
            print("encoder")

        time.sleep(1)
        now = time.time()


def take_lidar_measure_05_05_2019(i_measure: int):
    t = LidarThread()
    t.start()
    time.sleep(2)
    store_lidar_data_05_05_2019(t, i_measure)
    # print(t.get_measures())
    # time.sleep(3)
    t.close_connection()
    time.sleep(3)
    print(t.is_alive())
    # sys.exit(0)


def take_lidar_and_encoder_measures_05_05_2019(i_measure: int):
    t_lidar = LidarThread()
    t_encoder = EncoderThread()
    t_lidar.start()
    t_encoder.start()
    time.sleep(2)
    store_lidar_and_encoder_data_05_05_2019(t_lidar, t_encoder, i_measure)
    # print(t.get_measures())
    # time.sleep(3)
    t_lidar.close_connection()
    t_encoder.close_connection()
    time.sleep(3)
    print(t_lidar.is_alive())
    print(t_encoder.is_alive())
    sys.exit(0)


if __name__ == "__main__":
    measure_number = 7
    take_lidar_and_encoder_measures_05_05_2019(measure_number)
