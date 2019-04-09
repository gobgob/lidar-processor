#!/usr/bin/python3

"""
The idea is to get a turn of measures, converts them into cartesian coordinates and apply a Hough transform so that
lines are detected. If an 8 cm line is found, then it is one of the three immobile beacons.

The immobile beacons are used to change basis from the robot's to the table's.
"""

from typing import List
import math
import numpy as np


def keep_good_measures(turn: List, threshold: int):
    """

    :param turn: list of measures ; one measure is [angle (in rad), distance (in m), quality (from 0 to 47)]
    :param threshold:
    :return:
    """
    return [measure[:2] for measure in turn if measure[2] > threshold]


def polar_to_x(measure: List):
    angle, distance = measure
    return distance*math.cos(math.radians(angle))


def polar_to_y(measure: List):
    angle, distance = measure
    return distance*math.sin(math.radians(angle))


def one_turn_to_cartesian_points(turn: List):
    return [(polar_to_x(measure), polar_to_y(measure)) for measure in turn]


def get_width_height(cartesian_points):
    """

    :param cartesian_points:
    :return:
    """
    points = np.array(cartesian_points)
    print(points.shape)
    x_min, x_max, y_min, y_max = points[:, 0].min(), points[:, 0].max(), points[:, 1].min(), points[:, 1].max()
    return x_max - x_min, y_max - y_min


def get_mins(cartesian_points):
    """

    :param cartesian_points:
    :return:
    """
    points = np.array(cartesian_points)
    print(points.shape)
    x_min, x_max, y_min, y_max = points[:, 0].min(), points[:, 0].max(), points[:, 1].min(), points[:, 1].max()
    return x_min, y_min


def change_basis(cartesian_points):
    l = []
    x_min, y_min = get_mins(cartesian_points)
    for i in range(len(cartesian_points)):
        x, y = cartesian_points[i]
        x, y = x - x_min, y - y_min
        l.append([x, y])
    return l, [-x_min, -y_min]


def hough_transform(cartesian_points, angle_step=0.2):
    """

    :param cartesian_points:
    :param angle_step:
    :return:
    """
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width, height = get_width_height(cartesian_points)
    diag_len = int(round(math.sqrt(width * width + height * height)))
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)
    accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
    for i in range(len(cartesian_points)):
        x, y = cartesian_points[i]
        for t_idx in range(num_thetas):
            rho = diag_len + int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            accumulator[rho, t_idx] += 20
    return accumulator, thetas, rhos


def peak_votes(accumulator, thetas, rhos):
    """ Finds the max number of votes in the hough accumulator """
    idx = np.argmax(accumulator)
    rho = rhos[int(idx / accumulator.shape[1])]
    theta = thetas[idx % accumulator.shape[1]]

    return idx, theta, rho


def theta2gradient(theta):
    return np.cos(theta) / np.sin(theta)


def rho2intercept(theta, rho):
    return rho / np.sin(theta)


def find_immobile_beacons(accumulative_space):
    pass
