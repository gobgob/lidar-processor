#!/usr/bin/python3

"""
Communication with high level of the robot.
The protocol is given at https://github.com/gobgob/chariot-elevateur/blob/master/doc/protocole-lidar-hl.txt

3
"""

import queue
import socket
from threading import Thread

from main.constants import *

__author__ = "Clément Besnier"

hl_host = "127.0.0.0"
hl_port = 8765


class HLThread(Thread):
    """
    Communication to the High-Level
    https://github.com/gobgob/chariot-elevateur/blob/master/high_level/src/main/java/senpai/comm/LidarEth.java
    """
    def __init__(self, logger_name=None):
        Thread.__init__(self)

        self.logger = logging.getLogger(logger_name)
        self.communicating = True
        self.messages = queue.LifoQueue()
        if logger_name:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logging.basicConfig(stream=sys.stdout)

        self.logger.info("On ouvre la socket du haut-niveau.")
        self.hl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.hl_socket.connect((hl_host, hl_port))
        except OSError:
            self.logger.error("Le serveur du haut-niveau est inaccessible")

        self.match_has_begun = False
        self.team_colour = None
        self.match_stopped = False

    def ask_status(self):
        self.hl_socket.send("ASK_STATUS\n".encode("ascii"))

    def send_robot_position(self, x: int, y: int, radius: int, robot_id: int, timestamp: int):
        message_to_send = "OBSTACLE "+str(x)+" "+str(y)+" "+str(radius)+" "+str(robot_id)+" "+str(timestamp)+"\n"
        self.hl_socket.send(message_to_send.encode("ascii"))

    def run(self):
        self.logger.info("Connection on {}".format(hl_port))
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
            if not self.communicating:
                self.logger.info("On arrête la communication avec le haut-niveau")
                break
        self.logger.info("connexion fermée")

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
