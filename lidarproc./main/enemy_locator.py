#!/home/pi/lidar-processor/lidar_env/bin/python

"""
Opponent robots are located thanks to their specific beacons on their top.

At the beginning, we look for the robot

"""
import time
from typing import List

import numpy as np

import main.geometry as geom
from main.constants import *
from main.clustering import Cluster
import main.table as ta

__author__ = "Clément Besnier"


P_PURPLE_START_ZONE = [geom.Point(p[0], p[1]) for p in PURPLE_START_ZONE]
P_ORANGE_START_ZONE = [geom.Point(o[0], o[1]) for o in ORANGE_START_ZONE]


def find_robots_in_zone(zone: ta.Rectangle, clusters: List[Cluster], robot_position: geom.Point,
                        robot_orientation: float):
    """

    :param zone:
    :param clusters:
    :param robot_position:
    :param robot_orientation:
    :return:
    """

    robot_paramters = []

    zone = zone.m_translate(robot_position).rotate(np.pi / 2 - robot_orientation)
    # zone = zone.m_translate(robot_position).rotate(robot_orientation)
    print("centre de la zone de départ adverse "+str(zone))
    opponent_robots = []
    for cluster in clusters:
        if zone.is_close_enough(cluster):
            opponent_robots.append(cluster.get_mean())

    print("number of clusters in zone: ", len(opponent_robots), opponent_robots)

    for i, opponent_robot in enumerate(opponent_robots):
        robot_paramters.append([opponent_robot[0], opponent_robot[1], i, int(time.time())])
    return robot_paramters


def find_robots_in_purple_zone(clusters: List[Cluster]):
    """

    :param clusters:
    :return: x, y, radius, index, timestamp
    """
    robot_position = geom.Point(PURPLE_SELF_X, PURPLE_SELF_Y)
    robot_orientation = PURPLE_SELF_THETA

    purple_zone = ta.Rectangle(P_PURPLE_START_ZONE)
    if isinstance(clusters[0], Cluster):
        return find_robots_in_zone(purple_zone, clusters, robot_position, robot_orientation)
    return find_robots_in_zone(purple_zone, clusters, robot_position, robot_orientation)


def find_robot_in_orange_zone(clusters: List[Cluster]):
    """

    :param clusters:
    :return: x, y, radius, index, timestamp
    """
    robot_position = geom.Point(PURPLE_SELF_X, PURPLE_SELF_Y)
    robot_orientation = PURPLE_SELF_THETA

    orange_zone = ta.Rectangle(P_ORANGE_START_ZONE)

    if isinstance(clusters[0], Cluster):
        return find_robots_in_zone(orange_zone, clusters, robot_position, robot_orientation)
    return find_robots_in_zone(orange_zone, clusters, robot_position, robot_orientation)


def find_robots(clusters: List[Cluster]):
    """

    :param clusters:
    :return:
    """
    robots = []
    for cluster in clusters:
        solution = cluster.get_mean()
        robots.append([solution[0], solution[1], time.time()])
    return robots
