#!/home/pi/lidar-processor/lidar_env/bin/python

"""
Works with https://github.com/gobgob/rplidar_a3 which is the server

Received data must respect the following rules:
- each turn of measures is seperated by "M",
- measures in one turn of measures are separated by ";",
- one measure is "<angle>:<distance>:<quality>"

1
"""
import socket
import struct
import time
from threading import Thread
import queue
from typing import List

from main.constants import *

try:
    import numpy as np
except ImportError:
    logging.error("There is no numpy module!!!")


__author__ = ["Clément Besnier", ]

lidar_host = "172.24.1.1"
lidar_port = 17685
encoder_host = "172.16.0.2"
encoder_port = 80

if "numpy" in sys.modules:
    def from_encoder_position_to_lidar_measure(x, y, theta) -> np.ndarray:
        """
        The LiDAR center is not at the rotation center so to compare LiDAR measures and encoder measures,
        a basis change is needed.

        >>> from_encoder_position_to_lidar_measure(125, 523, np.pi/3)
        array([ 65.        , 419.07695155,   1.04719755])

        :param x:
        :param y:
        :param theta:
        :return:
        """
        return np.array([x-120*np.cos(theta), y-120*np.sin(theta), theta])

    def from_lidar_measure_to_encoder_position(x, y, theta) -> np.ndarray:
        """
        The LiDAR center is not at the rotation center so to compare LiDAR measures and encoder measures,
        a basis change is needed.

        >>> from_lidar_measure_to_encoder_position(125, 523, np.pi/3)
        array([ 185.        ,  626.92304845,    1.04719755])

        :param x:
        :param y:
        :param theta:
        :return:
        """
        return np.array([x+120*np.cos(theta), y+120*np.sin(theta), theta])


    def distance_array(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        diff = a - b
        return np.sqrt(diff @ diff.T)


    def are_encoder_measures_and_lidar_measures_different(encoder_measure: np.ndarray, lidar_measure: np.ndarray):
        return np.abs(encoder_measure[2] - lidar_measure[2]) < too_much_angle_shift or \
                distance_array(encoder_measure[:2], lidar_measure[:2])


def split_turn(turn: List[str]) -> List[List[float]]:
    return [[float(i) for i in measure.split(":")] for measure in "".join(turn).split(";") if measure]


def split_encoder_data(encoder_measure: bytes) -> List[int, int, float, float]:
    """
    From an encoder measure to the position and orientation of robot with a timestamp.

    >>> b = [255, 0, 53, 80, 251, 255, 255, 232, 3, 0, 0, 208, 15, 73, 64, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0]

    >>> bi = bytearray(b[3:])
    >>> x, y, theta, t = split_encoder_data(bi)
    >>> x
    -1200

    >>> y
    1000

    >>> theta
    3.141590118408203

    :param encoder_measure:
    :return:
    """
    x, = struct.unpack('i', encoder_measure[:4])
    y, = struct.unpack('i', encoder_measure[4:8])
    orientation, = struct.unpack('f', encoder_measure[8:12])
    return [x, y, orientation, time.time()]


def trame_delimiter(content):
    """

    >>> b = [134, 84, 12, 45, 77, 255, 0, 53, 80, 251, 255, 255, 232, 3, 0, 0, 208, 15, 73, 64, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0]
    >>> bi = bytearray(b)
    >>> trame_delimiter(bi+bi+bi)
    [[-1200, 1000, 3.141590118408203], [-1200, 1000, 3.141590118408203], [-1200, 1000, 3.141590118408203]]

    :param content:
    :return:
    """
    measures = []
    current_measure = bytearray()
    remaining_to_read = 56
    are_robot_position_measures = True
    for c in content:
        if remaining_to_read == 56:
            if c == 255:
                remaining_to_read -= 1
        elif remaining_to_read == 55:
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
            processed_measure = split_encoder_data(current_measure[1:])
            measures.append(processed_measure)
            current_measure = bytearray()

    print([i[:3] for i in measures])


class EncoderThread(Thread):
    def __init__(self, logger_name=None):
        Thread.__init__(self)
        self.measuring = True
        self.measures = queue.LifoQueue()
        if logger_name:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logging.basicConfig(stream=sys.stdout)
            self.logger = logging.getLogger(__name__)
        self.logger.info("On ouvre la connexion aux codeuses.")
        self.encoder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            self.encoder_socket.connect((encoder_host, encoder_port))
        except OSError:
            self.logger.error("Le serveur de codeuses est inaccessible")
            self.encoder_socket = None
            sys.exit(1)

        if self.encoder_socket:
            try:
                self.encoder_socket.send(bytes([0xFF, 0x00, 0x01, 0x01]))  # sign on odometry b'\xFF\x00\x01\x01'
                self.encoder_socket.send(bytes([0xFF, 0x01, 0x01, 0x01]))  # sign off info b'\xFF\x01\x01\x00'
                self.encoder_socket.send(bytes([0xFF, 0x02, 0x01, 0x01]))  # sign off error b'\xFF\x02\x01\x00'
                # self.encoder_socket.send(bytes([0xFF, 0x80, 0x00]))
            except BrokenPipeError as e:
                self.logger.warning("La communication avec le bas-niveau s'est fini trop tôt :"+str(e))
        time.sleep(1)

    def run(self):
        if self.encoder_socket:
            self.logger.info("Connexion au port {}".format(encoder_port))
            current_measure = bytearray()
            are_robot_position_measures = True
            remaining_to_read = 56
            while self.measuring:
                content = self.encoder_socket.recv(100)
                for c in content:
                    if remaining_to_read == 56:
                        if c == 255:
                            remaining_to_read -= 1
                    elif remaining_to_read == 55:
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
                        processed_measure = split_encoder_data(current_measure[1:])
                        self.measures.put(processed_measure.copy(), False)
                        current_measure = bytearray()

                if not self.measuring:
                    self.logger.info("On arrête la récupération des mesures des codeuses")
                    break
            self.logger.info("Connexion aux codeuses fermée")

    def get_measuring(self) -> bool:
        return self.measuring

    def close_connection(self):
        self.measuring = False
        self.encoder_socket.send(b'\xFF\x00\x01\x00')
        time.sleep(1)
        self.encoder_socket.close()

    def get_measures(self) -> List:
        if self.encoder_socket:
            self.logger.debug("Measures of encoder, empty ?"+str(self.measures.empty()))
            measure = self.measures.get(False)
            return measure
        else:
            return []


class LidarThread(Thread):
    def __init__(self, logger_name=None):
        Thread.__init__(self)
        self.measuring = True
        self.measures = queue.LifoQueue()

        if logger_name:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logging.basicConfig(stream=sys.stdout)
            self.logger = logging.getLogger(__name__)
        self.logger.info("On se connecte au LiDAR")

        self.lidar_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.lidar_socket.connect((lidar_host, lidar_port))
        except OSError:
            self.logger.error("Le serveur du LiDAR est inaccessible")
            self.lidar_socket = None
            sys.exit(1)

    def run(self):
        if self.lidar_socket:
            self.logger.info("Connection au port {}".format(lidar_port))
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
                if not self.measuring:
                    break
            self.logger.info("Connexion au LiDAR fermée")

    def get_measuring(self) -> bool:
        return self.measuring

    def close_connection(self):
        self.measuring = False
        self.lidar_socket.close()

    def get_measures(self) -> List:
        if self.lidar_socket:
            res = self.measures.get()
            # self.logger.info("measure "+ str(res))
            return res
        else:
            return []


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
