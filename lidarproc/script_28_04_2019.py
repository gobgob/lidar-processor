#!/home/pi/lidar-processor/lidar_env/bin/python

"""
Display measures
"""

import numpy as np

import lidarproc.main.data_cleansing as dacl
from lidarproc.main.geometry import Point, Vector
from lidarproc.main.table import Table, Square
from lidarproc.plot_measures import display_deg2rad_polar_measures
from lidarproc.retrieve_realistic_measures import get_table_measures

import lidarproc.main.output_rendering as outr

__author__ = "Clément Besnier"


def display_just_measures():
    samples = ["0_-1820_pi_over_2", "1210_1400_pi", "-1210_1400_0"]
    measures = get_table_measures(samples[1])
    for i in range(len(measures)):
        one_turn_measure = dacl.keep_good_measures(measures[i], 100)
        one_turn_measure = dacl.keep_not_too_far_or_not_too_close(one_turn_measure)
        display_deg2rad_polar_measures(one_turn_measure)


def display_measures_and_table():
    identifier = 1
    p1 = Point(0, -1820)  # *-1
    # p2 = Point(-1210, -1400)  # *-1
    p2 = Point(-1300, -1400)  # *-1
    p3 = Point(1210, -1400)  # *-1

    v1, v2, v3 = Vector(), Vector(), Vector()
    v1.set_coordinates(p1.x, p1.y)
    v2.set_coordinates(p2.x, p2.y)
    v3.set_coordinates(p3.x, p3.y)
    translation_vectors = [v1, v2, v3]

    # measures retrieval
    samples = ["0_-1820_pi_over_2", "1210_1400_pi", "-1210_1400_0"]

    measures = get_table_measures(samples[identifier])
    one_turn_measures = []
    for i in range(len(measures)):
        one_turn_measure = dacl.keep_good_measures(measures[i], 100)
        one_turn_measure = dacl.keep_not_too_far_or_not_too_close(one_turn_measure)
        one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
        one_turn_measures.append(one_turn_measure)

    # table instantiation
    table = Table()

    beacon_1 = Square([Point(-1500 - 100, 2000), Point(-1500, 2000), Point(-1500, 2000 - 100),
                       Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([Point(1500, 1000 + 50), Point(1500 + 100, 1000 + 50), Point(1500 + 100, 1000 - 50),
                       Point(1500, 1000 - 50)])
    beacon_3 = Square([Point(-1500 - 100, 0 + 100), Point(-1500, 0 + 100), Point(-1500, 0), Point(-1500 - 100, 0)])

    # beacon_1.take_symmetric()
    # beacon_2.take_symmetric()
    # beacon_3.take_symmetric()

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(Point(-1500, 0))
    table.add_edge_point(Point(1500, 0))
    table.add_edge_point(Point(1500, 2000))
    table.add_edge_point(Point(-1500, 2000))

    # table.translate(translation_vectors[identifier])

    # rotation_angle = 0.5
    # rotation_angle = np.pi/2
    # table.rotate(rotation_angle)

    # measure = Point(0, 1800)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)

    table.init_plot()
    table.plot_edges()
    table.plot_lidar_measures(one_turn_measures[1])

    table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.plot()


if __name__ == "__main__":
    # display_measures_and_table()
    display_just_measures()
