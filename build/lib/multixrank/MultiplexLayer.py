import networkx
import numpy
import os
import pandas
import sys

from multixrank.logger_setup import logger


class MultiplexLayer:

    """Multiplex layer"""

    def __init__(self, key, abspath, graph_type, multiplex, tau, self_loops):

        """

        Args:
            abspath: str
            existing absolute path

            graph_type: str
            takes values 00=(unweighted, undirected), 01=(unweighted, directed),
            10=(weighted, undirected), 11=(weighted, directed)

            multiplex: str
            Parent multiplex key
        """

        self.key = key
        self.abspath = abspath
        self.multiplex = multiplex
        self.tau = tau
        self.graph_type = graph_type
        self.self_loops = self_loops

        if not os.path.isfile(abspath):  # error if path not exist
            logger.error("This path does not exist: {}".format(abspath))
            sys.exit(1)

        if not (graph_type in ['00', '10', '01', '11']):
            logger.error('MultiplexLayer multigraph type must take one of these values: 00, 10, 01, 11. '
                         'Current value: {}'.format(graph_type))
            sys.exit(1)

        self._networkx = None

    @property
    def networkx(self) -> networkx.Graph:
        """Converts layer to multigraph networkx object"""

        if self._networkx is None:

            # if multigraph is None:
            name_lst = ['source', 'target']  # layer file column labels
            dtype_dic = dict(zip(name_lst, [str]*len(name_lst)))

            # unweighted vs weighted ######################################
            edge_attr = ['network_key']
            usecols = [0, 1]  # two cols like in unweighted
            if self.graph_type[1] == '1':  # weighted layer
                name_lst = ['source', 'target', 'weight']
                dtype_dic['weight'] = numpy.float64
                edge_attr = ['network_key', 'weight']
                usecols = [0, 1, 2]  # three cols in weighted

            # undirected vs directed ######################################
            networkx_graph_obj = networkx.Graph()  # layer file column labels
            if self.graph_type[0] == '1':  # directed layer
                networkx_graph_obj = networkx.DiGraph()

            multiplex_layer_edge_list_df = pandas.read_csv(
                self.abspath, sep="\t", header=None, names=name_lst, dtype=dtype_dic, keep_default_na=False, usecols=usecols)
            # remove df lines with self-loops, ie source==target if bipartite_notes=true
            if not self.self_loops:
                multiplex_layer_edge_list_df = multiplex_layer_edge_list_df.loc[
                    ~(multiplex_layer_edge_list_df.source == multiplex_layer_edge_list_df.target)]
            multiplex_layer_edge_list_df['network_key'] = self.key
            self._networkx = networkx.from_pandas_edgelist(
                df=multiplex_layer_edge_list_df, source='source',
                target='target', create_using=networkx_graph_obj, edge_attr=edge_attr)

            self._networkx.remove_edges_from(networkx.selfloop_edges(self._networkx))

            # networkx has no edges
            if len(self._networkx.nodes()) == 0:
                logger.error(
                    'The following multiplex layer does not return any edge: {}'.format(self.key))
                sys.exit(1)

        return self._networkx
