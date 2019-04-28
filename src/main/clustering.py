"""


"""
from typing import List

__author__ = "Clément Besnier"

import numpy as np
from scipy.optimize import root
from main.constants import *


class Cluster:
    """
    Cluster of points. May be an obstacle or a beacon.
    """
    def __init__(self):
        self.points = []
        self.mean = None

    def get_std(self):
        return np.std(self.points)

    def is_linear(self):
        """
        TODO
        Hough transform
        :return:
        """

    def compute_mean(self):
        self.mean = np.sum(self.points, axis=0)/len(self.points)

    def get_mean(self):
        self.compute_mean()
        return self.mean

    def add_point(self, point):
        self.points.append(point)

    def add_points(self, points):
        self.points.extend(points)

    def distance(self, other):
        if isinstance(other, Cluster):
            cluster_mean = np.sum(self.points, axis=0) / len(self.points)
            other_mean = np.sum(other.points, axis=0) / len(other.points)
            return distance(cluster_mean, other_mean)

    def add_cluster(self, other):
        self.points.extend(other)

    def __len__(self):
        return len(self.points)

    def is_a_circle(self, radius):
        """

        >>> thetas = np.deg2rad(np.arange(0, 150, 6))
        >>> real_x, real_y = (-420, 780)
        >>> real_radius = 100
        >>> xx = real_radius * np.cos(thetas) + real_x
        >>> yy = real_radius * np.sin(thetas) + real_y
        >>> import matplotlib.pyplot as plt
        >>> plt.plot(xx, yy)
        >>> points = [np.array([xx[i], yy[i]]) for i in range(len(xx))]
        >>> cluster = Cluster()
        >>> cluster.add_points(points)
        >>> cluster.is_a_circle(100)

        :param radius:
        :return:
        """
        def objective_function(x, y):
            circle_position = np.array([x, y])
            dist_sum = 0
            for point in self.points:
                dist_sum += (distance(point, circle_position) - radius)**2
            return dist_sum
        initial_guess = self.get_mean()
        # initial_guess = 0
        solution = root(objective_function, initial_guess, method="lm")

        print("solution", solution.x)
        print("error", solution.fun)


def distance(point, other):
    diff = point - other
    res = np.sqrt(diff @ diff.T)
    return res


def distance_al_kashi(angle1, distance1, angle2, distance2):
    """

    :param angle1:
    :param distance1:
    :param angle2:
    :param distance2:
    :return:
    """
    return np.sqrt(distance1**2+distance2**2 - 2*distance1*distance2*np.cos(angle2 - angle1))


def cluster_distance_mean(cluster, other):
    """
    >>> cluster_distance_mean([np.array([1, 2]), np.array([-1, -2])], [np.array([0, 4]), np.array([0, 4])])
    4.0

    :param cluster:
    :param other:
    :return:
    """
    cluster_mean = np.sum(cluster, axis=0)/len(cluster)
    other_mean = np.sum(other, axis=0)/len(other)
    return distance(cluster_mean, other_mean)


def cluster_distance_closest(cluster, other):
    """

    :param cluster:
    :param other:
    :return:
    """
    dist1 = distance(cluster[0], other[-1])
    dist2 = distance(cluster[-1], other[0])
    return min([dist1, dist2])


def clusterize(cartesian_measures: List[np.ndarray]):
    """

    :param cartesian_measures: Cartseian coordinates
    :return:
    """
    n = 0
    clusters = [[cartesian_measures[0]]]

    for i in range(1, len(cartesian_measures)-1):
        if distance(cartesian_measures[i-1], cartesian_measures[i]) > minimum_distance_between_clusters:
            n += 1
            clusters.append([])
        clusters[n].append(cartesian_measures[i])
    if distance(cartesian_measures[0], cartesian_measures[-1]) <= minimum_distance_between_clusters:
        clusters[-1].extend(clusters[0])
        clusters[0] = clusters.pop()
        n -= 1

    if len(clusters) > 1:
        j = 0
        k = 1
        while k < n:
            # dist_j = cluster_distance_mean(clusters[j], clusters[k])
            dist_j = cluster_distance_closest(clusters[j], clusters[k])
            # if cluster barycenters are close enough to each other, then clusters are merged
            if dist_j < 200:
                clusters[j].extend(clusters[k])
                del clusters[k]
                n -= 1
            else:
                # if the j'th and k'th are far enough, then, they are just different clusters
                j += 1
                k += 1
                # if a cluster has too few points, then it is deleted
                if len(clusters[j - 1]) < minimum_points_in_cluster:
                    del clusters[j - 1]
                    n -= 1
        # if cluster_distance_mean(clusters[0], clusters[-1]) < 200:
        if cluster_distance_closest(clusters[0], clusters[-1]) < 200:
            clusters[-1].extend(clusters[0])
            clusters[0] = clusters.pop()

        means = []
        for cluster in clusters:
            mean_cluster = np.sum(cluster, axis=0) / len(cluster)
            means.append(mean_cluster)
            # print(mean_cluster)
        return clusters, means


if __name__ == "__main__":
    pass
