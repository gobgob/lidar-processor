"""
Table with LiDAR obstacles.
"""

from __future__ import annotations

from typing import List

import numpy as np
import matplotlib.pylab as pl

from src.constants import *


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
        self.determinant = self.compute_determinant()

    def compute_determinant(self):
        return self.p1.x * self.p2.y - self.p1.y * self.p2.x

    def compute_x_difference(self):
        return self.p1.x - self.p2.x

    def compute_y_difference(self):
        return self.p1.y - self.p2.y

    def get_determinant(self):
        return self.determinant

    def get_x_difference(self):
        return self.x_difference

    def get_y_difference(self):
        return self.y_difference

    def collide(self, other: Segment):
        denominator = (self.get_x_difference() * other.get_y_difference() -
                       self.get_y_difference() * other.get_x_difference())
        px = (self.get_determinant() * other.get_x_difference() - self.get_x_difference() * other.get_determinant()) / \
            denominator

        py = (self.get_determinant() * other.get_y_difference() - self.get_y_difference() * other.get_determinant()) / \
            denominator
        pass


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
        return [[-position.x, -position.y] for position in self.positions]

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

    def check_visible_points(self, robot_point: Point):
        vertices = []
        # vertices.extend([ for obstacle in self.o])
        #         # for vertex in self.positions:
        #         #     pass


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

    def plot_edges(self):
        xx = []
        yy = []
        for point in self.edges:
            xx.append(point.x)
            yy.append(point.y)
        xx.append(xx[0])
        yy.append(yy[0])
        pl.plot(xx, yy, "g-")

    def plot(self):
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
                edges.append((obstacle[i], obstacle[i + 1]))
            edges.append((obstacle.positions[-1], obstacle.positions[0]))

        # invisible_vertices = []
        # for vertex in vertices:
        #     for edge in edges:
        #         if
        #         invisible_vertices.append(vertex)


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


if __name__ == "__main__":
    main()
    main_2()
