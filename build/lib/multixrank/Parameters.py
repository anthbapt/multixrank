import sys
from fractions import Fraction

import numpy

from multixrank.logger_setup import logger
from multixrank.MultiplexAll import MultiplexAll


class Parameters:

    """Class for the parameters"""

    def __init__(self, r, lamb: list, multiplexall: MultiplexAll, seed_count_list2d):

        """Initialize parameters from the user or by default"""

        self.lamb = lamb
        self.r = r

    @staticmethod
    def check_eta(eta_lst, multiplex_count):

        if len(eta_lst) != multiplex_count:
            logger.error("Incorrect eta. eta list length must be equal to the number of multiplexes: {}".format(eta_lst))
            sys.exit(1)
        if round(sum(eta_lst)) != 1.0:
            logger.error("Incorrect 'eta'. The sum of the elements must equal 1: {}".format(eta_lst))
            sys.exit(1)
        for eta in eta_lst:
            if eta > 1 or eta < 0:
                logger.error("Incorrect 'eta' parameter vector. "
                                          "Each element must be greater than or equal 0 "
                                          "and smaller than or equal 1: {}".format(eta))
                sys.exit(1)

    @staticmethod
    def check_tau(tau_lst, layer_count):

        if len(tau_lst) != layer_count:
            logger.error("Incorrect tau. tau list length must be equal to the number of layers of the multiplex: {}".format(tau_lst))
            sys.exit(1)
        if round(sum(tau_lst)) != 1.0:
            logger.error("Incorrect 'tau'. The sum of the elements must equal 1: {}".format(tau_lst))
            sys.exit(1)
        for tau in tau_lst:
            if tau > 1 or tau < 0:
                logger.error("Incorrect 'tau' parameter vector. "
                                          "Each element must be greater than or equal 0 "
                                          "and smaller than or equal 1: {}".format(tau))
                sys.exit(1)
