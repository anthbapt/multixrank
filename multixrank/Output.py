import os
import pandas
import pathlib
from scipy.stats import stats


class Output:

    def __init__(self, rwr_df, multiplexall, top: int):

        self.rwr_result_list = rwr_df
        self.multiplexall = multiplexall

        self._df = rwr_df

        multiplex_node_prob_zero_df = self._df.loc[self._df.score == 0][['multiplex', 'node']].drop_duplicates()
        multiplex_node_prob_zero_df['score'] = 0
        self._df = (self._df.loc[self._df.score > 0]).groupby(['multiplex', 'node']).agg({'score': stats.gmean}).reset_index()
        self._df = pandas.concat([multiplex_node_prob_zero_df, self._df], axis=0)
        self._df = self._df.drop_duplicates(['multiplex', 'node'], keep='first')
        self._df.sort_values('score', ascending=False, inplace=True)

        #######################################################################
        #
        # Keep only top k nodes
        #
        #######################################################################

        if not (top is None):
            self._df = self._df.groupby('multiplex').head(top)

    def to_sif(self, bipartiteall, path: str):
        pathlib.Path(os.path.dirname(path)).mkdir(exist_ok=True, parents=True)
        out_lst = []  # list of edges with relation type to write
        selected_nodes = self._df.node.tolist()

        # Multiplex undirected edges
        for u, v, edgeidx in self.multiplexall.multigraph.edges:
            if (u in selected_nodes) or (v in selected_nodes):
                edge_data_dic = self.multiplexall.multigraph.get_edge_data(u, v, edgeidx)
                out_lst.append((u, edge_data_dic['network_key'], v))

        # Multiplex directed edges
        for u, v, edgeidx in self.multiplexall.multidigraph.edges:
            if u in selected_nodes or v in selected_nodes:
                edge_data_dic = self.multiplexall.multigraph.get_edge_data(u, v)
                for edge_key in edge_data_dic:
                    out_lst.append((u, edge_data_dic['network_key'], v))

        # Bipartite undirected edges
        for u, v in bipartiteall.graph.edges:
            if u in selected_nodes or v in selected_nodes:
                edge_data_dic = bipartiteall.graph.get_edge_data(u, v)
                out_lst.append((u, edge_data_dic['network_key'], v))

        # Bipartite directed edges
        for u, v in bipartiteall.digraph.edges:
            if u in selected_nodes or v in selected_nodes:
                edge_data_dic = bipartiteall.digraph.get_edge_data(u, v)
                out_lst.append((u, edge_data_dic['network_key'], v))

        out_df = pandas.DataFrame(out_lst, columns=['node1', 'relationship_type', 'node2'], dtype=str)
        out_df.to_csv(path, sep="\t", header=False, index=False)

    def to_tsv(self, outdir: str, degree: bool):
        pathlib.Path(outdir).mkdir(exist_ok=True, parents=True)
        out_df = self._df

        #######################################################################
        #
        # Annotate nodes with layers and degrees
        #
        #######################################################################

        if degree:

            undirdegree_df = pandas.DataFrame(columns=['multiplex', 'layer', 'node', 'degree'])
            inoutdegree_df = pandas.DataFrame(columns=['multiplex', 'layer', 'node', 'indegree', 'outdegree'])

            for multiplex in self.multiplexall.multiplex_tuple:
                for layer in multiplex.layer_tuple:
                    if layer.graph_type[0] == '0':  # undirected graph
                        degree_layer_df = pandas.DataFrame(layer.networkx.degree, columns=['node', 'degree'])
                        degree_layer_df['multiplex'] = multiplex.key
                        degree_layer_df['layer'] = layer.key
                        undirdegree_df = pandas.concat([undirdegree_df, degree_layer_df], axis=0)

                    if layer.graph_type[0] == '1':  # directed graph
                        indegree_layer_df = pandas.DataFrame(layer.networkx.in_degree, columns=['node', 'indegree'])
                        outdegree_layer_df = pandas.DataFrame(layer.networkx.out_degree, columns=['node', 'outdegree'])
                        inoutdegree_layer_df = indegree_layer_df.merge(outdegree_layer_df, on='node')
                        inoutdegree_layer_df['multiplex'] = multiplex.key
                        inoutdegree_layer_df['layer'] = layer.key
                        inoutdegree_df = pandas.concat([inoutdegree_df, inoutdegree_layer_df], axis=0)

            degree_out_df = pandas.concat([undirdegree_df, inoutdegree_df], axis=0)
            out_df = out_df.merge(degree_out_df, on=['multiplex', 'node'])

        out_df.dropna(axis=1, how='all', inplace=True)  # drop columns where all nan

        #######################################################################
        #
        # To csv
        # Will write one file per multiplex
        #
        #######################################################################

        for multiplex in sorted(out_df.multiplex.unique()):

            out_i_df = out_df.loc[out_df.multiplex == multiplex]
            multiplex_tsv_path = os.path.join(outdir, "multiplex_" + str(multiplex) + ".tsv")
            out_i_df.to_csv(multiplex_tsv_path, sep='\t', index=False, header=True, na_rep='NA')

        return out_df
