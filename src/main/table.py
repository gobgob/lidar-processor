"""
Table with LiDAR obstacles.
"""

from typing import List

import matplotlib.pylab as pl


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def multiply_by(self, a):
        return Point(a*self.x, a*self.y)


class Obstacle:
    def __init__(self, center: Point):
        self.center = center


class Square(Obstacle):
    def __init__(self, positions: List[Point]):
        center = Point(0, 0)
        for position in positions:
            center += position
        center.multiply_by(1/4.)

        super().__init__(center)

        self.positions = positions

    def compute_projection_on(self, point: Point):
        # TODO compute projection of a point on the obstacle
        pass

    def take_symmetric(self):
        return [[-position.x, -position.y] for position in self.positions]


class Table:
    def __init__(self):
        self.obstacles = []
        self.fig = None

    def add_obstacle(self, obstacle: Obstacle):
        self.obstacles.append(obstacle)

    def init_plot(self,):
        self.fig = pl.figure()
        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.set_xlim(-1700, 1700)
        ax.set_ylim(-100, 2100)
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
        points = [Point(-1500, 0), Point(1500, 0), Point(1500, 2000), Point(-1500, 2000)]
        xx = []
        yy = []
        for point in points:
            xx.append(point.x)
            yy.append(point.y)
        xx.append(xx[0])
        yy.append(yy[0])
        pl.plot(xx, yy, "g-")

    def plot(self):
        pl.show()


def main():
    table = Table()
    # for orange
    beacon_1 = Square([Point(-1500-100, 2000), Point(-1500, 2000), Point(-1500, 2000-100),
                       Point(-1500-100, 2000-100)])
    beacon_2 = Square([Point(1500, 1000+50), Point(1500+100, 1000+50), Point(1500+100, 1000-50),
                       Point(1500, 1000-50)])
    beacon_3 = Square([Point(-1500-100, 0+100), Point(-1500, 0+100), Point(-1500, 0), Point(-1500-100, 0)])

    table.add_obstacle(beacon_1)
    table.add_obstacle(beacon_2)
    table.add_obstacle(beacon_3)

    table.init_plot()
    table.plot_edges()
    table.plot_obstacles()
    table.plot()


if __name__ == "__main__":
    main()
