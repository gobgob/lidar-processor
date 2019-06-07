#!/home/pi/lidar-processor/lidar_env/bin/python


"""
Hough transform is used to find lines in images;
"""

import math
import numpy as np
from skimage import io as skio
import matplotlib.pylab as pl

from main.constants import *

import main.output_rendering as outr
import main.data_cleansing as dacl
import retrieve_realistic_measures as retrm

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


# def make_bigger_points(points, image):
#     for x, y in points:
#         print(x, y)
#         # rr, cc = skdr.circle(int(x), int(y), 10)
#         # image[rr, cc] = 255
#     return image


def reconstruct_image_with_lines_polar(polar_points, angles, dists):
    # print(angles)
    # print(dists)
    # fig = pl.figure()
    # ax = fig.add_subplot(111)
    # ax.clear()
    # # ax.set_xlim(0, distance_max_x_cartesien)
    # ax.set_xlim(-int(distance_max_x_cartesien/2), int(distance_max_x_cartesien/2))
    # # ax.set_ylim(0, distance_max_y_cartesien)
    # ax.set_ylim(-int(distance_max_y_cartesien/2), int(distance_max_y_cartesien/2))
    # ax.axhline(0, 0)
    # ax.axvline(0, 0)
    # # pl.grid()
    #
    xx = []
    yy = []
    # for x, y in points:
    #     xx.append(x)
    #     yy.append(y)
    # pl.plot(xx, yy, 'r.')
    cartesian_good_data = outr.one_turn_to_cartesian_points(polar_points)
    width, height = outr.get_width_height(cartesian_good_data)
    diag_len = int(round(math.sqrt(width * width + height * height)))
    # cartesian_good_data, translation = outr.change_basis(cartesian_good_data)

    for theta, rho in polar_points:
        pl.polar(math.radians(theta), rho, 'r,')
    # pl.show()

    # fig.canvas.draw()
    print("fini ?")
    for theta, rho in zip(angles, dists):
        # print("oui ?")
        xxx, yyy = [], []
        # print(-int(distance_max_x_cartesien / 2), int(distance_max_x_cartesien / 2))
        # cost = math.cos(theta)
        # sint = math.sin(theta)
        # x0 = rho*cost
        # y0 = rho*sint
        # x1 = x0 - 10000*sint
        # y1 = y0 + 10000*cost
        # x2 = x0 + 10000*sint
        # y2 = y0 - 10000*cost
        # pl.plot(x1, y1, 'b-')
        # pl.plot(x2, y2, 'b-')
        # for x in range(0, distance_max_x_cartesien):
        for x in range(-int(distance_max_x_cartesien/2), int(distance_max_x_cartesien/2)):
            # print(x)
            y = rho / math.sin(theta) - (math.cos(theta)/math.sin(theta)) * x - diag_len
            a, d = outr.cartesian_to_polar([x, y])

            # print("y", y)
            # xxx.append(x)
            # yyy.append(y)
            xxx.append(a)
            yyy.append(d)
            # print("cartesian", [x+translation[0], -y-translation[1]])
            # a, d = outr.cartesian_to_polar([x-translation[0], (y-translation[1])])

            # print("polar", a, d)
            # pl.polar(a, d, "b-")
        pl.polar(xxx, yyy, 'b-')
        # pl.plot(xxx, yyy, 'b-')
        # fig.canvas.draw()
    pl.show()
    # fig.canvas.draw()

    # skio.imsave("line_a" + '.jpg', image)


