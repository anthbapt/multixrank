**Changes In Version 0.2 (Jul 11, 2023)**

- works with latest version of scipy (v.1.11.1)
- works with latest version of networkx (v.3.1)
- support different mean for the aggregation of scores across the different layers of each multiplex network
	* 'gmean': geometric mean, use by default and the only defined for multiXrank < v.0.2
	* 'mean': arithmetic mean
	* 'hmean': harmonic mean
    	* 'sum': sum of nodes score through each layer
	* 'nomean': output scores of every layers without mean
- support personalised pagerank and pagerank methods

**Changes In Version 0.1 (May 16, 2022)**

- BUG Fixed test lambda parameter
- BUG directed networks fixed

**Changes In Version 0.0.8 (Jul 9, 2021)**

- BUG Fixed default parameters and lambda parameter for one-multiplex-only system
- TST Added tests

**Changes In Version 0.0.7 (Jul 8, 2021)**

- BUG fixed get_normalization_bipartite_alpha_beta
- TST Added biological and hetionet tests

**Changes In Version 0.0.6 (Jun 26, 2021)**

- ENH Print error and exit if multiplex or bipartite emp

**Changes In Version 0.0.5 (Jun 26, 2021)**

- BUG fixed BipartiteAll matrix

**Changes In Version 0.0.4 (Jun 24, 2021)**

- BUG Fixed self_loops parameter

**Changes In Version 0.0.3 (Jun 22, 2021)**

- BUG Fixed weighted networks bug
- ENH Added Boolean self_loops parameter to keep or not self-loops
- RFR TSV output gives one file per multiplex
- RFR Boolean codes with first digit=directed, second digit=weighted: 00, 01, 10, 11.
- BUG Fixed transition matrix

**Changes In Version 0.0.2 (Mai 7, 2021)**

- DOC Large documentation changes
- ENH File and parameter inputs defined in YAML config file
- RFR Large refactoring of the code into different classes
- TST More tests

**Changes In Version 0.0.1 (April 1, 2021)**

- Original code of Anthony Baptista reformatted for a python package

