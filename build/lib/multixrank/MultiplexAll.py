import networkx


class MultiplexAll:

    """Class for one multiplex"""

    def __init__(self, multiplex_tuple):

        """Process all multiplexes together"""

        self.multiplex_tuple = multiplex_tuple
        self._nodes = list()
        self._multigraph = None  # networkx multigraph with undirected edges
        self._multidigraph = None  # networkx multigraph with undirected edges
        self._supra_adj_matrix_list = []  # networkx multigraph with undirected edges

    @property
    def multidigraph(self) -> networkx.MultiGraph:
        """Creates undirected networkx multigraph"""

        if self._multidigraph is None:
            self._multidigraph = networkx.MultiGraph()
            for multiplex in self.multiplex_tuple:
                self._multidigraph = networkx.compose(self._multidigraph, multiplex.multidigraph)
        return self._multidigraph

    @property
    def multigraph(self) -> networkx.MultiGraph:
        """Creates undirected networkx multigraph"""

        if self._multigraph is None:
            self._multigraph = networkx.MultiGraph()
            for multiplex in self.multiplex_tuple:
                self._multigraph = networkx.compose(self._multigraph, multiplex.multigraph)
        return self._multigraph

    @property
    def nodes(self) -> list:
        """Get list with all nodes"""

        if not self._nodes:
            for multiplex in self.multiplex_tuple:
                self._nodes = self._nodes + multiplex.nodes
            self._nodes = sorted(set(self._nodes))
        return self._nodes

    @property
    def supra_adj_matrix_list(self) -> list:
        """List of Supra-adjacency matrices for each multiplex"""

        if self._supra_adj_matrix_list == []:
            for i, multiplex_obj in enumerate(self.multiplex_tuple):
                self._supra_adj_matrix_list.append(multiplex_obj.supra_adj_matrixcoo.T) # changed
        return self._supra_adj_matrix_list
