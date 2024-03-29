.. PyMotifCounter documentation master file, created by
   sphinx-quickstart on Wed Oct 20 13:10:29 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyMotifCounter's documentation!
==========================================

``PyMotifCounter`` is a unified interface to fast motif enumeration algorithms such as:

* ``mfinder``
* ``fanmod``
* ``NetMODE``
* ``PGD``

The objective of this version is to offer an interface to external processes as if they were
Python functions.

This is achieved by abstracting the inputs, parameters and outputs of each binary, creating a high
level interface which accepts a ``networkx`` graph and returns a motif / graphlet distribution as a
``pandas.DataFrame``.

A typical usage example is as follows:

.. literalinclude:: resources/code_examples/basic_usage.py
   :language: Python

Which would produce the following distribution:

.. figure:: resources/figures/fig_dist_motif_3.png
    :alt: Motif distribution of size 3



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   examples
   algorithms
   motivation
   design_notes
   current_todos
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
