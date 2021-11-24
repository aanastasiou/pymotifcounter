"""
Base objects outlining the functionality of PyMotifCounter

    
:author: Athanasios Anastasiou
:date: Oct 2021
"""

import os
import types
import subprocess
import pandas

from .parameters import *
import tempfile
import shutil
from .exceptions import *
from functools import reduce


class PyMotifCounterOutputTransformerBase:
    """
    Transforms the output of a motif counter to a computable object (usually a pandas DataFrame).
    """
    def __call__(self, str_data, ctx=None):
        """
        Actually performs the conversion and returns a dataframe of results.

        :param str_data: The data holding the information to parse
        :type str_data: str
        :param ctx: Optional context of a given process call. It contains a snapshot of parameters and intermediate
                    stages associated with a given call.
        :type ctx: dict
        :returns: Computable form of the motif count data.
        :rtype: pandas.DataFrame
        """
        return None

    def from_file(self, file_path, ctx=None):
        """
        Convenience function to allow parsing any given output from binaries.

        :param file_path: A file-path to read data from
        :param file_path: str
        :param ctx: Optional context of a given call.
        :type ctx: dict
        :returns: See ``__call__()`` of the same object
        """
        with open(file_path, "rt") as fd:
            str_data = fd.read()

        return self.__call__(str_data, ctx)


class PyMotifCounterInputTransformerBase:
    """
    Transforms any given networkx graph to the representation expected by a given motif counting algorithm.
    """
    def __call__(self, a_graph):
        """
        Returns a generator of the representation of each edge of a_graph.

        :param a_graph: A ``networkx`` graph object to be analysed.
        :type a_graph: <<networkx.Graph>>
        :returns:
        """
        return None

    def to_file(self, a_graph, file_path):
        """
        Convenience function to send the output of the representation to a file on the disk.

        :param a_graph: A ``networkx`` graph object to be analysed
        :type a_graph: <<networkx.Graph>>
        :param file_path: The file to save the graph representation to.
        :type file_path: str
        :returns: See ``__call__()`` of the same object.
        :rtype:
        """
        with open(file_path, "wt") as fd:
            for a_line in self.__call__(a_graph):
                fd.write(a_line)


