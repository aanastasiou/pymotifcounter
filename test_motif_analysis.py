from pymotifcounter.concretecounters import PyMotifCountermfinder, PyMotifCounterNetMODE
import networkx
#import logging

if __name__ == "__main__":
    # input_ffile = "some_file.graphml"
    
    # logging.basicConfig(level = logging.DEBUG, format="%(asctime)s %(message)s")
    
    g = networkx.watts_strogatz_graph(100,8,0.9)
    z_netmode = PyMotifCounterNetMODE(binary_location = "binaries/NetMODE/NetMODE")(g)
    z_mfinder = PyMotifCountermfinder(binary_location = "binaries/mfinder/mfinder1.21/mfinder")(g)
