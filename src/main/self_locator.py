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


def find_own_position(beacons: List[Beacon], own_colour_team: TeamColor):
    """


    :param beacons: list of the 3 beacons.
    :param own_colour_team:
    :return: [first space coordinate of the robot, second space coordinate of the robot, radius of the robot,
    index of the robot, timestamp]
    """

    for beacon in beacons:
        # TODO improve it, because I need to get polar coordinates to do it correctly
        if own_colour_team == TeamColor.orange:
            x = beacons_orange[beacon.index][0] - beacon.cluster
            y = beacons_orange[beacon.index][1]
            print(x, y)
        elif own_colour_team == TeamColor.purple:
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
