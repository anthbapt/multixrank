import networkx

from concurrent.futures import ThreadPoolExecutor
from itertools import chain
import os

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
            self._multidigraph = networkx.MultiGraph().to_directed()
            for multiplex in self.multiplex_tuple:
                if networkx.is_directed(multiplex.multidigraph) == True:
                    self._multidigraph = networkx.compose(self._multidigraph, multiplex.multidigraph)
                else:
                    multiplex.multidigraph = multiplex.multidigraph.to_directed()
                    self._multidigraph = networkx.compose(self._multidigraph, multiplex.multidigraph)
        return self._multidigraph

    @property
    def multigraph3(self) -> networkx.MultiGraph:
        """Creates undirected networkx multigraph"""

        if self._multigraph is None:
            self._multigraph = networkx.MultiGraph()
            # Use generators to efficiently aggregate nodes and edges
            all_nodes = (
                node 
                for multiplex in self.multiplex_tuple 
                for node in multiplex.multigraph.nodes(data=True)
            )
            all_edges = (
                edge 
                for multiplex in self.multiplex_tuple 
                for edge in multiplex.multigraph.edges(keys=True, data=True)
            )
            # Bulk add nodes and edges
            self._multigraph.add_nodes_from(all_nodes)
            self._multigraph.add_edges_from(all_edges)

        return self._multigraph

    def extract_multigraph_data(self, multiplex):
        """Helper function to extract nodes and edges from a single multiplex."""
        nodes = list(multiplex.multigraph.nodes(data=True))
        edges = list(multiplex.multigraph.edges(keys=True, data=True))
        return nodes, edges

    @property
    def multigraph8(self) -> networkx.MultiGraph:
        """Creates undirected networkx multigraph"""
        
        if self._multigraph is None:
            self._multigraph = networkx.MultiGraph()

            # Calculate thread pool size based on CPU count and workload size
            max_workers = min(os.cpu_count() or 2, len(self.multiplex_tuple))

            # Parallelize extraction using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(self.extract_multigraph_data, self.multiplex_tuple))

            # Bulk add nodes and edges
            self._multigraph.add_nodes_from(chain.from_iterable(n for n, _ in results))
            self._multigraph.add_edges_from(chain.from_iterable(e for _, e in results))

        return self._multigraph

    def merge_graphs(self, graphs):
        """Helper function to build self._multigraph with other graphs."""
        for g in graphs:

            self._multigraph.add_nodes_from(g.nodes(data=True))

            # Directly inject edges into adjacency structure
            for u, v, key, data in g.edges(keys=True, data=True):
                # Update u -> v direction
                if u not in self._multigraph._adj:
                    self._multigraph._adj[u] = {}
                u_adj = self._multigraph._adj[u]
                if v not in u_adj:
                    u_adj[v] = {}
                u_adj[v][key] = data

                # Update v -> u direction (undirected graph)
                if v not in self._multigraph._adj:
                    self._multigraph._adj[v] = {}
                v_adj = self._multigraph._adj[v]
                if u not in v_adj:
                    v_adj[u] = {}
                v_adj[u][key] = data
        

    @property
    def multigraph(self) -> networkx.MultiGraph:
        """Creates undirected networkx multigraph"""
        
        if self._multigraph is None:
            self._multigraph = networkx.MultiGraph()

            # Calculate thread pool size based on CPU count and workload size
            max_workers = min(os.cpu_count() or 2, len(self.multiplex_tuple))

            # Parallelize extraction using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                graphs = list(executor.map(
                    lambda m: m.multigraph,
                    self.multiplex_tuple
                ))

            self.merge_graphs(graphs)

        return self._multigraph

    @property
    def multigraph_old(self) -> networkx.MultiGraph:
        """Creates undirected networkx multigraph"""

        if self._multigraph is None:
            self._multigraph = networkx.MultiGraph()
            for multiplex in self.multiplex_tuple:
                self._multigraph = networkx.compose(self._multigraph, multiplex.multigraph_old)

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
