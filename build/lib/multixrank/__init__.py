__version__ = "0.1"

"""
MultiXrank
========
Universal multilayer Exploration by Random Walk with Restart
See https://multixrank.readthedocs.com for complete documentation.
"""

import numpy
import os
import pandas
import pathlib
import shutil
import sys

from multixrank import constants
from multixrank.BipartiteAll import BipartiteAll
from multixrank.ConfigParser import ConfigParser
from multixrank.Output import Output
from multixrank.PathManager import PathManager
from multixrank.TransitionMatrix import TransitionMatrix
from multixrank.logger_setup import logger


class Multixrank(object):
    """Main class to run the random walk with restart in universal multiplex networks"""


    def __init__(self, config: str, wdir: str):
        """
        Constructs an object for the random walk with restart.

        Args:
            config (str): Path to the configuration file in YML format. Paths will be used relative to the wdir path variable below
            wdir (str): Path to the working directory that will be as starting point to the paths in the config file.
        """

        #######################################################################
        #
        # Read ConfigPath
        #
        #######################################################################

        config_parser_obj = ConfigParser(config=config, wdir=wdir)
        config_parser_obj.parse()

        self.wdir = os.path.join(os.getcwd(), wdir)

        if not os.path.isdir(self.wdir):
            logger_setup.logger.error('This input config_path is NOT a directory: {}'.format(self.wdir))
            sys.exit(1)

        #######################################################################
        #
        # paramater object from config_parser and properties
        #
        #######################################################################
        parameter_obj = config_parser_obj.parameter_obj
        self.r = parameter_obj.r
        self.lamb = parameter_obj.lamb
        logger.debug("Parameter 'lambda' is equal to: {}".format(self.lamb))

        #######################################################################
        #
        # multiplexall object from config_parser and properties
        #
        #######################################################################

        multiplexall_obj = config_parser_obj.multiplexall_obj
        self.multiplexall_obj = multiplexall_obj

        #######################################################################
        #
        # bipartite object from config_parser and properties
        #
        #######################################################################

        self.bipartiteall_obj = config_parser_obj.bipartitelist_obj

        self.multiplex_layer_count_list = [len(multiplexone_obj.layer_tuple) for multiplexone_obj in multiplexall_obj.multiplex_tuple]

        # self.multiplexall_node_2dlist = config_parser_obj.multiplexall_node_list2d
        self.multiplexall_node_list2d = [multiplexone_obj.nodes for multiplexone_obj in multiplexall_obj.multiplex_tuple]

        # self. N nb of nodes in each multiplex
        # self.N = list()
        self.multiplexall_node_count_list = [len(x) for x in self.multiplexall_node_list2d]

        #######################################################################
        #
        # seed object from config_parser and properties
        #
        #######################################################################

        self.seed_obj = config_parser_obj.seed_obj

    # 1.3.3 :
    def __random_walk_restart(self, prox_vector, transition_matrixcoo, r):
        """

        Function that realize the RWR and give back the steady probability distribution for
        each multiplex in a dataframe.

        self.results (list) : A list of ndarray. Each ndarray correspond to the probability distribution of the
            nodes of the multiplex.

        """
        rwr_result_lst = list()
        threshold = 1e-10
        residue = 1
        itera = 1
        prox_vector_norm = prox_vector / (sum(prox_vector))
        restart_vector = prox_vector_norm
        while residue >= threshold:
            old_prox_vector = prox_vector_norm
            prox_vector_norm = (1 - r) * (transition_matrixcoo.dot(prox_vector_norm)) + r * restart_vector
            residue = numpy.sqrt(sum((prox_vector_norm - old_prox_vector) ** 2))
            itera += 1
        for k in range(len(self.multiplex_layer_count_list)):
            start = sum(numpy.array(self.multiplexall_node_count_list[:k]) * numpy.array(self.multiplex_layer_count_list[:k]))
            end = start + self.multiplexall_node_count_list[k] * self.multiplex_layer_count_list[k]
            data = numpy.array(prox_vector_norm[start:end])
            rwr_result_lst.append(data)
        return rwr_result_lst

    ###########################################################################
    # 2 :Analysis func##############################tions
    ###########################################################################

    # 2.1 :
    ###########################################################################

    # 2.1.1 :
    def random_walk_rank(self) -> pandas.DataFrame:
        """
        Function that carries ous the full random walk with restart from a list of seeds.

        Returns :
                rwr_ranking_df (pandas.DataFrame) : A pandas Dataframe with columns: multiplex, node, layer, score
        """
        bipartite_matrix = self.bipartiteall_obj.bipartite_matrix
        transition_matrix_obj = TransitionMatrix(multiplex_all=self.multiplexall_obj, bipartite_matrix=bipartite_matrix, lamb=self.lamb)
        transition_matrixcoo = transition_matrix_obj.transition_matrixcoo

        # Get initial seed probability distribution
        prox_vector, seed_score = self.seed_obj.get_seed_scores(transition=transition_matrixcoo)
        # import pdb; pdb.set_trace()
        # Run RWR algorithm
        rwr_ranking_lst = self.__random_walk_restart(prox_vector, transition_matrixcoo, self.r)
        rwr_ranking_df = self.__random_walk_rank_lst_to_df(rwr_result_lst=rwr_ranking_lst)

        return rwr_ranking_df

    def write_ranking(self, random_walk_rank: pandas.DataFrame, path: str, top: int=None, degree: bool=False):
        """Writes the 'random walk results' to a subnetwork with the 'top' nodes as a SIF format (See Cytoscape documentation)

        Args:
            rwr_ranking_df (pandas.DataFrame) : A pandas Dataframe with columns: multiplex, node, layer, score, which is the output of the random_walk_rank function
            path (str): Path to the SIF file
            top (int): Top nodes based on the random walk score to be included in the SIF file
        """
        output_obj = Output(random_walk_rank, self.multiplexall_obj, top=top)
        output_obj.to_tsv(outdir=path, degree=degree)

    def to_sif(self, random_walk_rank: pandas.DataFrame, path: str, top: int = None):
        """Writes the 'random walk results' to a subnetwork with the 'top' nodes as a SIF format (See Cytoscape documentation)

        Args:
            rwr_ranking_df (pandas.DataFrame) : A pandas Dataframe with columns: multiplex, node, layer, score, which is the output of the random_walk_rank function
            path (str): Path to the TSV file with the random walk results
            top (int): Top nodes based on the random walk score to be included in the TSV file
        """
        output_obj = Output(random_walk_rank, self.multiplexall_obj, top=top)
        pathlib.Path(os.path.dirname(path)).mkdir(exist_ok=True, parents=True)
        output_obj.to_sif(path=path, bipartiteall=self.bipartiteall_obj)

    def __random_walk_rank_lst_to_df(self, rwr_result_lst) -> pandas.DataFrame:
        rwrrestart_df = pandas.DataFrame({'multiplex': [], 'node': [], 'layer': [], 'score': []})
        for i, multiplex in enumerate(self.multiplexall_obj.multiplex_tuple):
            multiplex_label_lst = [multiplex.key] * len(multiplex.nodes) * len(
                multiplex.layer_tuple)
            nodes = [item for subl in [multiplex.nodes] * len(multiplex.layer_tuple) for item in
                     subl]
            layer_lst = [item for subl in
                         [[layer.key] * len(multiplex.nodes) for layer in multiplex.layer_tuple] for
                         item in subl]
            score = list(rwr_result_lst[i].T[0])
            rwrrestart_df = pandas.concat([rwrrestart_df, pandas.DataFrame(
                {'multiplex': multiplex_label_lst, 'node': nodes, 'layer': layer_lst, 'score': score})], axis=0)
        return rwrrestart_df


class Example:

    def __init__(self):
        """Initiates example class"""
        self.package_path = PathManager.get_package_path()
        self.airport_input_path = os.path.join(self.package_path, 'data_example', 'airport')

    def write(self, path):
        """Writes file tree of working example to 'path' directory

        Args:
            path (str): Path to the output directory
        """
        try:
            shutil.copytree(self.airport_input_path, path)
        except FileExistsError:
            logger.error('Directory exists: {}'.format(path))