def reconstruct_image_with_lines_cartesian(cartesian_data, angles, dists):
    # print(angles)
    # print(dists)
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.clear()
    # ax.set_xlim(0, distance_max_x_cartesien)
    ax.set_xlim(-int(distance_max_x_cartesien), int(distance_max_x_cartesien))
    # ax.set_ylim(0, distance_max_y_cartesien)
    ax.set_ylim(-int(distance_max_y_cartesien), int(distance_max_y_cartesien))
    ax.axhline(0, 0)
    ax.axvline(0, 0)
    # pl.grid()

    xx = []
    yy = []
    for x, y in cartesian_data:
        xx.append(x)
        yy.append(y)
    pl.plot(xx, yy, 'r,')

    # for x, y in cartesian_data:
    #     pl.plot(x, y, 'r,')

    # pl.show()
    # fig.canvas.draw()
    # for theta, rho in zip(angles, dists):
    #     cost = math.cos(theta)
    #     sint = math.sin(theta)
    #     x0 = rho*cost
    #     y0 = rho*sint
    #     x1 = x0 - 10000*sint
    #     y1 = y0 + 10000*cost
    #     x2 = x0 + 10000*sint
    #     y2 = y0 - 10000*cost
    #     pl.plot(x1, y1, 'b-')
    #     pl.plot(x2, y2, 'b-')
    width, height = outr.get_width_height(cartesian_data)
    diag_len = int(round(math.sqrt(width * width + height * height)))

    for theta, rho in zip(angles, dists):
        xxx, yyy = [], []

        # for x in range(0, distance_max_x_cartesien):
        for x in range(-int(distance_max_x_cartesien), int(distance_max_x_cartesien)):
            # print(x)
            y = (rho / math.sin(theta) - (math.cos(theta)/math.sin(theta)) * x) - diag_len

            xxx.append(x)
            yyy.append(y)
        pl.plot(xxx, yyy)
    fig.canvas.draw()
    pl.show()
    # fig.canvas.draw()

    # skio.imsave("line_a" + '.jpg', image)


def measures_to_images(data):
    for i, measure in enumerate(data):
        good_data = dacl.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        cartesian_good_data, translation = outr.change_basis(cartesian_good_data)

        width, height = outr.get_width_height(cartesian_good_data)
        image = np.zeros((int(width), int(height)), dtype=np.uint8)

        display_measures(cartesian_good_data)
        # skio.imsave(str(i)+'.jpg', image)
        print(i)


def measures_to_accumulators_array(data):
    """
    Use cartesian representation
    :param data:
    :return:
    """
    print("-----------measures_to_accumulators_array-----------")
    for i, measure in enumerate(data):
        good_data = dacl.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        # cartesian_good_data, translation = outr.change_basis(cartesian_good_data)

        # width, height = outr.get_width_height(cartesian_good_data)
        # width, height = int(width), int(height)
        # print(width, height)
        # image = np.zeros((int(width), int(height)), dtype=np.uint8)

        print("i", i)
        accumulator, thetas, rhos = outr.hough_transform(cartesian_good_data)
        skio.imsave("accumulator_"+str(i) + '.jpg', accumulator)

        ids, theta, rho = outr.peak_votes(accumulator, thetas, rhos)
        # accum, angles, dists = sktr.hough_line_peaks(accumulator, thetas, rhos, 10, 12, num_peaks=3)
        print(ids, theta, rho)

        reconstruct_image_with_lines_cartesian(cartesian_good_data, [theta], [rho])


def measures_to_accumulators_dict(data):
    """
    Use polar representation

    :param data:
    :return:
    """
    print("-----------measures_to_accumulators_dict-----------")
    for i, measure in enumerate(data):
        good_data = dacl.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        # cartesian_good_data, translation = outr.change_basis(cartesian_good_data)

        # width, height = outr.get_width_height(cartesian_good_data)
        # width, height = int(width), int(height)
        # print(width, height)
        # image = np.zeros((int(width), int(height)), dtype=np.uint8)

        print(i)
        accumulator, thetas, rhos = outr.hough_transform_to_dict(cartesian_good_data)
        # skio.imsave("accumulator_"+str(i) + '.jpg', accumulator)

        accum, angles, dists, extrema = outr.take_brightest_points(accumulator, thetas, rhos)

        # print(extrema)

        # accum, angles, dists = sktr.hough_line_peaks(accumulator, thetas, rhos, 10, 12, num_peaks=3)
        print(accum, angles, dists)
        # idx, theta, rho = outr.peak_votes(accumulator, thetas, rhos)
        reconstruct_image_with_lines_polar(good_data, angles, dists)


if __name__ == "__main__":
    # measures = retm.get_data()
    measures = retrm.get_realistic_data()
    # measures_to_images([measures[1]])

    # display measures through an array
    measures_to_accumulators_array([measures[3]])

    # good_data = outr.keep_good_measures(measures[3], 30)
    # cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)
    # display_measures(cartesian_good_data)

    # display measures analysed through a dictionary
    measures_to_accumulators_dict([measures[3]])

    # display raw measures
    print("-----------Measures display-----------")
    filtered_data = dacl.keep_good_measures(measures[3], 30)
    display_polar_measures(filtered_data)
    display_measures(filtered_data)
