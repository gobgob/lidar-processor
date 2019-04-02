import socket
import time
from threading import Thread
import queue
from typing import List

hote = "127.0.0.1"
port = 17685


def split_turn(turn: List[str]):
    return [measure.split(":") for measure in "".join(turn).split(";")]


def read_lidar_measures():
    global measuring
    lidar_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lidar_socket.connect((hote, port))
    print("Connection on {}".format(port))
    measures = queue.Queue(maxsize=10)

    while measuring:
        # socket.send(b"R")
        # time.sleep(1)
        current_measure = []
        content = lidar_socket.recv(5000).decode("utf-8")
        for c in content:
            if c == 'M':
                measures.put(split_turn(current_measure))
                current_measure = []
            else:
                current_measure.append(c)
    if not measures.empty():
        print(measures.get())
    print("Close")
    lidar_socket.close()


if __name__ == "__main__":
    measuring = True
    Thread(target=read_lidar_measures).start()
    input("Blabla")
    measuring = False
