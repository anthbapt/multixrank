=============================================================================================
MultiXrank - Universal Multilayer Exploration by Random Walk with Restart
=============================================================================================

.. image:: https://img.shields.io/pypi/v/multixrank.svg
    :target: https://pypi.python.org/pypi/multixrank

.. image:: https://img.shields.io/pypi/pyversions/multixrank.svg
    :target: https://www.python.org

.. image:: https://readthedocs.org/projects/multixrank-doc/badge/?version=latest
    :target: https://multixrank-doc.readthedocs.io/en/latest/?badge=latest
    
.. image:: https://travis-ci.com/anthbapt/multixrank.svg?branch=master
    :target: https://app.travis-ci.com/anthbapt/multixrank

.. image:: https://github.com/anthbapt/multixrank/workflows/CI/badge.svg
    :target: https://github.com/anthbapt/multixrank/actions?query=branch%3Amaster+workflow%3ACI
    

MultiXrank is a Python package for the exploration of heterogeneous multilayer networks, with random walk with restart method. It permits prioritization of nodes between full heterogeneous networks, whatever their complexities.
If you use MultiXrank in scientific works, **please cite the following article**:

**Baptista, A., González, A., Baudot, A.**.
`Universal Multilayer Network Exploration by Random Walk with Restart`, arXiv:2107.04565.

Commands for a quick installation:

.. code-block:: bash

    conda create --name multixrank python=3.10 -y
    python3 -m pip install multixrank

Commands for a quick working example in the python console:

.. code-block:: python

    import multixrank
    multixrank.Example().write(path="airport")

This generates a working example based on the "airport" multiplex:

.. code-block:: bash

    `-- airport
        |-- bipartite
        |   |-- 1_2.tsv
        |   |-- 1_3.tsv
        |   `-- 2_3.tsv
        |-- config_minimal.yml
        |-- multiplex
        |   |-- 1
        |   |   |-- FR26.tsv
        |   |   |-- FR3.tsv
        |   |   |-- FR3_2.tsv
        |   |   `-- FR7.tsv
        |   |-- 2
        |   |   |-- UK15.tsv
        |   |   |-- UK26.tsv
        |   |   `-- UK3.tsv
        |   `-- 3
        |       |-- G1.tsv
        |       |-- G24.tsv
        |       `-- G6.tsv
        `-- seeds.txt

The minimal configuration file 'config.yml' looks like this.

.. code-block:: bash

    multiplex:
        1:
            layers:
                - multiplex/1/FR26.tsv
                - multiplex/1/FR3.tsv
                - multiplex/1/FR7.tsv
        2:
            layers:
                - multiplex/2/UK15.tsv
                - multiplex/2/UK26.tsv
                - multiplex/2/UK3.tsv
        3:
            layers:
                - multiplex/3/G1.tsv
                - multiplex/3/G24.tsv
                - multiplex/3/G6.tsv
    bipartite:
        bipartite/1_2.tsv:
            source: 1
            target: 2
        bipartite/1_3.tsv:
            source: 1
            target: 3
        bipartite/2_3.tsv:
            source: 2
            target: 3
    seed:
        seeds.txt

.. code-block:: python

    import multixrank
    multixrank_obj = multixrank.Multixrank(config="airport/config_minimal.yml", wdir="airport")
    ranking_df = multixrank_obj.random_walk_rank()
    multixrank_obj.write_ranking(ranking_df, path="output_airport")
    multixrank_obj.to_sif(ranking_df, path="output_airport/airport_seed7_top3.sif", top=3)

This runs the software and writes the results to the output_airport folder:

.. code-block:: bash

    $ ls output_airport/
    airport_seed7_top3.sif  multiplex_1.tsv  multiplex_2.tsv  multiplex_3.tsv

There is a ranking file for each multiplex:

.. code-block:: bash

    $ head -n 4 output_airport/multiplex_1.tsv
    multiplex	node	score
    1	7	0.250002565842259
    1	169	0.0025983048938841304
    1	199	0.0018837852068513332

The `MultiXrank documentation <https://multixrank-doc.readthedocs.io/>`_ is hosted at ReadTheDocs.

MultiXrank is maintained by Anthony Baptista (anthony dot baptista at univ-amu dot fr) and Aitor González (aitor dot gonzalez at univ-amu dot fr)
