#!/usr/bin/python3

"""
Log configuration
Inspired by.
"""


tolerance_predicted_fixe_r = 2
tolerance_predicted_fixe_theta = 2
tolerance_predicted_fixe = [tolerance_predicted_fixe_r, tolerance_predicted_fixe_theta]
# [distance en mm, angle en radian]
tolerance_kalman_r = 100
tolerance_kalman_theta = 100
tolerance_kalman = [tolerance_kalman_r, tolerance_kalman_theta]
# [distance en mm, angle en radian]
seuil_association = 150

sigma_q = 15
sigma_angle = 35
sigma_distance = 35
facteur_temps = 8

distance_max_x_cartesien = 7000
distance_max_y_cartesien = 7000
distance_max = 6000
afficher_en_polaire = False
affichage = True

