#!/usr/bin/python3


"""
Hough transform is used to find lines in images;
"""

import math
import numpy as np
from skimage import io as skio
from skimage import draw as skdr
from skimage import transform as sktr
import matplotlib.pylab as pl

from src.constants import *

import src.main.output_rendering as outr
import src.scripts.retrieve_measures as retm

__author__ = ["Clément Besnier", ]


def display_measures(points):
    # pl.ion()
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.clear()
    ax.set_xlim(-distance_max_x_cartesien / 2, distance_max_x_cartesien / 2)
    ax.set_ylim(-distance_max_y_cartesien / 2, distance_max_y_cartesien / 2)
    ax.axhline(0, 0)
    ax.axvline(0, 0)
    # pl.grid()

    xx = []
    yy = []
    for x, y in points:
        xx.append(x)
        yy.append(-y)

    pl.plot(xx, yy, 'r,')
    fig.canvas.draw()
    pl.show()


# def make_bigger_points(points, image):
#     for x, y in points:
#         print(x, y)
#         # rr, cc = skdr.circle(int(x), int(y), 10)
#         # image[rr, cc] = 255
#     return image


def reconstruct_image_with_lines(points, angles, dists):
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.clear()
    ax.set_xlim(-distance_max_x_cartesien / 2, distance_max_x_cartesien / 2)
    ax.set_ylim(-distance_max_y_cartesien / 2, distance_max_y_cartesien / 2)
    ax.axhline(0, 0)
    ax.axvline(0, 0)
    # pl.grid()

    xx = []
    yy = []
    for x, y in points:
        xx.append(x)
        yy.append(-y)
    pl.plot(xx, yy, 'r,')
    # fig.canvas.draw()
    print("fini ?")
    for theta, rho in zip(angles, dists):
        # print("oui ?")
        xxx, yyy = [], []
        print(-int(distance_max_x_cartesien / 2), int(distance_max_x_cartesien / 2))
        cost = math.cos(theta)
        sint = math.sin(theta)
        x0 = rho*cost
        y0 = rho*sint
        x1 = x0 - 1000*sint
        y1 = y0 + 1000*cost
        x2 = x0 + 1000*sint
        y2 = y0 - 1000*cost
        pl.plot([x1, y1], [x2, y2], 'b-')
        # for x in range(-int(distance_max_x_cartesien / 2), int(distance_max_x_cartesien / 2)):
        #     # print(x)
        #     xxx.append(x)
        #     y = rho / math.sin(theta) - math.tan(theta) * x
        #     # print("y", y)
        #     yyy.append(y)
        # pl.plot(xxx, yyy, 'b-')
        fig.canvas.draw()
    pl.show()
    fig.canvas.draw()

    # skio.imsave("line_a" + '.jpg', image)


def measures_to_images(data):
    for i, measure in enumerate(data):
        good_data = outr.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        width, height = outr.get_width_height(cartesian_good_data)
        image = np.zeros((int(width), int(height)), dtype=np.uint8)

        display_measures(cartesian_good_data)
        # skio.imsave(str(i)+'.jpg', image)
        print(i)


def measures_to_accumulators(data):
    for i, measure in enumerate(data):
        good_data = outr.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        width, height = outr.get_width_height(cartesian_good_data)
        width, height = int(width), int(height)
        print(width, height)
        # image = np.zeros((int(width), int(height)), dtype=np.uint8)

        print(i)
        accumulator, thetas, rhos = outr.hough_transform(cartesian_good_data)
        skio.imsave("accumulator_"+str(i) + '.jpg', accumulator)

        accum, angles, dists = sktr.hough_line_peaks(accumulator, thetas, rhos, 10, 12, num_peaks=5)
        print(accum, angles, dists)
        # idx, theta, rho = outr.peak_votes(accumulator, thetas, rhos)
        reconstruct_image_with_lines(cartesian_good_data, angles, dists)


if __name__ == "__main__":
    measures = retm.get_data()
    # measures_to_images([measures[1]])
    measures_to_accumulators([measures[1]])

    # good_data = outr.keep_good_measures(measures[1], 30)
    # cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)
    # display_measures(cartesian_good_data)
