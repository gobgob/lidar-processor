#! /usr/bin/python3

"""
Main script to launch before the match

"""

import time
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

            elif t_hl.get_team_colour() == TeamColor.yellow:
                start_enemy_positions = eloc.find_robot_in_orange_zone(one_turn_clusters)
                computed_opponent_robot_position = True

            # retrieves and filters measures
            one_turn_points = dacl.filter_points(t_lidar.get_measures(), 50)
            cartesian_one_turn_points = outr.one_turn_to_cartesian_points(one_turn_points)
            one_turn_clusters = clus.clusterize(cartesian_one_turn_points)

            # find beacons position
            beacon_positions = sloc.find_beacons(one_turn_clusters)
            # find own position
            self_position = sloc.find_own_position(beacon_positions)
            t_ll.send_self_position(self_position)

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

        # region # estimations of positions
        beacons = sloc.find_beacons(clusters)
        own_position = sloc.find_own_position(beacons)
        robots = eloc.find_robots(clusters)
        # endregion

        previous_clusters.put(clusters.copy())
        previous_beacons.put(beacons.copy())
        previous_opponent_robots.put(robots.copy())
        previous_self_positions.put(own_position.copy())

        time.sleep(1)
    # endregion

    # region # end of match
    t_lidar.close_connection()
    time.sleep(3)
    # sys.exit(0)
    # endregion


if __name__ == "__main__":
    main()
