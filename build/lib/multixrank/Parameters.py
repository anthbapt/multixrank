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
    
    @staticmethod
    def check_delta(delta_lst, multiplex_count):

        if len(delta_lst) != multiplex_count:
            logger.error("Incorrect delta. delta list length must be equal to the number multiplexes: {}".format(delta_lst))
            sys.exit(1)
        if round(sum(delta_lst)) != 1.0:
            logger.error("Incorrect 'delta'. The sum of the elements must equal 1: {}".format(delta_lst))
            sys.exit(1)
        for delta in delta_lst:
            if delta > 1 or delta < 0:
                logger.error("Incorrect 'delta' parameter vector. "
                                          "Each element must be greater than or equal 0 "
                                          "and smaller than or equal 1: {}".format(delta))
                sys.exit(1)


    @staticmethod
    def check_lamb(lamb, multiplex_count):
        
        tol = 2
        lambd = numpy.zeros((multiplex_count,multiplex_count))
        for i in range(multiplex_count) :
            for j in range(multiplex_count) :
                lambd[i,j] = float(Fraction(lamb[i,j]))
        lamb = lambd
                
        for k in range(numpy.shape(lamb)[0]) :
            for i in range(numpy.shape(lamb)[1]) :
                if (lamb[k,i] > 1 or lamb[k,i] < 0) :
                    print("Incorrect lamb, each element must be " \
                          "between 0 and 1")
                    print("the " + str(k) + "," + str(i) + " term is " \
                          "incorrect")
                    raise StopIteration
            if (round(sum(lamb[:,k]), tol) != 1.00) or \
                round(sum(lamb[:,k]) - lamb[k,k], tol) != round(1-lamb[k,k], tol) :
                print("Incorrect lamb, the lamb[k,k] term need to " \
                      "equal to sum(lamb[k,:]")
                print("the " + str(k)  + " column is incorrect")
                raise StopIteration
    

