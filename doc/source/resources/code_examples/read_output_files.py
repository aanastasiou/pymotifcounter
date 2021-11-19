"""
Reads motif counts for a small population of motif count results.
"""
from pymotifcounter.concretecounters import (PyMotifCounterOutputTransformerMfinder,
                                             PyMotifCounterOutputTransformerFanmod,
                                             PyMotifCounterOutputTransformerNetMODE)
import glob

# The active transformer determines the format.
# This example reads networks in the format expected by mfinder.
# Assign the ACTIVE_TRANSFORMER to one of the other imported
# transformers to change the format.
ACTIVE_TRANSFORMER = PyMotifCounterOutputTransformerMfinder

if __name__ == "__main__":
    # Obtain a sorted list of result files from the disk
    network_files = sorted(glob.glob("net_data_*_motif_count"),
                           key=lambda x: int(x.replace("net_data_", "").replace("_motif_count", "")))

    # Convert their counts to data frames.
    result_dataframes = []
    for a_net_id, a_network in enumerate(network_files):
        result_dataframes.append(ACTIVE_TRANSFORMER().from_file(a_network))
