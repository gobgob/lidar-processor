"""

"""

import main.main as mm
import main.clustering as clus
import src.main.output_rendering as outr
from scripts.retrieve_realistic_measures import get_realistic_data

__author__ = "Clément Besnier"


def test_clustering():
    one_turn_measure = get_realistic_data()
    one_turn_measure = outr.keep_good_measures(one_turn_measure, 30)
    one_turn_measure = mm.remove_too_far_or_too_close(one_turn_measure)
    cartesian_one_turn_measure = outr.one_turn_to_cartesian_points(one_turn_measure)
    clusters = clus.clusterize(cartesian_one_turn_measure)
    return clusters

