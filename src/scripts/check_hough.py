#!/usr/bin/python3

import math
import numpy as np
from skimage import io as skio
from skimage import draw as skdr

import src.main.output_rendering as outr
import src.scripts.retrieve_measures as retm


def measures_to_images(data):
    for i, measure in enumerate(data):
        good_data = outr.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        width, height = outr.get_width_height(cartesian_good_data)
        image = np.zeros((int(width), int(height)), dtype=np.uint8)

        for x, y in cartesian_good_data:
            # print(x, y)

            rr, cc = skdr.circle(int(y), int(x), 15)
            image[rr, cc] = 255
        skio.imsave(str(i)+'.jpg', image)
        print(i)


def measures_to_accumulators(data):
    for i, measure in enumerate(data):
        good_data = outr.keep_good_measures(measure, 30)

        cartesian_good_data = outr.one_turn_to_cartesian_points(good_data)

        width, height = outr.get_width_height(cartesian_good_data)
        image = np.zeros((int(width), int(height)), dtype=np.uint8)

        for x, y in cartesian_good_data:
            # print(x, y)

            rr, cc = skdr.circle(int(x), int(y), 15)
            image[rr, cc] = 255
        print(i)
        accumulator, thetas, rhos = outr.hough_transform(cartesian_good_data)
        skio.imsave("accumulator_"+str(i) + '.jpg', accumulator)

        idx, theta, rho = outr.peak_votes(accumulator, thetas, rhos)
        for x in range(int(width)):
            y = rho/math.sin(theta) - math.tan(theta)*x
            image[x, int(y)] = 255
        skio.imsave("line_"+str(i) + '.jpg', image)


if __name__ == "__main__":
    measures = retm.get_data()
    measures_to_images(measures)
    measures_to_accumulators([measures[1]])
