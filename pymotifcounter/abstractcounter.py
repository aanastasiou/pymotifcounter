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


class Parameter:
    """
    Represents a parameter that is used to pass data to an external program.
    """
    def __init__(self,name, \
                 alias = None, \
                 is_required = False, \
                 help_str = None, \
                 validation_expr = None, \
                 default_value = None):
        self._value = None
        self._name = name
        self._alias = alias
        self._is_required = is_required
        self._help_str = help_str
        self._validation_expr = validation_expr
        self._default_value = default_value

    def _check_value(self, a_value):
        """
        Checks that a given value could be a valid value for this parameter.
        """
        if self._validation_expr.match(str(a_value)) is None and self._is_required:
            raise PyMotifCounterException_InvalidParamValue(f"Expected {self._validation_expr}, received {self._value}")
        else:
            return True
        
    def _validate(self):
        """
        Ensures that the parameter conforms to its specification
        """
        return self._check_value(self._value)
        
    def _set_value(self, a_value):
        self._check_value(a_value)
        self._value = a_value
        return self        
        
    def __call__(self):
        if self._validate():
            return self.__repr__()
            
    def __repr__(self):
        # return f"-{self._name} {str(self._value)}"
        return ["-"+self._name, str(self._value)]
        

class PyMotifCounterResultBase:
    """
    Transforms the output of a motif counter to a computable object (usually a pandas DataFrame).
    """
    def __init__(self):
        pass
        
    def __call__(self, a_ctx):
        """
        Actually performs the conversion and returns a dataframe of results.
        """
        return None
        
class PyMotifCounterNetworkRepBase:
    """
    Transforms any given networkx graph to the representation expected by a given motif counting algorithm.
    """
                    
    def __call__(self, a_graph):
        return None
        
          
class PyMotifCounterProcessBase:
    """
    Represents an external motif counting process.
    """
    
    def __init__(self, parameters = None, binary_location = None):
        if binary_location is not None:
            if not os.path.exists(binary_location):
                raise ValueError(f"{binary_location} does not exist")
            
        self._parameters = parameters or {}
        self._binary_location = binary_location
        self._input_transformer = PyMotifCounterNetworkRepBase() 
        self._output_transformer = PyMotifCounterResultBase() 
        
        
    def add_parameter(self, a_param):
        if a_param._name in self._parameters or a_param._alias in self._parameters:
            raise ValueError(f"Parameter {a_param._name} / {a_param._alias} already exists.")
            
        self._parameters[a_param._name] = a_param
        self._parameters[a_param._alias] = a_param
        return self                
        
    def get_parameter_value(self, a_param_name_or_alias):
        """
        Returns the parameter object if it exists.
        
        Notes:
            * The parameter is validated on assignment. On recall, it is assumed that its value is valid.
        """
        if a_param_name_or_alias not in self._parameters:
            raise ValueError(f"Parameter {a_param_name_or_alias} is undefined")
        return self._parameters[a_param_name_or_alias]
        
    def set_parameter_value(self, a_param_name_or_alias, a_value):
        """
        Modifies the value of an existing parameter.
        
        Notes:
            * The parameter must have been added with add_parameter first.
        """
        # Check that the parameter exists.
        if a_param_name_or_alias not in self._parameters:
            raise ValueError(f"Parameter {a_param_name_or_alias} is undefined")
        # Check that the new value is valid.
        return self._parameters[a_param_name_or_alias]._set_value(a_value)        
        
    def _validate_parameters(self):
        param_values = set(self._parameters.values())
        for a_param_value in param_values:
            a_param_value._validate()
        return self
        
    def _transform_network(self, a_graph):
        """
        Transforms a given networkx graph to the intermediate representation expected 
        by a given algorithm.
        """
        return self._input_transformer(a_graph)
        
    def _before_run(self, ctx):
        """
        Constructs a process context for a particular run.
        
        Notes:
            * Typically, obtain a network representation and add it to the context.
        """
        return ctx
        
    def _run(self, ctx):
        """
        Actually calls the external binary and adds the return value to the context
        
        Notes:
            * Typically, create the process object and pass at least the network to it.
        """
        return ctx
        
    def _after_run(self, ctx):
        """
        Performs any clean up required and returns the context.
        
        Notes:
            * Typically, erase any intermediate files if they were created anywhere else than the tmp/ folder
        """
        return ctx
    
    def __call__(self, a_graph):
        """
        Kickstarts the whole binary calling process.
        """
        # Make sure that all parameters have valid values according to the underlying
        # motif counting algorithm.
        self._validate_parameters()
        # Transform a given network to the representation expected by the underlying 
        # motif counting algorithm.
        transformed_network = self._transform_network(a_graph)
        ctx = {}
        ctx.update({"transformed_graph":transformed_network, \
                    "original_graph":a_graph})
        # Prepare...
        ctx = self._before_run(ctx)
        # ...execute...
        ctx = self._run(ctx)        
        # ...clean up.
        ctx = self._after_run(ctx) # ctx must also contain the entire file returned by the algorithm
        # Transform the output to a computable form
        return self._output_transformer(ctx)
