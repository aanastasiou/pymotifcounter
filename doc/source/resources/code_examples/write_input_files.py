"""
Creates data for a small population of networks
from two structural classes: Small-World and Random networks.
"""

from pymotifcounter.concretecounters import (PyMotifCounterInputTransformerMfinder,
                                             PyMotifCounterInputTransformerFanmod,
                                             PyMotifCounterInputTransformerNetMODE)
import networkx

N_NETWORKS = 3  # Number of networks in each class
N_NODES = 100   # Number of nodes in each network
K_AVERAGE = 8   # Average node degree

# The active transformer determines the format.
# This example saves the networks in the format expected by mfinder
# Assign the ACTIVE_TRANSFORMER to one of the other imported
# transformers to change the format.
ACTIVE_TRANSFORMER = PyMotifCounterInputTransformerMfinder

if __name__ == "__main__":
    # Prepare N_NETWORKS small-world networks
    networks = [networkx.watts_strogatz_graph(N_NODES,
                                              K_AVERAGE,
                                              0.08)
                for k in range(0, N_NETWORKS)]

    # Prepare N_NETWORKS random networks
    networks += [networkx.watts_strogatz_graph(N_NODES,
                                               K_AVERAGE,
                                               0.9)
                 for k in range(0, N_NETWORKS)]


    # Write everything to THE CURRENT WORKING DIRECTORY in
    # the format expected by mfinder
    for a_net_id, a_network in enumerate(networks):
        ACTIVE_TRANSFORMER().to_file(a_network,
                                     f"net_data_{a_net_id}")
