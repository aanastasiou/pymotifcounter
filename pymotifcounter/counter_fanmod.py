"""
Implements the fanmod_cmd concrete counter.

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


class PyMotifCounterOutputTransformerFanmod(PyMotifCounterOutputTransformerBase):
    # TODO: MID, The parser --> DataFrame is pretty standard by now, should be incorporated in the standard round-trip
    @staticmethod
    def _get_parser():
        """
        Parses the "Result overview:" section of fanmod's output.

        :return: The top level element of a PyParsing parser that handles the extraction of the useful data.
        :rtype: pyparsing.ParserElement
        """
        # TODO: LOW, Consider abstracting these two somehow as these definitions will be useful for every parser.
        # TODO: HIGH, Make sure that the float can parse just integer part too.
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

    def __call__(self, a_ctx):
        """
        Transforms the raw string output from the fanmod process to a computable pandas DataFrame

        :param a_ctx: Dictionary of context information from the subsequent execution steps
        :type a_ctx: dict
        :return: A DataFrame with all enumerated motifs according to fanmod's algorithm.
        :rtype: pandas.DataFrame
        """
        parsed_output = self._get_parser().searchString(a_ctx["proc_response"])
        # TODO: LOW, Revise the parser so that it only has one root level.
        # Notice here how the parser's row field names are propagated to the columns of the returned DataFrame
        df_output = pandas.DataFrame(columns=list(filter(lambda x: x != "Adj_Matrix", parsed_output[0]["enumeration"][0].keys())), index=None)
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
        # Obtain network representation
        # First of all, encode the node ID to a number.
        nodeid_to_num = dict(zip(a_graph.nodes(), range(1, a_graph.number_of_nodes()+1)))
        num_to_noded = {value: key for key, value in nodeid_to_num.items()}
        # Create the edge list
        return "".join(map(lambda x: f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\n",
                           networkx.to_edgelist(a_graph)))


class PyMotifCounterFanmod(PyMotifCounterBase):
    def __init__(self, binary_location=None):
        # Build the base model
        # TODO: HIGH, this can be abstracted further to a function that performs autodiscovery of the binary's location
        # TODO: HIGH, the validation can be a function
        # TODO: MID, add the output file name and use it when it is specified
        super().__init__(binary_location=binary_location or "fanmod_cmd")
        # Exchange the input transformer
        self._input_transformer = PyMotifCounterInputTransformerFanmod()
        # Exchange the result transformer
        self._output_transformer = PyMotifCounterOutputTransformerFanmod()
        # Add the right parameters
        # Note here, fanmod's parameters for motif size and random networks are almost identical to mfinder's
        # Motif size
        self.add_parameter(PyMotifCounterParameter(name="s",
                                                   alias="motif_size",
                                                   help_str="Motif size to search",
                                                   validation_expr=re.compile("[3-4]")))
        # Number of random networks to establish significance over.
        self.add_parameter(PyMotifCounterParameter(name="r",
                                                   alias="n_random",
                                                   help_str="Number of random networks to generate",
                                                   validation_expr=re.compile("[0-9]+")))
        # TODO: LOW, if the default value is bool then the parameter is flag.
        # TODO: HIGH, Change the validation here from numeric to proper bool when you fix the validation to be performed by a function
        # TODO: MID, Check to see if the "directedness" of the algorithm could depend on the networkx.Graph at the input so that the parameter value is set automatically.
        # Whether the network is directed (by default it should be considered directed)
        self.add_parameter(PyMotifCounterParameter(name="d",
                                                   alias="is_directed",
                                                   help_str="Set if the graph is directed",
                                                   validation_expr=re.compile("[0-1]+"),
                                                   default_value=1,
                                                   is_flag=True,
                                                   is_required=True))
        self.set_parameter_value("s", 3)
        self.set_parameter_value("r", 0)
        self.set_parameter_value("d", 1)
                                     
    def _run(self, ctx):
        # Group parameters
        # TODO: HIGH, this step can be abstracted
        all_param_values = set(self._parameters.values())
        p_params = []
        for a_param_value in all_param_values:
            p_params.extend(a_param_value())

        # TODO: HIGH, this needs exception handling
        # TODO: HIGH, Add a prefix that depends on the binary
        # fanmod_cmd works off of a file, so first save the input representation down to a file in temporary storage
        tmp_fileno, tmp_filename = tempfile.mkstemp()
        ctx["temporary_filename"] = tmp_filename
        # Populate the file with the intermediate representation
        with os.fdopen(tmp_fileno, "wt") as fd:
            fd.write(ctx["transformed_graph"])
        # TODO: HIGH, this can become a parameter with a __TEMP__default value
        # Add the input file as a parameter
        p_params += ["-i", tmp_filename]

        # For fanmod_cmd, we also have to determine the output file explicitly
        _, tmp_filename_out = tempfile.mkstemp()
        ctx["temporary_filename_output"] = tmp_filename_out
        p_params += ["-o", tmp_filename_out]
        # Create the process object
        # TODO: HIGH, this needs exception handling for timeout
        # TODO: HIGH, if the process returns an error, this error should be piped up as an exception
        p = subprocess.Popen([self._binary_location] + p_params, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Call the process
        out, err = p.communicate(timeout=320)
        # With fanmod we know exactly where we have placed the file and can retrieve it from there.
        with open(ctx["temporary_filename_output"], "rt") as fd:
            out = fd.read()
        
        ret_ctx = {}
        ret_ctx.update(ctx)
        ret_ctx.update({"proc_response": out,
                        "proc_error": err,
                        "fanmod_input_file": ctx["temporary_filename"],
                        "fanmod_output_file": ctx["temporary_filename_output"]})
        return ret_ctx
        
    def _after_run(self, ctx):
        """
        Performs any cleanup after the process has run and produced results.
        
        Notes:
            * Fanmod requires both an input and an output file at its input which have to be deleted when the
              process finishes.
        """
        if os.path.exists(ctx["fanmod_input_file"]):
            os.remove(ctx["fanmod_input_file"])
            
        if os.path.exists(ctx["fanmod_output_file"]):
            os.remove(ctx["fanmod_output_file"])
        
        return ctx
