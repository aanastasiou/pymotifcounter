from pymotifcounter.concretecounters import PyMotifCountermfinder
import networkx
#import logging

if __name__ == "__main__":
    # input_ffile = "some_file.graphml"
    
    # logging.basicConfig(level = logging.DEBUG, format="%(asctime)s %(message)s")
    
    g = networkx.watts_strogatz_graph(100,8,0.9)
    z = PyMotifCountermfinder(binary_location = "binaries/mfinder/mfinder1.21/mfinder")(g)
