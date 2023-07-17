.. _personalised_pagerank:

Personalised PageRank
========================

By default, multiXrank uses a set of seed(s) to define the initial restart probability of the random walk with restart. 
However, is possible to bypass this selection of seed(s) by using an ad-hoc initial restart probability.
This ad-hoc initial restart probability is defined as a normalised distribution of all the nodes. 
Please note that this normalised distribution does not take into account the replica nodes (node duplicate in each layer of the multiplex network).

The code provided below illustrates the use of an ad-hoc initial restart probability.

In this section, we will consider the airport multilayer network described in the Quick start section.
This multilayer network is composed of the following networks:

.. code-block:: bash

    `-- airport
        |-- bipartite
        |   |-- 1_2.tsv
        |   |-- 1_3.tsv
        |   `-- 2_3.tsv
        |-- multiplex
        |   |-- 1
        |   |   |-- FR26.tsv
        |   |   |-- FR3.tsv
        |   |   `-- FR7.tsv
        |   |-- 2
        |   |   |-- UK15.tsv
        |   |   |-- UK26.tsv
        |   |   `-- UK3.tsv
        |   `-- 3
        |       |-- G1.tsv
        |       |-- G24.tsv
        |       `-- G6.tsv

Notably, in the multilayer network considered here, there are 69 nodes: 18 nodes in the first multiplex network, 28 in the second multiplex network, and 23 in the third multiplex network.


.. code-block:: python

    import numpy as np
    import multixrank

    num_nodes = 69
    proba_init = np.ones(num_nodes)/num_nodes
    multixrank.Example().write(path="airport_test")
    multixrank_obj = multixrank.Multixrank(config="airport_test/config_minimal.yml", wdir="airport_test", pr = proba_init)
    ranking_df = multixrank_obj.random_walk_rank()
    multixrank_obj.write_ranking(ranking_df, path="output_airport_test")

We remark that if the initial probability distribution is uniform, then this approach is the well-known PageRank method [1].

However if the number of layers in the different multiplex is different, the probability distribution will not be uniform. This is come from :math:`p_{kj} = \frac{p_{k}}{L_{i}}`, with 
:math:`p_{kj}` being the score of the node :math:`k` in the layer :math:`j` of the multiplex network :math:`i`, and :math:`L_{i}` being the number of layers in the multiplex network :math:`i`.

[1] **Brin, S., and Page, L.** The anatomy of a large-scale hypertextual Web search engine Computer Networks and ISDN Systems , Vol. 30, No. 1 p. 107 - 117 (1998)
