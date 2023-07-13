import itertools
import sys

import numpy
import pandas

from multixrank import logger_setup
from multixrank import logger_setup
from multixrank.MultiplexAll import MultiplexAll


class Seed:

    """Handle seeds"""

    def __init__(self, path: str, multiplexall: MultiplexAll):
        """Handles seeds

        Args:
            path (str): seed path
            node (list): List of nodes in multiplexes

        Returns:
            none

        """

        # self._seed_df = pandas.read_csv(path, sep="\t", header=None, names=["seeds"], dtype=str)
        self._path = path
        self._multiplexall_obj = multiplexall

        self._seed_list = list()
        self._multiplex_seed_list2d = list()

    @property
    def seed_list(self) -> list:
        """Get list with all nodes"""

        if not self._seed_list:

            df = pandas.read_csv(self._path, sep="\t", header=None, names=["seeds"], dtype=str)
            seed_list = sorted(set(df["seeds"].to_list()))

            ###################################################################
            #
            # Check seed list
            #
            ###################################################################

            if len(seed_list) <= 0:  # no seeds
                logger_setup.logger.error(
                    "These seed nodes were not found in the network: {}".format(
                        self._seed_list))
                sys.exit(1)

            seeds_not_in_multiplex_set = set(seed_list) - set(self._multiplexall_obj.nodes)
            if len(seeds_not_in_multiplex_set) > 0:  # seeds not in multiplex
                logger_setup.logger.error(
                    "These seed nodes were not found in the network: {}".format(
                        seeds_not_in_multiplex_set))
                sys.exit(1)

            self._seed_list = seed_list

        return self._seed_list

    @property
    def multiplex_seed_list2d(self) -> list:
        """Returns valid seed label list"""

        if not self._multiplex_seed_list2d:

            for multiplex in self._multiplexall_obj.multiplex_tuple:

                self._multiplex_seed_list2d.append(list(set(self.seed_list) & set(multiplex.nodes)))

        return self._multiplex_seed_list2d

    # 1.3.1 :
    def get_seed_scores(self, transition) -> (numpy.array, pandas.DataFrame):
        """

        Function that determine the initial probability distribution thanks to seeds and normalization.
        For the seed_rank() and homogeneous_seed_rank() functions.

        Returns :
                seed_score (pandas.core.frame.DataFrame) : A Dataframe with value of probaility for the seeds in each layer
                The value of probability is zero outhere from seeds.

        """

        multiplexall_layer_count_list = [len(m.layer_tuple) for m in self._multiplexall_obj.multiplex_tuple]
        multiplexall_node_count_list = [len(m.nodes) for m in self._multiplexall_obj.multiplex_tuple]
        multiplexall_node_list2d = [multiplexone_obj.nodes for multiplexone_obj in self._multiplexall_obj.multiplex_tuple]

        multiplexall_layer_key_list = []
        multiplexall_layer_key_list2d = []
        for multiplex in self._multiplexall_obj.multiplex_tuple:
            multiplexall_layer_key_list2d.append([layer_obj.key for layer_obj in multiplex.layer_tuple])
            for layer in multiplex.layer_tuple:
                multiplexall_layer_key_list.append(layer.key)

        multiplexall_layer_key_lst = [layer.key for multiplex in self._multiplexall_obj.multiplex_tuple for layer in multiplex.layer_tuple]
        seed_score_df = pandas.DataFrame(0, index=self.seed_list, columns=multiplexall_layer_key_lst)
        prox_vector = numpy.zeros((numpy.shape(transition)[0], 1))
        for seed_label in seed_score_df.index:  # loop through seeds
            for multiplex_idx, multiplex in enumerate(self._multiplexall_obj.multiplex_tuple):
                if seed_label in multiplex.nodes:
                    for layer_idx, layer in enumerate(multiplex.layer_tuple):
                        seed_score_df.loc[seed_label, layer.key] = multiplex.eta * layer.tau / len(self.multiplex_seed_list2d[multiplex_idx])
                        start = sum(numpy.array(multiplexall_node_count_list[:multiplex_idx]) * numpy.array(multiplexall_layer_count_list[:multiplex_idx])) + (multiplexall_node_count_list[multiplex_idx] * layer_idx)
                        pos = multiplexall_node_list2d[multiplex_idx].index(seed_label) + start
                        prox_vector[pos] = seed_score_df.loc[seed_label, layer.key]
        return prox_vector, seed_score_df
