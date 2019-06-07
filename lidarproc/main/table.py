#!/home/pi/lidar-processor/lidar_env/bin/python

"""
Table with LiDAR obstacles.
"""

from typing import List, Union

import numpy as np
try:
    import matplotlib.pylab as pl
    from check_clustering import main_clustering
except ImportError:
    pl = None
    main_clustering = None

from lidarproc.main.constants import *
from lidarproc.main.clustering import Cluster
import lidarproc.main.data_retrieval as dr
import lidarproc.main.geometry as geom


__author__ = "Clément Besnier"


class Obstacle:
    def __init__(self, center: geom.Point):
        self.center = center


class Rectangle:
    def __init__(self, limits: List[geom.Point]):
        self.upper_left, self.lower_right = limits
        center = geom.Point(0, 0)
        for position in limits:
            center = center + position
        self.center = center.multiply_by(1 / 2.)

    def get_center(self):
        return self.center

    def is_point_in_rectangle(self, point: Union[geom.Point, np.ndarray]):
        if isinstance(point, geom.Point):
            return self.upper_left.x-SOFT_THRESHOLD_RECTANGLE <= point.x <= self.lower_right.x+SOFT_THRESHOLD_RECTANGLE and \
                   self.lower_right.y-SOFT_THRESHOLD_RECTANGLE <= point.y <= self.upper_left.y+SOFT_THRESHOLD_RECTANGLE
        elif isinstance(point, np.ndarray):
            return self.upper_left.x-SOFT_THRESHOLD_RECTANGLE <= point[0] <= self.lower_right.x+SOFT_THRESHOLD_RECTANGLE and \
                   self.lower_right.y-SOFT_THRESHOLD_RECTANGLE <= point[1] <= self.upper_left.y+SOFT_THRESHOLD_RECTANGLE

    def is_close_enough(self, cluster: Cluster):
        return dr.distance_array(cluster.get_mean(), self.center.to_array()) < 400

    def is_cluster_in_rectangle(self, cluster: Union[Cluster, List]):
        if isinstance(cluster, Cluster):
            for point in cluster.points:
                if not self.is_point_in_rectangle(point):
                    return False
            return len(cluster.points) > 0
        elif type(cluster) == list:
            for point in cluster:
                print(point)
                if not self.is_point_in_rectangle(geom.Point(point[0], point[1])):
                    return False
            return len(cluster) > 0
        return False

    def rotate(self, angle: float):
        """

        :param angle:
        :return:
        """
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

        ul = rotation_matrix @ self.upper_left.to_array().T
        lr = rotation_matrix @ self.lower_right.to_array().T
        return Rectangle([geom.Point(ul[0], ul[1]), geom.Point(lr[0], lr[1])])

    def translate(self, point: geom.Point):
        """

        :param point:
        :return:
        """
        return Rectangle([self.upper_left + point, self.lower_right + point])

    def m_translate(self, point: geom.Point):
        """
        m for minus
        :param point:
        :return:
        """
        return Rectangle([self.upper_left - point, self.lower_right - point])

    def __str__(self):
        return str(self.center)


class Square(Obstacle):
    def __init__(self, positions: List[geom.Point]):
        center = geom.Point(0, 0)
        for position in positions:
            center = center + position
        center = center.multiply_by(1 / 4.)

        super().__init__(center)

        self.positions = positions
        assert len(positions) == 4

    def compute_projection_on(self, point: geom.Point):
        # TODO compute projection of a point on the obstacle
        pass

    def take_symmetric(self):
        self.positions = [geom.Point(-position.x, position.y) for position in self.positions]
        self.center = geom.Point(-self.center.x, self.center.y)

    def translate(self, vector: geom.Vector):
        return Square([vector.apply_to_point(position) for position in self.positions])
        # self.center = vector.apply_to_point(self.center)
        # self.positions =

    def rotate(self, angle: float):
        """
        >>> v = geom.Vector()
        >>> v.set_coordinates(2., 3.)
        >>> v.rotate(np.pi)
        >>> np.isclose(v.x, -2)
        True
        >>> np.isclose(v.y, -3)
        True

        :param angle:
        :return:
        """
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        positions = []
        for position in self.positions:
            res = rotation_matrix @ np.array([position.x, position.y]).T
            point = geom.Point(res[0], res[1])
            positions.append(point)
        return Square(positions)


