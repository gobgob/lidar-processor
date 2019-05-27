#!/usr/bin/python3

"""

At the beginning, we know the position of the robot and immobile beacons.

We can follow the immobile beacons as the robot moves.

If we know where the beacons are, we know where the robot is so we get a precise measure of its current position.
"""

from typing import List

import numpy as np

from main.constants import *
from main.clustering import Cluster, Beacon
import main.geometry as geom
import main.data_retrieval as dr
import main.table as table

__author__ = "Clément Besnier"
p_beacons_orange = [[geom.Point(point[0], point[1]) for point in limits]for limits in beacons_orange]
p_beacons_purple = [[geom.Point(point[0], point[1]) for point in limits]for limits in beacons_purple]


def define_point_beacons(own_colour: TeamColor):
    if own_colour.value == TeamColor.orange.value:
        bo1 = table.Rectangle(p_beacons_orange[0]).get_center()
        bo2 = table.Rectangle(p_beacons_orange[1]).get_center()
        bo3 = table.Rectangle(p_beacons_orange[2]).get_center()
        return bo1, bo2, bo3
    elif own_colour.value == TeamColor.purple.value:
        bp1 = table.Rectangle(p_beacons_purple[0]).get_center()
        bp2 = table.Rectangle(p_beacons_purple[1]).get_center()
        bp3 = table.Rectangle(p_beacons_purple[2]).get_center()
        return bp1, bp2, bp3


def find_starting_beacons(own_colour: TeamColor, clusters: List[Cluster]):
    b1, b2, b3 = define_point_beacons(own_colour)
    if own_colour.value == TeamColor.orange.value:
        starting_position = geom.Point(-1210, 1400)
        starting_orientation = 0
    elif own_colour.value == TeamColor.purple.value:
        starting_position = geom.Point(1210, 1400)
        starting_orientation = np.pi

    p_b1_lidar = geom.from_theoretical_table_to_lidar(b1, starting_position, starting_orientation)
    p_b2_lidar = geom.from_theoretical_table_to_lidar(b2, starting_position, starting_orientation)
    p_b3_lidar = geom.from_theoretical_table_to_lidar(b3, starting_position, starting_orientation)

    # print("b1 vu du LiDAR"+str(p_b1_lidar))
    # print("b2 vu du LiDAR"+str(p_b2_lidar))
    # print("b3 vu du LiDAR"+str(p_b3_lidar))

    found_b1, found_b2, found_b3 = None, None, None

    for cluster in clusters:
        mean = cluster.get_mean()
        if mean is not None:
            d1 = dr.distance_array(mean, p_b1_lidar.to_array())
            d2 = dr.distance_array(mean, p_b2_lidar.to_array())
            d3 = dr.distance_array(mean, p_b3_lidar.to_array())

            if d1 < 200:
                found_b1 = mean.copy()
                print("mean et b1 : ", mean, p_b1_lidar)
            if d2 < 200:
                found_b2 = mean.copy()
                print("mean et b2 : ", mean, p_b2_lidar)
            if d3 < 200:
                found_b3 = mean.copy()
                print("mean et b3 : ", mean, p_b3_lidar)

    return found_b1, found_b2, found_b3


def find_beacons(cluster: List[Cluster]) -> List[Beacon]:
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


def print_beacons(beacons: List[Beacon]):
    for b in beacons:
        print("Beacon")
        print("* center: ", b.center)
        print("* index: ", b.index)
        print("* x", b.x_center)
        print("* y", b.y_center)


def find_relative_point_beacons(beacons: List[geom.Point], robot_position: geom.Point, robot_orientation: float):
    """
    >>> beacons = list(define_point_beacons(TeamColor.orange))
    >>> find_relative_point_beacons(beacons, geom.Point(), 0)
    :param beacons:
    :param robot_position:
    :param robot_orientation:
    :return:
    """


def find_own_position(beacons: List[Beacon], own_colour_team: TeamColor):
    """


    :param beacons: list of the 3 beacons.
    :param own_colour_team:
    :return: [first space coordinate of the robot, second space coordinate of the robot, radius of the robot,
    index of the robot, timestamp]
    """

    b1, b2, b3 = define_point_beacons(own_colour_team)

    for beacon in beacons:
        # TODO improve it, because I need to get polar coordinates to do it correctly
        if own_colour_team.value == TeamColor.orange.value:
            x = beacons_orange[beacon.index][0] - beacon.cluster
            y = beacons_orange[beacon.index][1]
            print(x, y)
        elif own_colour_team.value == TeamColor.purple.value:
            x = beacons_purple[beacon.index][0]
            y = beacons_purple[beacon.index][1]
            print(x, y)

    beacon_1 = Beacon()
    beacon_1.set_by_upper_left_and_lower_right(beacons_purple[0][0], beacons_purple[0][1])

    beacon_2 = Beacon()
    beacon_2.set_by_upper_left_and_lower_right(beacons_purple[1][0], beacons_purple[1][1])

    beacon_3 = Beacon()
    beacon_3.set_by_upper_left_and_lower_right(beacons_purple[2][0], beacons_purple[2][1])
    return None


def change_basis(rp: geom.Point, ori: float, measures: List):
    # measures = outr.one_turn_to_cartesian_points(measures)
    new_measures = []
    for measure in measures:
        p = geom.Point(measure[0], measure[1])
        p.rotate(-ori)
        new_measure = p + rp
        new_measures.append([new_measure.x, new_measure.y])
    return new_measures
