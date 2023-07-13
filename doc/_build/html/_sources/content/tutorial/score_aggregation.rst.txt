.. _score_aggregation:

Score aggregations
========================

In multiXrank version v.0.1, the scores of the nodes in the different layers of each multiplex network were aggregated using a geometric mean.
In the latest version of multiXrank (v.0.2), the user can choose an aggregation strategy between the following ones:

    * nomean: non-aggregated score
        .. math::
            x_{k} = [p_{k1}, p_{k2}, ..., p_{kL_{i}}]
    * mean: arithmetic mean
        .. math::
            x_{k} = \frac{ \sum_{j=0}^{L_{i}} p_{kj} }{L_{i}} 
    * gmean: geometric mean
        .. math::
            x_{k} = \sqrt[L_{i}]{ \prod_{j=0}^{L_{i}} p_{kj} }
    * hmean: harmonic mean
        .. math::
            x_{k} = \frac{ L_{i} }{ \sum_{j=0}^{L_{i}} \frac{1}{ p_{kj}} }
    * sum: sum of nodes score through each layer
        .. math::
            x_{k} = \sum_{j=0}^{L_{i}} p_{kj}

where :math:`x_{k}` is the score of the node :math:`k`, :math:`L_{i}` is the number of layers in the multiplex network :math:`i`, :math:`p_{kj}` is 
the score of the node :math:`k` in the layer :math:`j` of the multiplex network :math:`i`.

By default, the aggregation uses the geometric mean. If the user wants to use another aggregation strategy (or output non-aggregated scores), the following code can be adapted.

.. code-block:: python

    import multixrank
    multixrank_obj = multixrank.Multixrank(config="airport/config_minimal.yml", wdir="airport")
    ranking_df = multixrank_obj.random_walk_rank()
    multixrank_obj.write_ranking(ranking_df, path="output_airport", aggregation = "mean")
    
    

The example code presented above uses the airport multilayer network described in the Quick start section.
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