class Table:
    def __init__(self):
        self.obstacles = []
        self.edges = []
        self.vectors = []
        self.points = []
        self.fig = None

    # def add_obstacle(self, obstacle: Obstacle):
    #     self.obstacles.append(obstacle)

    def add_square_obstacle(self, obstacle: Square):
        self.obstacles.append(obstacle)

    def add_edge_point(self, edge: geom.Point):
        self.edges.append(edge)

    def add_vector(self, vector: geom.Vector):
        self.vectors.append(vector)

    def add_point(self, point: geom.Point):
        self.points.append(point)

    def init_plot(self, ):
        self.fig = pl.figure()
        ax = self.fig.add_subplot(111)
        ax.clear()
        xlimits = 3000
        y_max_limit = 3000
        y_min_limit = -2000
        ax.set_xlim(-xlimits, xlimits)
        ax.set_ylim(y_min_limit, y_max_limit)
        ax.axhline(0, 0)
        ax.axvline(0, 0)

    def plot_vector(self, vector: geom.Vector):
        pl.plot([0, vector.x], [0, vector.y], "-")

    def plot_vectors(self):
        print("vectors")
        for vector in self.vectors:
            pl.plot([0, vector.x], [0, vector.y], "-")
            print(vector.x, vector.y)

    def plot_point(self, point: geom.Point):
        pl.plot(point.x, point.y, "+")

    def plot_points(self):
        print("points")
        xx = []
        yy = []
        for point in self.points:
            xx.append(point.x)
            yy.append(point.y)
            print(point.x, point.y)
        pl.plot(xx, yy, "+")

    def plot_unitary_vector(self, point: geom.Point, angle):
        pl.plot([point.x, point.x+100*np.cos(angle)], [point.y, point.y+100*np.sin(angle)], "-")

    def plot_vector_from_point(self, point: geom.Point, vector: geom.Vector):
        other_point = vector.apply_to_point(point)
        pl.plot([point.x, other_point.x], [point.y, other_point.y])

    def plot_obstacles(self):
        for obstacle in self.obstacles:
            xx = []
            yy = []
            if isinstance(obstacle, Square):
                for position in obstacle.positions:
                    xx.append(position.x)
                    yy.append(position.y)
                xx.append(xx[0])
                yy.append(yy[0])
            pl.plot(xx, yy, 'r-')
        self.fig.canvas.draw()

    def plot_clusters(self, clusters):
        """

        :return:
        """
        xx = []
        yy = []
        for cluster_center in clusters:
            xx.append(cluster_center[0])
            yy.append(cluster_center[1])
        pl.plot(xx, yy, "y,")

    def plot_edges(self):
        xx = []
        yy = []
        for point in self.edges:
            xx.append(point.x)
            yy.append(point.y)
        xx.append(xx[0])
        yy.append(yy[0])
        pl.plot(xx, yy, "g-")

    @staticmethod
    def plot():
        pl.show()

    def simulate_measure(self, measure_point: geom.Point, angle: float, rho: float):
        # thetas = np.deg2rad(np.arange(0, 180, angle_resolution))
        # print(measure_point)
        vectors = []
        for obstacle in self.obstacles:
            vec = geom.Vector()
            vec.set_by_points(measure_point, obstacle.center)
            vectors.append(vec)
            # print(obstacle.center)
            # print(vec)

        robot_vector = geom.Vector()
        robot_vector.set_coordinates(np.cos(angle) * rho, np.sin(angle) * rho)

        return vectors, robot_vector

        # for i in range(len(thetas)):
        #     thetas[i]

    @staticmethod
    def plot_lidar_measures(measures):
        xx, yy = [], []

        for measure in measures:
            xx.append(measure[0])
            yy.append(measure[1])
        pl.plot(xx, yy, "r,")

    @staticmethod
    def plot_measures(measure_point: geom.Point, vectors: List[geom.Vector], robot_vector: geom.Vector):
        for vector in vectors:
            res = vector.apply_to_point(measure_point)
            # print([measure_point.x, res.x], [measure_point.y, res.y])
            pl.plot([measure_point.x, res.x], [measure_point.y, res.y], "b-")

        robot_vector.apply_to_point(measure_point)
        # pl.plot([measure_point.x, measure_point.x+robot_vector.x], [measure_point.y, measure_point.y+robot_vector.y])
        pl.arrow(measure_point.x, measure_point.y, robot_vector.x, robot_vector.y, width=1)

    def translate(self, vector: geom.Vector):
        self.obstacles = [obstacle.translate(vector) for obstacle in self.obstacles]
        self.edges = [vector.apply_to_point(edge_point) for edge_point in self.edges]
        self.points = [vector.apply_to_point(point) for point in self.points]
        self.vectors = [vector + table_vector for table_vector in self.vectors]

    def rotate(self, angle: float):
        self.obstacles = [obstacle.rotate(angle) for obstacle in self.obstacles]
        self.edges = [edge_point.rotate(angle) for edge_point in self.edges]
        self.points = [point.rotate(angle) for point in self.points]
        self.vectors = [vector.rotate(angle) for vector in self.vectors]

    def generate_measures(self, robot_point: geom.Point):
        vertices = []
        edges = []
        for obstacle in self.obstacles:
            for i in range(len(obstacle.positions) - 1):
                vertices.append(obstacle.positions[i])
                edges.append(geom.Segment(obstacle.positions[i], obstacle.positions[i + 1]))
            edges.append(geom.Segment(obstacle.positions[-1], obstacle.positions[0]))
            vertices.append(obstacle.positions[-1])

        # for edge in edges:
        #     xx = []
        #     yy = []
        #     xx.append(edge.p1.x)
        #     xx.append(edge.p2.x)
        #     yy.append(edge.p1.y)
        #     yy.append(edge.p2.y)
        #     pl.plot(xx, yy, "m-")

        # print("len(vertices)", len(vertices))
        for vertex in vertices:
            for edge in edges:
                if vertex not in [edge.p1, edge.p2]:
                    s = geom.Segment(robot_point, vertex)
                    if edge.collide(s):
                        # xx = []
                        # yy = []
                        # xx.append(s.p1.x)
                        # xx.append(s.p2.x)
                        # yy.append(s.p1.y)
                        # yy.append(s.p2.y)
                        # pl.plot(xx, yy)
                        if vertex in vertices:
                            vertices.remove(vertex)
                        if edge in edges:
                            edges.remove(edge)

        # print("len(vertices)", len(vertices))
        for vertex in vertices:
            s = geom.Segment(robot_point, vertex)
            pl.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], "m-")

        # for e in edges:
        #     print(e)

        # print(len(vertices))
        # for j in vertices:
        #     print(j)
