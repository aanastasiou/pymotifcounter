"""
Implements the pgd concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import os
import re
import tempfile
import shutil
import networkx
import subprocess
import pyparsing
import pandas
from .abstractcounter import *


class PyMotifCounterOutputTransformerPgd(PyMotifCounterOutputTransformerBase):
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

    def __call__(self, str_data, a_ctx=None):
        """
        Transforms the raw string output from the mfinder process to a computable pandas DataFrame

        :param str_data:
        :type str_data:
        :param a_ctx: Dictionary of context information from the subsequent execution steps
        :type a_ctx: dict
        :return: A DataFrame with all enumerated motifs according to mfinder's algorithm.
        :rtype: pandas.DataFrame
        """
        parsed_output = self._get_parser().searchString(str_data)
        # TODO: LOW, Revise the parser so that it only has one root level.
        # Notice here how the parser's row field names are propagated to the columns of the returned DataFrame
        df_output = pandas.DataFrame(columns=list(parsed_output[0]["enumeration"][0].keys()), index=None)
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


class PyMotifCounterInputTransformerPgd(PyMotifCounterInputTransformerBase):
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
        return (f"{nodeid_to_num[x[0]]}, {nodeid_to_num[x[1]]}\n" for x in networkx.to_edgelist(a_graph))


class PyMotifCounterPgd(PyMotifCounterBase):
    def __init__(self, binary_location="pgd"):

        in_param = PyMotifCounterParameterFilepath(name="f",
                                                   alias="pgd_in",
                                                   help_str="Input file",
                                                   exists=True,
                                                   is_required=True,
                                                   pos=0)

        out_param = PyMotifCounterParameterFilepath(name="out",
                                                    alias="pgd_out",
                                                    help_str="Output file name",
                                                    exists=False,
                                                    default_value="-",
                                                    is_required=True,)

        pgd_parameters = [PyMotifCounterParameterStr(name="w",
                                                     alias="workers",
                                                     help_str="Number of PROCESSING UNITS (workers) for "
                                                              "the algorithm to use",
                                                     default_value="max",),
                          PyMotifCounterParameterInt(name="b",
                                                     alias="block_size",
                                                     help_str="Size of batch (number of jobs) dynamically assigned to "
                                                              "the processing unit, that is, 1, 64, 512, etc.  "
                                                              "Default: -b 64",
                                                     default_value=64,
                                                     validation_callbacks=(is_ge(0),)),
                          ]

        super().__init__(binary_location=binary_location,
                         input_parameter=in_param,
                         output_parameter=out_param,
                         input_transformer=PyMotifCounterInputTransformerPgd(),
                         output_transformer=PyMotifCounterOutputTransformerPgd(),
                         parameters=pgd_parameters)

