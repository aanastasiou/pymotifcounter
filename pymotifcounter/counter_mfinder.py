"""
Implements the mfinder concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import networkx
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
        return (f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\t1\n" for x in networkx.to_edgelist(a_graph))


class PyMotifCounterMfinder(PyMotifCounterBase):
    """
    The concrete implementation of the mfinder counter.

    This counter supports the following parameters:

    :param s: Motif size to search (3 <= s <= 8) (default ``3``)
    :type s: Integer
    :param r: Number of random networks to generate (Default ``0``)
    :type r: Integer >0
    :param nd: Set if the input networks is **not** directed. (Default ``False``)
    :type nd: Bool
    """
    def __init__(self, binary_location="mfinder"):

        # Input and output parameters
        in_param = PyMotifCounterParameterFilepath(name="io_in",
                                                   alias="mfinder_in",
                                                   help_str="Input file",
                                                   exists=True,
                                                   is_required=True,
                                                   pos=0)

        out_param = PyMotifCounterParameterFilepath(name="f",
                                                    alias="mfinder_out",
                                                    help_str="Output file name",
                                                    exists=False,
                                                    is_required=True,)

        # Any other parameter accepted by the algorithm
        mfinder_parameters = [PyMotifCounterParameterInt(name="s",
                                                         alias="motif_size",
                                                         help_str="Motif size to search",
                                                         default_value=3,
                                                         validation_callbacks=(is_ge(3), is_le(8))),
                              PyMotifCounterParameterInt(name="r",
                                                         alias="n_random",
                                                         help_str="Number of random networks to generate",
                                                         default_value=0,
                                                         validation_callbacks=(is_ge(0),)),
                              PyMotifCounterParameterFlag(name="nd",
                                                          alias="is_undirected",
                                                          help_str="Input network is a non-directed network",
                                                          default_value=False,
                                                          is_required=False),
                              ]
        # Build the final object.
        super().__init__(binary_location=binary_location,
                         input_parameter=in_param,
                         output_parameter=out_param,
                         input_transformer=PyMotifCounterInputTransformerMfinder(),
                         output_transformer=PyMotifCounterOutputTransformerMfinder(),
                         parameters=mfinder_parameters)

