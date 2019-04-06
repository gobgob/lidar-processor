#!/usr/bin/python3

"""
Works with https://github.com/gobgob/rplidar_a3 which is the server
"""

import socket
import time
from threading import Thread
import queue
from typing import List
import sys

__author__ = ["Clément Besnier", ]

hote = "127.0.0.1"
port = 17685


def split_turn(turn: List[str]):
    return [measure.split(":") for measure in "".join(turn).split(";") if measure]

class LidarThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.measuring = True
        self.measures = queue.Queue(maxsize=10)
        self.lidar_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lidar_socket.connect((hote, port))

    def run(self):
        print("Connection on {}".format(port))
        current_measure = []
        while self.measuring:
            content = self.lidar_socket.recv(500).decode("utf-8")
            for c in content:
                if c == 'M':
                    a = split_turn(current_measure)
                    self.measures.put(a)
                    current_measure = []
                    # self.close()
                else:
                    current_measure.append(c)
        print("connexion fermée")

    def get_measuring(self):
        return self.measuring

    def close_connection(self):
        self.lidar_socket.close()
        self.measuring = False

    def get_measures(self):
        return self.measures.get()


if __name__ == "__main__":
    t = LidarThread()
    t.start()
    time.sleep(10)
    print(t.get_measures())
    time.sleep(3)
    t.close_connection()
    time.sleep(3)
    print(t.is_alive())
    # sys.exit(0)
    

