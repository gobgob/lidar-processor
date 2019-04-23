"""

"""

import numpy as np

import src.main.main as mm
import src.main.clustering as clus
import src.main.output_rendering as outr
from src.scripts.retrieve_realistic_measures import get_realistic_data

__author__ = "Clément Besnier"


def main_clustering():
    one_turn_measure = get_realistic_data()[0]
    one_turn_measure = outr.keep_good_measures(one_turn_measure, 30)
    one_turn_measure = mm.remove_too_far_or_too_close(one_turn_measure)
    cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
    cartesian_one_turn_measure = [np.array(measure) for measure in cartesian_one_turn_measure]
    clusters = clus.clusterize(cartesian_one_turn_measure)
    return clusters


if __name__ == "__main__":
    main_clustering()
