#! /usr/bin/python3

"""
Main script to launch before the match.

The aim is to follow opponent robots' positions and to calibrate regularly its owb position thanks to immobile beacons.

"""

import time
import datetime
import queue

from main.constants import *
import main.output_rendering as outr
import main.data_retrieval as datr
import main.data_cleansing as dacl
import main.communication as comm
import main.clustering as clus
# import main.tracking as trac
import main.self_locator as sloc
import main.enemy_locator as eloc

__author__ = "Clément Besnier"

logging.basicConfig(filename="lidar_logs"+datetime.datetime.today().ctime().replace(":", "")+".txt")


def main():
    # region # thread initialisation
    t_lidar = datr.LidarThread()
    t_lidar.start()

    t_ll = datr.EncoderThread()
    t_ll.start()

    t_hl = comm.HLThread()
    t_hl.start()

    time.sleep(3)
    # endregion

    # region # variable initialisation
    start_enemy_positions = []
    own_colour_team = None
    computed_opponent_robot_position = False
    previous_clusters = queue.Queue(3)
    previous_beacons = queue.Queue(3)
    previous_opponent_robots = queue.Queue(3)
    previous_self_positions = queue.Queue(3)
    # endregion

    # region # before the match
    one_turn_points = dacl.filter_points(t_lidar.get_measures(), 50)
    one_turn_clusters = clus.clusterize(one_turn_points)

    while not t_hl.has_match_begun():
        # team colour
        if t_hl.get_team_colour() is not None:
            # computes the position
            if t_hl.get_team_colour() == TeamColor.purple:
                start_enemy_positions = eloc.find_robots_in_purple_zone(one_turn_clusters)
                computed_opponent_robot_position = True
                own_colour_team = TeamColor.purple

            elif t_hl.get_team_colour() == TeamColor.orange:
                start_enemy_positions = eloc.find_robot_in_orange_zone(one_turn_clusters)
                computed_opponent_robot_position = True
                own_colour_team = TeamColor.orange

            # retrieves and filters measures
            one_turn_points = dacl.filter_points(t_lidar.get_measures(), 50)
            cartesian_one_turn_points = outr.one_turn_to_cartesian_points(one_turn_points)
            one_turn_clusters = clus.clusterize(cartesian_one_turn_points)

            # find beacons position
            beacon_positions = sloc.find_beacons(one_turn_clusters)
            # find own position
            self_position = sloc.find_own_position(beacon_positions, own_colour_team)
            t_ll.send_position_shift(self_position)

            # send the positions of the opponent robots
            if computed_opponent_robot_position:
                for enemy_position in start_enemy_positions:
                    t_hl.send_robot_position(*enemy_position)
    # endregion

    # region # match
    while not t_hl.has_match_stopped():
        # region # measures
        one_turn_points = dacl.filter_points(t_lidar.get_measures(), THRESHOLD_QUALITY)
        cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_points)
        clusters = clus.clusterize(cartesian_one_turn_measure)
        previous_clusters.put(clusters)
        # endregion

        # region # retrieves position from encoders
        proprioceptive_position = datr.from_encoder_position_to_lidar_measure(*t_ll.get_measures())
        # endregion

        # region # estimations of positions
        beacons = sloc.find_beacons(clusters)
        own_position = sloc.find_own_position(beacons, own_colour_team)
        robots = eloc.find_robots(clusters)
        # endregion

        previous_clusters.put(clusters.copy())
        previous_beacons.put(beacons.copy())
        previous_opponent_robots.put(robots.copy())
        previous_self_positions.put(own_position.copy())

        if datr.are_encoder_measures_and_lidar_measures_different(proprioceptive_position, own_position):
            t_ll.send_position_shift(proprioceptive_position - own_position)  # convention
        time.sleep(1)
    # endregion

    # region # end of match
    t_lidar.close_connection()
    time.sleep(3)
    # sys.exit(0)
    # endregion


if __name__ == "__main__":
    main()
