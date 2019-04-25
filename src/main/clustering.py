"""


"""
from typing import List

__author__ = "Clément Besnier"

import math
import numpy as np
from constants import *


class Cluster:
    def __init__(self):
        self.points = []
        self.mean = None

    def compute_mean(self):
        self.mean = np.sum(self.points, axis=0)/len(self.points)

    def get_mean(self):
        self.compute_mean()
        return self.mean

    def add_point(self, point):
        self.points.append(point)

    def distance(self, other):
        pass


def distance(point, other):
    diff = point - other
    res = np.sqrt(diff @ diff.T)
    return res


def cluster_distance(cluster, other):
    """
    >>> cluster_distance([np.array([1, 2]), np.array([-1, -2])], [np.array([0, 4]), np.array([0, 4])])
    4.0

    :param cluster:
    :param other:
    :return:
    """
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
        if distance(cartesian_measures[i - 2], cartesian_measures[i - 1]) > tsec and \
                distance(cartesian_measures[i-1], cartesian_measures[i]) > tsec:
            n += 1
            clusters.append([])
        clusters[n].append(cartesian_measures[i])
    print("nombre de clusters : ", n)

    if len(clusters) > 1:
        j = 0
        k = 1
        while k < n:
            dist_j = cluster_distance(clusters[j], clusters[k])
            # if not (dist_j > tmaxsel or dist_j < tminsel):
            #     new_clusters.append(clusters[j])
            #     n -= 1
            if dist_j < 200:
                clusters[j].extend(clusters[k])
                del clusters[k]
                n -= 1

            j += 1
            k += 1
            # else:
        print("nombre de clusters : ", len(clusters))
        means = []
        for cluster in clusters:
            mean_cluster = np.sum(cluster, axis=0) / len(cluster)
            means.append(mean_cluster)
            print(mean_cluster)

        return clusters, means


if __name__ == "__main__":
    pass
