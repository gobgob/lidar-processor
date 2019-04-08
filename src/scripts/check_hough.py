#!/usr/bin/python3


"""
Hough transform is used to find lines in images;
"""

import math
import numpy as np
from skimage import io as skio
from skimage import draw as skdr
from skimage import transform as sktr

import src.main.output_rendering as outr
import src.scripts.retrieve_measures as retm

__author__ = ["Clément Besnier", ]


def make_bigger_points(points, image):
    for x, y in points:
        # print(x, y)
        rr, cc = skdr.circle(int(x), int(y), 10)
        image[rr, cc] = 255
    return image


def reconstruct_image_with_lines(image, angles, dists):
    for theta, rho in zip(angles, dists):
        for x in range(int(image.shape[0])):
            y = rho/math.sin(theta) - math.tan(theta)*x
            print(y % image.shape[1], x)
            image[x, int(y) % image.shape[1]] = 255
    skio.imsave("line_a" + '.jpg', image)


def measures_to_images(data):
    for i, measure in enumerate(data):
        good_data = outr.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        width, height = outr.get_width_height(cartesian_good_data)
        image = np.zeros((int(width), int(height)), dtype=np.uint8)

        image = make_bigger_points(cartesian_good_data, image)
        skio.imsave(str(i)+'.jpg', image)
        print(i)


def measures_to_accumulators(data):
    for i, measure in enumerate(data):
        good_data = outr.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        width, height = outr.get_width_height(cartesian_good_data)
        width, height = int(width), int(height)
        print(width, height)
        image = np.zeros((int(width), int(height)), dtype=np.uint8)

        print(i)
        accumulator, thetas, rhos = outr.hough_transform(cartesian_good_data)
        skio.imsave("accumulator_"+str(i) + '.jpg', accumulator)

        accum, angles, dists = sktr.hough_line_peaks(accumulator, thetas, rhos, 10, 12, num_peaks=30)
        print(accum, angles, dists)
        # idx, theta, rho = outr.peak_votes(accumulator, thetas, rhos)
        reconstruct_image_with_lines(image, angles, dists)


if __name__ == "__main__":
    measures = retm.get_data()
    # measures_to_images([measures[1]])
    measures_to_accumulators([measures[1]])
