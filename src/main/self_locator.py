#!/home/pi/lidar-processor/lidar_env/bin/python

"""

At the beginning, we know the position of the robot and immobile beacons.

We can follow the immobile beacons as the robot moves.

If we know where the beacons are, we know where the robot is so we get a precise measure of its current position.

It is also possible to use the encoders' measures as the first estimation of the new robot state. Then two closest
clusters to the expected positions of beacons are searched.
"""

from typing import List, Tuple, Union

import numpy as np

from main.constants import *
from main.clustering import Cluster, Beacon
import main.geometry as geom
import main.data_retrieval as dr
import main.table as table

__author__ = "Clément Besnier"
p_beacons_orange = [[geom.Point(point[0], point[1]) for point in limits]for limits in beacons_orange]
p_beacons_purple = [[geom.Point(point[0], point[1]) for point in limits]for limits in beacons_purple]


def define_point_beacons(own_colour: TeamColor):
    """
    Gets the positions of the beacons according to our colour in the table basis.
    :param own_colour:
    :return:
    """
    if own_colour.value == TeamColor.orange.value:
        bo1 = table.Rectangle(p_beacons_orange[0]).get_center()
        bo2 = table.Rectangle(p_beacons_orange[1]).get_center()
        bo3 = table.Rectangle(p_beacons_orange[2]).get_center()
        return bo1, bo2, bo3
    elif own_colour.value == TeamColor.purple.value:
        bp1 = table.Rectangle(p_beacons_purple[0]).get_center()
        bp2 = table.Rectangle(p_beacons_purple[1]).get_center()
        bp3 = table.Rectangle(p_beacons_purple[2]).get_center()
        return bp1, bp2, bp3


def find_starting_beacons(own_colour: TeamColor, clusters: List[Cluster]):
    b1, b2, b3 = define_point_beacons(own_colour)
    if own_colour.value == TeamColor.orange.value:
        starting_position = geom.Point(-1210, 1400)
        starting_orientation = 0
    elif own_colour.value == TeamColor.purple.value:
        starting_position = geom.Point(1210, 1400)
        starting_orientation = np.pi
    else:
        return [None, None, None]

    p_b1_lidar = geom.from_theoretical_table_to_lidar(b1, starting_position, starting_orientation)
    p_b2_lidar = geom.from_theoretical_table_to_lidar(b2, starting_position, starting_orientation)
    p_b3_lidar = geom.from_theoretical_table_to_lidar(b3, starting_position, starting_orientation)

    # print("b1 vu du LiDAR"+str(p_b1_lidar))
    # print("b2 vu du LiDAR"+str(p_b2_lidar))
    # print("b3 vu du LiDAR"+str(p_b3_lidar))

    found_b1, found_b2, found_b3 = None, None, None
    min_d_cluster_beacon1 = 3000
    min_d_cluster_beacon2 = 3000
    min_d_cluster_beacon3 = 3000

    threshold_closest_beacon = 500

    for cluster in clusters:
        mean = cluster.get_mean()
        if mean is not None:
            d_cluster_beacon1 = dr.distance_array(mean, p_b1_lidar.to_array())
            d_cluster_beacon2 = dr.distance_array(mean, p_b2_lidar.to_array())
            d_cluster_beacon3 = dr.distance_array(mean, p_b3_lidar.to_array())

            if d_cluster_beacon1 < min_d_cluster_beacon1 and d_cluster_beacon1 < threshold_closest_beacon:
                min_d_cluster_beacon1 = d_cluster_beacon1
                found_b1 = mean.copy()
                print("mean et b1 et distance trouvée : ", mean, p_b1_lidar, min_d_cluster_beacon1)
            if d_cluster_beacon2 < min_d_cluster_beacon2 and d_cluster_beacon2 < threshold_closest_beacon:
                min_d_cluster_beacon1 = d_cluster_beacon2
                found_b2 = mean.copy()
                print("mean et b2 et distance trouvée : ", mean, p_b2_lidar, min_d_cluster_beacon2)
            if d_cluster_beacon3 < min_d_cluster_beacon3 and d_cluster_beacon3 < threshold_closest_beacon:
                min_d_cluster_beacon1 = d_cluster_beacon3
                found_b3 = mean.copy()
                print("mean et b3 et distance trouvée : ", mean, p_b3_lidar, min_d_cluster_beacon3)

    return [found_b1, found_b2, found_b3]


