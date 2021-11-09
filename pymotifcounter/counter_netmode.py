"""
Implements the NetMODE concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import os
import re
import shutil
import networkx
import subprocess
import pyparsing
import pandas
from .abstractcounter import *

# TODO, HIGH: Document the concrete classes

class PyMotifCounterOutputTransformerNetMODE(PyMotifCounterOutputTransformerBase):
    @staticmethod
    def _get_parser():
        """
        Returns a parser that is used to transform the output of a given algorithm
        to computable form.

        Notes:
            * This is usually a pyparsing parser.
        """
        float_num = pyparsing.Regex(r"([+-]?)(nan|([0-9]*)\.([0-9]+))").setParseAction(lambda s, l, t: float(t[0]))
        int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s, l, t: int(t[0]))
        gID = (pyparsing.Suppress("gID:") + int_num("gID"))
        freq = (pyparsing.Suppress("freq:") + int_num("freq"))
        ave_rand_freq = pyparsing.Group(
            pyparsing.Suppress("ave_rand_freq:") + float_num("ave_rand_freq") + pyparsing.Suppress("(sd:") + float_num(
                "sd") + pyparsing.Suppress(")"))("ave_rand_freq")
        conc = (pyparsing.Suppress("conc:") + float_num("conc"))
        ave_rand_conc = pyparsing.Group(
            pyparsing.Suppress("ave_rand_conc:") + float_num("ave_rand_conc") + pyparsing.Suppress("(sd:") + float_num(
                "sd") + pyparsing.Suppress(")"))("ave_rand_conc")
        fzscore = (pyparsing.Suppress("f-ZScore:") + float_num("f-ZScore"))
        fpvalue = (pyparsing.Suppress("f-pValue:") + float_num("f-pValue"))
        czscore = (pyparsing.Suppress("c-ZScore:") + float_num("c-ZScore"))
        cpvalue = (pyparsing.Suppress("c-pValue:") + float_num("c-pValue"))
        row_data = pyparsing.Group(
            gID + freq + ave_rand_freq + conc + ave_rand_conc + fzscore + fpvalue + czscore + cpvalue)
        data_parsing = (pyparsing.Suppress(r"calc Z-Score") + pyparsing.ZeroOrMore(row_data))("zscore")
        return data_parsing

    def __call__(self, a_ctx):
        """
        Transforms the output of NetMODE to a computable form (pandas.DataFrame)

        :param a_ctx: Context variable
        :type a_ctx: dict
        :return: Computable form of the enumeration
        :rtype: pandas.DataFrame
        """
        # Process the output (if succesful)
        # TODO:HIGH, need to inspect the `err` and raise appropriate errors
        output_data = self._get_parser().parseString(a_ctx["proc_response"])
        ret_dataframe = pandas.DataFrame(
            columns=list(output_data["zscore"][0].keys()) + ["ave_rand_freq_sd", "ave_rand_conc_sd"], index=None)
        for an_item_idx, an_item in enumerate(output_data["zscore"]):
            ret_dataframe.at[an_item_idx, "gID"] = an_item["gID"]
            ret_dataframe.at[an_item_idx, "freq"] = an_item["freq"]
            ret_dataframe.at[an_item_idx, "conc"] = an_item["conc"]
            ret_dataframe.at[an_item_idx, "f-ZScore"] = an_item["f-ZScore"]
            ret_dataframe.at[an_item_idx, "f-pValue"] = an_item["f-pValue"]
            ret_dataframe.at[an_item_idx, "c-ZScore"] = an_item["c-ZScore"]
            ret_dataframe.at[an_item_idx, "c-pValue"] = an_item["c-pValue"]
            ret_dataframe.at[an_item_idx, "ave_rand_freq"] = an_item["ave_rand_freq"]["ave_rand_freq"]
            ret_dataframe.at[an_item_idx, "ave_rand_conc"] = an_item["ave_rand_conc"]["ave_rand_conc"]
            ret_dataframe.at[an_item_idx, "ave_rand_freq_sd"] = an_item["ave_rand_freq"]["sd"]
            ret_dataframe.at[an_item_idx, "ave_rand_conc_sd"] = an_item["ave_rand_conc"]["sd"]
        return ret_dataframe


class PyMotifCounterInputTransformerNetMODE(PyMotifCounterInputTransformerBase):
    def __call__(self, a_graph):
        """
        Transforms a networkx graph to a flat edge list representation.

        :param a_graph: The networkx graph to convert
        :type a_graph: networkx.Graph
        :return: Flat edge list represetnation
        :rtype: str
        """
        # Obtain network representation
        # First of all, encode the node ID to a number. NetMODE works only with numeric nodes
        nodeid_to_num = dict(zip(a_graph.nodes(), range(1, a_graph.number_of_nodes() + 1)))
        num_to_noded = {value: key for key, value in nodeid_to_num.items()}
        # Create the edge list, translate node ids and convert to string data in one call.
        return f"{a_graph.number_of_nodes()}\n" + "".join(
            map(lambda x: f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\n", networkx.to_edgelist(a_graph)))


class PyMotifCounterNetMODE(PyMotifCounterBase):
    def __init__(self, binary_location=None):
        # Build the base model
        bin_loc = shutil.which("NetMODE") or ""
        super().__init__(binary_location=bin_loc)
        # Exchange the input transformer
        self._input_transformer = PyMotifCounterInputTransformerNetMODE()
        # Exchange the result transformer
        self._output_transformer = PyMotifCounterOutputTransformerNetMODE()
        # Add the right parameters
        self.add_parameter(PyMotifCounterParameter(name="k",
                                                   alias="motif_size",
                                                   help_str="k-node subgraphs (=3,4,5 or 6)",
                                                   default_value=3,
                                                   validation_expr=re.compile("[3-6]")))

        self.add_parameter(PyMotifCounterParameter(name="c",
                                                   alias="n_random",
                                                   help_str="Number of comparison graphs (An integer in [0, 2^31))",
                                                   default_value=0,
                                                   validation_expr=re.compile("[0-9]+")))

    def _run(self, ctx):
        """
        Enumerates motifs in a graph using NetMODE.

        :param ctx: Context variable
        :type ctx: dict
        :return: Updated context variable.
        :rtype: dict
        """
        # Group parameters
        all_param_values = set(self._parameters.values())
        p_params = []
        for a_param_value in all_param_values:
            p_params.extend(a_param_value())

        # Create the process object
        p = subprocess.Popen([self._binary_location] + p_params, universal_newlines=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Call the process
        out, err = p.communicate(input=ctx["transformed_graph"], timeout=320)

        ret_ctx = {}
        ret_ctx.update(ctx)
        ret_ctx.update({"proc_response": out,
                        "proc_error": err})
        return ret_ctx

    def _after_run(self, ctx):
        """
        Performs any cleanup after NetMODE has run and produced results.

        Notes:
            * NetMODE creates an adjacency matrix file in the CWD with all
              the adjacency matrices of the motifs it enumerated. This is
              not strictly needed because the adjacency matrix can be inferred
              by the motif's ID.

        :param ctx: Context variable
        :type ctx: dict
        :return: Updated Context variable (no updates for NetMODE at this step)
        :rtype: dict
        """
        if os.path.exists("adjMat.txt"):
            os.remove("adjMat.txt")
        return ctx
