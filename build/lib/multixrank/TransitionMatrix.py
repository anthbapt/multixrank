from multixrank import MultiplexAll

import numpy
import scipy


class TransitionMatrix:

    def __init__(self, multiplex_all: MultiplexAll, bipartite_matrix: numpy.array, lamb: numpy.array):

        self.multiplex_all = multiplex_all
        self.bipartite_matrix = bipartite_matrix
        self.lamb = lamb

        self._transition_matrixcoo = None

    @property
    def transition_matrixcoo(self):

        if self._transition_matrixcoo is None:
            bipartite_matrix = self.bipartite_matrix
            self.multiplexall_supra_adj_matrix_list = []
            for i, multiplex_obj in enumerate(self.multiplex_all.multiplex_tuple):
                self.multiplexall_supra_adj_matrix_list.append(multiplex_obj.supra_adj_matrixcoo)

            size1 = len(self.multiplex_all.multiplex_tuple)
            self.get_normalization_Diago()
            transition = numpy.zeros((size1, size1), dtype=object)
            # give full zero block matrix for transition matrix, essential if there
            # are no bipartite
            for i in range(size1):
                diago = self.Diago[:,i]
                transition[i, i] = self.get_normalisation_alpha_alpha(i, self.multiplexall_supra_adj_matrix_list[i], diago)
                for j in range(size1):
                    if j != i:
                        transition[j, i] = self.get_normalization_bipartite_alpha_beta(j, i, bipartite_matrix[j, i], diago)
            self._transition_matrixcoo = scipy.sparse.bmat(transition, format="coo")
        return self._transition_matrixcoo

    # 1.2.3.1 :
    def get_normalization_Diago(self) -> numpy.ndarray:
        """

        Function that determine the column sum of each bipartite matrix for the condition
        concerning the transition matrix alpha_alpha.

        Returns :
                self.Diago (numpy.ndarray) : A ndarray with the column sum of each bipartite matrix.

        """

        bipartite_matrix = self.bipartite_matrix
        # import pdb; pdb.set_trace()
        # multiplexall_node_count_list2d = [len(x) for x in self.multiplexall_node_list2d]
        multiplexall_node_count_list = [len(m.nodes) for m in self.multiplex_all.multiplex_tuple]
        multiplexall_layer_count_list = [len(m.layer_tuple) for m in self.multiplex_all.multiplex_tuple]

        size1 = len(self.multiplex_all.multiplex_tuple)
        self.Diago = numpy.zeros((size1, size1), dtype=object)
        for i in range(size1):
            self.Diago[i, i] = numpy.zeros(multiplexall_node_count_list[i] * multiplexall_layer_count_list[i])
            for j in range(i + 1, size1):
                tot_strength_nodes = (bipartite_matrix[i, j]).sum(axis=0)
                self.Diago[i, j] = numpy.array(list(tot_strength_nodes.flat))
                tot_strength_nodes = (bipartite_matrix[j, i]).sum(axis=0)
                self.Diago[j, i] = numpy.array(list(tot_strength_nodes.flat))
        # import pdb; pdb.set_trace()
        return self.Diago

    # 1.2.3.3 :
    def get_normalisation_alpha_alpha(self, alpha, adjacency, diago) -> scipy.sparse.csr.csr_matrix:
        """

        Function that compute Normalization for the alpha_alpha term of Transition matrix.
        The term alpha_alpha correspond to the supra-adjacency matrix of multiplex alpha.

        Args :
            alpha (int) : Row index of Transition matrix.

            beta (int) : Column index of Transition matrix.

            matrix (scipy.sparse.coo.coo_matrix) : Supra-adjacency matrix for multiplex ithat we want
            to normalize.

        Returns :
                alpha_alpha (scipy.sparse.csr.csr_matrix) : Normalized Supra-adjacency matrix for i .

        """

        # multiplexall_node_count_list = [len(x) for x in self.multiplexall_node_list2d]
        multiplexall_node_count_list = [len(m.nodes) for m in self.multiplex_all.multiplex_tuple]
        multiplexall_layer_count_list = [len(m.layer_tuple) for m in self.multiplex_all.multiplex_tuple]

        # print(adjacency)
        size1 = len(self.multiplex_all.multiplex_tuple)
        tot_strength_nodes_alpha = adjacency.sum(axis=0)
        diago_up = list(tot_strength_nodes_alpha.flat)
        diago_down = list(tot_strength_nodes_alpha.flat)
        
        for k in range(multiplexall_node_count_list[alpha] *
                       multiplexall_layer_count_list[alpha]):
            # add for loop for each element in diago (each element correspond to a bipartite matrix, [i,i] list of 0)
            if sum(diago)[k] == 0 : # pas de bipartite
                diago_up[k] = 0
                if diago_down[k] == 0:
                    diago_down[k] = 1
                else :
                    diago_down[k] = 1/diago_down[k]
            else : # so at least one bipartite no zeros
                diago_down[k] = 0
                list_value_diago = numpy.zeros(len(diago))
                for l in range(len(diago)) :
                    if (diago[l][k] != 0) :
                        list_value_diago[l] = 1
                list_value_diago = list_value_diago*self.lamb[:,alpha].T
                norm = 1
                for l in range(size1) :
                    if (l != alpha) :
                        norm -= list_value_diago[l]
                if diago_up[k] == 0 :
                    diago_up[k] = 1
                else : 
                    diago_up[k] = norm*(1/diago_up[k])
        Normalization_matrix_up = scipy.sparse.diags(diago_up, format = "coo")
        Normalization_matrix_down = scipy.sparse.diags(diago_down, format = "coo")
        Transition_up = adjacency.dot(Normalization_matrix_up)
        Transition_down = adjacency.dot(Normalization_matrix_down) 
        alpha_alpha = Transition_up + Transition_down
        return alpha_alpha

    # 1.2.3.2 :
    def get_normalization_bipartite_alpha_beta(self, alpha, beta,
                                               matrix, diago) -> scipy.sparse.csr.csr_matrix:
        """

        Function that compute Normalization for the alpha_beta term of Transition matrix.
        The term alpha_beta correspond to the bipartite between multiplex alpha and beta.

        Args :
            alpha (int) : Row index of Transition matrix.

            beta (int) : Column index of Transition matrix.

            matrix (scipy.sparse.coo.coo_matrix) : bipartite between i and j that we want to
            normalize.

        Returns :
                alpha_beta (scipy.sparse.csr.csr_matrix) : Normalized bipartite between i and j.

        """

        Tot_strength_nodes = matrix.sum(axis=0)
        # adjacency = self.SupraAdjacencyMatrix[beta].sum(axis=0)  # anthony's script
        adjacency = self.multiplex_all.supra_adj_matrix_list[beta].sum(axis=0)
        adjacency = list(adjacency.flat)
        diago_up = list(Tot_strength_nodes.flat)
        diago_down = list(Tot_strength_nodes.flat)

        # list with layer count for each multiplex
        self_L = [len(x.layer_tuple) for x in self.multiplex_all.multiplex_tuple]
        for k in range(len(diago_up)):
            if (self_L[beta] == 1) and (adjacency[
                                            k] == 0):  # node not in multiplex alpha, only in bip
                diago_up[k] = 0
                list_value_diago = numpy.zeros(len(self_L))
                for l in range(len(self_L)):
                    if (diago[l][k] != 0):
                        list_value_diago[l] = 1
                list_value_diago = list_value_diago * self.lamb[:, beta].T
                norm = 0
                for l in range(len(self_L)):
                    if (l != beta):
                        norm += list_value_diago[l]
                if diago_down[k] == 0:
                    diago_down[k] = 1
                else:
                    diago_down[k] = (self.lamb[alpha, beta] / norm) * (
                                1 / diago_down[k])
            else:  # node in multiplex alpha so standard normalization
                diago_down[k] = 0
                if diago_up[k] == 0:
                    diago_up[k] = 1
                else:
                    diago_up[k] = self.lamb[alpha, beta] * (1 / diago_up[k])
        Normalization_matrix_up = scipy.sparse.diags(diago_up, format="coo")
        Normalization_matrix_down = scipy.sparse.diags(diago_down, format="coo")
        Transition_up = matrix.dot(Normalization_matrix_up)
        Transition_down = matrix.dot(Normalization_matrix_down)
        alpha_beta = Transition_up + Transition_down
        return alpha_beta
