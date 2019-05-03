#!/usr/bin/python3

"""
Log configuration
Inspired by.
"""

import os
import sys
import enum

__author__ = "Clément Besnier"

PROJECT_NAME = "lidar-processor"
# Useful in case we don't run the code in the right directory.
own_path = os.path.join(os.getenv("HOME"), PROJECT_NAME)
sys.path.append(own_path)
# region LiDAR settings
angle_resolution = 0.3
# endregion

tolerance_predicted_fixe_r = 2
tolerance_predicted_fixe_theta = 2
tolerance_predicted_fixe = [tolerance_predicted_fixe_r, tolerance_predicted_fixe_theta]
# [distance in mm, angle in radian]
tolerance_kalman_r = 100
tolerance_kalman_theta = 100
tolerance_kalman = [tolerance_kalman_r, tolerance_kalman_theta]
# [distance en mm, angle en radian]
seuil_association = 150

sigma_q = 15
sigma_angle = 35
sigma_distance = 35
facteur_temps = 8

distance_max_x_cartesien = 4000
distance_max_y_cartesien = 4000
distance_max = 6000
afficher_en_polaire = False
affichage = True

minimum_distance = 80  # in mm
maximum_distance = 3500  # in mm
minimum_distance_between_clusters = 80
tmaxsel = 500
tminsel = 500
minimum_points_in_cluster = 5
maximum_points_in_cluster = 50

FIX_BEACON_RADIUS = 100
ADVERSE_ROBOT_BEACON_RADIUS = 80


class TeamColor(enum.Enum):
    purple = enum.auto()
    yellow = enum.auto()
