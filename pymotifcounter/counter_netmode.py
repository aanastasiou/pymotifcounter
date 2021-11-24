"""
Implements the NetMODE concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import os
import itertools
import networkx
import pyparsing
import pandas
from .abstractcounter import *


class PyMotifCounterOutputTransformerNetMODE(PyMotifCounterOutputTransformerBase):
    @staticmethod
    def _get_parser():
        """
        Returns a parser that is used to transform the output of Fanmod to computable form.

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

    def __call__(self, str_data, ctx=None):
        """
        Transforms the output of NetMODE to a computable form (pandas.DataFrame)

        :param str_data:
        :type str_data:
        :param ctx:
        :type ctx:
        :returns:
        :rtype:
        """
        # Process the output (if succesful)
        output_data = self._get_parser().parseString(str_data)
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
        return itertools.chain((f"{a_graph.number_of_nodes()+1}\n" for _ in [1]),
                               (f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\n"
                                for x in networkx.to_edgelist(a_graph)))


class PyMotifCounterNetMODE(PyMotifCounterBase):
    """
    Concrete implementation of the NetMODE counter.

    The following parameters are supported:

    :param k: k-node subgraphs ( 3<=k<=6) (Default ``3``)
    :type k: Integer
    :param c: Number of comparison graphs (An integer in [0, 2^31)) (Default ``0``)
    :type c: Integer
    :param t: Number of threads to use (Default ``1``)
    :type t: Integer >0
    :param e: Bidirectional edge random_method (0:fixed, 1:no regard, 2: global constant, 3:local constant (default),
              4:uniform
    :type e: Integer
    :param b: Number of random graphs to be discarded (Default ``0``)
    :type b: Integer
    """
    def __init__(self, binary_location="NetMODE"):
        # Specify input and output parameters
        in_param = PyMotifCounterParameterFilepath(name="netmode_in",
                                                   help_str="NetMODE accepts input via stdin",
                                                   default_value="-",
                                                   exists=False,
                                                   is_required=False)

        out_param = PyMotifCounterParameterFilepath(name="netmode_out",
                                                    help_str="NetMODE returns output via stdout",
                                                    default_value="-",
                                                    exists=False,
                                                    is_required=False)

        netmode_parameters = [PyMotifCounterParameterInt(name="k",
                                                         alias="motif_size",
                                                         help_str="k-node subgraphs (=3,4,5 or 6)",
                                                         default_value=3,
                                                         validation_callbacks=(is_ge(3), is_le(6),)),
                              PyMotifCounterParameterInt(name="c",
                                                         alias="n_random",
                                                         help_str="Number of comparison graphs (An integer in [0, 2^31))",
                                                         default_value=0,
                                                         validation_callbacks=(is_ge(0),)),
                              PyMotifCounterParameterInt(name="t",
                                                         alias="n_threads",
                                                         help_str="Number of threads to use",
                                                         default_value=1,
                                                         validation_callbacks=(is_ge(1),),
                                                         is_required=False),
                              PyMotifCounterParameterInt(name="e",
                                                         alias="edge_select_method",
                                                         help_str="Bidirectional edge random_method (0:fixed, "
                                                                  "1:no regard, 2: global constant, "
                                                                  "3:local constant (default), 4:uniform",
                                                         default_value=3,
                                                         validation_callbacks=(is_ge(0), is_le(4),),
                                                         is_required=False),
                              PyMotifCounterParameterInt(name="b",
                                                         alias="burnin",
                                                         help_str="Number of random graphs to be discarded",
                                                         default_value=0,
                                                         validation_callbacks=(is_ge(0),),
                                                         is_required=False),
                              ]
        # Build the base object
        super().__init__(binary_location=binary_location,
                         input_parameter=in_param,
                         output_parameter=out_param,
                         input_transformer=PyMotifCounterInputTransformerNetMODE(),
                         output_transformer=PyMotifCounterOutputTransformerNetMODE(),
                         parameters=netmode_parameters)

    def _after_run(self, ctx):
        """
        Erases the intermediate adjacency matrix file that netmode creates.

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
