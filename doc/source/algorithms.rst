====================
Supported algorithms
====================

+=============+============================================+
| Algorithm   | Motif range enumerated                     |
+=============+============================================+
| ``mfinder`` | :math:`s \in \left\{ 3 \ldots 8 \right\}`  |
| ``fanmod``  | :math:`s \in \left\{3 \ldots 8 \right\}`   |
| ``NetMODE`` | :math:`k \in \left\{3 \ldots 6 \right\}`   |
+-------------+--------------------------------------------+


1. ``mfinder``
    * `Website <https://www.weizmann.ac.il/mcb/UriAlon/download/network-motif-software>`_
    * To compile ``mfinder`` in 2021, you have to add ``-fcommon`` to ``CFLAGS``.
        * See https://stackoverflow.com/questions/36209788/gcc-multiple-definition-of-error

2. ``fanmod``
    * `Website <https://github.com/aanastasiou/fanmod-cmd>`_
    * The original ``fanmod`` was operated *only* via a ``wxwidgets`` Graphical User
      Interface (GUI). Subsequent work produced ``fanmod_cmd`` and that version
      was used as the basis for the code that produces the ``fanmod_cmd`` binary
      used in this project.

3. ``NetMODE``
    * `Website <https://sourceforge.net/projects/netmode/>`_
    * `Paper <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0050093>`_

* ``mfinder`` calculates motifs all the way to motif size 3-8
* ``NetMODE`` calculates motifs all the way to motif size 3-6
* ``mfinder`` reports a motif class even if it has zero samples enumerated
* ``NetMODE`` reports only those that were enumerated.
