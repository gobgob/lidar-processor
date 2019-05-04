#!/usr/bin/python3

"""

At the beginning, we know the position of the robot and immobile beacons.

We can follow the immobile beacons as the robot moves.

If we know where the beacons are, we know where the robot is so we get a precise measure of its current position.
"""
import time
from typing import List

import numpy as np

from main.constants import *
from main.clustering import Cluster, Beacon

__author__ = "Clément Besnier"


def find_beacons(cluster: List[Cluster]):
    """
    
    :param cluster: 
    :return: 
    """""
    fix_beacons = []
    for cluster in cluster:
        beacon = cluster.is_a_fix_beacon()
        if beacon:
            fix_beacons.append(beacon)
    return fix_beacons


def find_own_position(beacons: List[Beacon], own_colour_team: TeamColor) -> List[int, int]:
    """


    :param beacons: list of the 3 beacons.
    :param own_colour_team:
    :return: [first space coordinate of the robot, second space coordinate of the robot, radius of the robot,
    index of the robot, timestamp]
    """

    for beacon in beacons:
        # TODO imporve it, because I need to get polar coordinates to do it correctly
        if own_colour_team == TeamColor.orange:
            x = beacons_orange[beacon.index][0] - beacon.cluster
            y = beacons_orange[beacon.index][1]
            print(x, y)
        elif own_colour_team == TeamColor.purple:
            x = beacons_purple[beacon.index][0]
            y = beacons_purple[beacon.index][1]
            print(x, y)
