from pynetmode import PyNetMODE
import networkx
import logging

if __name__ == "__main__":
    # input_ffile = "some_file.graphml"
    
    logging.basicConfig(level = logging.DEBUG, format="%(asctime)s %(message)s")
    
    # Load the mass-link network
    # logging.info(f"Loading file {input_file}")
    # body_net = networkx.read_graphml(input_file).to_undirected()
    # logging.info("Done")
    # # Initialise the graph
    # # The graph is initialised ONLY with the covalent and hydrogen bonds. This will construct the square network.
    # # After the square network is constructed, we add the additional constraints as secondary edges
    # # Get the constraint edges
    # # pdb.set_trace()
    # constraint_edges = list(filter(lambda x:x[2]["type"] in ["constraint"] if "type" in x[2] else False, body_net.edges(data=True)))
    # # Remove them from the intiial netrowk
    # body_net.remove_edges_from(constraint_edges)
    # body_net = networkx.power(body_net,2)
    # # Add the constraint edges again
    # body_net.add_edges(from(constraint_edges)
    body_net = networkx.watts_strogatz_graph(100,8,0.1)
    pn = PyNetMODE(netmode_binary_dir = "binaries/NetMODE/", knodesize=4)
    m = pn.get_motif_spectrum(body_net)
