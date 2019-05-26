#!/usr/bin/python3

"""

At the beginning, we know the position of the robot and immobile beacons.

We can follow the immobile beacons as the robot moves.

If we know where the beacons are, we know where the robot is so we get a precise measure of its current position.
"""

from typing import List

from main.constants import *
from main.clustering import Cluster, Beacon
import main.geometry as geom
import main.table as table

__author__ = "Clément Besnier"
p_beacons_orange = [[geom.Point(point[0], point[1]) for point in limits]for limits in beacons_orange]
p_beacons_purple = [[geom.Point(point[0], point[1]) for point in limits]for limits in beacons_purple]


def define_point_beacons(own_colour: TeamColor):
    if own_colour.value == TeamColor.orange.value:
        bo1 = table.Rectangle(p_beacons_orange[0]).get_center()
        print(bo1)
        bo2 = table.Rectangle(p_beacons_orange[1]).get_center()
        print(bo2)
        bo3 = table.Rectangle(p_beacons_orange[2]).get_center()
        print(bo3)
        return bo1, bo2, bo3
    elif own_colour.value == TeamColor.purple.value:
        bp1 = table.Rectangle(p_beacons_purple[0]).get_center()
        print(bp1)
        bp2 = table.Rectangle(p_beacons_purple[1]).get_center()
        print(bp2)
        bp3 = table.Rectangle(p_beacons_purple[2]).get_center()
        print(bp3)
        return bp1, bp2, bp3


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


def change_basis(rp: geom.Point, ori: float, measures: List):
    # measures = outr.one_turn_to_cartesian_points(measures)
    new_measures = []
    for measure in measures:
        p = geom.Point(measure[0], measure[1])
        p.rotate(-ori)
        new_measure = p + rp
        new_measures.append([new_measure.x, new_measure.y])
    return new_measures
