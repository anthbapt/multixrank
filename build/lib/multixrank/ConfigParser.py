import os
import sys

import numpy
import yaml
from fractions import Fraction

from multixrank import logger_setup, constants
from multixrank.BipartiteAll import BipartiteAll
from multixrank.Bipartite import Bipartite
from multixrank.MultiplexAll import MultiplexAll
from multixrank.Multiplex import Multiplex
from multixrank.MultiplexLayer import MultiplexLayer
from multixrank.ParameterEta import ParameterEta
from multixrank.ParameterLambda import ParameterLambda
from multixrank.Parameters import Parameters
from multixrank.Seed import Seed
from multixrank.logger_setup import logger


class ConfigParser:

    def __init__(self, config: str, wdir=os.getcwd()):

        """Takes a config_path of the config yaml file"""

        self.config_path = config
        self.wdir = wdir

        with open(self.config_path) as fin:
            self.config_dic = yaml.load(fin, Loader=yaml.BaseLoader)

        # default is 00 for all interaction types
        self.config_parameters_dic = None

        # This parameter defines whether self_loops will be kept or not
        self.self_loops = True
        if 'self_loops' in self.config_dic:
            self.self_loops = bool(int(self.config_dic['self_loops']))

    def parse(self):

        """Parses the config yaml file and give fields to specialized functions"""

        #######################################################################
        #
        # Parses multiplex layers
        # and create MultiplexLayer, MultiplexOne and MultiplexAll objects
        #
        #######################################################################

        self.multiplexall_obj = self.__parse_multiplex()

        #######################################################################
        #
        # Parses bipartite
        #
        #######################################################################

        self.bipartitelist_obj = self.__parse_bipartite()

        #######################################################################
        #
        # Parses Seeds
        #
        #######################################################################

        self.seed_obj = self.__parse_seed()
        
        #######################################################################
        #
        # Parameter 'delta' check
        #
        #######################################################################

        if 'delta' in self.config_dic:  # user defined (changed)
            delta_lst = [float(Fraction(delta)) for delta in self.config_dic['delta']] # changed
            Parameters.check_eta(delta_lst , len(self.multiplexall_obj.multiplex_tuple)) # changed
            
            
            
        ###################################################################
        #
        # Parameter 'lamb' check
        #
        ###################################################################

        if 'lamb' in self.config_dic:  # user defined (changed)
            lamb = numpy.array(self.config_dic['lamb'])
            Parameters.check_lamb(lamb , len(self.multiplexall_obj.multiplex_tuple)) # changed
                

        #######################################################################
        #
        # Parameter 'eta': Parse and set
        #
        #######################################################################

        if 'eta' in self.config_dic:  # user defined
            eta_lst = [float(Fraction(eta)) for eta in self.config_dic['eta']]
            Parameters.check_eta(eta_lst , len(self.multiplexall_obj.multiplex_tuple)) # changed
        else:  # default eta
            n = len(self.multiplexall_obj.multiplex_tuple)
            alpha = [len(x) for x in self.seed_obj.multiplex_seed_list2d]
            # Generate eta default
            eta_lst = ParameterEta(n, alpha).vect_X().tolist()
        logger.debug("Parameter 'eta' is equal to: {}".format(eta_lst))

        for i,multiplex_obj in enumerate(self.multiplexall_obj.multiplex_tuple):
            multiplex_obj.eta = eta_lst[i]

        #######################################################################
        #
        # Parses parameters
        #
        #######################################################################

        seed_count_list2d = [len(i) for i in self.seed_obj.multiplex_seed_list2d]
        self.parameter_obj = self.__parse_parameters(seed_count_list2d=seed_count_list2d)

    def __parse_bipartite(self):
        """
        Reads multiplex field and create MultiplexAll object
        """

        if not ('bipartite' in self.config_dic):

            return BipartiteAll({}, multiplexall=self.multiplexall_obj)

        config_bipartite_dic = self.config_dic['bipartite']
        source_target_bipartite_dic = {}

        # loop over each multiplex
        for i, layer_key in enumerate(config_bipartite_dic):

            layer_abs_path = os.path.join(self.wdir, layer_key)

            graph_type = '00'
            if 'graph_type' in config_bipartite_dic[layer_key]:
                graph_type = config_bipartite_dic[layer_key]['graph_type']

            if 'source' in config_bipartite_dic[layer_key]:
                bipartite_source = config_bipartite_dic[layer_key]['source']
            else:
                logger_setup.logger.error("No 'source' field found for bipartite network")
                sys.exit(1)

            if 'target' in config_bipartite_dic[layer_key]:
                bipartite_target = config_bipartite_dic[layer_key]['target']
            else:
                logger_setup.logger.error("No 'target' field found for bipartite network")
                sys.exit(1)

            layer_obj = Bipartite(key=layer_key, abspath=layer_abs_path, graph_type=graph_type, self_loops=self.self_loops)
            source_target_bipartite_dic[(bipartite_source, bipartite_target)] = layer_obj

        return BipartiteAll(source_target_bipartite_dic, multiplexall=self.multiplexall_obj)

    def __parse_multiplex(self):
        """
        Reads multiplex field and create MultiplexAll object
        """

        if not ('multiplex' in self.config_dic):

            logger.error("No required 'multiplex' field found in config file: {}".format(self.config_path))
            sys.exit(1)

        config_multiplex_dic = self.config_dic['multiplex']
        multiplex_count = len(config_multiplex_dic)
        # convert int to strings
        multiplex_obj_list = []

        # loop over each multiplex
        for multiplex_idx, multiplex_key in enumerate(config_multiplex_dic):

            layer_obj_list = []
            multiplex_node_list = []
            layer_key_tuple = tuple(config_multiplex_dic[multiplex_key]['layers'])

            ###################################################################
            #
            # tau
            #
            ###################################################################

            tau_lst = [float(Fraction(1/len(layer_key_tuple)))] * len(layer_key_tuple)
            if 'tau' in config_multiplex_dic[multiplex_key]:
                tau_lst  = [float(Fraction(tau)) for tau in config_multiplex_dic[multiplex_key]['tau']]
            Parameters.check_tau(tau_lst , len(layer_key_tuple))
            logger.debug("Multiplex '{}'. Parameter 'tau' is equal: {}".format(multiplex_key, tau_lst))


            ###################################################################
            #
            # layer multigraph types
            #
            ###################################################################

            graph_type_lst = ['00'] * len(layer_key_tuple)
            if 'graph_type' in config_multiplex_dic[multiplex_key]:
                graph_type_lst = config_multiplex_dic[multiplex_key]['graph_type']

            ###################################################################
            #
            # layers
            #
            ###################################################################

            # loop over layers
            for layer_idx, layer_key in enumerate(layer_key_tuple):

                layer_abs_path = os.path.join(self.wdir, layer_key)
                layer_obj = MultiplexLayer(key=layer_key, abspath=layer_abs_path,
                                           graph_type=graph_type_lst[layer_idx], multiplex=multiplex_key, tau=tau_lst[layer_idx], self_loops=self.self_loops)
                multiplex_node_list = sorted([*set(multiplex_node_list + [*layer_obj.networkx.nodes])])
                layer_obj_list.append(layer_obj)

            # Append missing nodes from other layers in one multiplex to each layer
            for layer_idx, layer_obj in enumerate(layer_obj_list):
                layer_missing_nodes = sorted(set(multiplex_node_list) - set(list(layer_obj.networkx.nodes)))
                layer_obj.networkx.add_nodes_from(layer_missing_nodes)
                layer_obj_list[layer_idx] = layer_obj  # update

            ###################################################################
            #
            # Parameter: delta
            # If only layer: delta=0
            # If more than one layer: delta=0.5
            #
            ###################################################################

            if 'delta' in config_multiplex_dic[multiplex_key]:  # user-defined delta
                delta = float(config_multiplex_dic[multiplex_key]['delta'])
            else:  # default delta
                if len(layer_obj_list) == 1:  # only one layer, delta=0
                    delta = 0
                else:  # more than one layer, delta=0.5
                    delta = 0.5
            logger.debug("Multiplex: {}. Parameter 'delta' is equal to: {}".format(multiplex_key, delta))

            ###################################################################
            #
            # multiplex object
            #
            ###################################################################

            multiplex_one_obj = Multiplex(multiplex_key, layer_tuple=tuple(layer_obj_list), delta=delta)
            multiplex_obj_list.append(multiplex_one_obj)

        return MultiplexAll(multiplex_tuple=tuple(multiplex_obj_list))

    def __parse_parameters(self, seed_count_list2d):

        r = constants.r
        if 'r' in self.config_dic:
            r = float(self.config_dic['r'])
        logger.debug("r is equal to: {}".format(r))
        
        lamb_arr = None
        if 'lamb' in self.config_dic:  # used-defined lambda
            lamb_2dlst = [[float(Fraction(j)) for j in i] for i in self.config_dic['lamb']]
            lamb_arr = numpy.array(lamb_2dlst)
        else:
            # Number of multiplex in the system
            multiplex_count = len(self.multiplexall_obj.multiplex_tuple)
            # List of number of layers in each multiplex
            multiplex_layer_count = [len(multiplex_obj.layer_tuple) for multiplex_obj in
             self.multiplexall_obj.multiplex_tuple]
            if multiplex_count == 1:  # One multiplex only
                lamb_arr = [[0]]
            else:  # More than multiplex
                lamb_arr = ParameterLambda(n=multiplex_count, N=multiplex_layer_count).matrix_X()

        parameters_obj = Parameters(r=r, lamb=lamb_arr, multiplexall=self.multiplexall_obj, seed_count_list2d=seed_count_list2d)

        return parameters_obj

    def __parse_seed(self):

        if not ('seed' in self.config_dic):

            logger.error("Field 'seed' is required in config file: {}".format(self.config_path))
            sys.exit(1)

        seed_path = os.path.join(self.wdir, self.config_dic['seed'])
        seed_obj = Seed(path=seed_path, multiplexall=self.multiplexall_obj)

        return seed_obj
