"""
Visualise a motif's graph, given its ID.
"""

from pymotifcounter.util import motif_id_to_adj_mat
from matplotlib import pyplot as plt
import networkx

if __name__ == "__main__":
    # Get the adjacency matrix of a motif given its ID and the size
    # of its "motif class".
    #
    # Here, we are trying to visualise motif 98 from the class of
    # fully connected motifs of size 3.
    motif_6_a = motif_id_to_adj_mat(98, 3)

    # From here onwards, use standard networkx functions
    # to visualise the motif subgraph
    motif_g = networkx.from_numpy_array(motif_6_a,
                                        create_using=networkx.DiGraph)

    networkx.draw_spectral(motif_g)
    plt.tight_layout()
    plt.show()