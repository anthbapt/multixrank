import networkx
import numpy
import scipy

import itertools

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
                if isinstance(bipartite_obj.networkx_graph, networkx.Graph):
                    self._graph.add_edges_from(bipartite_obj.networkx_graph.edges(data=True))
        return self._graph

    @property
    def graph_old(self):
        """Returns graph with all undirected edges in all bipartites"""

        if self._graph is None:
            self._graph = networkx.Graph()
            for edge_tple in self.source_target_bipartite_dic:
                bipartite_obj = self.source_target_bipartite_dic[edge_tple]
                if isinstance(bipartite_obj.networkx_graph_old, networkx.Graph):
                    self._graph.add_edges_from(bipartite_obj.networkx_graph_old.edges(data=True))
        return self._graph

    @property
    def digraph(self):
        """Returns graph with all directed edges in all bipartites"""

        if self._digraph is None:
            self._digraph = networkx.DiGraph()
            for edge_tple in self.source_target_bipartite_dic:
                bipartite_obj = self.source_target_bipartite_dic[edge_tple]
                if isinstance(bipartite_obj.networkx_graph, networkx.Graph):
                    self._digraph.add_edges_from(bipartite_obj.networkx_graph.edges(data=True))
        return self._digraph

    @property
    def digraph_old(self):
        """Returns graph with all directed edges in all bipartites"""

        if self._digraph is None:
            self._digraph = networkx.DiGraph()
            for edge_tple in self.source_target_bipartite_dic:
                bipartite_obj = self.source_target_bipartite_dic[edge_tple]
                if isinstance(bipartite_obj.networkx_graph_old, networkx.Graph):
                    edge_data_lst = [(u, v, bipartite_obj.networkx_graph_old[u][v]) for u, v in bipartite_obj.networkx_graph_old.edges]
                    self._digraph.add_edges_from(edge_data_lst)
        return self._digraph

    @property
    def bipartite_matrix(self):
        if self._bipartite_matrix is None:
            multiplexall_supra_adj_matrix_list = []
            for i, multiplex_obj in enumerate(self.multiplexall.multiplex_tuple):
                multiplexall_supra_adj_matrix_list.append(multiplex_obj.supra_adj_matrixcoo)

            self._bipartite_matrix = numpy.zeros((len(self.multiplex_layer_count_list2d), len(self.multiplex_layer_count_list2d)), dtype=object)

            for i, multiplexone_obj1 in enumerate(self.multiplexall.multiplex_tuple):
                for j, multiplexone_obj2 in enumerate(self.multiplexall.multiplex_tuple):
                    multiplex_key1 = multiplexone_obj1.key
                    multiplex_key2 = multiplexone_obj2.key

                    if multiplex_key1 != multiplex_key2 and (multiplex_key1, multiplex_key2) in self.source_target_bipartite_dic:
                        bipartite_layer_obj = self.source_target_bipartite_dic[(multiplex_key1, multiplex_key2)]
                        bipartite_layer_networkx = bipartite_layer_obj.networkx_graph
                        bipartite_layer_networkx.remove_edges_from(networkx.selfloop_edges(bipartite_layer_networkx))
                        two_multiplex_nodes = multiplexone_obj1.nodes + multiplexone_obj2.nodes
                        bipartite_layer_networkx_nodes = bipartite_layer_networkx.nodes
                        new_nodes = set(two_multiplex_nodes) - set(bipartite_layer_networkx_nodes)
                        bipartite_layer_networkx.add_nodes_from(new_nodes)

                        # Extract nodes for each multiplex
                        nodes_i = multiplexone_obj1.nodes
                        nodes_j = multiplexone_obj2.nodes
                        node_to_i = {node: idx for idx, node in enumerate(nodes_i)}
                        node_to_j = {node: idx for idx, node in enumerate(nodes_j)}

                        rows, cols, data = [], [], []
                        for u, v, edge_data in bipartite_layer_networkx.edges(data=True):
                            # Check if edge is from i to j
                            if u in node_to_i and v in node_to_j:
                                rows.append(node_to_i[u])
                                cols.append(node_to_j[v])
                                data.append(edge_data.get('weight', 1.0))
                            # For undirected graphs, check reverse edge
                            elif not bipartite_layer_networkx.is_directed() and v in node_to_i and u in node_to_j:
                                rows.append(node_to_i[v])
                                cols.append(node_to_j[u])
                                data.append(edge_data.get('weight', 1.0))

                        # Create sparse matrix for i->j block
                        shape = (len(nodes_i), len(nodes_j))
                        if rows:
                            B_block = scipy.sparse.coo_matrix((data, (rows, cols)), shape=shape, dtype=numpy.float64)
                            B_block = B_block.tocsr()
                        else:
                            B_block = scipy.sparse.csr_matrix(shape, dtype=numpy.float64)

                        # Assign transpose to [j, i]
                        self._bipartite_matrix[j, i] = B_block.T

                        # If undirected, set [i, j] as transpose of [j, i]
                        if not bipartite_layer_networkx.is_directed():
                            self._bipartite_matrix[i, j] = self._bipartite_matrix[j, i].T.copy()

            # Handle cases where i != j but no bipartite graph exists
            for i in range(len(self.multiplex_layer_count_list2d)):
                for j in range(len(self.multiplex_layer_count_list2d)):
                    if i != j and isinstance(self._bipartite_matrix[i, j], int):
                        row = multiplexall_supra_adj_matrix_list[i].shape[0]
                        col = multiplexall_supra_adj_matrix_list[j].shape[1]
                        self._bipartite_matrix[i, j] = scipy.sparse.coo_matrix((row, col))
                    elif i != j:
                        # Original code's logic for expanding the matrix
                        temp = numpy.zeros((self.multiplex_layer_count_list2d[i], self.multiplex_layer_count_list2d[j]), dtype=object)
                        for k in range(self.multiplex_layer_count_list2d[i]):
                            temp[k] = self._bipartite_matrix[i, j]
                        self._bipartite_matrix[i, j] = scipy.sparse.bmat(temp, format='coo')

        return self._bipartite_matrix

    @property
    def bipartite_matrix_readable(self) -> numpy.ndarray:
        """
        Constructs a block matrix representing bipartite connections between different multiplexes.

        For each pair of multiplexes (i, j), this method:
        1. Retrieves the bipartite graph connecting the two multiplexes.
        2. Removes self-loops and ensures all nodes from both multiplexes are present.
        3. Converts the graph to a sparse matrix and stores it in the appropriate block.
        4. Ensures symmetry for undirected bipartite graphs.
        5. Fills missing blocks with zero matrices and constructs the final block structure.

        Returns:
            numpy.ndarray: A 2D array where each element is a sparse matrix representing
                            bipartite connections between two multiplexes.
        """

        if self._bipartite_matrix is None:
            # Initialize list of supra-adjacency matrices for each multiplex
            supra_adj_matrices = [
                multiplex.supra_adj_matrixcoo 
                for multiplex in self.multiplexall.multiplex_tuple
            ]

            # Get the number of layers for each multiplex
            num_multiplexes = len(self.multiplex_layer_count_list2d)
            self._bipartite_matrix = numpy.zeros(
                (num_multiplexes, num_multiplexes), 
                dtype=object
            )

            # Process each pair of multiplexes to populate bipartite connections
            for i, src_multiplex in enumerate(self.multiplexall.multiplex_tuple):
                for j, tgt_multiplex in enumerate(self.multiplexall.multiplex_tuple):
                    if src_multiplex.key == tgt_multiplex.key:
                        continue  # Skip same multiplex

                    bipartite_key = (src_multiplex.key, tgt_multiplex.key)
                    if bipartite_key not in self.source_target_bipartite_dic:
                        continue

                    # Retrieve and preprocess bipartite graph
                    bipartite_layer = self.source_target_bipartite_dic[bipartite_key]
                    bipartite_graph = bipartite_layer.networkx_graph
                    
                    # Remove self-loops and add missing nodes
                    bipartite_graph.remove_edges_from(networkx.selfloop_edges(bipartite_graph))
                    combined_nodes = src_multiplex.nodes + tgt_multiplex.nodes
                    bipartite_graph.add_nodes_from(set(combined_nodes) - set(bipartite_graph.nodes))

                    # Convert to sparse matrix format
                    bipartite_sparse = networkx.to_scipy_sparse_array(
                        bipartite_graph, 
                        nodelist=combined_nodes, 
                        format="csr"
                    )

                    # Extract relevant block for current multiplex pair
                    src_size = len(src_multiplex.nodes)
                    tgt_size = len(tgt_multiplex.nodes)
                    connection_block = bipartite_sparse[:src_size, src_size:]

                    # Store connection and handle undirected case
                    self._bipartite_matrix[j, i] = connection_block.T
                    if not bipartite_graph.is_directed():
                        self._bipartite_matrix[i, j] = connection_block

            # Post-process to fill missing connections and build block matrices
            for i in range(num_multiplexes):
                for j in range(num_multiplexes):
                    if i == j:
                        continue

                    # Replace missing entries with zero matrices
                    if isinstance(self._bipartite_matrix[i, j], int):
                        rows = supra_adj_matrices[i].shape[0]
                        cols = supra_adj_matrices[j].shape[1]
                        self._bipartite_matrix[i, j] = scipy.sparse.coo_matrix((rows, cols))

                    # Create block matrix structure for layer-wise connections
                    layer_blocks = numpy.full(
                        (self.multiplex_layer_count_list2d[i], 
                        self.multiplex_layer_count_list2d[j]),
                        self._bipartite_matrix[i, j],
                        dtype=object
                    )
                    self._bipartite_matrix[i, j] = scipy.sparse.bmat(layer_blocks, format='coo')

        return self._bipartite_matrix

    @property
    def bipartite_matrix_old(self) -> numpy.ndarray:
        """"""

        #######################################################################
        #
        # Will add B bipartite multigraph matrix to each B_i_j with i!=j
        #
        #######################################################################

        if self._bipartite_matrix is None:

            multiplexall_supra_adj_matrix_list = []
            # type(multiplex_obj) = Multiplex
            for i, multiplex_obj in enumerate(self.multiplexall.multiplex_tuple):
                # type(multiplex_obj.supra_adj_matrixcoo) = <class 'scipy.sparse._coo.coo_array'>
                multiplexall_supra_adj_matrix_list.append(multiplex_obj.supra_adj_matrixcoo)

            # in __init__:
            # self.multiplex_layer_count_list2d = [len(multiplexall.layer_tuple)
            #                                      for multiplexall in
            #                                      multiplexall.multiplex_tuple]

            self._bipartite_matrix = numpy.zeros((len(self.multiplex_layer_count_list2d), len(self.multiplex_layer_count_list2d)), dtype=object)

            for i, multiplexone_obj1 in enumerate(self.multiplexall.multiplex_tuple):
                for j, multiplexone_obj2 in enumerate(self.multiplexall.multiplex_tuple):
                    multiplex_key1 = multiplexone_obj1.key
                    multiplex_key2 = multiplexone_obj2.key

                    if not (multiplex_key1 == multiplex_key2):
                        if (multiplex_key1, multiplex_key2) in self.source_target_bipartite_dic:
                            bipartite_layer_obj = self.source_target_bipartite_dic[(multiplex_key1, multiplex_key2)]
                            bipartite_layer_networkx = bipartite_layer_obj.networkx_graph_old
                            bipartite_layer_networkx.remove_edges_from(networkx.selfloop_edges(bipartite_layer_networkx))
                            two_multiplex_nodes = multiplexone_obj1.nodes + multiplexone_obj2.nodes
                            bipartite_layer_networkx_nodes = bipartite_layer_networkx.nodes
                            new_bipartite_layer_networkx_nodes = two_multiplex_nodes - bipartite_layer_networkx_nodes
                            
                            bipartite_layer_networkx.add_nodes_from(new_bipartite_layer_networkx_nodes)

                            B = networkx.to_scipy_sparse_array(bipartite_layer_networkx, nodelist=two_multiplex_nodes, format="csr")    
                            # in __init__:
                            # self.multiplexall_node_list2d = [multiplexall.nodes for multiplexall in multiplexall.multiplex_tuple]
                            self._bipartite_matrix[j, i] = B[0:len(self.multiplexall_node_list2d[i]), len(self.multiplexall_node_list2d[i])::].T
                            if bipartite_layer_networkx.is_directed() == False :
                            	self._bipartite_matrix[i, j] = self._bipartite_matrix[j, i].T
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
