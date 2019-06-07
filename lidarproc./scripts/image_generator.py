#
import numpy as np
import matplotlib.pyplot as pl

import main.geometry as geom

import main.table as ta

__author__ = "Clément Besnier"

table = ta.Table()
# for orange
beacon_1 = ta.Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                   geom.Point(-1500 - 100, 2000 - 100)])
beacon_2 = ta.Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                   geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
beacon_3 = ta.Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                   geom.Point(-1500 - 100, 0)])

beacon_1.take_symmetric()
beacon_2.take_symmetric()
beacon_3.take_symmetric()

table.add_square_obstacle(beacon_1)
table.add_square_obstacle(beacon_2)
table.add_square_obstacle(beacon_3)

table.add_edge_point(geom.Point(-1500, 0))
table.add_edge_point(geom.Point(1500, 0))
table.add_edge_point(geom.Point(1500, 2000))
table.add_edge_point(geom.Point(-1500, 2000))

measure = geom.Point(1000, 1300)

vectors, robot_vector = table.simulate_measure(measure, np.pi/3, 200)

table.init_plot()
table.plot_edges()
table.plot_obstacles()
table.plot_measures(measure, vectors, robot_vector)
table.plot()
pl.show()
