"""
Implements the fanmod_cmd concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import networkx
import pyparsing
import pandas
from .abstractcounter import *


class PyMotifCounterOutputTransformerFanmod(PyMotifCounterOutputTransformerBase):
    # TODO: MID, The parser --> DataFrame is pretty standard by now, should be incorporated in the standard round-trip
    @staticmethod
    def _get_parser():
        """
        Parses the "Result overview:" section of fanmod's output.

        :return: The top level element of a PyParsing parser that handles the extraction of the useful data.
        :rtype: pyparsing.ParserElement
        """
        # TODO: LOW, Consider abstracting some standard pyparsing definitions as they could be useful for many parsers.
        # TODO: HIGH, Make sure that the float can parse just integer part too and it becomes "Numeric".
        float_num = pyparsing.Regex(r"([+-]?)(nan|([0-9]*)\.([0-9]+))").setParseAction(lambda s, l, t: float(t[0]))
        int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s, l, t: int(t[0]))
        # Elements that are specific to fanmod
        id_element = int_num("ID")
        adj_mat_element = pyparsing.Regex(r"[0-1]+")("Adj_Matrix")
        freq_element = (float_num("Frequency") + pyparsing.Literal("%"))
        mean_freq_element = (float_num("Mean_Freq") + pyparsing.Literal("%"))
        st_dev_element = float_num("Standard_Dev")
        z_score_element = float_num("Z_Score")
        p_value_element = (float_num ^ int_num)("p_Value")
        stats_element = (mean_freq_element + pyparsing.Suppress(",")) + \
                        (st_dev_element + pyparsing.Suppress(",")) + \
                        (z_score_element + pyparsing.Suppress(",")) + \
                        p_value_element
        other_element = pyparsing.OneOrMore(pyparsing.Group(pyparsing.Suppress(",") + adj_mat_element))
        # TODO: HIGH, Check which fields are percentages and make sure this is denoted in the output
        # Build up the row parser
        row_data = pyparsing.Group(id_element + pyparsing.Suppress(",") +
                                   adj_mat_element +
                                   pyparsing.Suppress(",") +
                                   freq_element +
                                   pyparsing.Optional(pyparsing.Suppress(",") + stats_element) +
                                   other_element)
        # Build the "table" parser.
        data_parsing = pyparsing.OneOrMore(row_data)("enumeration")
        return data_parsing

    def __call__(self, str_data, a_ctx):
        """
        Transforms the raw string output from the fanmod process to a computable pandas DataFrame

        :param str_data:
        :type str_data:
        :param a_ctx: Dictionary of context information from the subsequent execution steps
        :type a_ctx: dict
        :return: A DataFrame with all enumerated motifs according to fanmod's algorithm.
        :rtype: pandas.DataFrame
        """
        parsed_output = self._get_parser().searchString(str_data)
        # TODO: LOW, Revise the parser so that it only has one root level.
        # Notice here how the parser's row field names are propagated to the columns of the returned DataFrame
        df_output = pandas.DataFrame(columns=list(filter(lambda x: x != "Adj_Matrix",
                                                         parsed_output[0]["enumeration"][0].keys())),
                                     index=None)
        for a_row_idx, a_row_data in enumerate(parsed_output[0]["enumeration"]):
            # TODO: HIGH, The conversion can be performed more automatically through pandas rather than a loop
            df_output.at[a_row_idx, "ID"] = a_row_data["ID"]
            df_output.at[a_row_idx, "Frequency"] = a_row_data["Frequency"]
            # Fanmod produces different outputs depending on whether the random net population was produced
            if "Mean_Freq" in a_row_data:
                df_output.at[a_row_idx, "Mean_Freq"] = a_row_data["Mean_Freq"]
                df_output.at[a_row_idx, "Standard_Dev"] = a_row_data["Standard_Dev"]
                df_output.at[a_row_idx, "Z_Score"] = a_row_data["Z_Score"]
                df_output.at[a_row_idx, "p_Value"] = a_row_data["p_Value"]
        return df_output


class PyMotifCounterInputTransformerFanmod(PyMotifCounterInputTransformerBase):
    def __call__(self, a_graph):
        """
        Returns a generator over a graph's edge list representation.

        :param a_graph: The networkx graph to transform
        :type a_graph: <<networkx.Graph>>
        :returns: A generator for each line of the edge list
        :rtype: generator
        """
        # Obtain network representation
        # First of all, encode the node ID to a number.
        nodeid_to_num = dict(zip(a_graph.nodes(), range(1, a_graph.number_of_nodes()+1)))
        return (f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\n" for x in networkx.to_edgelist(a_graph))


class PyMotifCounterFanmod(PyMotifCounterBase):
    """
    The concrete Fanmod counter.

    This counter supports the following parameters:

    :param s: Motif size to search (3 <= s <=8) (default ``3``)
    :type s: Integer
    :param r: Number of random networks to generate (default ``0``)
    :type r: Integer >0
    :param d: Set if the graph to analyse is directed (default ``True``)
    :type d: Bool
    """
    def __init__(self, binary_location="fanmod_cmd"):
        # Determine the io
        # TODO: MID, Give a common name across all inputs and outputs
        # TODO: MID, Provide a way for parameters to be accessed as attributes or keys and preferably in a unified way

        in_param = PyMotifCounterParameterFilepath(name="i",
                                                   alias="fanmod_input",
                                                   help_str="Input graph file",
                                                   default_value="",
                                                   exists=True,
                                                   is_required=True)

        out_param = PyMotifCounterParameterFilepath(name="o",
                                                    alias="fanmod_output",
                                                    help_str="Output CSV file",
                                                    default_value="",
                                                    exists=False,
                                                    is_required=True)

        # Determine other parameters for the algorithm
        fanmod_parameters = [PyMotifCounterParameterInt(name="s",
                                                        alias="motif_size",
                                                        help_str="Motif size to search",
                                                        default_value=3,
                                                        validation_callbacks=(is_ge(3), is_le(8),)),
                             PyMotifCounterParameterInt(name="r",
                                                        alias="n_random",
                                                        help_str="Number of random networks to generate",
                                                        default_value=0,
                                                        validation_callbacks=(is_ge(0),)),
                             # Whether the network is directed (by default it should be considered directed)
                             PyMotifCounterParameterFlag(name="d",
                                                         alias="is_directed",
                                                         help_str="Set if the graph is directed",
                                                         default_value=True,
                                                         is_required=True)]

        # Initialise the object
        super().__init__(binary_location=binary_location,
                         input_parameter=in_param,
                         output_parameter=out_param,
                         input_transformer=PyMotifCounterInputTransformerFanmod(),
                         output_transformer=PyMotifCounterOutputTransformerFanmod(),
                         parameters=fanmod_parameters)
