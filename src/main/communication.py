#!/usr/bin/python3

"""
Communication with high level of the robot.
"""
import queue
import socket
from threading import Thread

from main.constants import *

__author__ = "Clément Besnier"

hl_host = "127.0.0.0"
hl_port = 8765


class HLThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.measuring = True
        self.messages = queue.Queue(maxsize=10)
        self.hl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hl_socket.connect((hl_host, hl_port))

    def ask_status(self):
        self.hl_socket.send("ASK_STATUS\n".encode("ascii"))

    def send_robot_position(self, x: int, y: int, radius: int, robot_id: int, timestamp: int):
        message_to_send = "OBSTACLE "+str(x)+" "+str(y)+" "+str(radius)+" "+str(robot_id)+" "+str(timestamp)+"\n"
        self.hl_socket.send(message_to_send.encode("ascii"))

    def run(self):
        print("Connection on {}".format(hl_port))
        current_measure = []

        while self.measuring:
            content = self.hl_socket.recv(100).decode("ascii")
            for c in content:
                if c == '\n':
                    current_measure = "".join(current_measure)
                    if current_measure == "ACK":
                        self.messages.put("ACK")
                    elif current_measure == "INIT VIOLET":
                        self.messages.put(TeamColor.purple)
                    elif current_measure == "INIT JAUNE":
                        self.messages.put(TeamColor.yellow)
                    elif current_measure == "START":
                        self.messages.put(current_measure)
                    elif current_measure == "STOP":
                        self.messages.put(current_measure)

                    current_measure = []
                else:
                    current_measure.append(c)
        print("connexion fermée")

    def get_measuring(self):
        return self.measuring

    def close_connection(self):
        self.hl_socket.close()
        self.measuring = False

    def get_measures(self):
        return self.messages.get()
