.. _algorithms:

====================
Supported algorithms
====================

.. csv-table:: Overview
    :header: Algorithm, Motif size range, Directed / Undirected, Multi-threading, Prob. Counting, Key publication, More information
    :widths: auto
    :align: center

    ``mfinder``, :math:`3 \le s \le 8`, Both, No, Yes, Network Motifs: Simple Building Blocks of Complex Networks [3]_, `Website <https://www.weizmann.ac.il/mcb/UriAlon/download/network-motif-software>`_
    ``fanmod``, :math:`3 \le s` [#]_, Both, No, Yes, FANMOD: a tool for fast network motif detection [4]_, `Website <https://github.com/aanastasiou/fanmod-cmd>`_ [#]_
    ``NetMODE``, :math:`3 \le k \le 6`, Both, Yes, No, NetMODE: Network Motif Detection without Nauty [5]_, `Website <https://sourceforge.net/projects/netmode/>`_
    ``PGD``, :math:`2 \le k \le 4`, Undirected, Yes, No, Efficient Graphlet Counting for Large Networks [6]_, `Website <http://graphlets.org/>`_

Notes
-----

* ``mfinder`` reports a motif class even if it has zero samples enumerated
    * ``NetMODE`` reports only those that were enumerated.

* ``pgd`` reports a motif distribution for *undirected* motifs of size :math:`2,3,4` *simultaneously*,
  as a result of the same "run".
      * Because of the way ``pgd`` reports its results, the ``motif_id`` is given in the format ``(motif_id, N_NODES)``.
      * Both of these numbers can be used with the :ref:``motif_id_to_adj_mat()`` to reconstruct the adjacency matrix
        without *ambiguity*.



.. [#] ``fanmod`` itself does not enforce a strict limit to the size of motifs it can enumerate but the underlying
       `nauty <https://pallini.di.uniroma1.it/>`_ library will complain for motif sizes greater than 8.
.. [#] Please note that `the original fanmod `website <http://theinf1.informatik.uni-jena.de/motifs/>`_ is no
       longer accessible. An `Internet Archive snapshot of it can be found here <https://web.archive.org/web/20180805111938/http://theinf1.informatik.uni-jena.de/motifs/>`_.
       The original ``fanmod`` was operated *only* via a ``wxwidgets`` Graphical User
       Interface (GUI). Subsequent work (by `Sebastian Bücker <https://github.com/gabbage/fanmod-cmd>`_) produced
       ``fanmod_cmd`` and that version was used as the basis for `the code-base that produces the binary
       used in this project <https://github.com/aanastasiou/fanmod-cmd>`_.

.. [3] `Milo R., Shen-Orr S., Itzkovitz S., Kashtan N., Chklovskii D., and Alon U., ‘Network Motifs: Simple Building Blocks of Complex Networks’, Science, vol. 298, no. 5594, pp. 824–827, Oct. 2002, doi: 10.1126/science.298.5594.824. <https://www.cs.cornell.edu/courses/cs6241/2019sp/readings/Milo-2002-motifs.pdf>`_
.. [4] `S. Wernicke and F. Rasche, ‘FANMOD: a tool for fast network motif detection’, Bioinformatics, vol. 22, no. 9, pp. 1152–1153, May 2006, doi: 10.1093/bioinformatics/btl038. <https://academic.oup.com/bioinformatics/article/22/9/1152/199945>`_
.. [5] `X. Li, R. J. Stones, H. Wang, H. Deng, X. Liu, and G. Wang, ‘NetMODE: Network Motif Detection without Nauty’, PLOS ONE, vol. 7, no. 12, p. e50093, Dec. 2012, doi: 10.1371/journal.pone.0050093. <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0050093>`_
.. [6] `N. K. Ahmed, J. Neville, R. A. Rossi, and N. Duffield, ‘Efficient Graphlet Counting for Large Networks’, in 2015 IEEE International Conference on Data Mining, Nov. 2015, pp. 1–10. doi: 10.1109/ICDM.2015.141. <https://ieeexplore.ieee.org/document/7373304>`_


