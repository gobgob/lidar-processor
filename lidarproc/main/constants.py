#!/home/pi/lidar-processor/lidar_env/bin/python

"""
Log configuration
Inspired by.
"""

import os
import sys
import enum
import logging

__author__ = "Clément Besnier"

PROJECT_NAME = "lidar-processor"
# Useful in case we don't run the code in the right directory.
home_path = os.getenv("HOME") if os.getenv("HOME") is not None else "C:/Users/Clément/PycharmProjects/"
own_path = os.path.join(home_path, PROJECT_NAME)
sys.path.append(own_path)
# region LiDAR settings
angle_resolution = 0.3
# endregion

TIME_RESOLUTION_ENCODER = 0.02

THRESHOLD_QUALITY = 30

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
minimum_points_in_cluster = 3
maximum_points_in_cluster = 50

TOLERANCE_FOR_CIRCLE_COHERENCE = 100

FIX_BEACON_RADIUS = 50  # in mm
OPPONENT_ROBOT_BEACON_RADIUS = 80

too_much_angle_shift = 2  # in degree


class TeamColor(enum.Enum):
    purple = "purple"
    orange = "orange"
    # purple = enum.auto()
    # orange = enum.auto()


# region start position
PURPLE_SELF_X = 1210
PURPLE_SELF_Y = 1400
PURPLE_SELF_THETA = 3.14

ORANGE_SELF_X = -1200
ORANGE_SELF_Y = 1400
ORANGE_SELF_THETA = 0
# endregion

# region opponent robot
ORANGE_START_ZONE = [[-1500, 1700],  # upper left
                     # [-1500, 1100],
                     [-1050, 1100],  # lower right
                     # [-1050, 1700],
                     ]

PURPLE_START_ZONE = [[1050, 1700],  # upper left
                     # [1050, 1100],
                     # [1500, 1100],
                     [1500, 1700]  # lower right
                     ]
# endregion

# region beacons
beacon_1_orange = [[-1500 - 100 - 44, 2000],  # upper left
                   [-1500 - 44, 2000 - 100]  # lower right
                   ]

beacon_2_orange = [[1500 + 44, 1000 + 50],  # upper left
                   [1500 + 100 + 44, 1000 - 50]  # lower right
                   ]

beacon_3_orange = [[-1500 - 100 - 44, 0 + 100],  # upper left
                   [-1500 - 44, 0]  # lower right
                   ]

beacons_orange = [beacon_1_orange, beacon_2_orange, beacon_3_orange]

beacon_1_purple = [[1500 + 100 + 44, 2000],  # upper left
                   [1500 + 44, 2000 - 100]  # lower right
                   ]

beacon_2_purple = [[-1500 - 100 - 44, 1000 + 50],  # upper left
                   [-1500 - 44, 1000 - 50]  # lower right
                   ]

beacon_3_purple = [[1500 + 44, 100],  # upper left
                   [1500 + 100 + 44, 0]  # lower right
                   ]

beacons_purple = [beacon_1_purple, beacon_2_purple, beacon_3_purple]

SOFT_THRESHOLD_RECTANGLE = 50
QUALITY_THRESHOLD = 150

n_measures_for_median = 3
