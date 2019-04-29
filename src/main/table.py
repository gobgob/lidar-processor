"""
Table with LiDAR obstacles.
"""

from __future__ import annotations

from typing import List

import numpy as np
import matplotlib.pylab as pl

from check_clustering import main_clustering
from main.main import remove_too_far_or_too_close
from main.output_rendering import keep_good_measures
from retrieve_realistic_measures import get_table_measures


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def multiply_by(self, a):
        return Point(a * self.x, a * self.y)

    def distance(self, other):
        return np.sqrt(np.power(self.x - other.x, 2) + np.power(self.y - other.y, 2))

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def rotate(self, angle: float):
        """
        >>> point = Point(2., 3.)
        >>> point.rotate(np.pi)
        >>> np.isclose(point.x, -2)
        True
        >>> np.isclose(point.y, -3)
        True

        :param angle:
        :return:
        """
        res = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]) @ np.array([self.x, self.y]).T
        self.x = res[0]
        self.y = res[1]
        return Point(self.x, self.y)


class Vector:
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_by_points(self, point1, point2):
        self.x = point2.x - point1.x
        self.y = point2.y - point1.y

    def compute_angle(self):
        return np.arctan(self.y / self.x)

    def compute_distance(self):
        return np.sqrt(self.x ** 2 + self.y ** 2)

    def apply_to_point(self, point: Point):
        print(point)
        return Point(point.x + self.x, point.y + self.y)

    def __str__(self):
        return str(self.x) + " - " + str(self.y)

    def set_coordinates(self, x: float, y: float):
        self.x = x
        self.y = y

    def rotate(self, angle: float):
        """
        >>> v = Vector()
        >>> v.set_coordinates(2., 3.)
        >>> v.rotate(np.pi)
        >>> np.isclose(v.x, -2)
        True
        >>> np.isclose(v.y, -3)
        True

        :param angle:
        :return:
        """
        res = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]) @ np.array([self.x, self.y]).T
        self.x = res[0]
        self.y = res[1]


class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        self.x_difference = self.compute_x_difference()
        self.y_difference = self.compute_y_difference()
        # self.determinant = self.compute_determinant()

    def __str__(self):
        return "p1: "+str(self.p1)+", p2: "+str(self.p2)

    # def compute_determinant(self):
    #     return self.p1.x * self.p2.y - self.p1.y * self.p2.x

    def compute_x_difference(self):
        return self.p2.x - self.p1.x

    def compute_y_difference(self):
        return self.p2.y - self.p1.y

    # def get_determinant(self):
    #     return self.determinant

    def get_x_difference(self):
        return self.x_difference

    def get_y_difference(self):
        return self.y_difference

    def collide(self, other: Segment):
        """
        if denominator are of same sign and numerator is lesser than denominator, then the segments collide

        >>> pa = Point(1.8, 2.1)
        >>> pb = Point(0.8, 1.1)
        >>> pc = Point(1, 1.25)
        >>> pd = Point(0, 1.25)
        >>> s1 = Segment(pa, pb)
        >>> print(s1)

        >>> s2 = Segment(pc, pd)
        >>> print(s2)

        >>> s1.collide(s2)

        >>> s2.collide(s1)


        >>> pa = Point(-1., 0.5)
        >>> pb = Point(1., 0.5)
        >>> pc = Point(0., 1.)
        >>> pd = Point(0., 2.)
        >>> s1 = Segment(pa, pb)
        >>> print(s1)

        >>> s2 = Segment(pc, pd)
        >>> print(s2)

        >>> s1.collide(s2)

        >>> s2.collide(s1)

        :param other:
        :return:
        """
        false_segment = Segment(self.p1, other.p1)
        # print(false_segment)

        numerator = (false_segment.get_x_difference() * other.get_y_difference() -
                     false_segment.get_y_difference() * other.get_x_difference())

        denominator = (self.get_x_difference() * other.get_y_difference() -
                       self.get_y_difference() * other.get_x_difference())

        # print(numerator)
        # print(denominator)
        t = numerator / denominator
        print("t", t)
        if 0 <= t <= 1:
            print("x: ", self.p1.x + t * (self.p2.x - self.p1.x))
            print("y: ", self.p1.y + t * (self.p2.y - self.p1.y))

        # px = (self.get_determinant() * other.get_x_difference() - self.get_x_difference() * other.get_determinant())
        # / \ denominator
        # py = (self.get_determinant() * other.get_y_difference() - self.get_y_difference() * other.get_determinant())
        # / \ denominator
        return ((0 <= denominator and 0 <= numerator) or (denominator <= 0 and numerator <= 0)) and \
               (abs(numerator) <= abs(denominator))

        # if 0 < denominator and 0 < numerator or denominator < 0 and numerator < 0:
        #     return numerator < denominator
        # else:
        #     return False


class Obstacle:
    def __init__(self, center: Point):
        self.center = center


