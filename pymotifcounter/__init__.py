"""
A quick and dirty wrapper around netmode to automate the availability of network motif analysis

"""

import os
import subprocess
import networkx
import re
import pyparsing
import numpy
import pandas
from matplotlib import pyplot as plt
import random


class MotifSpectrum:
    def __init__(self, motif_counts, identified_motifs):
        if not isinstance(motif_counts, pandas.DataFrame):
            pass
            
        if set(motif_counts.columns) != set(["ave_rand_conc", "ave_rand_conc_sd", "ave_rand_freq_sd", \
                                             "c-ZScore", "c-pValue", "conc", "f-ZScore", "f-pValue", "freq", "gID"]):
            pass
        
        if type(identified_motifs) is not dict:
            pass
            
        if type(list(identified_motifs.items())[random.randint(0,len(identified_motifs)-1)][1]) is not networkx.DiGraph:
            pass
            
        self._identified_motifs = identified_motifs
        self._motif_counts = motif_counts
        
    @property
    def motifs(self):
        return self._identified_motifs
        
    @property
    def spectrum(self):
        return self._motif_counts
        
    def plot_spectrum(self):
        current_axis = plt.gca()
        
        plt.bar(self.motif_counts["gID"], self._motif_counts["freq"])
        plt.xlabel("Motif ID")
        plt.ylabel("Count")
        plt.grid(True)
        
    def plot_equivalent_random_spectrum(self):
        current_axis = plt.gca()
        
        plt.bar(self._motif_counts["gID"], self._motif_counts["ave_rand_freq"])
        plt.xlabel("Equivalent Random Network Motif ID")
        plt.ylabel("Count")
        plt.grid(True)
        
    def plot_motif(self, motif_id):
        motif_data = self._motif_counts[self._motif_counts["gID"] == motif_id]
        motif_graph = self._identified_motifs[motif_id]
        current_axes = plt.gca()
        networkx.draw_spring(motif_graph[0])
        current_axes.axis("on")
        current_axes.set_xlabel(f"graphID:{motif_id} ({motif_data['freq'][motif_data['freq'].index[0]]})")
        
    def plot_motif_table(self):
        number_of_motifs = len(self._motif_counts)
        number_of_subplots = int(numpy.ceil(numpy.sqrt(number_of_motifs)))
        for a_motif in enumerate(self._identified_motifs):
            plt.subplot(number_of_subplots, number_of_subplots, a_motif[0]+1)
            self.plot_motif(a_motif[1])


