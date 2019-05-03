#! /usr/bin/python3

"""


"""

import time

from main.constants import *
import main.output_rendering as outr
import main.data_retrieval as datr
import main.data_cleansing as dacl
import main.communication as comm
import main.clustering as clus
import main.tracking as trac
import main.self_locator as sloc
import main.enemy_locator as eloc

__author__ = "Clément Besnier"


def main():

    t_lidar = datr.LidarThread()
    t_lidar.start()

    t_ll = datr.EncoderThread()
    t_ll.start()

    t_hl = comm.HLThread()
    t_hl.start()

    # TODO preparation before the match
    while not t_hl.has_match_begun():
        # team colour
        if t_hl.get_team_colour() is not None:
            if t_hl.get_team_colour() == TeamColor.purple:
                start_position = [1, 2]
            elif t_hl.get_team_colour() == TeamColor.yellow:
                start_position = [1, 3]
        # TODO measure and compute the positions of the adverse robots
        # TODO send the position
            x, y, r, i = 0, 0, 100, 1

            t_hl.send_robot_position(x, y, r, i, int(time.time()))

    previous_clusters = []
    one_turn_measure = t_lidar.get_measures()
    one_turn_measure = dacl.keep_good_measures(one_turn_measure, 30)
    one_turn_measure = dacl.remove_too_far_or_too_close(one_turn_measure)
    cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
    clusters = clus.clusterize(cartesian_one_turn_measure)
    beacons, robots = trac.track_clusters(previous_clusters, clusters)

    # TODO the match has just begun
    while not t_hl.has_match_stopped():
        one_turn_measure = t_lidar.get_measures()
        one_turn_measure = dacl.keep_good_measures(one_turn_measure, 30)
        one_turn_measure = dacl.remove_too_far_or_too_close(one_turn_measure)
        cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
        clusters = clus.clusterize(cartesian_one_turn_measure)
        print(clusters)

        # TODO determine the position of beacons and adverse robot just with the last measure
        beacons = sloc.find_beacons(clusters)
        robots = eloc.find_robots(clusters)
        previous_clusters = clusters.copy()
        time.sleep(1)
    t_lidar.close_connection()
    time.sleep(3)
    # sys.exit(0)


if __name__ == "__main__":
    main()