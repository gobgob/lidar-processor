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


def find_robots_in_purple_zone(clusters: List[Cluster]) -> np.ndarray:
    """

    :param clusters:
    :return: x, y, radius, index, timestamp
    """
    return None


def find_robot_in_yellow_zone(clusters: List[Cluster]) -> np.ndarray:
    """

    :param clusters:
    :return: x, y, radius, index, timestamp
    """
    return None
