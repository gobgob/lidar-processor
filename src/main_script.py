#! /usr/bin/python3

"""
Main script to launch before the match.

The aim is to follow opponent robots' positions and to calibrate regularly its owb position thanks to immobile beacons.

/home/pi/lidar-processor/lidar_env/bin/python /home/pi/lidar-processor/src/main_script.py

"""
import shutil
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
import numpy as np
__author__ = "Clément Besnier"

# region logs
log_folder = os.path.join(os.getenv("HOME"), "lidar-processor", "logs")
last_log_folder = os.path.join(log_folder, "last")
history_log_folder = os.path.join(log_folder, "history")

if not os.path.exists(log_folder):
    os.mkdir(log_folder)

if not os.path.exists(last_log_folder):

    os.mkdir(last_log_folder)

if not os.path.exists(history_log_folder):
    os.mkdir(history_log_folder)

log_files = os.listdir(last_log_folder)
for filename in log_files:
    shutil.move(os.path.join(last_log_folder, filename),
                os.path.join(os.getenv("HOME"), "lidar-processor", "logs", "history"))

log_filename = "lidar_logs" + datetime.datetime.today().ctime().replace(":", "")
# log_filename = ""
if log_filename:
    logging.basicConfig(filename=os.path.join(os.getenv("HOME"), "lidar-processor", "logs", "last",
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
    # previous_clusters = []
    # previous_beacons = []
    # previous_opponent_robots = []
    # previous_self_positions = []
    # endregion

    # region # before the match
    logger.info("Premières mesures")
    one_turn_points = dacl.filter_points(t_lidar.get_measures(), QUALITY_THRESHOLD)
    cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_points)
    # print(one_turn_points[0])
    one_turn_clusters, means = clus.polar_clusterize(cartesian_one_turn_measure)
    one_turn_clusters = clus.Cluster.to_clusters(one_turn_clusters)

    print("Il y a ", len(one_turn_clusters), "clusters.")

    logger.info("Match a commencé : "+str(t_hl.has_match_begun()))
    logger.info("taille clusters : "+str(len(one_turn_clusters)))

    while not t_hl.has_match_begun():
        # team colour
        if t_hl.get_team_colour():
            logger.info("La couleur : "+t_hl.get_team_colour().name)
        else:
            logger.warning("Pas de couleur")
        if t_hl.get_team_colour() is not None:
            # computes the position
            if t_hl.get_team_colour().value == TeamColor.purple.value:
                start_enemy_positions = eloc.find_robot_in_orange_zone(one_turn_clusters)
                computed_opponent_robot_position = True
                own_colour_team = TeamColor.purple
                logger.info("On est violet")
                # beacons should be at

            elif t_hl.get_team_colour().value == TeamColor.orange.value:
                start_enemy_positions = eloc.find_robots_in_purple_zone(one_turn_clusters)
                computed_opponent_robot_position = True
                own_colour_team = TeamColor.orange
                logger.info("On est orange")
                # beacons should be at

            # retrieves and filters measures
            one_turn_points = dacl.filter_points(t_lidar.get_measures(), QUALITY_THRESHOLD)
            cartesian_one_turn_points = outr.one_turn_to_cartesian_points(one_turn_points)
            one_turn_clusters, means = clus.clusterize(cartesian_one_turn_points)
            one_turn_clusters = clus.Cluster.to_clusters(one_turn_clusters)
            print("Il y a ", len(one_turn_clusters), "clusters.")

            # for mean in means:
            #     logger.info("moyenne cluster : "+str(type(mean))+" "+str(mean))

            # find beacons position
            # beacon_positions = sloc.find_beacons(one_turn_clusters)
            # logger.debug("nombre de balises : "+str(len(beacon_positions)))
            # sloc.print_beacons(beacon_positions)
            # find own position
            # self_position = sloc.find_own_position(beacon_positions, own_colour_team)
            # logger.info(self_position)
            if own_colour_team:
                found_b1, found_b2, found_b3 = sloc.find_starting_beacons(own_colour_team, one_turn_clusters)

            # send the positions of the opponent robots
            if computed_opponent_robot_position:
                for enemy_position in start_enemy_positions:
                    t_hl.send_robot_position(*enemy_position)
        time.sleep(3)
    # endregion
    logger.info("Le match vient de commencer")

    # region # match
    while not t_hl.has_match_stopped():
        # region # measures
        one_turn_points = dacl.filter_points(t_lidar.get_measures(), THRESHOLD_QUALITY)
        cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_points)
        clusters, means = clus.clusterize(cartesian_one_turn_measure)
        one_turn_clusters = clus.Cluster.to_clusters(clusters)
        # endregion

        # region # retrieves position from encoders
        proprioceptive_position = datr.from_encoder_position_to_lidar_measure(*t_ll.get_measures()[:3])
        # print("odometry position", proprioceptive_position)
        # endregion

        # region # estimations of positions
        beacons = sloc.find_beacons_with_odometry(one_turn_clusters, proprioceptive_position, own_colour_team)
        # beacons = sloc.find_beacons(one_turn_clusters)
        # print("Le nombre de balises trouvé : ", len(beacons))
        # print("On affiche la position des balises trouvées", beacons)
        # print("-------------------------")
        own_state = sloc.compute_own_state(beacons, own_colour_team)
        if own_state is None:
            logger.warning("On n'a pas pu trouver les balises nécessaires à la localisation du robot.")

        hl_own_state = np.array([own_state[0], own_state[1], proprioceptive_position[2]])
        t_hl.set_recalibration(proprioceptive_position - hl_own_state)
        # own_position = sloc.find_own_position(beacons, own_colour_team)
        # robots = eloc.find_robots(clusters)
        # print(own_state)
        # endregion

        # region # history management
        # if one_turn_clusters:
        #     previous_clusters.append(one_turn_clusters.copy())
        #     if len(previous_clusters) > 3:
        #         previous_clusters.pop(0)
        #
        # if beacons:
        #     previous_beacons.append(beacons.copy())
        #     if len(previous_beacons) > 3:
        #         previous_beacons.pop(0)

        # previous_opponent_robots.append(robots.copy())
        # if len(previous_opponent_robots) > 3:
        #     previous_opponent_robots.pop(0)
        # if own_state:
        #     previous_self_positions.append(own_state.copy())
        #     if len(previous_self_positions) > 3:
        #         previous_self_positions.pop(0)
        # # endregion
        #
        # if own_state:
        #     if datr.are_encoder_measures_and_lidar_measures_different(proprioceptive_position, own_state):
        #         t_hl.set_recalibration(proprioceptive_position - own_state)  # convention
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