class Square(Obstacle):
    def __init__(self, positions: List[Point]):
        center = Point(0, 0)
        for position in positions:
            center = center + position
        center = center.multiply_by(1 / 4.)

        super().__init__(center)

        self.positions = positions
        assert len(positions) == 4

    def compute_projection_on(self, point: Point):
        # TODO compute projection of a point on the obstacle
        pass

    def take_symmetric(self):
        self.positions = [Point(-position.x, -position.y) for position in self.positions]

    def translate(self, vector: Vector):
        return Square([vector.apply_to_point(position) for position in self.positions])
        # self.center = vector.apply_to_point(self.center)
        # self.positions =

    def rotate(self, angle: float):
        """
        >>> v = Vector()
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
            point = Point(res[0], res[1])
            positions.append(point)
        return Square(positions)


class Table:
    def __init__(self):
        self.obstacles = []
        self.edges = []
        self.fig = None

    # def add_obstacle(self, obstacle: Obstacle):
    #     self.obstacles.append(obstacle)

    def add_square_obstacle(self, obstacle: Square):
        self.obstacles.append(obstacle)

    def add_edge_point(self, edge: Point):
        self.edges.append(edge)

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

    def simulate_measure(self, measure_point: Point, angle: float, rho: float):
        # thetas = np.deg2rad(np.arange(0, 180, angle_resolution))
        print(measure_point)
        vectors = []
        for obstacle in self.obstacles:
            vec = Vector()
            vec.set_by_points(measure_point, obstacle.center)
            vectors.append(vec)
            print(obstacle.center)
            print(vec)

        robot_vector = Vector()
        robot_vector.set_coordinates(np.cos(angle) * rho, np.sin(angle) * rho)

        return vectors, robot_vector

        # for i in range(len(thetas)):
        #     thetas[i]

    def plot_lidar_measures(self, measures):
        xx, yy = [], []

        for measure in measures:
            xx.append(measure[0])
            yy.append(measure[1])
        pl.plot(xx, yy, "r,")

    def plot_measures(self, measure_point: Point, vectors: List[Vector], robot_vector: Vector):
        for vector in vectors:
            res = vector.apply_to_point(measure_point)
            pl.plot([measure_point.x, res.x], [measure_point.y, res.y], "b-")

        robot_vector.apply_to_point(measure_point)
        # pl.plot([measure_point.x, measure_point.x+robot_vector.x], [measure_point.y, measure_point.y+robot_vector.y])
        pl.arrow(measure_point.x, measure_point.y, robot_vector.x, robot_vector.y, width=1)

    def translate(self, vector: Vector):
        self.obstacles = [obstacle.translate(vector) for obstacle in self.obstacles]
        self.edges = [vector.apply_to_point(edge_point) for edge_point in self.edges]

    def rotate(self, angle: float):
        self.obstacles = [obstacle.rotate(angle) for obstacle in self.obstacles]
        self.edges = [edge_point.rotate(angle) for edge_point in self.edges]

    def generate_measures(self, robot_point: Point):
        vertices = []
        edges = []
        for obstacle in self.obstacles:
            for i in range(len(obstacle.positions) - 1):
                vertices.append(obstacle.positions[i])
                edges.append(Segment(obstacle.positions[i], obstacle.positions[i + 1]))
            edges.append(Segment(obstacle.positions[-1], obstacle.positions[0]))
            vertices.append(obstacle.positions[-1])

        # for edge in edges:
        #     xx = []
        #     yy = []
        #     xx.append(edge.p1.x)
        #     xx.append(edge.p2.x)
        #     yy.append(edge.p1.y)
        #     yy.append(edge.p2.y)
        #     pl.plot(xx, yy, "m-")

        print("len(vertices)", len(vertices))
        for vertex in vertices:
            for edge in edges:
                if vertex not in [edge.p1, edge.p2]:
                    s = Segment(robot_point, vertex)
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

        print("len(vertices)", len(vertices))
        for vertex in vertices:
            s = Segment(robot_point, vertex)
            pl.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], "m-")

        # for e in edges:
        #     print(e)

        # print(len(vertices))
        # for j in vertices:
        #     print(j)


def main():
    table = Table()
    # for orange
    beacon_1 = Square([Point(-1500 - 100, 2000), Point(-1500, 2000), Point(-1500, 2000 - 100),
                       Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([Point(1500, 1000 + 50), Point(1500 + 100, 1000 + 50), Point(1500 + 100, 1000 - 50),
                       Point(1500, 1000 - 50)])
    beacon_3 = Square([Point(-1500 - 100, 0 + 100), Point(-1500, 0 + 100), Point(-1500, 0), Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(Point(-1500, 0))
    table.add_edge_point(Point(1500, 0))
    table.add_edge_point(Point(1500, 2000))
    table.add_edge_point(Point(-1500, 2000))

    measure = Point(-1000, 1100)

    vectors, robot_vector = table.simulate_measure(measure, 0.5, 200)

    table.init_plot()
    table.plot_edges()
    table.plot_obstacles()
    table.plot_measures(measure, vectors, robot_vector)
    table.plot()


def main_2():
    table = Table()
    # for orange
    beacon_1 = Square([Point(-1500 - 100, 2000), Point(-1500, 2000), Point(-1500, 2000 - 100),
                       Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([Point(1500, 1000 + 50), Point(1500 + 100, 1000 + 50), Point(1500 + 100, 1000 - 50),
                       Point(1500, 1000 - 50)])
    beacon_3 = Square([Point(-1500 - 100, 0 + 100), Point(-1500, 0 + 100), Point(-1500, 0), Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(Point(-1500, 0))
    table.add_edge_point(Point(1500, 0))
    table.add_edge_point(Point(1500, 2000))
    table.add_edge_point(Point(-1500, 2000))

    translation_vector = Vector()
    translation_vector.set_coordinates(+1000, -1100)
    table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    rotation_angle = 0.5
    table.rotate(rotation_angle)

    measure = Point(-1000, 1100)
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
    beacon_1 = Square([Point(-1500 - 100, 2000), Point(-1500, 2000), Point(-1500, 2000 - 100),
                       Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([Point(1500, 1000 + 50), Point(1500 + 100, 1000 + 50), Point(1500 + 100, 1000 - 50),
                       Point(1500, 1000 - 50)])
    beacon_3 = Square([Point(-1500 - 100, 0 + 100), Point(-1500, 0 + 100), Point(-1500, 0), Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(Point(-1500, 0))
    table.add_edge_point(Point(1500, 0))
    table.add_edge_point(Point(1500, 2000))
    table.add_edge_point(Point(-1500, 2000))

    # translation_vector = Vector()
    # translation_vector.set_coordinates(+1000, -1100)
    # table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    # rotation_angle = 0.5
    # table.rotate(rotation_angle)

    measure = Point(-300, 1400)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)
    vectors, robot_vector = table.simulate_measure(measure, 0, 200)

    table.init_plot()
    table.plot_edges()
    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.generate_measures(measure)
    table.plot()


def main_4():
    table = Table()
    # for orange
    beacon_1 = Square([Point(-1500 - 100, 2000), Point(-1500, 2000), Point(-1500, 2000 - 100),
                       Point(-1500 - 100, 2000 - 100)])
    beacon_2 = Square([Point(1500, 1000 + 50), Point(1500 + 100, 1000 + 50), Point(1500 + 100, 1000 - 50),
                       Point(1500, 1000 - 50)])
    beacon_3 = Square([Point(-1500 - 100, 0 + 100), Point(-1500, 0 + 100), Point(-1500, 0), Point(-1500 - 100, 0)])

    table.add_square_obstacle(beacon_1)
    table.add_square_obstacle(beacon_2)
    table.add_square_obstacle(beacon_3)

    table.add_edge_point(Point(-1500, 0))
    table.add_edge_point(Point(1500, 0))
    table.add_edge_point(Point(1500, 2000))
    table.add_edge_point(Point(-1500, 2000))

    # translation_vector = Vector()
    # translation_vector.set_coordinates(+1000, -1100)
    # table.translate(translation_vector)

    # rotation_angle = np.pi / 3
    # rotation_angle = 0.5
    # table.rotate(rotation_angle)

    measure = Point(-300, 1400)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)

    clusters = main_clustering()
    print("clusters", clusters)

    table.init_plot()
    table.plot_edges()
    table.plot_clusters(clusters)
    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.generate_measures(measure)
    table.plot()


def main_5():
    table = Table()

    table.add_edge_point(Point(-1500, 0))
    table.add_edge_point(Point(1500, 0))
    table.add_edge_point(Point(1500, 2000))
    table.add_edge_point(Point(-1500, 2000))

    samples = ["0_-1820_pi_over_2", "1210_1400_pi"]
    measures = get_table_measures(samples[0])
    for i in range(len(measures)):
        one_turn_measure = keep_good_measures(measures[i], 100)
        one_turn_measure = remove_too_far_or_too_close(one_turn_measure)

    translation_vector = Vector()
    translation_vector.set_coordinates(+1000, -1100)
    table.translate(translation_vector)

    rotation_angle = np.pi / 3
    rotation_angle = 0.5
    table.rotate(rotation_angle)

    # measure = Point(0, 1800)
    # measure = translation_vector.apply_to_point(measure)
    # measure.rotate(rotation_angle)

    table.init_plot()
    table.plot_edges()
    table.plot_measures()

    # table.plot_obstacles()
    # table.plot_measures(measure, vectors, robot_vector)
    table.plot()


if __name__ == "__main__":
    # main()
    # main_2()
    # main_3()
    main_4()
