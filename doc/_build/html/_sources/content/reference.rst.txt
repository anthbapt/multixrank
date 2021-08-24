Reference
===================================

Initialization, random walk function and output
--------------------------------------------------

These are the main multixrank methods.

.. automodule:: multixrank.Multixrank
    :members: random_walk_rank,write_ranking,to_sif
    :special-members: __init__

Example class
--------------------------------

There is a class to generate a working example.

.. automodule:: multixrank.Example
    :members: write
    :special-members: __init__

.. _reference_configuration:

Configuration and network files
--------------------------------

This configuration file defines network paths, multiplexes, bipartites and numerical parameters for the random walk.
A working example can be found in the :ref:`Tutorial <tutorial>` section.

This is an example of a minimal configuration YAML file: :download:`config_minimal.yml <../../multixrank/data_example/airport/config_minimal.yml>`

This is an example of a configuration YAML file with all parameters: :download:`config_full.yml <../../multixrank/data_example/airport/config_full.yml>`

Multiplex and bipartite **unweighted** networks are given as two-column TSV files without a header.
This is an example: :download:`FR3.tsv <../../multixrank/data_example/airport/multiplex/1/FR3.tsv>`

Multiplex and bipartite **weighted** networks are given as two-column TSV files without a header.
This is an example: :download:`1_3_3columns.tsv <../../multixrank/tests/test_data/airport/bipartite/1_3_3columns.tsv>`

.. _reference_parameter:

Parameters
--------------------------------

Below we explain the numerical parameters needed to run the random walk.

.. figure:: parameters.png
    :alt: Parameter schema
    :align: center
    :width: 600

    MultiXrank RWR parameters to explore universal multilayer networks composed of N multiplex networks (each composed of several layers containing the same set of nodes but different edges). The parameters 'delta' are associated with the probability to jump from one layer to another in a given multiplex network, 'lambda' with the probability to jump from one multiplex network to another multiplex network, 'tau' with the probability to restart in a given layer of a given multiplex network, and 'eta' with the probability to restart in a given multiplex network.

**r**

- The global restart probability is given by the float number **r** between 0 and 1

**delta**

- A vector of length equal to the number of multiplex networks with probabilities
- A given element of the delta vector gives the probability to change the layer in a given multiplex network

**tau**

- 'tau' is given as a list of vectors where each vector corresponds to the restart probabilities in each multiplex network
- Elements of each vector correspond to the restart probabilities at the given layer
- For, instance the tau\ :sub:`23`\  corresponds to the restart probability at the third layer of the second multiplex network

**eta**

- The 'eta' parameter vector given the restart probability at a given multiplex network
- A vector of probabilities with length equals to the number of multiplex networks
- This vector sums up to one

**lambda**

The parameter 'lambda' is associated with the probability to jump from one multiplex network to another one.
For instance, lambda\ :sub:`ij`\  represents the probability to jump from the multiplex network i to the multiplex network j.

**graph_type** field: unweighted/weighted, undirected/directed

The multiplex and bipartite graph types as either undirected or directed and unweighted or weighted are given by codes
00, 01, 10 and 11 in the following way:

.. list-table::
   :widths: 60 25 25 25
   :header-rows: 1

   * - Graph type
     - Directed
     - Weighted
     - Code
   * - Undirected, unweighted
     - No
     - No
     - 00
   * - Undirected, weighted
     - No
     - Yes
     - 01
   * - Directed, unweighted
     - Yes
     - No
     - 10
   * - Directed, weighted
     - Yes
     - Yes
     - 11

**self_loops**

- The 'self_loops' parameter defines whether self loops are removed or not
- This parameter is a Boolean and takes values 0 or 1.
- Setting this parameter to 1, it solves the problem of zero columns in the transition matrix if the network was wrongly built.
