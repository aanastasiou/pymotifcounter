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
from .exceptions import *


class PyMotifCounterOutputTransformerBase:
    """
    Transforms the output of a motif counter to a computable object (usually a pandas DataFrame).
    """
    def __call__(self, a_ctx):
        """
        Actually performs the conversion and returns a dataframe of results.
        """
        return None


class PyMotifCounterInputTransformerBase:
    """
    Transforms any given networkx graph to the representation expected by a given motif counting algorithm.
    """
    def __call__(self, a_graph):
        """
        Returns a generator of the representation of each edge of a_graph.
        """
        return None

    def to_file(self, a_graph, file_path):
        """
        Convenience function to send the output of the representation to a file on the disk.

        :param a_graph:
        :type a_graph:
        :param file_path:
        :type file_path:
        :returns:
        :rtype:
        """
        with open(file_path, "wt") as fd:
            for a_line in self.__call__(a_graph):
                fd.write(a_line)


class PyMotifCounterBase:
    """
    Represents an external motif counting process.
    """
    
    def __init__(self, binary_location="",
                 input_file_param=None,
                 output_file_param=None,
                 parameters=None):
        """
        Initialises a motif counter object.

        :param binary_location:
        :type binary_location:
        :param input_file_param:
        :type input_file_param:
        :param output_file_param:
        :type output_file_param:
        :param parameters:
        :type parameters:
        """
        if not os.path.exists(binary_location):
            raise PyMotifCounterError(f"{self.__class__.__name__}::Binary location {binary_location} invalid.")

        # TODO: HIGH, Parameters need to be re-iterated to check for duplicates appropriately.
        self._parameters = parameters or {}

        if not isinstance(input_file_param, PyMotifCounterParameterBase):
            raise TypeError(f"input_file_param should be PyMotifCounterParameter, received {type(input_file_param)}")
        else:
            self.add_parameter(input_file_param)

        if not isinstance(output_file_param, PyMotifCounterParameterBase):
            raise TypeError(f"output_file_param should be PyMotifCounterParameter, received {type(output_file_param)}")
        else:
            self.add_parameter(output_file_param)

        self._binary_location = binary_location
        self._input_file_param_name = input_file_param._name
        self._output_file_param_name = output_file_param._name
        self._input_transformer = PyMotifCounterInputTransformerBase()
        self._output_transformer = PyMotifCounterOutputTransformerBase()
        
    def add_parameter(self, a_param):
        if a_param._name in self._parameters or a_param._alias in self._parameters:
            raise PyMotifCounterError(f"{self.__class__.__name__}::Parameter {a_param._name} / {a_param._alias} "
                                      f"already defined.")
            
        self._parameters[a_param._name] = a_param
        self._parameters[a_param._alias] = a_param

        return self                
        
    def get_parameter(self, a_param_name_or_alias):
        """
        Returns the parameter object if it exists.
        """
        if a_param_name_or_alias not in self._parameters:
            raise PyMotifCounterError(f"{self.__class__.__name__}::Parameter {a_param_name_or_alias} "
                                      f"undefined.")
        return self._parameters[a_param_name_or_alias]

    def show_parameters(self):
        """
        Returns a human readable representation for each unique parameter defined
        """
        return [param_info for param_info in map(lambda x:str(x), set(self._parameters.values()))]
        
    def validate_parameters(self):
        param_values = set(self._parameters.values())
        for a_param_value in param_values:
            a_param_value.validate()
        return self

    def _get_parameters_form(self, ctx):
        """
        Retrieves the "parameter form" for each defined parameter as it would be required by subprocess.popen()

        Notes:
            * The ``ctx`` dictionary is used to pass information between the individual stages of a particular "run".

        :param ctx: Current state of the process ctx.
        :type ctx: dict
        :returns: Updated context with ``base_parameters`` attribute (unrolled parameters as
                  expected by subprocess.popen())
        :rtype: dict
        """
        all_param_forms = set(self._parameters.values())
        p_params = []
        for a_param_value in all_param_forms:
            p_params.extend(a_param_value.get_parameter_form())
        new_ctx = {}
        new_ctx.update(ctx)
        new_ctx["base_parameters"] = p_params
        return new_ctx

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
        # TODO: MID, Add a named parameter here to enable saving the ctx variable of a run down to a file if required.
        # Validate parameters
        self.validate_parameters()

        # Initialise the context for this run with the given graph
        ctx = {"base_original_graph": a_graph}

        # Update the input parameter value to whatever its appropriate value should be
        in_param = self.get_parameter(self._input_file_param_name)
        in_param_value = in_param.value
        if in_param_value == "-":
            # If the input parameter is stdin then use the attached transformer to transform a given
            # network to the representation expected by the underlying motif counting algorithm.
            ctx.update({"base_transformed_graph": "".join(self._input_transformer(a_graph))})
        elif not in_param.is_set():
            # If the input parameter has not been assigned to a value then send the input to a temporary file
            _, in_tmp_file_name = tempfile.mkstemp()
            self._input_transformer.to_file(a_graph, file_path=in_tmp_file_name)
            in_param.value = in_tmp_file_name
        else:
            # TODO: HIGH, Raise an exception about the file parameter not being in the right state.
            pass

        # Similarly, update the output parameter but in this case no actual io is performed because the
        # output is not yet available.
        out_param = self.get_parameter(self._output_file_param_name)
        out_param_value = out_param.value
        # If the output is to be sent to a temporary file, determine that here.
        if not out_param.is_set():
            _, out_tmp_file_name = tempfile.mkstemp()
            out_param.value = out_tmp_file_name

        # # Provided that everything is alright, get all the parameters in their appropriate form
        ctx = self._get_parameters_form(ctx)

        # Run any other preparation
        ctx = self._before_run(ctx)

        # ...execute...
        # TODO: HIGH, this needs exception handling

        # Create the process object
        # TODO: HIGH, this needs exception handling for timeout
        # TODO: HIGH, if the process returns an error, this error should be piped up as an exception
        p = subprocess.Popen([self._binary_location] + p_params, universal_newlines=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Call the process
        out, err = p.communicate(timeout=320)

        ctx.update({"base_proc_response": out,
                    "base_proc_error": err})

        # ...clean up.
        ctx = self._after_run(ctx)
        # Transform the output to a computable form
        return self._output_transformer(ctx)
