"""

"""

from main.table import *

__author__ = "Clément Besnier"


# region ++ mains
def main():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    measure = geom.Point(-1000, 1100)

    vectors, robot_vector = table.simulate_measure(measure, 0.5, 200)

    table.init_plot()
    table.plot_edges()
    table.plot_obstacles()
    table.plot_measures(measure, vectors, robot_vector)
    table.plot()


def main_2():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    translation_vector = geom.Vector()
    translation_vector.set_coordinates(+1000, -1100)
    table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    rotation_angle = 0.5
    table.rotate(rotation_angle)

    measure = geom.Point(-1000, 1100)
    measure = translation_vector.apply_to_point(measure)
    measure.rotate(rotation_angle)
    vectors, robot_vector = table.simulate_measure(measure, 0, 200)

    table.init_plot()
    table.plot_edges()
    table.plot_obstacles()
    table.plot_measures(measure, vectors, robot_vector)
    table.plot()


def main_3():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    # translation_vector = geom.Vector()
    # translation_vector.set_coordinates(+1000, -1100)
    # table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    # rotation_angle = 0.5
    # table.rotate(rotation_angle)

    measure = geom.Point(-300, 1400)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)
    # vectors, robot_vector = table.simulate_measure(measure, 0, 200)

    table.init_plot()
    table.plot_edges()
    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.generate_measures(measure)
    table.plot()


def main_4():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    # translation_vector = geom.Vector()
    # translation_vector.set_coordinates(+1000, -1100)
    # table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    # rotation_angle = 0.5
    # table.rotate(rotation_angle)

    measure = geom.Point(-300, 1400)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)

    clusters = main_clustering()
    # print("clusters", clusters)

    table.init_plot()
    table.plot_edges()
    table.plot_clusters(clusters)
    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.generate_measures(measure)
    table.plot()


def main_5():
    table = Table()

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    samples = ["0_-1820_pi_over_2", "1210_1400_pi"]
    measures = get_table_measures(samples[0])
    for i in range(len(measures)):
        one_turn_measure = dacl.keep_good_measures(measures[i], 100)
        # one_turn_measure = dacl.keep_not_too_far_or_not_too_close(one_turn_measure)

    translation_vector = geom.Vector()
    translation_vector.set_coordinates(+1000, -1100)
    table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    rotation_angle = 0.5
    table.rotate(rotation_angle)

    # measure = geom.Point(0, 1800)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)

    table.init_plot()
    table.plot_edges()
    # table.plot_measures()

    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.plot()
# endregion


def display_table():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    table.init_plot()
    table.plot_edges()
    table.plot_obstacles()
    table.plot()


if __name__ == "__main__":
    # main()
    # main_2()
    # main_3()
    # main_4()
    display_table()
