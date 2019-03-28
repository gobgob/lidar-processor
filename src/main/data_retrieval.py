import socket
import time

import queue
hote = "127.0.0.1"
port = 17685


def read_lidar_measures():
    lidar_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lidar_socket.connect((hote, port))
    print("Connection on {}".format(port))
    measures = queue.Queue()
    with open("mesures.txt", "w") as f:

        while True:
            # socket.send(b"R")
            # time.sleep(1)
            one_message = lidar_socket.recv(100000).decode("utf-8")
            f.write(one_message + "\n")
            measures.put(one_message)
    print("Close")
    lidar_socket.close()