class PyNetMODE:
    @staticmethod
    def _get_adj_mat_parser():
        def adjacency_matrix_to_network(s, l, t):
            s = []
            for an_entry in t:
                s.append(list(map(lambda x:int(x), an_entry)))
            adj_mat = numpy.array(s)
            dims = adj_mat.shape
            if dims[0] != dims[1]:
                raise TypeError(f"{t} is not a valid adjacency matrix")
            G = networkx.from_numpy_array(adj_mat, create_using = networkx.DiGraph)
            return [G]
            
        int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s, l, t:int(t[0]))
        graph_id = pyparsing.Suppress(pyparsing.Literal("graphID = ")) + int_num("graphID")
        adj_mat_row = pyparsing.Regex(r"[0-1][0-1][0-1][0-1]?[0-1]?[0-1]?")
        adj_mat = pyparsing.OneOrMore(adj_mat_row)("G").setParseAction(adjacency_matrix_to_network)
        motif_entries = pyparsing.OneOrMore(pyparsing.Group(graph_id + adj_mat))
        return motif_entries
            
    @staticmethod
    def _get_parser():
        float_num = pyparsing.Regex(r"([+-]?)(nan|([0-9]*)\.([0-9]+))").setParseAction(lambda s, l ,t:float(t[0]))
        int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s,l,t:int(t[0]))
        gID = (pyparsing.Suppress("gID:") + int_num("gID"))
        freq = (pyparsing.Suppress("freq:") + int_num("freq"))
        ave_rand_freq = pyparsing.Group(pyparsing.Suppress("ave_rand_freq:") + float_num("ave_rand_freq") + pyparsing.Suppress("(sd:") + float_num("sd") + pyparsing.Suppress(")"))("ave_rand_freq")
        conc = (pyparsing.Suppress("conc:") + float_num("conc"))
        ave_rand_conc = pyparsing.Group(pyparsing.Suppress("ave_rand_conc:") + float_num("ave_rand_conc") + pyparsing.Suppress("(sd:") + float_num("sd") + pyparsing.Suppress(")"))("ave_rand_conc")
        fzscore = (pyparsing.Suppress("f-ZScore:") + float_num("f-ZScore"))
        fpvalue = (pyparsing.Suppress("f-pValue:") + float_num("f-pValue"))
        czscore = (pyparsing.Suppress("c-ZScore:") + float_num("c-ZScore"))
        cpvalue = (pyparsing.Suppress("c-pValue:") + float_num("c-pValue"))
        row_data = pyparsing.Group(gID + freq + ave_rand_freq + conc + ave_rand_conc + fzscore + fpvalue + czscore + cpvalue)
        data_parsing = (pyparsing.Suppress(r"calc Z-Score") + pyparsing.ZeroOrMore(row_data))("zscore")
        return data_parsing
        
    def __init__(self, knodesize=3, nrandom=0, burnin=0, edge_random_method=1, nthreads=1, netmode_binary_dir = None):
        self._knodesize = knodesize
        self._nrandom = nrandom
        self._burnin = burnin
        self._edge_random_method = edge_random_method
        self._nthreads = nthreads
        if not os.path.exists(f"{netmode_binary_dir}NetMODE"):
            raise FileNotFoundError(f"NetMODE binary not found at {netmode_binary_dir}")
        else:
            self._netmode_binary_dir = netmode_binary_dir
            
        self._output_parser = self._get_parser()
        self._adjacency_matrix_parser = self._get_adj_mat_parser()
    
    @property
    def knodesize(self):
        return self._knodesize
        
    @knodesize.setter
    def knodesize(self, new_knode_size):
        self._knodesize = new_knode_size
        
    @property
    def nrandom(self):
        return self._nrandom
    
    @nrandom.setter
    def nrandom(self, new_nrandom):
        self._nrandom = new_nrandom
        
    @property
    def burnin(self):
        return self._burnin
    
    @burnin.setter
    def burnin(self, new_burnin):
        self._burnin = new_burnin
        
    @property
    def edge_random_method(self):
        return self._edge_random_method
        
    @edge_random_method.setter
    def edge_random_method(self, new_edge_random_method):
        self._edge_random_method = new_edge_random_method
        
    @property
    def nthreads(self):
        return self._nthreads
        
    @nthreads.setter
    def nthreads(self, new_nthreads):
        self._nthreads = new_nthreads
        
    def get_motif_spectrum(self, G, retrieve_motif_adj = False):
        # Obtain network representation
        # First of all, you have to encode the node ID to a number. NetMODE works only with numeric nodes
        nodeid_to_num = dict(zip(G.nodes(), range(1, G.number_of_nodes()+1)))
        num_to_noded = {value:key for key, value in nodeid_to_num.items()}
        # Create the edge list, translate node ids and convert to string data in one call.
        netmode_input = f"{G.number_of_nodes()}\n" + "".join(map(lambda x:f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\n", networkx.to_edgelist(G)))
        # Create the process object
        p = subprocess.Popen([f"{self._netmode_binary_dir}NetMODE", "-k", f"{self._knodesize}", "-e", f"{self._edge_random_method}", "-c", f"{self._nrandom}"], universal_newlines=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Call the process
        out, err = p.communicate(input = netmode_input, timeout=320)
        # Process theoutput (if succesfull)
        # TODO:HIGH, need to inspect the `err` and raise appropriate errors
        outputData = self._output_parser.parseString(out)
        D = pandas.DataFrame(columns=list(outputData["zscore"][0].keys()) + ["ave_rand_freq_sd", "ave_rand_conc_sd"], index = None)
        for an_item in enumerate(outputData["zscore"]):
            D.at[an_item[0], "gID"] = an_item[1]["gID"]
            D.at[an_item[0], "freq"] = an_item[1]["freq"]
            D.at[an_item[0], "conc"] = an_item[1]["conc"]
            D.at[an_item[0], "f-ZScore"] = an_item[1]["f-ZScore"]
            D.at[an_item[0], "f-pValue"] = an_item[1]["f-pValue"]
            D.at[an_item[0], "c-ZScore"] = an_item[1]["c-ZScore"]
            D.at[an_item[0], "c-pValue"] = an_item[1]["c-pValue"]
            D.at[an_item[0], "ave_rand_freq"] = an_item[1]["ave_rand_freq"]["ave_rand_freq"]
            D.at[an_item[0], "ave_rand_conc"] = an_item[1]["ave_rand_conc"]["ave_rand_conc"]
            D.at[an_item[0], "ave_rand_freq_sd"] = an_item[1]["ave_rand_freq"]["sd"]
            D.at[an_item[0], "ave_rand_conc_sd"] = an_item[1]["ave_rand_conc"]["sd"]
            
        with open("adjMat.txt", "rt") as fd:
            adj_mat_data = fd.read()
        parsed_adjacency_results = self._adjacency_matrix_parser.parseString(adj_mat_data)
        identified_motifs = {}
        for an_item in parsed_adjacency_results:
            identified_motifs[an_item["graphID"]] = an_item["G"]
            
        return MotifSpectrum(D, identified_motifs)
        
if __name__ == "__main__":
    pass
    
            
        
            
