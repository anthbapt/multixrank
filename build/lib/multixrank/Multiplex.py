import sys

import networkx
import numpy
import scipy

from multixrank import logger_setup


class Multiplex:

    """Class for one multiplex"""

    def __init__(self, key, layer_tuple, delta=None, eta=None):

        """Reads information about one multiplex"""

        self.key = key
        self.layer_tuple = layer_tuple

        # if delta > 1 or delta < 0:
        #     logger_setup.logger.error("Incorrect 'delta' parameter value not greater than or equal 0 and "
        #                               "smaller than or equal 1. {}".format(delta))
        #     sys.exit(1)
        self.delta = delta
        self.eta = eta

        self._nodes = list()
        self._multigraph = None  # networkx multigraph with undirected edges
        self._multidigraph = None  # networkx multigraph with undirected edges
        self._supra_adj_matrixcoo = None

    @property
    def multigraph(self) -> networkx.MultiGraph:
        """Creates undirected networkx multigraph"""

        if self._multigraph is None:
            self._multigraph = networkx.MultiGraph()
            self._multigraph.add_nodes_from(self.nodes, multiplex=self.key)
            for layer in self.layer_tuple:
                if isinstance(layer.networkx, networkx.Graph):
                    edge_data_lst = [(u, v, layer.networkx[u][v]) for u, v in layer.networkx.edges]
                    self._multigraph.add_edges_from(edge_data_lst)
        return self._multigraph

    @property
    def multidigraph(self) -> networkx.MultiGraph:
        """Creates directed networkx multigraph"""

        if self._multidigraph is None:
            self._multidigraph = networkx.MultiDiGraph()
            self._multidigraph.add_nodes_from(self.nodes, multiplex=self.key)
            for layer in self.layer_tuple:
                if isinstance(layer.networkx, networkx.DiGraph):
                    edge_data_lst = [(u, v, layer.networkx[u][v]) for u, v in layer.networkx.edges]
                    self._multidigraph.add_edges_from(edge_data_lst)
        return self._multidigraph

    @property
    def nodes(self) -> list:
        """Gets list of nodes"""

        if not self._nodes:
            for layer in self.layer_tuple:
                self._nodes = self._nodes + list(layer.networkx.nodes)
            self._nodes = sorted(set(self._nodes))

        return self._nodes

    @property
    def supra_adj_matrixcoo(self):
        """

        Function that creates the Supra-adjacency matrix for this multiplex
        In this part we use sparse matrix to optimize time complexity and memory.

        """

        if self._supra_adj_matrixcoo is None:

            node_count = len(self.nodes)
            # Layers = self.Layers_new[
            #          sum(self.layer_count): self.layer_count + sum(
            #              self.layer_count)]
            # Id = scipy.sparse.csr_matrix(scipy.sparse.identity(self.N[k]))
            Id = scipy.sparse.csr_matrix(scipy.sparse.identity(node_count))
            # L = int(self.multiplex_layer_count_2dlist[k])
            L = len(self.layer_tuple)  # nb of layers
            mask = numpy.zeros((L, L))
            pieces = list()
            # nodes_name = self.multiplexall_node_2dlist[k]
            # nodes_name = self.nodes  # node list
            compt = 0
            if (L != 1):
                # for i in range(self.multiplex_layer_count_2dlist[k]):
                for i, layer_obj in enumerate(self.layer_tuple):
                    # Adjacency_layer = networkx.to_scipy_sparse_matrix(Layers[i], nodelist=nodes_name, format="coo")
                    self._supra_adj_matrixcoo = networkx.to_scipy_sparse_matrix(layer_obj.networkx, nodelist=self.nodes, format="coo")
                    mask[i, i] = compt
                    compt += 1
                    pieces.append((1 - self.delta) * self._supra_adj_matrixcoo)
                    for j in range((i + 1), L):
                        mask[j, i] = compt
                        compt += 1
                        pieces.append((self.delta / (L - 1)) * Id)
                        mask[i, j] = compt
                        compt += 1
                        pieces.append((self.delta / (L - 1)) * Id)
                temp = numpy.zeros((L, L), dtype=object)
                for i in range(L):
                    for j in range(L):
                        temp[i, j] = pieces[int(mask[i, j])]
                # self.SupraAdjacencyMatrix.append(
                #     scipy.sparse.bmat(temp, format="coo"))
                self._supra_adj_matrixcoo = scipy.sparse.bmat(temp, format="coo")
            else:
                layer_obj = self.layer_tuple[0]
                self._supra_adj_matrixcoo = networkx.to_scipy_sparse_matrix(layer_obj.networkx,
                                                                            nodelist=self.nodes,
                                                                            format="coo")
        return self._supra_adj_matrixcoo
