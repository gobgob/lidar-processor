#!/usr/bin/python3

"""
Script used when we only base on encoders to tell our absolute position.
It can nonetheless return the absolute position of the opponent robots.

"""

import os
import shutil
import time
import datetime
import queue

from lidarproc.main.constants import *
from lidarproc import HOME
import lidarproc.main.output_rendering as outr
import lidarproc.main.data_retrieval as datr
import lidarproc.main.data_cleansing as dacl
import lidarproc.main.communication as comm
import lidarproc.main.clustering as clus
# import lidarproc.main.tracking as trac
import lidarproc.main.enemy_locator as eloc


__author__ = ["Clément Besnier", ]


# region logs
log_folder = os.path.join(HOME, "lidar-processor", "logs")
last_log_folder = os.path.join(log_folder, "last")
history_log_folder = os.path.join(log_folder, "history")

if not os.path.exists(log_folder):
    os.mkdir(log_folder)

if not os.path.exists(last_log_folder):
    os.mkdir(last_log_folder)

if not os.path.exists(history_log_folder):
    os.mkdir(history_log_folder)

if len(os.listdir(last_log_folder)) != 0:
    shutil.move(last_log_folder+"/*", os.path.join(HOME, "lidar-processor", "logs", "hitory"))

# log_filename = "lidar_logs" + datetime.datetime.today().ctime().replace(":", "")
log_filename = ""
if log_filename:
    logging.basicConfig(filename=os.path.join(HOME, "lidar-processor", "logs", "last",
                                              log_filename + ".txt"), level=15)
else:
    logging.basicConfig(stream=sys.stdout, level=5)
# endregion


def main():
    logger = logging.getLogger(log_filename)
    logger.info("On a lancé le script de match")

    # region # thread initialisation
    t_lidar = datr.LidarThread(log_filename)
    t_lidar.start()

    t_ll = datr.EncoderThread(log_filename)
    t_ll.start()

    t_hl = comm.HLThread(log_filename)
    t_hl.start()

    logger.info("Fils de communication lancés")

    time.sleep(3)
    # endregion

    # region # variable initialisation
    start_enemy_positions = []
    own_colour_team = None
    computed_opponent_robot_position = False
    previous_beacons = []
    previous_self_positions = []
    previous_clusters = []
    previous_opponent_robots = []
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
                logger.info("On est violet")

            elif t_hl.get_team_colour() == TeamColor.orange:
                start_enemy_positions = eloc.find_robot_in_orange_zone(one_turn_clusters)
                computed_opponent_robot_position = True
                own_colour_team = TeamColor.orange
                logger.info("On est orange")

            # retrieves and filters measures
            one_turn_points = dacl.filter_points(t_lidar.get_measures(), 50)
            cartesian_one_turn_points = outr.one_turn_to_cartesian_points(one_turn_points)
            one_turn_clusters = clus.clusterize(cartesian_one_turn_points)

            # send the positions of the opponent robots
            if computed_opponent_robot_position:
                for enemy_position in start_enemy_positions:
                    t_hl.send_robot_position(*enemy_position)
    # endregion

    logger.info("Le match vient de commencer")

    # region # match
    while not t_hl.has_match_stopped():
        # region # measures
        one_turn_points = dacl.filter_points(t_lidar.get_measures(), THRESHOLD_QUALITY)
        cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_points)
        clusters = clus.clusterize(cartesian_one_turn_measure)
        # endregion

        # region # retrieves position from encoders
        proprioceptive_position = datr.from_encoder_position_to_lidar_measure(*t_ll.get_measures())
        # endregion

        # region # estimations of positions
        robots = eloc.find_robots(clusters)
        # endregion

        # region history management
        previous_clusters.append(clusters.copy())
        if len(previous_clusters) > 3:
            previous_clusters.pop(0)

        previous_opponent_robots.append(robots.copy())
        if len(previous_opponent_robots) > 3:
            previous_opponent_robots.pop(0)
        # endregion

        time.sleep(1)
    # endregion
    logger.info("Le match est fini")
    # region # end of match

    t_lidar.close_connection()
    t_hl.close_connection()
    t_ll.close_connection()
    time.sleep(3)
    logger.info("On a fermé les connexions")
    # sys.exit(0)
    # endregion


if __name__ == "__main__":
    main()
