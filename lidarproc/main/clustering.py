#!/home/pi/lidar-processor/lidar_env/bin/python

"""
Clustering module.

3
"""
from typing import List, Tuple

import numpy as np
from scipy.optimize import root

import lidarproc.main.geometry as geom
from lidarproc.main.constants import *


__author__ = "Clément Besnier"


class Beacon:
    def __init__(self):
        self.radius = 0
        self.x_center = 0
        self.y_center = 0
        self.center = None
        self.index = 0
        self.cluster = None

    def set_parameters(self, x: int, y: int, r: int, i: int):
        self.x_center = x
        self.y_center = y
        self.radius = r
        self.index = i
        self.center = geom.Point(x, y)

    def set_cluster(self, cluster):
        self.cluster = cluster

    def set_by_upper_left_and_lower_right(self, upper_left, lower_right):
        self.x_center = (upper_left[0]+lower_right[0])/2
        self.y_center = (upper_left[1]+lower_right[1])/2
        self.center = geom.Point(self.x_center, self.y_center)

    def set_radius(self, radius):
        self.radius = radius

    def set_index(self, index):
        self.index = index

    def __str__(self):
        return str(self.center)+" , "+str(self.radius)+" n°"+str(self.index)


class Cluster:
    """
    Cluster of points. May be an obstacle or a beacon.
    """
    def __init__(self):
        self.points = []
        self.mean = None
        self.beacon_radius = FIX_BEACON_RADIUS
        self.adverse_robot_radius = OPPONENT_ROBOT_BEACON_RADIUS

    def get_std(self):
        return np.std(self.points)

    def is_linear(self):
        """
        Hough transform or RANSAC
        :return:
        """
        pass

    def compute_mean(self):
        if len(self.points) > 0:
            self.mean = np.sum(self.points, axis=0)/len(self.points)
        else:
            self.mean = np.array([0, 0])

    def get_mean(self):
        if len(self.points) > 0:
            self.compute_mean()
            return self.mean
        else:
            return None

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

    def is_a_fix_beacon(self):
        """

        >>> thetas = np.deg2rad(np.arange(0, 150, 6))
        >>> real_x, real_y = (-420, 780)
        >>> real_radius = 100
        >>> xx = real_radius * np.cos(thetas) + real_x
        >>> yy = real_radius * np.sin(thetas) + real_y

        # >>> import matplotlib.pyplot as plt
        # >>> l = plt.plot(xx, yy)

        >>> points = [np.array([xx[i], yy[i]]) for i in range(len(xx))]
        >>> cluster = Cluster()
        >>> cluster.add_points(points)
        >>> cluster.is_a_fix_beacon()

        :return:
        """

        initial_guess = self.get_mean()
        solution = root(self._beacons_objective_function, initial_guess, method="lm")

        beacon = None
        if np.isclose(solution.fun[0], 0, atol=TOLERANCE_FOR_CIRCLE_COHERENCE):
            beacon = Beacon()
            beacon.set_parameters(solution.x[0], solution.x[1], FIX_BEACON_RADIUS, 0)
            beacon.set_cluster(self)
        return beacon

    def is_an_opponent_robot_beacon(self):
        """
        Should check that the point is in table ?
        :return:
        """
        cluster_mean = self.get_mean()
        return cluster_mean

    def is_a_circle(self, radius):
        def objective_function(pos):
            circle_position = pos
            dist_sum = 0
            for point in self.points:
                dist_sum += (distance(point, circle_position) - radius) ** 2
            return dist_sum, 0
        initial_guess = self.get_mean()
        solution = root(objective_function, initial_guess, method="lm")

        return solution

    def _beacons_objective_function(self, pos):
        # circle_position = np.array([x, y])
        return self._objective_function(pos, self.beacon_radius)

    def _objective_function(self, pos, radius):
        circle_position = pos
        dist_sum = 0
        for point in self.points:
            dist_sum += (distance(point, circle_position) - radius) ** 2
        return dist_sum, 0

    def _adverse_objective_function(self, pos):
        return self._objective_function(pos, self.adverse_robot_radius)

    def new_cluster_by_points(self, points: List):
        new_cluster = Cluster()
        new_cluster.points = points
        return new_cluster

    @staticmethod
    def to_clusters(clusters):
        """

        :param clusters: list of lists of 2D points
        :return: list of clusters
        """
        real_clusters = []
        for cluster in clusters:
            new_cluster = Cluster()
            new_cluster.add_points(cluster)
            real_clusters.append(new_cluster)
        return real_clusters


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


def polar_distance(polar_measure_1, polar_measure_2):
    return distance_al_kashi(polar_measure_1[0], polar_measure_1[1], polar_measure_2[0], polar_measure_2[1])


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


def cluster_polar_distance_closest(cluster, other):
    """

    :param cluster:
    :param other:
    :return:
    """
    dist1 = polar_distance(cluster[0], other[-1])
    dist2 = polar_distance(cluster[-1], other[0])
    return min([dist1, dist2])


def polar_clusterize(polar_measures)-> Tuple[List, List]:
    """

    :param polar_measures: Polar coordinates
    :return:
    """
    if len(polar_measures) > 0:
        n = 0
        clusters = [[polar_measures[0]]]

        for i in range(1, len(polar_measures) - 1):
            if polar_distance(polar_measures[i - 1], polar_measures[i]) > minimum_distance_between_clusters:
                n += 1
                clusters.append([])
            clusters[n].append(polar_measures[i])
        if polar_distance(polar_measures[0], polar_measures[-1]) <= minimum_distance_between_clusters:
            clusters[-1].extend(clusters[0])
            clusters[0] = clusters.pop()
            n -= 1

        if len(clusters) > 1:
            j = 0
            k = 1
            while k < n:
                dist_j = cluster_polar_distance_closest(clusters[j], clusters[k])
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
            if cluster_polar_distance_closest(clusters[0], clusters[-1]) < 200:
                clusters[-1].extend(clusters[0])
                clusters[0] = clusters.pop()

            means = []
            for cluster in clusters:
                mean_cluster = np.sum(cluster, axis=0) / len(cluster)
                means.append(mean_cluster)
            return clusters, means
    else:
        return [], []


def clusterize(cartesian_measures: List[np.ndarray]) -> Tuple[List, List]:
    """

    :param cartesian_measures: Cartesian coordinates
    :return:
    """
    if len(cartesian_measures) > 0:
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
            return clusters, means
        else:
            return [], []


if __name__ == "__main__":
    pass
