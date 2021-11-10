.. PyMotifCounter documentation master file, created by
   sphinx-quickstart on Wed Oct 20 13:10:29 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyMotifCounter's documentation!
==========================================

PyMotifCounter offers a unified interface around a number of fast algorithms that 
enumerate network motifs in large networks. The algorithms currently supported are:

* ``mfinder``
* ``fanmod``
* ``NetMODE``
* ``PGD``

PyMotifCounter provides abstractions for the input format, processing parameters (and their validation) and 
output format to return a **computable form** of the enumeration.

A typical example of its usage is as follows: ::

    from pymotifcounter.concretecounters import PyMotifCounterNetMODE
    from matplotlib import pyplot as plt
    import networkx
    
    if __name__ == "__main__":
        # Create an example network
        g = networkx.watts_strogatz_graph(100,8,0.06)
        # Create a motif counter based on NetMODE
        motif_counter = PyMotifCounterNetMODE()
        # Produce the enumeration
        g_motif_count = motif_counter(g)
        # Examine the enumeration via a bar plot
        g_motif_count.plot.bar("gID", "freq");
        plt.show()



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   motivation
   design_notes
   current_todos
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
