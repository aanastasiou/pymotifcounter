"""
Base objects outlining the functionality of PyMotifCounter

    
:author: Athanasios Anastasiou
:date: Oct 2021
"""

import os
import re
import networkx
import subprocess
import pyparsing
import pandas
from .exceptions import *


class PyMotifCounterParameter:
    """
    Represents a parameter that is used to pass data to an external program.
    """
    def __init__(self, name,
                 alias=None,
                 validation_expr=None,
                 is_required=True,
                 help_str=None,
                 default_value=None,
                 is_flag=False):
        """
        Initialises a parameter and performs some basic validation.

        :param name: The name of the parameter as it is expected by the binary (e.g. -s, --directed, etc)
        :type name: str
        :param alias: An alternative name by which this parameter can also be known as.
        :type alias: str
        :param is_required: Whether this parameter should always be present when calling a binary
        :type is_required: bool
        :param help_str: A short description of the parameter's use. Usually taken verbatim from the binary ``--help``
                         output.
        :type help_str: str
        :param validation_expr: A regexp validation expression that describes the set of valid values for the parameter.
        :type validation_expr: re.Pattern
        :param default_value: The default value for this parameter
        :type default_value: Any
        :param is_flag: Whether this parameter is a flag (the parameter's ``name`` is not followed by its value on the
                        command line).
        :type is_flag: bool
        """

        self._value = None
        self._name = name
        self._alias = alias
        self._is_required = is_required
        self._help_str = help_str
        self._validation_expr = validation_expr
        self._default_value = default_value
        self._is_flag = is_flag

        if type(self._validation_expr) is not re.Pattern:
            if not self._is_flag:
                raise PyMotifCounterParameterError(f"Parameter {self._name} / {self._alias} must specify "
                                                   f"an appropriate validation expression. "
                                                   f"Received {self._validation_expr}")
            else:
                self._validation_expr = None

        if self._is_required and self._default_value is None:
            if not self._is_flag:
                raise PyMotifCounterParameterError(f"Required parameter {self._name} / {self._alias} must specify "
                                                   f"valid default value.")

        if self._is_required:
            if not self._is_flag:
                try:
                    self._check_value(self._default_value)
                except PyMotifCounterParameterError:
                    raise PyMotifCounterParameterError(f"Required parameter {self._name} / {self._alias} must specify "
                                                       f"valid default value.")
        self.validate()

    def _check_value(self, a_value):
        """
        Checks that the current parameter value is valid for this parameter's use context.

        :param a_value: The value to check for validity
        :type a_value: Any
        :returns: True
        :rtype: bool
        :raises: Validation exception

        """
        if a_value is not None or self._is_required:
            if not self._is_flag and self._validation_expr.match(str(a_value)) is None:
                raise PyMotifCounterParameterError(f"Parameter {self._name} / {self._alias} "
                                                   f"expected {self._validation_expr}, received {a_value}")
        else:
            raise PyMotifCounterParameterError(f"Parameter {self._name} / {self._alias} is required.")

        return True
        
    def validate(self):
        """
        Ensures that the parameter conforms to its specification
        """
        return self._check_value(self.get_value())
        
    def set_value(self, a_value):
        """
        Sets the parameter to a specific value.

        Notes:
            * Validation is handled **always** when a value is set to a parameter.

        :param a_value: The new value to set the parameter to.
        :type a
        :return:
        """
        self._check_value(a_value)
        self._value = a_value
        return self

    def get_value(self):
        """
        Gets the current value of the parameter.

        :return:
        """
        if not self._is_flag:
            return self._value or self._default_value
        else:
            return self._value is not None

    def get_parameter_form(self):
        """
        Returns the parameter in the right representation expected by ``subprocess.popen``

        :return: An ``n`` element list depending on the parameter type.
        :rtype: list
        """
        param_value = self.get_value()
        # Assume that the value is optional...
        value_to_return = []
        if param_value is not None or self._is_required:
            # If it is required (it cannot be None) or if it is not None anyway then assume that the value is
            # a flag (and if it is a flag a non-zero value would mean that it should be present in the output).
            value_to_return = [f"-{self._name}"]
            if not self._is_flag:
                # If the value is not a flag (but is still required -or has non-None value-) then add the actual value
                value_to_return += [str(param_value)]
        return value_to_return

        
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
        return None
        
          
class PyMotifCounterBase:
    """
    Represents an external motif counting process.
    """
    
    def __init__(self, binary_location="", parameters=None):
        if not os.path.exists(binary_location):
            raise PyMotifCounterError(f"{self.__class__.__name__}::Binary location {binary_location} invalid.")

        # TODO: HIGH, Parameters need to be re-iterated to check for duplicates appropriately.
        self._parameters = parameters or {}
        self._binary_location = binary_location
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
            raise PyMotifCounterError(f"{self.__class__.__name__}::Parameter {a_param._name} / {a_param._alias} "
                                      f"undefined.")
        return self._parameters[a_param_name_or_alias]
        
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
        # Initialise the context for this run
        ctx = {}
        # Validate parameters
        self.validate_parameters()
        # Provided that everything is alright, add the parameters to the context
        ctx = self._get_parameters_form(ctx)
        # Use the attached transformer to transform a given network to the representation
        # expected by the underlying motif counting algorithm.
        transformed_network = self._transform_network(a_graph)
        ctx.update({"base_transformed_graph": transformed_network,
                    "base_original_graph": a_graph})
        # Prepare...
        ctx = self._before_run(ctx)
        # ...execute...
        ctx = self._run(ctx)        
        # ...clean up.
        ctx = self._after_run(ctx)
        # Transform the output to a computable form
        return self._output_transformer(ctx)