def find_beacons_with_odometry(clusters: List[Cluster], odometry_state, own_colour: TeamColor, logger_name):

    """
    Function which uses raw estimation of encoders for robot's position to find a priori positions of beacons.

    :param clusters:
    :param odometry_state:
    :param own_colour:
    :return:
    """

    logger = logging.getLogger(logger_name)

    odometry_position = geom.Point(odometry_state[0], odometry_state[1])
    odometry_orientation = odometry_state[2]
    b1, b2, b3 = define_point_beacons(own_colour)

    logger.debug("position balise 1 table : "+str(b1))
    logger.debug("position balise 2 table : "+str(b2))
    logger.debug("position balise 3 table : "+str(b3))

    p_b1_lidar = geom.from_theoretical_table_to_lidar(b1, odometry_position, odometry_orientation)
    p_b2_lidar = geom.from_theoretical_table_to_lidar(b2, odometry_position, odometry_orientation)
    p_b3_lidar = geom.from_theoretical_table_to_lidar(b3, odometry_position, odometry_orientation)

    logger.debug("position balise 1 lidar : " + str(p_b1_lidar))
    logger.debug("position balise 2 lidar : " + str(p_b2_lidar))
    logger.debug("position balise 3 lidar : " + str(p_b3_lidar))

    # print("b1 vu du LiDAR"+str(p_b1_lidar))
    # print("b2 vu du LiDAR"+str(p_b2_lidar))
    # print("b3 vu du LiDAR"+str(p_b3_lidar))

    found_b1, found_b2, found_b3 = None, None, None

    for cluster in clusters:
        mean = cluster.get_mean()
        if mean is not None:
            d1 = dr.distance_array(mean, p_b1_lidar.to_array())
            d2 = dr.distance_array(mean, p_b2_lidar.to_array())
            d3 = dr.distance_array(mean, p_b3_lidar.to_array())

            if d1 < 200:
                found_b1 = mean.copy()
                print("mean et b1 : ", mean, p_b1_lidar)
            if d2 < 200:
                found_b2 = mean.copy()
                print("mean et b2 : ", mean, p_b2_lidar)
            if d3 < 200:
                found_b3 = mean.copy()
                print("mean et b3 : ", mean, p_b3_lidar)

    return [found_b1, found_b2, found_b3]


def find_beacons(clusters: List[Cluster]) -> List[Beacon]:
    """
    
    :param clusters: 
    :return: 
    """""
    fix_beacons = []
    for clusters in clusters:
        beacon = clusters.is_a_fix_beacon()
        if beacon:
            fix_beacons.append(beacon)
    return fix_beacons


def print_beacons(beacons: List[Beacon]):
    for b in beacons:
        if b is not None:
            print("Beacon")
            print("* center: ", b.center)
            print("* index: ", b.index)
            print("* x", b.x_center)
            print("* y", b.y_center)
        else:
            print("pas de mesure pour lui")


def find_relative_point_beacons(beacons: List[geom.Point],
                                robot_position: geom.Point, robot_orientation: float):
    """
    >>> beacons = list(define_point_beacons(TeamColor.orange))
    >>> find_relative_point_beacons(beacons, geom.Point(), 0)
    :param beacons:
    :param robot_position:
    :param robot_orientation:
    :return:
    """
    pass


