#!/usr/bin/python3

"""
Table with LiDAR obstacles.
"""

from typing import List

import numpy as np
import matplotlib.pylab as pl

from check_clustering import main_clustering
import main.data_cleansing as dacl
from main.clustering import Cluster
from retrieve_realistic_measures import get_table_measures
import main.geometry as geom


__author__ = "Clément Besnier"


class Obstacle:
    def __init__(self, center: geom.Point):
        self.center = center


class Rectangle:
    def __init__(self, limits: List[geom.Point]):
        self.upper_left, self.lower_right = limits

    def is_point_in_rectangle(self, point: geom.Point):
        return self.upper_left.x <= point.x <= self.lower_right.x and\
               self.lower_right.y <= point.y <= self.upper_left.y

    def is_cluster_in_rectangle(self, cluster: Cluster):
        for point in cluster.points:
            if not self.is_point_in_rectangle(geom.Point(point[0], point[1])):
                return False
        return True


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
        TODO
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


# region ++ mains
def main():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    measure = geom.Point(-1000, 1100)

    vectors, robot_vector = table.simulate_measure(measure, 0.5, 200)

    table.init_plot()
    table.plot_edges()
    table.plot_obstacles()
    table.plot_measures(measure, vectors, robot_vector)
    table.plot()


def main_2():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    translation_vector = geom.Vector()
    translation_vector.set_coordinates(+1000, -1100)
    table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    rotation_angle = 0.5
    table.rotate(rotation_angle)

    measure = geom.Point(-1000, 1100)
    measure = translation_vector.apply_to_point(measure)
    measure.rotate(rotation_angle)
    vectors, robot_vector = table.simulate_measure(measure, 0, 200)

    table.init_plot()
    table.plot_edges()
    table.plot_obstacles()
    table.plot_measures(measure, vectors, robot_vector)
    table.plot()


def main_3():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    # translation_vector = geom.Vector()
    # translation_vector.set_coordinates(+1000, -1100)
    # table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    # rotation_angle = 0.5
    # table.rotate(rotation_angle)

    measure = geom.Point(-300, 1400)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)
    # vectors, robot_vector = table.simulate_measure(measure, 0, 200)

    table.init_plot()
    table.plot_edges()
    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.generate_measures(measure)
    table.plot()


def main_4():
    table = Table()
    # for orange
    beacon_1 = Square([geom.Point(-1500 - 100, 2000), geom.Point(-1500, 2000), geom.Point(-1500, 2000 - 100),
                       geom.Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([geom.Point(1500, 1000 + 50), geom.Point(1500 + 100, 1000 + 50),
                       geom.Point(1500 + 100, 1000 - 50), geom.Point(1500, 1000 - 50)])
    beacon_3 = Square([geom.Point(-1500 - 100, 0 + 100), geom.Point(-1500, 0 + 100), geom.Point(-1500, 0),
                       geom.Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    # translation_vector = geom.Vector()
    # translation_vector.set_coordinates(+1000, -1100)
    # table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    # rotation_angle = 0.5
    # table.rotate(rotation_angle)

    measure = geom.Point(-300, 1400)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)

    clusters = main_clustering()
    # print("clusters", clusters)

    table.init_plot()
    table.plot_edges()
    table.plot_clusters(clusters)
    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.generate_measures(measure)
    table.plot()


def main_5():
    table = Table()

    table.add_edge_point(geom.Point(-1500, 0))
    table.add_edge_point(geom.Point(1500, 0))
    table.add_edge_point(geom.Point(1500, 2000))
    table.add_edge_point(geom.Point(-1500, 2000))

    samples = ["0_-1820_pi_over_2", "1210_1400_pi"]
    measures = get_table_measures(samples[0])
    for i in range(len(measures)):
        one_turn_measure = dacl.keep_good_measures(measures[i], 100)
        # one_turn_measure = dacl.keep_not_too_far_or_not_too_close(one_turn_measure)

    translation_vector = geom.Vector()
    translation_vector.set_coordinates(+1000, -1100)
    table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    rotation_angle = 0.5
    table.rotate(rotation_angle)

    # measure = geom.Point(0, 1800)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)

    table.init_plot()
    table.plot_edges()
    # table.plot_measures()

    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.plot()
# endregion


if __name__ == "__main__":
    # main()
    # main_2()
    # main_3()
    main_4()
