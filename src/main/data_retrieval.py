#!/usr/bin/python3

"""
Works with https://github.com/gobgob/rplidar_a3 which is the server

Received data must respect the following rules:
- each turn of measures is seperated by "M",
- measures in one turn of measures are separated by ";",
- one measure is "<angle>:<distance>:<quality>"


"""

import socket
import struct
import time
from threading import Thread
import queue
from typing import List

# import numpy as np

# from main.constants import *

__author__ = ["Clément Besnier", ]

lidar_host = "172.24.1.1"
lidar_port = 17685
encoder_host = "172.16.0.2"
encoder_port = 80


# def from_encoder_position_to_lidar_measure(x, y, theta):
#     """
#     The LiDAR center is not at the rotation center so to compare LiDAR measures and encoder measures,
#     a basis change is needed.
#
#     >>> from_encoder_position_to_lidar_measure(125, 523, np.pi/3)
#     array([ 65.        , 419.07695155,   1.04719755])
#
#     :param x:
#     :param y:
#     :param theta:
#     :return:
#     """
#     return np.array([x-120*np.cos(theta), y-120*np.sin(theta), theta])
#
#
# def distance_array(a, b):
#     diff = a - b
#     return np.sqrt(diff @ diff.T)
#
#
# def are_encoder_measures_and_lidar_measures_different(encoder_measure: np.ndarray, lidar_measure: np.ndarray):
#     return np.abs(encoder_measure[2] - lidar_measure[2]) < too_much_angle_shift or \
#             distance_array(encoder_measure[:2], lidar_measure[:2])


def split_turn(turn: List[str]):
    return [measure.split(":") for measure in "".join(turn).split(";") if measure]


def split_encoder_data(encoder_measure: bytes):
    """
    From an encoder measure to the position and orientation of robot with a timestamp.

    >>> measure = b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
    >>> x, y, theta, t = split_encoder_data(measure)
    >>> x
    16843009

    >>> y
    16843009

    >>> theta
    16843009

    :param encoder_measure:
    :return:
    """
    x, = struct.unpack('i', encoder_measure[:4])
    y, = struct.unpack('i', encoder_measure[4:8])
    orientation, = struct.unpack('f', encoder_measure[8:12])
    return [x, y, orientation, time.time()]


class EncoderThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.measuring = True
        self.measures = queue.Queue(maxsize=1)
        self.encoder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encoder_socket.connect((encoder_host, encoder_port))
        self.encoder_socket.send(bytes([0xFF, 0x00, 0x01, 0x01]))  # sign on odometry b'\xFF\x00\x01\x01'
        self.encoder_socket.send(bytes([0xFF, 0x01, 0x01, 0x01]))  # sign off info b'\xFF\x01\x01\x00'
        self.encoder_socket.send(bytes([0xFF, 0x02, 0x01, 0x01]))  # sign off error b'\xFF\x02\x01\x00'
        # self.encoder_socket.send(bytes([0xFF, 0x80, 0x00]))
        time.sleep(1)
        # content = self.encoder_socket.recv(100)
        # print(content)

    def run(self):
        print("Connection on {}".format(encoder_port))
        current_measure = bytearray()
        are_robot_position_measures = True
        remaining_to_read = 56
        while self.measuring:
            content = self.encoder_socket.recv(100)
            for c in content:
                # print(type(c))
                # print(remaining_to_read)
                if remaining_to_read == 56:
                    # print(c)
                    # print(bytes([0xFF]))
                    # print(b"\xFF")
                    # if c == b"\xFF":

                    # print(c == bytes([0xFF]))
                    # print(c == b"\xFF")
                    if c == 255:
                        remaining_to_read -= 1
                elif remaining_to_read == 55:
                    # print("c", c)
                    are_robot_position_measures = c == 0  # b"\x00"
                    if not are_robot_position_measures:
                        remaining_to_read = 56
                    else:
                        remaining_to_read -= 1

                elif are_robot_position_measures and 0 < remaining_to_read <= 54:
                    current_measure.append(c)
                    remaining_to_read -= 1

                if remaining_to_read == 0:
                    remaining_to_read = 56
                    # self.interpret_bytes(current_measure, )
                    # current_measure[0] is the number of data bytes
                    processed_measure = split_encoder_data(current_measure[1:])
                    # print(processed_measure)
                    self.measures.put(processed_measure)
                    current_measure = bytearray()
                # else:
                #     print(c)
        print("connexion fermée")

    def get_measuring(self):
        return self.measuring

    def close_connection(self):
        self.encoder_socket.send(b'\xFF\x00\x01\x00')
        time.sleep(1)
        self.encoder_socket.close()
        self.measuring = False

    def get_measures(self):
        print("measures of encoder "+str(self.measures.empty()))
        return self.measures.get()

    def send_position_shift(self, position_shift):
        """

        :param: position_shift
        :return:
        """
        # x, y, theta = position_shift[0], position_shift[1], position_shift[2]

        self.encoder_socket.send(b'')


class LidarThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.measuring = True
        self.measures = queue.Queue(maxsize=1)
        self.lidar_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.lidar_socket.connect((lidar_host, lidar_port))

    def run(self):
        print("Connection on {}".format(lidar_port))
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