class PyMotifCounterBase:
    """
    Represents an external motif counting process.
    """
    
    def __init__(self, binary_location,
                 input_parameter,
                 output_parameter,
                 input_transformer,
                 output_transformer,
                 parameters):
        """
        Initialises a motif counter object.

        :param binary_location: A path leading to a binary in a location other than the default.
        :type binary_location: str
        :param input_parameter: Specification of the default way that this process accepts input
        :type input_parameter: PyMotifCounterParameterFilepath
        :param output_parameter: Specification of hte default way this process conveys its output in
        :type output_parameter: PyMotifCounterParameterFilepath
        :param input_transformer: The transformer that converts ``networkx`` graph objects to the representation
                                  expected by the underlying algorithm.
        :type input_transformer: PyMotifCounterInputTransformerBase
        :param output_transformer: The transformer that converts motif count text data to ``pandas.DataFrame``
        :type output_transformer: PyMotifCounterOutputTransformerBase
        :param parameters: A list of ``PyMotifCounterParameter`` instances describing the parameters of the algorithm.
        :type parameters: list
        """
        # TODO: MID, Add a named parameter here to enable saving the ctx variable of a run, down to a file if required.
        # BINARY LOCATION
        # Otherwise, attempt to discover the binary on the system
        # If it is not found, the binary_location will be set to "" which will raise an exception from the base
        # object
        bin_loc = shutil.which(binary_location) or ""

        if not os.path.exists(bin_loc):
            raise PyMotifCounterError(f"{self.__class__.__name__}::Binary location {bin_loc} invalid.")

        # Add parameters other than io
        self._parameters = {}
        for a_prm in parameters:
            self.add_parameter(a_prm)

        # Add io parameters
        if not isinstance(input_parameter, PyMotifCounterParameterBase):
            raise TypeError(f"input_parameter should be PyMotifCounterParameterBase, received {type(input_parameter)}")

        if not isinstance(output_parameter, PyMotifCounterParameterBase):
            raise TypeError(f"output_parameter should be PyMotifCounterParameterBase, received {type(output_parameter)}")

        self._binary_location = bin_loc
        self._input_parameter = input_parameter
        self._output_parameter = output_parameter
        self._input_transformer = input_transformer
        self._output_transformer = output_transformer
        
    @property
    def in_param(self):
        return self._input_parameter

    @property
    def out_param(self):
        return self._output_parameter

    def add_parameter(self, a_param):
        """
        Adds a new parameter that the underlying algorithm depends on.

        :param a_param: An appropriate PyMotifCounterParameter instance that describes the parameter.
        :type a_param: PyMotifCounterParameter
        :returns: The PyMotifCounter object
        :rtype: PyMotifCounterBase
        """
        if a_param._name in self._parameters or (a_param._alias is not None and a_param._alias in self._parameters):
            raise PyMotifCounterError(f"{self.__class__.__name__}::Parameter {a_param._name} / {a_param._alias} "
                                      f"already defined.")
            
        self._parameters[a_param._name] = a_param
        self._parameters[a_param._alias] = a_param
        return self                
        
    def get_parameter(self, a_param_name_or_alias):
        """
        Returns the parameter object given its name.

        :param a_param_name_or_alias: The parameter name or its alias.
        :type a_param_name_or_alias: str
        :returns: An object describing the parameter.
        :rtype: PyMotifCounterParameter
        """
        if a_param_name_or_alias not in self._parameters:
            raise PyMotifCounterError(f"{self.__class__.__name__}::Parameter {a_param_name_or_alias} "
                                      f"undefined.")
        return self._parameters[a_param_name_or_alias]

    def show_parameters(self):
        """
        Returns a human readable representation for each unique parameter defined.
        """
        return [param_info for param_info in map(lambda x:str(x), set(self._parameters.values()))]
        
    def validate_parameters(self):
        """
        Validates all parameters.

        Notes:
            * Iteratively calls the validators of each parameter.

        :returns: The same PyMotifCounter object
        """
        param_values = set(self._parameters.values())
        for a_param_value in param_values:
            a_param_value.validate()
        return self

    def _get_parameters_form(self):
        """
        Returns the "parameter form" of all defined parameters.

        Notes:
            * Iteratively calls the ``get_parameter_form()`` of each defined parameter and returns the result.

        :returns: A list of "parameter form" for each defined parameter as it would be required by subprocess.popen().
        :rtype: list
        """
        all_param_forms = set(self._parameters.values())
        p_params = []
        for a_param_value in all_param_forms:
            p_params += a_param_value.get_parameter_form()
        return p_params

    def _transform_network(self, a_graph):
        """
        Transforms a given networkx graph to the intermediate representation expected 
        by a given algorithm.
        """
        return self._input_transformer(a_graph)
        
    def _before_run(self, ctx):
        """
        Executes any preparatory steps as required by a particular algorithm.
        
        :param ctx: Current state of the process ctx, **including** ``base_transformed_graph, base_original_graph``.
        :type ctx: dict
        :returns: Updated context (depends on process specifics)
        :rtype: dict
        """
        return ctx
        
    def _run(self, ctx):
        """
        Actually calls the external process and adds the return value to the context.

        :param ctx: Current state of the process ctx, **including** ``base_transformed_graph, base_original_graph,
                    base_parameters``.
        :type ctx: dict
        :returns: Updated context (depends on process specifics)
        :rtype: dict
        """
        return ctx
        
    def _after_run(self, ctx):
        """
        Performs any clean up.
        
        :param ctx: Current state of the process ctx, **including** ``base_transformed_graph, base_original_graph,
                    base_parameters``.
        :type ctx: dict
        :returns: Updated context (depends on process specifics)
        :rtype: dict
        """
        return ctx
    
    def __call__(self, a_graph):
        """
        Initiates a motif count.

        :param a_graph: The Networkx graph to enumerate motifs over.
        :type a_graph: networkx.Graph (or any other networkx class that is supported).
        :returns: Most commonly a DataFrame that contains information about a given motif count/
        :rtype: pandas.DataFrame
        :raises: PyMotifCounterParameterError from the validation step.
        """
        # Validate parameters
        self.validate_parameters()

        # Initialise the context for this run with the given graph
        ctx = {"base_original_graph": a_graph}

        # Decide how to handle the input
        if self.in_param.value == "-":
            # If the input parameter is stdin then use the attached transformer to transform a given
            # network to the representation expected by the underlying motif counting algorithm.
            ctx.update({"base_transformed_graph": "".join(self._input_transformer(a_graph))})
        else:
            # If the input parameter is not stdin it will be a temporary file
            _, in_tmp_file_name = tempfile.mkstemp()
            self._input_transformer.to_file(a_graph, file_path=in_tmp_file_name)
            self.in_param.default_value = in_tmp_file_name

        # Similarly, update the output parameter but in this case no actual io is performed because the
        # output is not yet available.
        # If the output is to be sent to a temporary file, determine that here.
        if self.out_param.value != "-":
            _, out_tmp_file_name = tempfile.mkstemp()
            self.out_param.default_value = out_tmp_file_name

        # Provided that everything is alright, get all the parameters in their appropriate form
        # In doing this, we still need to retain the parameter ordering to discriminate between positional arguments and
        # options
        all_parameters = set(self._parameters.values())
        p_params = [{"param": a_param.get_parameter_form(), "pos": a_param.pos} for a_param in all_parameters]

        # If either of the io variables are to be sent to an std stream then remove them from the parameters
        if self.in_param.value != "-":
            p_params += [{"param": self.in_param.get_parameter_form(), "pos": self.in_param.pos}]

        if self.out_param.value != "-":
            p_params += [{"param": self.out_param.get_parameter_form(), "pos": self.out_param.pos}]

        # Now sort these parameters and get th final form
        p_params = list(reduce(lambda x, y: x + y["param"], sorted(p_params, key=lambda z: z["pos"]), []))

        ctx.update({"base_parameters": p_params})

        # Run any other preparation
        ctx = self._before_run(ctx)

        # ...execute...
        # Create the process object
        # TODO: HIGH, this needs exception handling for timeout
        # TODO: HIGH, if the process returns an error, this error should be piped up as an exception

        # Decide where to direct the input
        if self.in_param.value != "-":
            p = subprocess.Popen([self._binary_location] + p_params,
                                 universal_newlines=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = p.communicate(timeout=320)
        else:
            p = subprocess.Popen([self._binary_location] + p_params,
                                 universal_newlines=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = p.communicate(input=ctx["base_transformed_graph"], timeout=320)

        ctx.update({"base_proc_response": out,
                    "base_proc_error": err})

        # Transform the output to a computable form
        if self.out_param.value != "-":
            final_output = self._output_transformer.from_file(self.out_param.value, ctx)
        else:
            final_output = self._output_transformer(out, ctx)
        ctx.update({"base_output_transformed": final_output})

        # Clean up temporary files
        if self.in_param.value != "-":
            if os.path.exists(self.in_param.value):
                os.remove(self.in_param.value)

        if self.out_param.value != "-":
            if os.path.exists(self.out_param.value):
                os.remove(self.out_param.value)

        # Do any other cleanup.
        ctx = self._after_run(ctx)

        return final_output
