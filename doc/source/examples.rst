=================
Detailed Examples
=================

Basic Use
=========

::

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


Changing parameter values
=========================

Continuing from the above example, let's get the distribution for motifs of size 4.

::

        # Enumerate motifs of size 4
        motif_counter.set_parameter_value("s",4)
        g_motif_count = motif_counter(g)
        g_motif_count.plot.bar("gID", "freq");
        plt.show()
