#!/usr/bin/python3

"""

At the beginning, we know the position of the robot and immobile beacons.

We can follow the immobile beacons as the robot moves.

If we know where the beacons are, we know where the robot is so we get a precise measure of its current position.
"""
import time
from typing import List

import numpy as np

from main.clustering import Cluster

__author__ = "Clément Besnier"


def find_beacons(cluster: List[Cluster]):
    """
    
    :param cluster: 
    :return: 
    """""
    fix_beacons = []
    for cluster in cluster:
        solution = cluster.is_a_fix_beacon()
        if np.numeric.isclose(solution.fun,  0.0001):
            fix_beacons.append(solution.x)
    return fix_beacons


def find_own_position(beacon_positions: List[np.ndarray]) -> List[int, int, int, int, float]:
    """

    :param beacon_positions: list of positions of the 3 beacons.
    :return: [first space coordinate of the robot, second space coordinate of the robot, radius of the robot,
    index of the robot, timestamp]
    """
    x, y, r, i, t = 0, 0, 0, 0, time.time()
    # TODO write the code!!!!!!! Of course.

    return [x, y, r, i, t]
