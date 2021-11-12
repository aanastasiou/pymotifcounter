====================
Supported algorithms
====================

.. csv-table:: Overview
    :header: Algorithm, Motif size range, Multi-threading, Prob. Counting, Key publication, More information
    :widths: auto
    :align: center

    ``mfinder``, :math:`3 \le s \le 8`, No, Yes, Network Motifs: Simple Building Blocks of Complex Networks [3]_, `Website <https://www.weizmann.ac.il/mcb/UriAlon/download/network-motif-software>`_
    ``fanmod``, :math:`3 \le s` [#]_, No, Yes, FANMOD: a tool for fast network motif detection [4]_, `Website <https://github.com/aanastasiou/fanmod-cmd>`_ [#]_
    ``NetMODE``, :math:`3 \le k \le 6`, Yes, No, NetMODE: Network Motif Detection without Nauty [5]_, `Website <https://sourceforge.net/projects/netmode/>`_

Notes
-----

* ``mfinder`` reports a motif class even if it has zero samples enumerated
    * ``NetMODE`` reports only those that were enumerated.


.. [#] ``fanmod`` itself does not enforce a strict limit to the size of motifs it can enumerate but the underlying
       `nauty <https://pallini.di.uniroma1.it/>`_ library will complain for motif sizes greater than 8.
.. [#] Please note that `the original fanmod `website <http://theinf1.informatik.uni-jena.de/motifs/>`_ is no
       longer accessible. The original ``fanmod`` was operated *only* via a ``wxwidgets`` Graphical User
       Interface (GUI). Subsequent work (by `Sebastian Bücker <https://github.com/gabbage/fanmod-cmd>`_) produced
       ``fanmod_cmd`` and that version was used as the basis for `the code-base that produces the binary
       used in this project <https://github.com/aanastasiou/fanmod-cmd>`_.

.. [3] `Milo R., Shen-Orr S., Itzkovitz S., Kashtan N., Chklovskii D., and Alon U., ‘Network Motifs: Simple Building Blocks of Complex Networks’, Science, vol. 298, no. 5594, pp. 824–827, Oct. 2002, doi: 10.1126/science.298.5594.824. <https://www.cs.cornell.edu/courses/cs6241/2019sp/readings/Milo-2002-motifs.pdf>`_
.. [4] `S. Wernicke and F. Rasche, ‘FANMOD: a tool for fast network motif detection’, Bioinformatics, vol. 22, no. 9, pp. 1152–1153, May 2006, doi: 10.1093/bioinformatics/btl038. <https://academic.oup.com/bioinformatics/article/22/9/1152/199945>`_
.. [5] `X. Li, R. J. Stones, H. Wang, H. Deng, X. Liu, and G. Wang, ‘NetMODE: Network Motif Detection without Nauty’, PLOS ONE, vol. 7, no. 12, p. e50093, Dec. 2012, doi: 10.1371/journal.pone.0050093. <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0050093>`_

