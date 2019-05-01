#! /usr/bin/python3

"""

"""

import numpy as np
import matplotlib.pyplot as pl

from main.constants import *
import main.main_script as mm
import main.clustering as clus
import main.output_rendering as outr
from retrieve_realistic_measures import get_realistic_data

__author__ = "Clément Besnier"


def main_clustering():
    one_turn_measure = get_realistic_data()[0]
    one_turn_measure = outr.keep_good_measures(one_turn_measure, 30)
    one_turn_measure = mm.remove_too_far_or_too_close(one_turn_measure)
    cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
    cartesian_one_turn_measure = [np.array(measure) for measure in cartesian_one_turn_measure]
    clusters, means = clus.clusterize(cartesian_one_turn_measure)
    return clusters, means


def plot_clustering(clusters):

    # display measures through an array
    # display raw measures
    print("-----------Measures display-----------")
    # display_polar_measures(one_turn_measure)
    # display_measures(one_turn_measure)

    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.clear()
    ax.set_xlim(-distance_max_x_cartesien, distance_max_x_cartesien)
    ax.set_ylim(-distance_max_y_cartesien, distance_max_y_cartesien)
    ax.axhline(0, 0)
    ax.axvline(0, 0)
    # pl.grid()

    # xx = []
    # yy = []
    # for x, y in cartesian_one_turn_measure:
    #     xx.append(x)
    #     yy.append(y)
    # pl.plot(xx, yy, 'r:')

    # fig.canvas.draw()
    # pl.show()

    # print(clusters)

    # xx = []
    # yy = []
    # for i in means:
    #     print(i)
    #     x = i[0]
    #     y = i[1]
    #     xx.append(x)
    #     yy.append(y)
    # pl.plot(xx, yy, "y+")

    for cluster_center in clusters:
        xx = []
        yy = []
        print(len(cluster_center))
        for i in cluster_center:
            x = i[0]
            y = i[1]
            xx.append(x)
            yy.append(y)
            # pl.Circle((x, y), 30, color='b', fill=False)
        pl.plot(xx, yy, '+')
    pl.show()


if __name__ == "__main__":
    # main_clustering()
    clusters, means = main_clustering()
    plot_clustering(clusters)
