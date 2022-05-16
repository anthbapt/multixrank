import networkx
import numpy
import scipy


class BipartiteAll:
    """Deals with list of bipartites"""

    def __init__(self, source_target_bipartite_dic, multiplexall):

        self.source_target_bipartite_dic = source_target_bipartite_dic
        self.multiplexall = multiplexall

        self.multiplex_layer_count_list2d = [len(multiplexall.layer_tuple)
                                             for multiplexall in
                                             multiplexall.multiplex_tuple]
        self.multiplexall_node_list2d = [multiplexall.nodes for
                                         multiplexall in
                                         multiplexall.multiplex_tuple]
        self.multiplex_dic = dict()
        for multiplexone_obj in self.multiplexall.multiplex_tuple:
            self.multiplex_dic[multiplexone_obj.key] = multiplexone_obj

        self._bipartite_matrix = None
        self._graph = None  # Networkx with all undirected edges in Bipartites
        self._digraph = None  # Networkx with all directed edges in Bipartites

    @property
    def graph(self):
        """Returns graph with all undirected edges in all bipartites"""

        if self._graph is None:
            self._graph = networkx.Graph()
            for edge_tple in self.source_target_bipartite_dic:
                bipartite_obj = self.source_target_bipartite_dic[edge_tple]
                if isinstance(bipartite_obj.networkx, networkx.Graph):
                    edge_data_lst = [(u, v, bipartite_obj.networkx[u][v]) for u, v in bipartite_obj.networkx.edges]
                    self._graph.add_edges_from(edge_data_lst)
        return self._graph

    @property
    def digraph(self):
        """Returns graph with all directed edges in all bipartites"""

        if self._digraph is None:
            self._digraph = networkx.DiGraph()
            for edge_tple in self.source_target_bipartite_dic:
                bipartite_obj = self.source_target_bipartite_dic[edge_tple]
                if isinstance(bipartite_obj.networkx, networkx.Graph):
                    edge_data_lst = [(u, v, bipartite_obj.networkx[u][v]) for u, v in bipartite_obj.networkx.edges]
                    self._digraph.add_edges_from(edge_data_lst)
        return self._digraph

    @property
    def bipartite_matrix(self):
        """"""

        #######################################################################
        #
        # Will add B bipartite multigraph matrix to each B_i_j with i!=j
        #
        #######################################################################

        if self._bipartite_matrix is None:

            multiplexall_supra_adj_matrix_list = []
            for i, multiplex_obj in enumerate(self.multiplexall.multiplex_tuple):
                multiplexall_supra_adj_matrix_list.append(multiplex_obj.supra_adj_matrixcoo)

            self._bipartite_matrix = numpy.zeros((len(self.multiplex_layer_count_list2d), len(self.multiplex_layer_count_list2d)), dtype=object)

            for i, multiplexone_obj1 in enumerate(self.multiplexall.multiplex_tuple):
                for j, multiplexone_obj2 in enumerate(self.multiplexall.multiplex_tuple):
                    multiplex_key1 = multiplexone_obj1.key
                    multiplex_key2 = multiplexone_obj2.key

                    if not (multiplex_key1 == multiplex_key2):
                        if (multiplex_key1, multiplex_key2) in self.source_target_bipartite_dic:
                            bipartite_layer_obj = self.source_target_bipartite_dic[(multiplex_key1, multiplex_key2)]
                            bipartite_layer_networkx = bipartite_layer_obj.networkx
                            bipartite_layer_networkx.remove_edges_from(networkx.selfloop_edges(bipartite_layer_networkx))
                            two_multiplex_nodes = multiplexone_obj1.nodes + multiplexone_obj2.nodes
                            bipartite_layer_networkx_nodes = bipartite_layer_networkx.nodes
                            new_bipartite_layer_networkx_nodes = two_multiplex_nodes - bipartite_layer_networkx_nodes
                            bipartite_layer_networkx.add_nodes_from(new_bipartite_layer_networkx_nodes)
                            B = networkx.to_scipy_sparse_matrix(bipartite_layer_networkx, nodelist=two_multiplex_nodes, format="csr")                              
                                
                            self._bipartite_matrix[j, i] = B[0:len(self.multiplexall_node_list2d[i]), len(self.multiplexall_node_list2d[i])::].T # changed
                            if bipartite_layer_networkx.is_directed() == False : # changed
                            	self._bipartite_matrix[i, j] = self._bipartite_matrix[j, i].T # changed
            for i in range(len(self.multiplex_layer_count_list2d)):
                for j in range(len(self.multiplex_layer_count_list2d)):
                    if i != j:
                        if isinstance(self._bipartite_matrix[i, j], int):
                            row = numpy.shape(multiplexall_supra_adj_matrix_list[i])[0]
                            col = numpy.shape(multiplexall_supra_adj_matrix_list[j])[1]
                            self._bipartite_matrix[i, j] = scipy.sparse.coo_matrix((row, col))
                        else:
                            temp = numpy.zeros((self.multiplex_layer_count_list2d[i],
                                               self.multiplex_layer_count_list2d[j]),
                                               dtype=object)
                            for k in range(self.multiplex_layer_count_list2d[i]):
                                temp[k] = self._bipartite_matrix[i, j]
                            self._bipartite_matrix[i, j] = scipy.sparse.bmat(temp, format='coo')

        return self._bipartite_matrix
