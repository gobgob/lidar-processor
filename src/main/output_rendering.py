#!/usr/bin/python3

"""
The idea is to get a turn of measures, converts them into cartesian coordinates and apply a Hough transform so that
lines are detected. If an 8 cm line is found, then it is one of the three immobile beacons.

The immobile beacons are used to change basis from the robot's to the table's.
"""

from typing import List
import math
import numpy as np
from collections import defaultdict


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


def cartesian_to_polar(cartesian):
    x, y = cartesian
    if x != 0:
        return [math.atan(y/x), math.sqrt(x*x+y*y)]
    else:
        return [math.pi/2, y]


def one_turn_to_cartesian_points(turn: List):
    return [(polar_to_x(measure), polar_to_y(measure)) for measure in turn]


# def cartesian_points_to_array(cartesian_points):
#     np.zeros(())


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


def hough_transform(cartesian_points, angle_step=0.3):
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
    # accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
    accumulator = defaultdict(int)

    # for i in range(len(cartesian_points)):
    for i in range(len(cartesian_points)):
        x, y = cartesian_points[i]
        for t_idx in range(num_thetas):
            rho = int(round(diag_len+x * cos_t[t_idx] + y * sin_t[t_idx]))
            accumulator[rho, thetas[t_idx]] += 1
    return accumulator, thetas, rhos


def take_brightest_points(accumulator):
    theta_max = 0
    rho_max = 0
    max_value = 0

    greatest_theta = 0
    greatest_rho = 0
    lowest_theta = 0
    lowest_rho = 0
    for key in accumulator:
        current_rho, current_theta = key
        if accumulator[key] > max_value:
            max_value = accumulator[key]
            rho_max, theta_max = key
        if current_rho > greatest_rho:
            greatest_rho = current_rho
        if current_theta > greatest_theta:
            greatest_theta = current_theta
        if current_theta < lowest_theta:
            lowest_theta = current_theta
        if current_rho < lowest_rho:
            lowest_rho = current_rho
    extrema = [lowest_theta, greatest_theta, lowest_rho, greatest_rho]
    print("extrema", extrema)
    print("theta", theta_max)
    print("rho", rho_max)

    return [max_value], [theta_max], [rho_max], extrema


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
