"""


"""
from typing import List

__author__ = "Clément Besnier"

import math
import numpy as np
from constants import *


# class Cluster:
#     def __init__(self):
#         self.items = []
#
#     def add_point(self, point):
#         self.items.append(point)
#
#     def distance(self, other: Cluster):
#         if

def distance(point, other):
    diff = point - other
    res = np.sqrt(diff @ diff.T)
    return res


def cluster_distance(cluster, other):
    cluster_mean = np.sum(cluster, axis=0)/len(cluster)
    other_mean = np.sum(other, axis=0)/len(other)
    return distance(cluster_mean, other_mean)


def clusterize(cartesian_measures: List[np.ndarray]):
    """

    :param cartesian_measures: Cartseian coordinates
    :return:
    """
    n = 0
    clusters = [[]]
    for i in range(2, len(cartesian_measures)):
        dist = distance(cartesian_measures[i - 2], cartesian_measures[i - 1])
        if dist > tsec and \
                distance(cartesian_measures[i-1], cartesian_measures[i]) > tsec:
            n += 1
            clusters.append([])
        clusters[n].append(cartesian_measures[i])
    new_clusters = []
    for j in range(n+1):
        dist_j = cluster_distance(clusters[j], clusters[n])
        if dist_j > tmaxsel or dist_j < tminsel:
            pass
        else:
            new_clusters.append(clusters[j])
            n -= 1
    return new_clusters


