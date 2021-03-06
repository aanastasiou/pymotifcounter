from pymotifcounter.concretecounters import (PyMotifCounterNetMODE,
                                             PyMotifCounterFanmod,
                                             PyMotifCounterMfinder,
                                             PyMotifCounterPgd)
import networkx
# from matplotlib import pyplot as plt
#import logging

if __name__ == "__main__":
    # input_ffile = "some_file.graphml"
    
    # logging.basicConfig(level = logging.DEBUG, format="%(asctime)s %(message)s")
    
    g = networkx.watts_strogatz_graph(100,8,0.9)

    # active_counter = PyMotifCounterNetMODE()
    # active_counter = PyMotifCounterMfinder()
    # active_counter = PyMotifCounterFanmod()
    active_counter = PyMotifCounterPgd()
    # active_counter.get_parameter("r").set_value(10)
    motif_count = active_counter(g)