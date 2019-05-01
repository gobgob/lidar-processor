#! /usr/bin/python3

"""


"""
import time
from typing import List

from main.constants import *
import main.output_rendering as outr
from main.data_retrieval import LidarThread, EncoderThread
from main.communication import HLThread
from main.clustering import clusterize
from main.tracking import track_clusters
from main.self_locator import find_beacons
from main.enemy_locator import find_robots

__author__ = "Clément Besnier"


def remove_too_far_or_too_close(one_turn: List) -> List:
    """

    :param one_turn: list of [<angle>, <distance>, <quality>]
    :return: list of [<angle>, <distance>]
    """
    return [measure for measure in one_turn if minimum_distance < measure[1] < maximum_distance]


def match_has_begun():
    return True


def main():
    measuring = True

    t_lidar = LidarThread()
    t_lidar.start()

    t_ll = EncoderThread()
    t_ll.start()

    t_hl = HLThread()
    t_hl.start()

    # TODO preparation before the match

    previous_clusters = []
    first = True

    # TODO the match has just begun
    while measuring:
        one_turn_measure = t_lidar.get_measures()
        one_turn_measure = outr.keep_good_measures(one_turn_measure, 30)
        one_turn_measure = remove_too_far_or_too_close(one_turn_measure)
        cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
        clusters = clusterize(cartesian_one_turn_measure)
        print(clusters)
        if match_has_begun():
            if first:
                pass

            beacons, robots = track_clusters(previous_clusters, clusters)
        else:
            # TODO determine the position of beacons and adverse robot just with the last measure
            beacons = find_beacons(clusters)
            robots = find_robots(clusters)
        previous_clusters = clusters.copy()
        time.sleep(1)
    t_lidar.close_connection()
    time.sleep(3)
    # sys.exit(0)


if __name__ == "__main__":
    main()
