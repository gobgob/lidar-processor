

"""


"""
import numpy as np
from numpy import mod, pi

__author__ = "Clément Besnier"


def convert_angle(angle, is_rad=False, convert_to_rad=True, supplementary_angle=0):
    if is_rad:
        return mod(supplementary_angle - angle, 2*pi)
    else:
        if convert_to_rad:
            return mod(supplementary_angle - np.deg2rad(angle), 2*pi)
        else:
            return mod(supplementary_angle - angle, 360)


def change_angle_referentiel(measures, is_rad=False, convert_to_rad=False, supplementary_angle=0):
    new_measures = []
    for i in measures:
        # angle = mod(pi/2 - f(i[0]), 2*pi)
        angle = convert_angle(i[0], is_rad, convert_to_rad, supplementary_angle)
        new_measures.append((angle, i[1]))
    return new_measures
