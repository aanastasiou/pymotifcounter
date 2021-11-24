"""
Implements the pgd concrete counter.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import networkx
import pyparsing
import pandas
from .abstractcounter import *


class PyMotifCounterOutputTransformerPgd(PyMotifCounterOutputTransformerBase):
    @staticmethod
    def _get_parser():
        """
        Parses the actual graphlet counts section of PGD's output.

        :return: The top level element of a PyParsing parser that handles the extraction of the useful data.
        :rtype: pyparsing.ParserElement
        """
        # TODO: HIGH, Use float_num to parse the rest of the sections and offer them as additional columns
        float_num = pyparsing.Regex(r"([+-]?)(nan|([0-9]*)\.([0-9]+))").setParseAction(lambda s, l, t: float(t[0]))
        int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s, l, t: int(t[0]))
        # Section start
        section_start_end = pyparsing.Suppress(pyparsing.Literal("****************************"
                                                                 "********************************"))
        # Section divide
        section_divide = pyparsing.Suppress(pyparsing.Literal("----------------------------------------"))
        # Parsing graphlet name as a generic identifier
        graphlet_name = pyparsing.Regex("[a-z_0-9]+")
        # Then using this mapping to get its motif id. Notice the return type: (Motif_id, N_Nodes)
        graphlet_to_id = {"total_4_clique": "(31710, 4)",
                          "total_4_chordcycle": "(23390, 4)",
                          "total_4_tailed_tris": "(4958, 4)",
                          "total_4_cycle": "(23130, 4)",
                          "total_3_star": "(30856, 4)",
                          "total_4_path": "(23112, 4)",

                          "total_4_tri": "(22796, 4)",
                          "total_4_2star": "(22536, 4)",
                          "total_4_2edge": "(18450, 4)",
                          "total_4_1edge": "(18432, 4)",
                          "total_4_indep": "(0, 4)",

                          "total_3_tris": "(238, 3)",
                          "total_2_star": "(78, 3)",
                          "total_3_1edge": "(160, 3)",
                          "total_3_indep": "(0, 3)",

                          "total_2_1edge": "(60, 2)",
                          "total_2_indep": "(0, 2)",
                          }
        # One result entry to be parsed is basically a key, value pair
        graphlet_count_entry = pyparsing.Group(graphlet_name("motif_id").setParseAction(lambda s, l, t: graphlet_to_id[t[0]]) +
                                               pyparsing.Suppress("=") +
                                               int_num("count"))

        # Graphlet counts is basically one or more key-value pairs, plus the section delimiters
        graphlet_counts = pyparsing.Group(section_start_end +
                                          pyparsing.OneOrMore(graphlet_count_entry ^ section_divide) +
                                          section_start_end
                                          )

        return graphlet_counts("enumeration")

    def __call__(self, str_data, a_ctx=None):
        """
        Transforms the raw string output from the pgd process to a computable pandas DataFrame

        :param str_data:
        :type str_data:
        :param a_ctx: Dictionary of context information from the subsequent execution steps
        :type a_ctx: dict
        :return: A DataFrame with all enumerated graphlets according to pgd.
        :rtype: pandas.DataFrame
        """
        parsed_output = self._get_parser().searchString(str_data)
        # TODO: LOW, Revise the parser so that it only has one root level.
        # Notice here how the parser's row field names are propagated to the columns of the returned DataFrame
        df_output = pandas.DataFrame(columns=list(parsed_output[0]["enumeration"][0].keys()), index=None)
        for a_row_idx, a_row_data in enumerate(parsed_output[0]["enumeration"]):
            # TODO: HIGH, The conversion can be performed more automatically through pandas rather than a loop
            df_output.at[a_row_idx, "motif_id"] = a_row_data["motif_id"]
            df_output.at[a_row_idx, "count"] = a_row_data["count"]
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
    """
    Implements the concrete pgd graphlet counter.

    The following parameters are supported:

    :param w: Number of PROCESSING UNITS (workers) for the algorithm to use (default ``max``)
    :type w: String (Numeric)
    :param b: Size of batch (number of jobs) dynamically assigned to the processing unit, that is, 1, 64, 512, etc.
              (Default: 64)
    :type b: Integer
    """
    def __init__(self, binary_location="pgd"):

        # pgd I/O parameters
        in_param = PyMotifCounterParameterFilepath(name="f",
                                                   alias="pgd_in",
                                                   help_str="Input file",
                                                   exists=True,
                                                   is_required=True,)

        out_param = PyMotifCounterParameterFilepath(name="out",
                                                    alias="pgd_out",
                                                    help_str="Output file name",
                                                    exists=False,
                                                    default_value="-",
                                                    is_required=True,)
        # Interface to the rest of the parameters
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
        # Build the base object
        super().__init__(binary_location=binary_location,
                         input_parameter=in_param,
                         output_parameter=out_param,
                         input_transformer=PyMotifCounterInputTransformerPgd(),
                         output_transformer=PyMotifCounterOutputTransformerPgd(),
                         parameters=pgd_parameters)


