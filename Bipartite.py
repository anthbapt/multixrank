import networkx
import numpy
import os
import pandas
import sys

from .logger_setup import logger

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
    def networkx_graph(self) -> networkx.Graph:
        """Converts layer to multigraph networkx object"""
        if self._networkx is None:
            # Configuration based on graph type
            is_directed = self.graph_type[0] == '1'
            is_weighted = self.graph_type[1] == '1'
            
            # Column setup
            cols = ['col2', 'col1']
            dtypes = {'col1': str, 'col2': str}
            usecols = [0, 1]
            edge_attrs = {}
            
            if is_weighted:
                cols.append('weight')
                dtypes['weight'] = numpy.float64
                usecols.append(2)

            # Read data with efficient column selection
            df = pandas.read_csv(
                self.abspath,
                sep="\t",
                header=None,
                names=cols,
                dtype=dtypes,
                usecols=usecols,
                engine='c'  # Use C engine for faster parsing
            )

            # Filter self-loops early
            if not self.self_loops:
                df = df[df.col1 != df.col2]

            # Convert to numpy arrays for fast processing
            sources = df.col2.values
            targets = df.col1.values
            weights = df.weight.values if is_weighted else None

            # Create graph with single-pass edge construction
            nx_graph = networkx.DiGraph() if is_directed else networkx.Graph()
            edge_data = {'network_key': self.key}
            
            if is_weighted:
                edges = ((s, t, {'network_key': self.key, 'weight': w}) 
                        for s, t, w in zip(sources, targets, weights))
            else:
                # Use same dict reference for all edges to save memory
                edges = ((s, t, edge_data) for s, t in zip(sources, targets))
            
            nx_graph.add_edges_from(edges)

            # Final validation
            if not nx_graph.edges():
                logger.error(f'Bipartite graph {self.key} has no edges after processing')
                sys.exit(1)

            self._networkx = nx_graph

        return self._networkx

    @property
    def networkx_graph_old(self) -> networkx.Graph:
        """Converts layer to multigraph networkx object"""

        if self._networkx is None:

            names = ['col2', 'col1']  # layer file column labels changed
            dtype = str
            edge_attr = ['network_key']
            usecols = [0, 1]  # two cols like in unweighted
            if self.graph_type[1] == '1':  # unweighted/weighted layer (0/1)
                names = ['col2', 'col1', 'weight'] # changed
                dtype = {'col1': str, 'col2': str, 'weight': numpy.float64}
                edge_attr = ['network_key', 'weight']
                usecols = [0, 1, 2]  # two cols like in unweighted

            networkx_graph_obj = networkx.Graph()  # layer file column labels
            if self.graph_type[0] == '1':  # undirected/directed layer (0/1)
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
