==============
PyMotifCounter
==============

A unified Python interface to fast motif enumeration algorithms such as:

* ``mfinder``
* ``fanmod``
* ``NetMODE``
* ``PGD``

A typical usage example is as follows:

.. code-block:: Python

    """
    Visualise the distribution of size-3 motifs.
    """

    from pymotifcounter.concretecounters import PyMotifCounterMfinder
    from matplotlib import pyplot as plt
    from networkx import watts_strogatz_graph

    if __name__ == "__main__":
        # Create an example network
        g = watts_strogatz_graph(100, 8, 0.2)
        # Create a motif counter based on mfinder
        motif_counter = PyMotifCounterMfinder()
        # Enumerate motifs using the selected counter
        g_mtf_count = motif_counter(g)
        # Visualise the distribution
        g_mtf_count.plot.bar("motif_id", "nreal")
        plt.tight_layout()
        plt.show()

Which would produce the following distribution:

.. image:: https://github.com/aanastasiou/pymotifcounter/blob/main/doc/source/resources/figures/fig_dist_motif_3.png?raw=true

Installation
------------
* Latest release can be installed from pypi by ``> pip install pymotifcounter``.

* Latest development version can be obtained by `cloning this repository <https://github.com/aanastasiou/pymotifcounter>`_

* For more details please see `the project's documentation on readthedocs <https://pymotifcounter.readthedocs.io/en/latest/>`_

