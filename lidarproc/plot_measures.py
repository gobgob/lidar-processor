#!/home/pi/lidar-processor/lidar_env/bin/python


"""
Display measures
"""

import math
import numpy as np
import matplotlib.pylab as pl

from lidarproc import retrieve_measures
from lidarproc.main.constants import *

import lidarproc.main.output_rendering as outr

__author__ = ["Clément Besnier", ]


def display_measures(polar_points):
    # pl.ion()
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.clear()
    ax.set_xlim(-distance_max_x_cartesien, distance_max_x_cartesien)
    ax.set_ylim(-distance_max_y_cartesien, distance_max_y_cartesien)
    ax.axhline(0, 0)
    ax.axvline(0, 0)
    # pl.grid()

    polar_points = [[90 - theta, rho] for theta, rho in polar_points]
    points = outr.one_turn_to_cartesian_points(polar_points)

    xx = []
    yy = []
    for x, y in points:
        xx.append(x)
        yy.append(y)

    pl.plot(xx, yy, 'r,')
    fig.canvas.draw()
    pl.show()


def display_polar_measures(polar_points):
    for theta, rho in polar_points:
        pl.polar(math.radians(theta), rho, 'r,')
    pl.show()


if __name__ == "__main__":
    measures = retrieve_measures.get_27052019_measures()
    # print(measures[0])
    display_measures(measures[0])
