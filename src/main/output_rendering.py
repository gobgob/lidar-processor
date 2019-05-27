#!/usr/bin/python3

"""
The idea is to get a turn of measures, converts them into cartesian coordinates and apply a Hough transform so that
lines are detected. If an 8 cm line is found, then it is one of the three immobile beacons.

The immobile beacons are used to change basis from the robot's to the table's.
"""

from typing import List, Union
import math
import numpy as np
from collections import defaultdict

__author__ = "Clément Besnier"


def polar_to_x(measure: Union[List, np.ndarray]):
    angle, distance = measure[0], measure[1]
    return distance*math.cos(angle)


def polar_to_y(measure: Union[List, np.ndarray]):
    angle, distance = measure[0], measure[1]
    return distance*math.sin(angle)


def cartesian_to_polar(cartesian):
    x, y = cartesian
    if x != 0:
        if x > 0 and y >= 0:
            angle = math.atan(y / x)
        elif x > 0 > y:
            angle = math.atan(y / x) + 2*math.pi
        elif x < 0:
            angle = math.atan(y / x) + math.pi
        elif x == 0 and y > 0:
            angle = math.pi/2
        elif x == 0 and y < 0:
            angle = 3*math.pi/2
        else:
            angle = 0
        return [angle, math.sqrt(x*x+y*y)]
    else:
        return [math.pi/2, y]


def one_turn_to_cartesian_points(turn: List):
    return [np.array([polar_to_x(measure), polar_to_y(measure)]) for measure in turn]


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
    :return: array
    """
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width, height = get_width_height(cartesian_points)
    diag_len = int(round(math.sqrt(width * width + height * height)))
    print("diag_len", diag_len)
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)
    accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)

    for i in range(len(cartesian_points)):
        x, y = cartesian_points[i]
        for t_idx in range(num_thetas):
            rho = diag_len+int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            if rho < 0:
                print("rho négatif", rho)
            accumulator[rho, t_idx] += 20
    return accumulator, thetas, rhos


def hough_transform_to_dict(cartesian_points, angle_step=0.3):
    """

    :param cartesian_points:
    :param angle_step:
    :return: dict
    """
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width, height = get_width_height(cartesian_points)
    diag_len = int(round(math.sqrt(width * width + height * height)))
    print("diag_len", diag_len)
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)
    accumulator = defaultdict(int)

    for i in range(len(cartesian_points)):
        x, y = cartesian_points[i]
        for t_idx in range(num_thetas):
            rho = diag_len+int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            # rho = int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            accumulator[rho, t_idx] += 1
            if rho < 0:
                print("rho négatif", rho)
    return accumulator, thetas, rhos


def take_brightest_points(accumulator, thetas, rhos):
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

    return [max_value], [thetas[theta_max]], rhos[[rho_max]], extrema


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
