import networkx
import numpy
import os
import pandas
import sys

from multixrank.logger_setup import logger


class Bipartite:

    """Multiplex layer"""

    def __init__(self, key, abspath, graph_type, self_loops):

        """

        Args:
            abspath: str
            existing absolute path

            graph_type: str
            takes values 00=(unweighted, undirected), 01=(unweighted, directed),
            10=(weighted, undirected), 11=(weighted, directed)
        """

        self.key = key
        self.abspath = abspath
        if not os.path.isfile(abspath):  # error if path not exist
            logger.error("This path does not exist: {}".format(abspath))
            sys.exit(1)

        if not (graph_type in ['00', '10', '01', '11']):
            logger.error('MultiplexLayer multigraph type must take one of these values: 00, 10, 01, 11. '
                         'Current value: {}'.format(graph_type))
            sys.exit(1)
        self.graph_type = graph_type
        self.self_loops = self_loops

        self._networkx = None

    @property
    def networkx(self) -> networkx.Graph:
        """Converts layer to multigraph networkx object"""

        if self._networkx is None:

            names = ['col2', 'col1']  # layer file column labels changed
            dtype = str
            edge_attr = ['network_key']
            usecols = [0, 1]  # two cols like in unweighted
            if self.graph_type[1] == '1':  # weighted layer
                names = ['col2', 'col1', 'weight'] # changed
                dtype = {'col1': str, 'col2': str, 'weight': numpy.float64}
                edge_attr = ['network_key', 'weight']
                usecols = [0, 1, 2]  # two cols like in unweighted

            networkx_graph_obj = networkx.Graph()  # layer file column labels
            if self.graph_type[0] == '1':  # directed layer
                networkx_graph_obj = networkx.DiGraph()

            multiplex_layer_edge_list_df = pandas.read_csv(self.abspath, sep="\t", header=None, names=names, dtype=dtype, usecols=usecols)
            # remove df lines with self-loops, ie source==target
            if not self.self_loops:
                multiplex_layer_edge_list_df = multiplex_layer_edge_list_df.loc[
                    ~(multiplex_layer_edge_list_df.col1 == multiplex_layer_edge_list_df.col2)]
            multiplex_layer_edge_list_df['network_key'] = self.key

            self._networkx = networkx.from_pandas_edgelist(
                df=multiplex_layer_edge_list_df, source='col2', target='col1',
                edge_attr=edge_attr, create_using=networkx_graph_obj) # changed

            self._networkx.remove_edges_from(networkx.selfloop_edges(self._networkx))

            # networkx has no edges
            # TODO replace edges with nodes
            if len(self._networkx.edges()) == 0:
                logger.error(
                    'The following bipartite graph does not return any edge: {}'.format(
                        self.key))
                sys.exit(1)

        return self._networkx
