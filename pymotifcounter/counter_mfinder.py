"""

    Implements the mfinder concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import os
import re
import networkx
import subprocess
import pyparsing
import pandas
from .abstractcounter import *


# class PyMotifCounterResultNetMODE(PyMotifCounterResultBase):
    # @staticmethod
    # def _get_parser():
        # """
        # Returns a parser that is used to transform the output of a given algorithm 
        # to computable form.
        
        # Notes:
            # * This is usually a pyparsing parser.
        # """
        # float_num = pyparsing.Regex(r"([+-]?)(nan|([0-9]*)\.([0-9]+))").setParseAction(lambda s, l ,t:float(t[0]))
        # int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s,l,t:int(t[0]))
        # gID = (pyparsing.Suppress("gID:") + int_num("gID"))
        # freq = (pyparsing.Suppress("freq:") + int_num("freq"))
        # ave_rand_freq = pyparsing.Group(pyparsing.Suppress("ave_rand_freq:") + float_num("ave_rand_freq") + pyparsing.Suppress("(sd:") + float_num("sd") + pyparsing.Suppress(")"))("ave_rand_freq")
        # conc = (pyparsing.Suppress("conc:") + float_num("conc"))
        # ave_rand_conc = pyparsing.Group(pyparsing.Suppress("ave_rand_conc:") + float_num("ave_rand_conc") + pyparsing.Suppress("(sd:") + float_num("sd") + pyparsing.Suppress(")"))("ave_rand_conc")
        # fzscore = (pyparsing.Suppress("f-ZScore:") + float_num("f-ZScore"))
        # fpvalue = (pyparsing.Suppress("f-pValue:") + float_num("f-pValue"))
        # czscore = (pyparsing.Suppress("c-ZScore:") + float_num("c-ZScore"))
        # cpvalue = (pyparsing.Suppress("c-pValue:") + float_num("c-pValue"))
        # row_data = pyparsing.Group(gID + freq + ave_rand_freq + conc + ave_rand_conc + fzscore + fpvalue + czscore + cpvalue)
        # data_parsing = (pyparsing.Suppress(r"calc Z-Score") + pyparsing.ZeroOrMore(row_data))("zscore")
        # return data_parsing
            
    # def __init__(self):
        # self._parser = self._get_parser()
        
    # def __call__(self, a_ctx):
        # # Process theoutput (if succesfull)
        # # TODO:HIGH, need to inspect the `err` and raise appropriate errors
        # outputData = self._parser.parseString(a_ctx["proc_response"])
        # ret_dataframe = pandas.DataFrame(columns=list(outputData["zscore"][0].keys()) + ["ave_rand_freq_sd", "ave_rand_conc_sd"], index = None)
        # for an_item_idx, an_item in enumerate(outputData["zscore"]):
            # ret_dataframe.at[an_item_idx, "gID"] = an_item["gID"]
            # ret_dataframe.at[an_item_idx, "freq"] = an_item["freq"]
            # ret_dataframe.at[an_item_idx, "conc"] = an_item["conc"]
            # ret_dataframe.at[an_item_idx, "f-ZScore"] = an_item["f-ZScore"]
            # ret_dataframe.at[an_item_idx, "f-pValue"] = an_item["f-pValue"]
            # ret_dataframe.at[an_item_idx, "c-ZScore"] = an_item["c-ZScore"]
            # ret_dataframe.at[an_item_idx, "c-pValue"] = an_item["c-pValue"]
            # ret_dataframe.at[an_item_idx, "ave_rand_freq"] = an_item["ave_rand_freq"]["ave_rand_freq"]
            # ret_dataframe.at[an_item_idx, "ave_rand_conc"] = an_item["ave_rand_conc"]["ave_rand_conc"]
            # ret_dataframe.at[an_item_idx, "ave_rand_freq_sd"] = an_item["ave_rand_freq"]["sd"]
            # ret_dataframe.at[an_item_idx, "ave_rand_conc_sd"] = an_item["ave_rand_conc"]["sd"]
        # return ret_dataframe    
        # # with open("adjMat.txt", "rt") as fd:
            # # adj_mat_data = fd.read()
        # # parsed_adjacency_results = self._adjacency_matrix_parser.parseString(adj_mat_data)
        # # identified_motifs = {}
        # # for an_item in parsed_adjacency_results:
            # # identified_motifs[an_item["graphID"]] = an_item["G"]
        
class PyMotifCounterNetworkmfinderRep(PyMotifCounterNetworkRepBase):
    def __call__(self, a_graph):
        # Obtain network representation
        # First of all, encode the node ID to a number.
        nodeid_to_num = dict(zip(a_graph.nodes(), range(1, a_graph.number_of_nodes()+1)))
        num_to_noded = {value:key for key, value in nodeid_to_num.items()}
        # Create the edge list
        return "".join(map(lambda x:f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\t1\n", networkx.to_edgelist(a_graph)))


# class PyMotifCounterNetMODE(PyMotifCounterProcessBase):
    # def __init__(self):
        # # Build the base model
        # # TODO: HIGH, if the binary_location is None, this should raise an exception when an attempt is made to run.
        # super().__init__(binary_location="NetMODE")
        # # Exchange the input transformer
        # self._input_transformer = PyMotifCounterNetworkNetMODERep()
        # # Exchange the result transformer
        # self._output_transformer = PyMotifCounterResultNetMODE()
        # # Add the right parameters        
        # self.add_parameter(Parameter(name="k", \
                                     # alias="motif_size", \
                                     # help_str="k-node subgraphs (=3,4,5 or 6)", \
                                     # validation_expr=re.compile("[3-6]")))
        # self.add_parameter(Parameter(name="c", \
                                     # alias="n_random", \
                                     # help_str="Number of comparison graphs (An integer in [0, 2^31))", \
                                     # validation_expr=re.compile("[0-9]+")))
        # self.set_parameter_value("k", 3)
        # self.set_parameter_value("c", 0)
                                     
    # def _run(self, ctx):
        # # Group parameters
        # all_param_values = set(self._parameters.values())
        # p_params = []
        # for a_param_value in all_param_values:
            # p_params.extend(a_param_value())
            
        # # Create the process object
        # # p = subprocess.Popen([f"{self._binary_location}NetMODE", "-k", f"{self._knodesize}", "-e", f"{self._edge_random_method}", "-c", f"{self._nrandom}"], universal_newlines=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # p = subprocess.Popen([self._binary_location] + p_params, universal_newlines=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # # Call the process
        # out, err = p.communicate(input = ctx["transformed_graph"], timeout=320)
        
        # ret_ctx = {}
        # ret_ctx.update(ctx)
        # ret_ctx.update({"proc_response":out, \
                        # "proc_error":err})        
        # return ret_ctx
        
    # def _after_run(self, ctx):
        # """
        # Performs any cleanup after the process has run and produced results.
        
        # Notes:
            # * NetMODE creates an adjacency matrix file in the CWD with all 
              # the adjacency matrices of the motifs it enumerated. This is 
              # not strictly needed because the adjacency matrix can be inferred 
              # by the motif's ID.
        # """
        # if os.path.exists("adjMat.txt"):
            # os.remove("adjMat.txt")
        # return ctx

