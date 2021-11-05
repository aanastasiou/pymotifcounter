"""
Implements the mfinder concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import os
import re
import tempfile
import networkx
import subprocess
import pyparsing
import pandas
from .abstractcounter import *


class PyMotifCounterOutputTransformerMfinder(PyMotifCounterOutputTransformerBase):
    @staticmethod
    def _get_parser():
        """
        Parses the "Full list of subgraphs size k ids:" section of mfinder's output.

        :return: The top level element of a PyParsing parser that handles the extraction of the useful data.
        :rtype: pyparsing.ParserElement
        """
        # TODO: LOW, Consider abstracting these two somehow as these definitions will be useful for every parser.
        float_num = pyparsing.Regex(r"([+-]?)(nan|([0-9]*)\.([0-9]+))").setParseAction(lambda s, l, t: float(t[0]))
        int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s, l, t: int(t[0]))

        row_data = pyparsing.Group((int_num("motif_id") +
                                   int_num("nreal") +
                                   (float_num("nrand_stats_m") + pyparsing.Suppress("+-") + float_num("nrand_stats_s")) +
                                    (float_num("nreal_z_score") ^ int_num("nreal_z_score")) +
                                   float_num("nreal_pval") +
                                   float_num("creal_mili") +
                                   int_num("uniq")))
        data_parsing = pyparsing.OneOrMore(row_data)("enumeration")
        return data_parsing

    def __call__(self, a_ctx):
        """
        Transforms the raw string output from the mfinder process to a computable pandas DataFrame

        :param a_ctx: Dictionary of context information from the subsequent execution steps
        :type a_ctx: dict
        :return: A DataFrame with all enumerated motifs according to mfinder's algorithm.
        :rtype: pandas.DataFrame
        """
        parsed_output = self._get_parser().searchString(a_ctx["proc_response"])
        # TODO: LOW, Revise the parser so that it only has one root level.
        # Notice here how the parser's row field names are propagated to the columns of the returned DataFrame
        df_output = pandas.DataFrame(columns=list(parsed_output[0]["enumeration"][0].keys()), index = None)
        for a_row_idx, a_row_data in enumerate(parsed_output[0]["enumeration"]):
            # TODO: HIGH, The conversion can be performed more automatically through pandas rather than a loop
            df_output.at[a_row_idx, "motif_id"] = a_row_data["motif_id"]
            df_output.at[a_row_idx, "nreal"] = a_row_data["nreal"]
            df_output.at[a_row_idx, "nrand_stats_m"] = a_row_data["nrand_stats_m"]
            df_output.at[a_row_idx, "nrand_stats_s"] = a_row_data["nrand_stats_s"]
            df_output.at[a_row_idx, "nreal_z_score"] = a_row_data["nreal_z_score"]
            df_output.at[a_row_idx, "nreal_pval"] = a_row_data["nreal_pval"]
            df_output.at[a_row_idx, "creal_mili"] = a_row_data["creal_mili"]
            df_output.at[a_row_idx, "uniq"] = a_row_data["uniq"]
        return df_output


class PyMotifCounterInputTransformerMfinder(PyMotifCounterInputTransformerBase):
    def __call__(self, a_graph):
        """
        Transforms a graph from a Networkx representation to a flat string.

        Notes:
            * Usually, the flat string representation is in the form of an edgelist that conforms to whatever
              format each process expects in its input.

        :param a_graph: The Networkx graph of which we wish to enumerate motifs.
        :return: A flat edge list with a format that depends on what each algorithms expects.
        :rtype: str
        """
        # Obtain network representation
        # First of all, encode the node ID to a number.
        nodeid_to_num = dict(zip(a_graph.nodes(), range(1, a_graph.number_of_nodes()+1)))
        num_to_noded = {value:key for key, value in nodeid_to_num.items()}
        # Create the edge list
        # TODO: LOW, consider turning this to an iterator to handle larger graphs
        return "".join(map(lambda x:f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\t1\n", networkx.to_edgelist(a_graph)))


class PyMotifCounterMfinder(PyMotifCounterBase):
    def __init__(self, binary_location = None):
        # Build the base model
        # TODO: HIGH, if the binary_location is None, this should raise an exception when an attempt is made to run.
        # TODO: HIGH, this can be abstracted further to a function that performs autodiscovery of the binary's location
        # TODO: HIGH, the validation can be a function
        # TODO: MID, add the output file name and use it when it is specified
        super().__init__(binary_location=binary_location or "mfinder")
        # Exchange the input transformer
        self._input_transformer = PyMotifCounterInputTransformerMfinder()
        # Exchange the result transformer
        self._output_transformer = PyMotifCounterOutputTransformerMfinder()
        # Add the right parameters        
        self.add_parameter(PyMotifCounterParameter(name="s",
                                                   alias="motif_size",
                                                   help_str="Motif size to search",
                                                   validation_expr=re.compile("[3-4]")))
        self.add_parameter(PyMotifCounterParameter(name="r",
                                                   alias="n_random",
                                                   help_str="Number of random networks to generate",
                                                   validation_expr=re.compile("[0-9]+")))
        self.set_parameter_value("s", 3)
        self.set_parameter_value("r", 0)
                                     
    def _run(self, ctx):
        """
        Enumerates motifs using mfinder

        :param ctx: Context variable including the "transformed_graph" field that contains the transformed input graph.
        :type ctx: dict
        :return: Updated context
        :rtype: dict
        """
        # Group parameters
        # TODO: MID, this step can be abstracted
        all_param_values = set(self._parameters.values())
        p_params = []
        for a_param_value in all_param_values:
            p_params.extend(a_param_value())
            
        # TODO: LOW, it is probably easy to make mfinder work with stdin/stdout as a binary
        # TODO: HIGH, this needs exception handling
        # mfinder works off of a file, so first save the input representation down to a file in temporary storage
        tmp_fileno, tmp_filename = tempfile.mkstemp()
        ctx["temporary_filename"] = tmp_filename
        with os.fdopen(tmp_fileno, "wt") as fd:
            fd.write(ctx["transformed_graph"])
        p_params = [tmp_filename] + p_params
        # Create the process object
        # TODO: HIGH, this needs exception handling for timeout
        p = subprocess.Popen([self._binary_location] + p_params, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Call the process
        out, err = p.communicate(timeout=320)
        # mfinder will write a file in the same directory as the input file
        split_tmp_filename = os.path.split(tmp_filename)
        split_tmp_filename_ext = os.path.splitext(split_tmp_filename[1])
        split_tmp_out_filename = f"{split_tmp_filename[0]}/{split_tmp_filename_ext[0][:7]}_OUT.txt"
        with open(split_tmp_out_filename, "rt") as fd:
            out = fd.read()
        
        ret_ctx = {}
        ret_ctx.update(ctx)
        ret_ctx.update({"proc_response": out,
                        "proc_error": err,
                        "mfinder_output_file": split_tmp_out_filename})
        return ret_ctx
        
    def _after_run(self, ctx):
        """
        Performs any cleanup after the process has run and produced results.
        
        Notes:
            * NetMODE creates an adjacency matrix file in the CWD with all 
              the adjacency matrices of the motifs it enumerated. This is 
              not strictly needed because the adjacency matrix can be inferred 
              by the motif's ID.

        :param ctx: Context variable
        :type ctx: dict
        :return: Updated context variable (no updates for mfinder at this step).
        :rtype: dict
        """
        # Simply erase both input and output temporary files
        if os.path.exists(ctx["temporary_filename"]):
            os.remove(ctx["temporary_filename"])
            
        if os.path.exists(ctx["mfinder_output_file"]):
            os.remove(ctx["mfinder_output_file"])
        
        return ctx

