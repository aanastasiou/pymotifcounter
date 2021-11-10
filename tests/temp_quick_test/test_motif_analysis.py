from pymotifcounter.concretecounters import PyMotifCounterMfinder, PyMotifCounterNetMODE, PyMotifCounterFanmod
from pymotifcounter.util import motif_id_to_adj_mat
import networkx
from matplotlib import pyplot as plt
#import logging

if __name__ == "__main__":
    # input_ffile = "some_file.graphml"
    
    # logging.basicConfig(level = logging.DEBUG, format="%(asctime)s %(message)s")
    
    g = networkx.watts_strogatz_graph(100,8,0.9)
    z_netmode = PyMotifCounterNetMODE()(g)
    z_mfinder = PyMotifCounterMfinder()(g)
    fanmod_counter = PyMotifCounterFanmod()
    z_fanmod = fanmod_counter(g)
    
    # g = networkx.from_numpy_array(motif_id_to_adj_mat(6604,4), create_using=networkx.DiGraph)
    # networkx.draw_spring(g)
    # plt.show()
