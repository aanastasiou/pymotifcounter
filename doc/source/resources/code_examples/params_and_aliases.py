"""
Visualise the distribution of size-k motifs, for k \in {4,5}.
"""

from pymotifcounter.concretecounters import PyMotifCounterMfinder
from matplotlib import pyplot as plt
from networkx import watts_strogatz_graph

if __name__ == "__main__":
    # Create an example network
    g = watts_strogatz_graph(100, 8, 0.2)
    # Create a motif counter based on mfinder
    motif_counter = PyMotifCounterMfinder()
    # The default value of parameter motif-size is 3.
    # Let's change it to 4
    motif_counter.get_parameter("s").value = 4
    # Produce the enumeration
    g_mtf_4_count = motif_counter(g)

    # mfinder calls the motif_size (s) but NetMODE calls it
    # (k). If you change enumerator to NetMODE, this code will
    # raise an exception.
    #
    # BUT!!!
    #
    # Semantically common variables for all algorithms can be addressed
    # with common names.
    # Notice here how motif size is changed to 5.
    #
    motif_counter.get_parameter("motif_size").value = 5
    # Produce the enumeration
    g_mtf_5_count = motif_counter(g)

    # Visualise distributions
    sb_ax = plt.subplot(211)
    plt.title("Motif size 4 distribution.")
    g_mtf_4_count.plot.bar("motif_id", "nreal", ax=sb_ax)

    sb_ax = plt.subplot(212)
    plt.title("Motif size 5 distribution.")
    g_mtf_5_count.plot.bar("motif_id", "nreal", ax=sb_ax)
    plt.tight_layout()

    plt.show()