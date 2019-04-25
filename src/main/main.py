"""


"""
import time
from typing import List

import numpy as np

from constants import *
import src.main.output_rendering as outr
from src.main.data_retrieval import LidarThread
from src.main.clustering import clusterize

__author__ = "Clément Besnier"


def remove_too_far_or_too_close(one_turn: List) -> List:
    """

    :param one_turn: list of [<angle>, <distance>, <quality>]
    :return: list of [<angle>, <distance>]
    """
    return [measure for measure in one_turn if minimum_distance < measure[1] < maximum_distance]


def main():
    measuring = True
    t = LidarThread()
    t.start()
    while measuring:
        one_turn_measure = t.get_measures()
        one_turn_measure = outr.keep_good_measures(one_turn_measure, 30)
        one_turn_measure = remove_too_far_or_too_close(one_turn_measure)
        cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
        clusters = clusterize(cartesian_one_turn_measure)
        print(clusters)

        time.sleep(3)
    t.close_connection()
    time.sleep(3)
    # sys.exit(0)


if __name__ == "__main__":
    main()
