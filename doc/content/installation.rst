Installation
=================================================

Commands for a quick installation:

.. code-block:: bash

    conda create --name multixrank python=3.10 -y
    python3 -m pip install multixrank

We also provide a singularity container in the multixrank github: https://github.com/anthbapt/multixrank .
First the image is built with this command as root:

.. code-block:: bash

    sudo singularity build multixrank.sif multixrank.singularity

Then you can use multixrank directly from the singularity image:

.. code-block:: bash

    singularity exec multixrank.sif python -c 'import multixrank'