def compute_own_state(beacons: List[np.ndarray], own_colour: TeamColor, logger_name) \
        -> Tuple[Union[geom.Point, None], Union[float, None]]:
    """
    The ultimate function which computes the position of the robot with the LiDAR!

    :param beacons: clusters which are measures of beacons
    :param own_colour: colour defined at the beginning of the match
    :return:
    """

    logger = logging.getLogger(logger_name)
    # positions of beacons in the table basis
    b1, b2, b3 = define_point_beacons(own_colour)

    if beacons[0] is not None and beacons[2] is not None:
        beacon1, beacon3 = beacons[0], beacons[2]
        logger.debug("balises 1 et 3 mesurées : "+str(beacon1)+" "+str(beacon3))

        p_beacon1 = geom.Point.from_array(beacon1)
        p_beacon3 = geom.Point.from_array(beacon3)

        # region computes robot position
        d13 = 1900  # dr.distance_array(beacon1, beacon3)
        d1 = np.sqrt(beacon1 @ beacon1.T) + FIX_BEACON_RADIUS
        d3 = np.sqrt(beacon3 @ beacon3.T) + FIX_BEACON_RADIUS
        logger.debug("d1 d3 d13 : " + str(d1) + ' ' + str(d3) + ' ' + str(d13))

        angle1 = np.arccos((d1 ** 2 + d13 ** 2 - d3 ** 2) / (2 * d1 * d13))
        angle3 = np.arccos((d3 ** 2 + d13 ** 2 - d1 ** 2) / (2 * d3 * d13))

        # logger.debug("angle alpha 1 "+str(np.rad2deg(angle1)))
        # logger.debug("angle alpha 3 "+str(np.rad2deg(angle3)))
        # logger.debug("angle alpha 1 rad " + str(angle1))
        # logger.debug("angle alpha 3 rad " + str(angle3))

        # theta_r = np.pi/2 - angle3 +

        if own_colour == TeamColor.purple:
            # robot_x = b1.x - np.sin(angle1)*d1
            # robot_y = b1.y + np.cos(angle1)*d1
            #
            # print("From b1", geom.Point(robot_x, robot_y))

            logger.debug("b1 : x et y" + str(b1.x) + " " + str(b1.y))
            logger.debug("b3 : x et y" + str(b3.x) + " " + str(b3.y))

            robot_x = b1.x - np.sin(angle1) * d1
            robot_y = b1.y - np.cos(angle1) * d1

            robot_position = geom.Point(robot_x, robot_y)
            logger.debug("From b1 " + str(robot_position))

            # robot_x = b1.x - np.sin(angle3) * d3
            # robot_y = b1.y - np.cos(angle3) * d3
            #
            # robot_position = geom.Point(robot_x, robot_y)
            # logger.debug("From b3 " + str(robot_position))

        elif own_colour == TeamColor.orange:
            robot_x = b1.x + np.sin(angle1) * d1
            robot_y = b1.y - np.cos(angle1) * d1
            #
            # print("From b1", geom.Point(robot_x, robot_y))

            # robot_x = b3.x + np.sin(angle3) * d3
            # robot_y = b3.y - np.cos(angle3) * d3

            robot_position = geom.Point(robot_x, robot_y)
            logger.debug("From b1 " + str(robot_position))
        else:
            logger.debug("La couleur donnée n'est pas bonne")
            return None, None

        # region computes robot orientation
        v_table_beacons = geom.Vector()
        v_table_beacons.set_by_points(b1, b3)

        # table_beacons_angle = np.pi / 2

        v_lidar_beacons = geom.Vector()
        v_lidar_beacons.set_by_points(p_beacon1 - robot_position, p_beacon3 - robot_position)

        lidar_beacons_angle = v_lidar_beacons.compute_basis_angle()

        # logger.debug("angle table beacons angle "+str(np.rad2deg(table_beacons_angle)))
        # logger.debug("angle table beacons angle rad "+str(table_beacons_angle))
        # logger.debug("angle lidar beacons angle "+str(np.rad2deg(lidar_beacons_angle)))
        # logger.debug("angle lidar beacons angle rad"+str(lidar_beacons_angle))

        # robot_orientation = (table_beacons_angle - lidar_beacons_angle - np.pi/2) % 2*np.pi
        robot_orientation = lidar_beacons_angle % (2*np.pi)
        logger.debug("Orientation du robot : "+str(robot_orientation))
        # endregion
        return robot_position, robot_orientation
    else:
        if beacons[0] is None:
            logger.debug("La balise 1 n'est pas détectée")
        if beacons[2] is None:
            logger.debug("La balise 3 n'est pas détectée")

        return None, None


def find_own_position(beacons: List[Beacon], own_colour_team: TeamColor):
    """

    :param beacons: list of the 3 beacons.
    :param own_colour_team:
    :return: [first space coordinate of the robot, second space coordinate of the robot, radius of the robot,
    index of the robot, timestamp]
    """

    b1, b2, b3 = define_point_beacons(own_colour_team)

    for beacon in beacons:
        # TODO improve it, because I need to get polar coordinates to do it correctly
        if own_colour_team.value == TeamColor.orange.value:
            x = beacons_orange[beacon.index][0] - beacon.cluster
            y = beacons_orange[beacon.index][1]
            print(x, y)
        elif own_colour_team.value == TeamColor.purple.value:
            x = beacons_purple[beacon.index][0]
            y = beacons_purple[beacon.index][1]
            print(x, y)

    beacon_1 = Beacon()
    beacon_1.set_by_upper_left_and_lower_right(beacons_purple[0][0], beacons_purple[0][1])

    beacon_2 = Beacon()
    beacon_2.set_by_upper_left_and_lower_right(beacons_purple[1][0], beacons_purple[1][1])

    beacon_3 = Beacon()
    beacon_3.set_by_upper_left_and_lower_right(beacons_purple[2][0], beacons_purple[2][1])
    return None


def change_basis(rp: geom.Point, ori: float, measures: List):
    """

    :param rp: robot position
    :param ori: robot orietation
    :param measures: list of angles and distances
    :return:
    """
    # measures = outr.one_turn_to_cartesian_points(measures)
    new_measures = []
    for measure in measures:
        p = geom.Point(measure[0], measure[1])
        p.rotate(-ori)
        new_measure = p + rp
        new_measures.append([new_measure.x, new_measure.y])
    return new_measures
