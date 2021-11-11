=================
Detailed Examples
=================

The source code in the following code examples can be copied right from this page by looking for the clipboard
image at the top right-hand corner of the source code box.

Basic Use
=========

* The following example is functional with all counters currently supported by ``PyMotifCounter``.

* To try out another counter, exchange ``PyMotifCounterMfinder`` for one of
  ``PyMotifCounterNetMODE, PyMotifCounterFanmod``

.. literalinclude:: resources/code_examples/basic_usage.py
    :language: Python

.. figure:: resources/fig_dist_motif_3.png
    :alt: Motif distribution of size 3

    Distribution of fully connected motifs of size 3 for a given network.



Parameter values and aliases
============================

* To change a parameter value, address it by its name, just as it would appear in the command line.
* Different authors are using different variable names to refer to the same entity. For example, *motif
  size* might be known as ``s`` in one algorithm but ``k`` in another. ``PyMotifCounter`` has *Parameter Aliases*
  so you can simply use ``motif_size`` and it will be translated to whatever the underlying algorithm uses.
* Let's visualise the motif distribution of size 4 and 5 motifs here:

.. literalinclude:: resources/code_examples/params_and_aliases.py
    :language: Python

.. figure:: resources/fig_dist_motif_4_5_sb.png
    :alt: Motif distribution for the classes of size 4 and size 5 fully connected motifs

    Motif distributions for motifs of size 4 and size 5.



Visualising motifs
==================

* Motif IDs translate to the adjacency matrix of the subgraph they describe.
* ``PyMotifCounter`` contains a function that can return that adjacency matrix for any further use.
* One of those uses might be to actually visualise the motif subgraph. Let's do that here:
* For more motif subgraphs, see `this motif dictionary <https://www.weizmann.ac.il/mcb/UriAlon/sites/mcb.UriAlon/files/uploads/NetworkMotifsSW/mfinder/motifdictionary.pdf>`_ [#]_

.. literalinclude:: resources/code_examples/params_and_aliases.py
    :language: Python


.. figure:: resources/fig_motif_98_3.png
    :alt: Motif 98 from the s 3 class, a directed 3-cycle

    Motif 98, from the class of fully connected motifs of size 3 is a directed 3-cycle.

.. [#] Motif dictionary linked from the `Uri Alon Lab <https://www.weizmann.ac.il/mcb/UriAlon/download/network-motif-software>`_, developers
       of ``mfinder``.