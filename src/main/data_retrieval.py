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

__author__ = ["Clément Besnier", ]

lidar_host = "127.0.0.1"
lidar_port = 17685
encoder_host = "172.16.0.2"
encoder_port = 80


def split_turn(turn: List[str]):
    return [measure.split(":") for measure in "".join(turn).split(";") if measure]


def split_encoder_data(encoder_measure: bytearray):
    """
    From an encoder measure to the position and orientation of robot with a timestamp.

    :param encoder_measure:
    :return:
    """
    decoded_turn = b"".join(encoder_measure).decode("utf8")
    x = decoded_turn[:4]
    y = decoded_turn[4:9]
    orientation = decoded_turn[9:13]
    return [x, y, orientation, time.time()]


class EncoderThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.measuring = True
        self.measures = queue.Queue(maxsize=10)
        self.encoder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encoder_socket.connect((encoder_host, encoder_port))
        self.encoder_socket.send(b'\xFF\x00\x01\x01')  # sign on odometry
        self.encoder_socket.send(b'\xFF\x01\x01\x00')  # sign off info
        self.encoder_socket.send(b'\xFF\x02\x01\x00')  # sign off error

    @staticmethod
    def interpret_bytes(byte_list, field_list):
        output = []
        i = 0
        for field in field_list:
            try:
                if field.type == int:
                    val, = struct.unpack_from("<i", byte_list, i)
                    i += struct.calcsize("<i")
                elif field.type == float:
                    val, = struct.unpack_from("<f", byte_list, i)
                    i += struct.calcsize("<f")
                elif field.type == bool:
                    val, = struct.unpack_from("<?", byte_list, i)
                    i += struct.calcsize("<?")
                else:
                    raise ValueError
                output.append(val)
            except (IndexError, struct.error, ValueError):
                print("Byte list:", byte_list, "Field name:", field.name)
                raise
        return output

    def run(self):
        print("Connection on {}".format(lidar_port))
        current_measure = bytearray()
        are_robot_position_measures = True
        remaining_to_read = 56
        while self.measuring:
            content = self.encoder_socket.recv(100)
            for c in content:
                if remaining_to_read == 56:
                    if c == b"\xFF":
                        remaining_to_read -= 1
                elif remaining_to_read == 55:
                    are_robot_position_measures = c == b"\x00"
                    remaining_to_read -= 1

                elif are_robot_position_measures and remaining_to_read <= 54:
                    current_measure.append(c)
                    remaining_to_read -= 1

                elif remaining_to_read == 0:
                    remaining_to_read = 56
                    # self.interpret_bytes(current_measure, )
                    processed_measure = split_encoder_data(current_measure)
                    self.measures.put(processed_measure)
                    current_measure = bytearray()

        print("connexion fermée")

    def get_measuring(self):
        return self.measuring

    def close_connection(self):
        self.encoder_socket.send(b'0xFF 0x00 0x01 0x00')
        time.sleep(1)
        self.encoder_socket.close()
        self.measuring = False

    def get_measures(self):
        return self.measures.get()


class LidarThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.measuring = True
        self.measures = queue.Queue(maxsize=10)
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
