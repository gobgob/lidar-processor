#! /usr/bin/python3

"""
Opponent robots are located thanks to their specific beacons on their top.

At the beginning, we look for the robot

"""
import time
from typing import List

import numpy as np

from main.constants import *
from main.clustering import Cluster
import main.table as ta

__author__ = "Clément Besnier"


def find_robots_in_zone(zone: ta.Rectangle, clusters: List[Cluster]):
    """

    :param zone:
    :param clusters:
    :return:
    """
    robot_paramters = []
    clusters_in_purple_zone = [cluster for cluster in clusters if zone.is_cluster_in_rectangle(cluster)]
    opponent_robots = [cluster for cluster in clusters_in_purple_zone if cluster.is_an_opponent_robot_beacon()]
    for i, opponent_robot in enumerate(opponent_robots):
        params = opponent_robot.is_a_circle(OPPONENT_ROBOT_BEACON_RADIUS)
        robot_paramters.append([params.x[0], params.x[1], OPPONENT_ROBOT_BEACON_RADIUS, i, int(time.time())])
    return robot_paramters


def find_robots_in_purple_zone(clusters: List[Cluster]) -> np.ndarray:
    """

    :param clusters:
    :return: x, y, radius, index, timestamp
    """
    purple_zone = ta.Rectangle(*PURPLE_START_ZONE)
    return find_robots_in_zone(purple_zone, clusters)


def find_robot_in_orange_zone(clusters: List[Cluster]) -> np.ndarray:
    """

    :param clusters:
    :return: x, y, radius, index, timestamp
    """
    orange_zone = ta.Rectangle(*ORANGE_SELF_THETA)
    return find_robots_in_zone(orange_zone, clusters)


def find_robots(cluster: List[Cluster]):
    """

    :param cluster:
    :return:
    """
    robots = []
    for cluster in cluster:
        solution = cluster.is_an_opponent_robot_beacon()
        if np.numeric.isclose(solution.fun, 0.0001):
            robots.append(solution.x)
    return robots
