#!/home/pi/lidar-processor/lidar_env/bin/python

"""
Main script to launch before the match.

The aim is to follow opponent robots' positions and to calibrate regularly our position thanks to immobile beacons.

/home/pi/lidar-processor/lidar_env/bin/python /home/pi/lidar-processor/src/main_script.py

"""

import sys
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
import lidarproc.main.self_locator as sloc
import lidarproc.main.enemy_locator as eloc
import numpy as np


__author__ = "Clément Besnier"

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

log_files = os.listdir(last_log_folder)
# for filename in log_files:
#     shutil.move(os.path.join(last_log_folder, filename),
#                 os.path.join(os.getenv("HOME"), "lidar-processor", "logs", "history"))

log_filename = "lidar_logs"  # + datetime.datetime.today().ctime().replace(":", "")
if os.path.exists(os.path.join(HOME, "lidar-processor", "logs", "last", log_filename + ".txt")):
    os.remove(os.path.join(HOME, "lidar-processor", "logs", "last", log_filename + ".txt"))
# log_filename = ""
if log_filename:
    logging.basicConfig(filename=os.path.join(HOME, "lidar-processor", "logs", "last",
                                              log_filename + ".txt"), level=5, filemode='w')
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

    # endregion

    # region # variable initialisation
    own_colour_team = None
    # endregion

    # region # before the match
    logger.info("Premières mesures")
    one_turn_points = dacl.filter_points(t_lidar.get_measures(), QUALITY_THRESHOLD)
    cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_points)
    one_turn_clusters, means, closest_points = clus.clusterize(cartesian_one_turn_measure)
    one_turn_clusters = clus.Cluster.to_clusters(one_turn_clusters, closest_points)

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
                own_colour_team = TeamColor.purple
                logger.info("On est violet")

            elif t_hl.get_team_colour().value == TeamColor.orange.value:
                own_colour_team = TeamColor.orange
                logger.info("On est orange")
            if own_colour_team:
                if t_hl.expecting_shift:
                    last_states = []

                    for i in range(n_measures_for_median):
                        t1 = time.time()

                        # region # measures
                        one_turn_points = dacl.filter_points(t_lidar.get_measures(), THRESHOLD_QUALITY)
                        odo_measure = t_ll.get_measures()[:3]
                        # endregion

                        # region lidar data processing
                        cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_points)
                        clusters, means, closest_points = clus.clusterize(cartesian_one_turn_measure)
                        one_turn_clusters = clus.Cluster.to_clusters(clusters, closest_points)
                        # endregion

                        t2 = time.time()
                        logger.debug("temps entre la mesure et le regroupement " + str(t2 - t1))

                        # region # retrieves position from encoders

                        logger.debug("raw measure of odometry " + str(odo_measure))
                        proprioceptive_position = datr.from_encoder_position_to_lidar_measure(*odo_measure)
                        logger.debug("odometry position from lidar " + str(proprioceptive_position))
                        # endregion
                        t3 = time.time()
                        logger.debug("Durée de récupération de la mesure des codeuses " + str(t3 - t2))

                        # region # estimations of positions

                        beacons = sloc.find_beacons_with_odometry(one_turn_clusters, proprioceptive_position,
                                                                  own_colour_team, log_filename)
                        t4 = time.time()
                        logger.debug(
                            "durée d'estimation de la position des balises à partir de l'odométrie " + str(t4 - t3))
                        estimated_position, estimated_orientation = sloc.compute_own_state(beacons, own_colour_team,
                                                                                           log_filename)
                        t5 = time.time()
                        logger.debug("Durée d'estimation de l'état du robot grâce au LiDAR" + str(t5 - t4))
                        if estimated_position is None or estimated_orientation is None:
                            logger.warning("On n'a pas pu trouver les balises nécessaires à la localisation du robot.")
                        else:
                            logger.info("Notre position corrigée : " + str(estimated_position))
                            logger.info("Notre orientation corrigée : " + str(estimated_orientation))
                            hl_own_state = np.array([estimated_position.x, estimated_position.y, estimated_orientation])
                            logger.debug("lidar : " + str(hl_own_state))
                            logger.debug("odo : " + str(proprioceptive_position))
                            logger.debug("décalage : " + str(hl_own_state - proprioceptive_position))
                            last_states.append(hl_own_state - proprioceptive_position)
                        t6 = time.time()
                        logger.debug("temps entre la mesure lidar et le retour " + str(t6 - t1))
                        time.sleep(0.1)
                    if len(last_states) == 3:
                        last_states = sloc.crop_angles(last_states)
                        median_shifts = sloc.choose_median_state(last_states)
                        t_hl.set_recalibration(median_shifts)
                        t_hl.send_shift()

                    else:
                        logger.debug('Aucun recalage possible.')
                        t_hl.set_recalibration(None)
                        t_hl.send_shift()

        time.sleep(0.05)
    # endregion
    logger.info("Le match vient de commencer")

    # region # match
    while not t_hl.has_match_stopped():
        if own_colour_team is None:
            logger.debug('On n\'a pas reçu de couleur donc le script lidar ne fait rien')
            time.sleep(1)
        else:
            if t_hl.expecting_shift:
                last_states = []

                for i in range(n_measures_for_median):
                    t1 = time.time()

                    # region # measures
                    one_turn_points = dacl.filter_points(t_lidar.get_measures(), THRESHOLD_QUALITY)
                    odo_measure = t_ll.get_measures()[:3]
                    # endregion

                    # region lidar data processing
                    cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_points)
                    clusters, means, closest_points = clus.clusterize(cartesian_one_turn_measure)
                    one_turn_clusters = clus.Cluster.to_clusters(clusters, closest_points)
                    # endregion

                    t2 = time.time()
                    logger.debug("temps entre la mesure et le regroupement "+str(t2 - t1))

                    # region # retrieves position from encoders

                    logger.debug("raw measure of odometry "+str(odo_measure))
                    proprioceptive_position = datr.from_encoder_position_to_lidar_measure(*odo_measure)
                    logger.debug("odometry position from lidar "+str(proprioceptive_position))
                    # endregion
                    t3 = time.time()
                    logger.debug("Durée de récupération de la mesure des codeuses "+str(t3 - t2))

                    # region # enemy position
                    # for enemy_position in eloc.find_robots(one_turn_clusters):
                    #     t_hl.send_robot_position(*enemy_position)
                    # endregion

                    # region # estimations of positions

                    beacons = sloc.find_beacons_with_odometry(one_turn_clusters, proprioceptive_position,
                                                              own_colour_team, log_filename)
                    t4 = time.time()
                    logger.debug("durée d'estimation de la position des balises à partir de l'odométrie "+str(t4-t3))
                    estimated_position, estimated_orientation = sloc.compute_own_state(beacons, own_colour_team,
                                                                                       log_filename)
                    t5 = time.time()
                    logger.debug("Durée d'estimation de l'état du robot grâce au LiDAR"+str(t5-t4))
                    if estimated_position is None or estimated_orientation is None:
                        logger.warning("On n'a pas pu trouver les balises nécessaires à la localisation du robot.")
                    else:
                        logger.info("Notre position corrigée : "+str(estimated_position))
                        logger.info("Notre orientation corrigée : "+str(estimated_orientation))
                        hl_own_state = np.array([estimated_position.x, estimated_position.y, estimated_orientation])
                        logger.debug("lidar : "+str(hl_own_state))
                        logger.debug("odo : "+str(proprioceptive_position))
                        logger.debug("décalage : "+str(hl_own_state - proprioceptive_position))
                        last_states.append(hl_own_state - proprioceptive_position)
                    t6 = time.time()
                    logger.debug("temps entre la mesure lidar et le retour "+str(t6-t1))
                    time.sleep(0.1)
                if len(last_states) > 0:
                    last_states = sloc.crop_angles(last_states)
                    median_shifts = sloc.choose_median_state(last_states)
                    t_hl.set_recalibration(median_shifts)
                    t_hl.send_shift()

                else:
                    logger.debug('Aucun recalage possible.')
                    t_hl.set_recalibration(None)
                    t_hl.send_shift()

                # endregion

                # endregion

        time.sleep(0.05)
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
