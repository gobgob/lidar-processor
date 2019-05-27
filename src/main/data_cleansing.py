#!/usr/bin/python3

"""
Point
- Keeps good measure
- Keeps not too far and not too close measures

Clusters
- Keeps not too spread
- Keeps not too few or not too much points

2
"""
from typing import List, Union

import numpy as np

from main.constants import *
from main.clustering import Cluster

__author__ = "Clément Besnier"


def filter_keep_good_measure(measure: List[Union[float, int]], threshold):
    return measure[2] > threshold


def keep_good_measures(turn: List, threshold: int):
    """

    :param turn: list of measures ; one measure is [angle (in rad), distance (in m), quality (from 0 to 47)]
    :param threshold:
    :return:
    """
    return [measure[:2] for measure in turn if filter_keep_good_measure(measure, threshold)]


def filter_keep_not_too_far_or_not_too_close(measure: List[float]):
    return minimum_distance < measure[1] < maximum_distance


def keep_not_too_far_or_not_too_close(one_turn: List) -> List:
    """

    :param one_turn: list of [<angle>, <distance>, <quality>]
    :return: list of [<angle>, <distance>]
    """
    return [measure for measure in one_turn if filter_keep_not_too_far_or_not_too_close(measure)]


def filter_points(one_turn: List, threshold: Union[int, float]) -> List[np.ndarray]:
    """

    :param one_turn: measures in cartesian coordinates and rotates so that angle measures are normalized
    :param threshold:
    :return:
    """
    return [np.array([np.pi/2 - np.deg2rad(measure[0]), measure[1]]) for measure in one_turn
            if filter_keep_not_too_far_or_not_too_close(measure) and
            filter_keep_good_measure(measure, threshold)]


def are_not_too_few_or_not_too_much(cluster: Cluster):
    return minimum_points_in_cluster <= len(cluster) <= maximum_points_in_cluster


def keep_not_too_few_or_not_too_much(clusters: List[Cluster]):
    """

    :param clusters:
    :return:
    """
    return [cluster for cluster in clusters if are_not_too_few_or_not_too_much(cluster)]


def is_not_too_spread(cluster: Cluster):
    """

    :param cluster:
    :return:
    """
    return 400 < cluster.get_std()


def remove_too_spread(clusters: List[Cluster]):
    """

    :param clusters:
    :return:
    """
    return [cluster for cluster in clusters if not is_not_too_spread(cluster)]


def filter_cluster(clusters: List[Cluster]):
    return [cluster for cluster in clusters if is_not_too_spread(cluster) and are_not_too_few_or_not_too_much(cluster)]
