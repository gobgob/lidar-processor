#!/home/pi/lidar-processor/lidar_env/bin/python

"""
To change basis: robot's view <=> table's view

Useless
"""
import numpy as np
from numpy import mod, pi

__author__ = "Clément Besnier"


def convert_angle(angle, is_rad=False, convert_to_rad=True, supplementary_angle=0):
    """

    :param angle:
    :param is_rad:
    :param convert_to_rad:
    :param supplementary_angle:
    :return:
    """
    if is_rad:
        return mod(supplementary_angle - angle, 2*pi)
    else:
        if convert_to_rad:
            return mod(supplementary_angle - np.deg2rad(angle), 2*pi)
        else:
            return mod(supplementary_angle - angle, 360)


def change_angle_referentiel(measures, is_rad=False, convert_to_rad=False, supplementary_angle=0):
    """

    :param measures:
    :param is_rad:
    :param convert_to_rad:
    :param supplementary_angle:
    :return:
    """
    new_measures = []
    for i in measures:
        # angle = mod(pi/2 - f(i[0]), 2*pi)
        angle = convert_angle(i[0], is_rad, convert_to_rad, supplementary_angle)
        new_measures.append((angle, i[1]))
    return new_measures
