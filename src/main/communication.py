#!/usr/bin/python3

"""
Communication with high level of the robot.
The protocole is given at https://github.com/gobgob/chariot-elevateur/blob/master/doc/protocole-lidar-hl.txt
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
        self.communicating = True
        self.messages = queue.Queue(maxsize=1)
        self.hl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hl_socket.connect((hl_host, hl_port))

        self.match_has_begun = False
        self.team_colour = None
        self.match_stopped = False
        # self.

    def ask_status(self):
        self.hl_socket.send("ASK_STATUS\n".encode("ascii"))

    def send_robot_position(self, x: int, y: int, radius: int, robot_id: int, timestamp: int):
        message_to_send = "OBSTACLE "+str(x)+" "+str(y)+" "+str(radius)+" "+str(robot_id)+" "+str(timestamp)+"\n"
        self.hl_socket.send(message_to_send.encode("ascii"))

    def run(self):
        print("Connection on {}".format(hl_port))
        current_measure = []

        while self.communicating:
            content = self.hl_socket.recv(100).decode("ascii")
            for c in content:
                if c == '\n':
                    current_measure = "".join(current_measure)
                    if current_measure == "ACK":
                        # self.messages.put("ACK")
                        pass
                    elif current_measure == "INIT VIOLET":
                        self.team_colour = TeamColor.purple
                    elif current_measure == "INIT JAUNE":
                        self.team_colour = TeamColor.orange
                    elif current_measure == "START":
                        self.match_has_begun = True
                    elif current_measure == "STOP":
                        self.match_stopped = True

                    current_measure = []
                else:
                    current_measure.append(c)
        print("connexion fermée")

    def get_measuring(self):
        return self.communicating

    def close_connection(self):
        self.hl_socket.close()
        self.communicating = False

    def has_match_begun(self):
        return self.match_has_begun

    def get_team_colour(self):
        return self.team_colour

    def has_match_stopped(self):
        return self.match_stopped
