#! /usr/bin/python3

"""

"""
from typing import List

import numpy as np

from main.clustering import Cluster

__author__ = "Clément Besnier"


def find_robots(cluster: List[Cluster]):
    robots = []
    for cluster in cluster:
        solution = cluster.is_an_adverse_robot_beacon()
        if np.numeric.isclose(solution.fun,  0.0001):
            robots.append(solution.x)
    return robots
