#!/usr/bin/python3

"""
The idea is to get a turn of measures, converts them into cartesian coordinates and apply a Hough transform so that
lines are detected. If an 8 cm line is found, then it is one of the three immobile beacons.

The immobile beacons are used to change basis from the robot's to the table's.
"""

from typing import List
from math import cos, sin


def keep_good_measures(turn: List, threshold: int):
    """

    :param turn: list of measures ; one measure is [angle (in rad), distance (in m), quality (from 0 to 47)]
    :param threshold:
    :return:
    """
    return [measure for measure in turn if measure[3] > threshold]


def polar_to_x(measure: List):
    angle, distance = measure
    return distance*cos(angle)


def polar_to_y(measure: List):
    angle, distance = measure
    return distance*sin(angle)


def one_turn_to_cartesian_points(turn: List):
    return [(polar_to_x(measure), polar_to_y(measure)) for measure in turn]


def hough_transform(cartesian_points):
    pass


def find_immobile_beacons(accumulative_space):
    pass

