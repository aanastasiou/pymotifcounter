"""

    A set of experiments to get familiar with click.Option objects
    
    
:author: Athanasios Anastasiou
:date: Oct 2021

class Process:
    parameters: List[Parameter]
    binarylocation: Path
    raw_output
    
    __call__()
        ctx = before_run()
        ctx = run(ctx)
        ctx = after_run(ctx) #ctx must also contain the entire file returned by the algorithm
        return ctx    
    
class Parameter
    tag
    docstr
    type
    is_required
    

class MotifResultParser


class MotifResult

    
class MotifCounter
    Process process
    MotifResultParser parser
        
    __call__()
    Run process
    run motifresultparser on the result of process
    return a MotifResult   

"""    
import re
import networkx
import typing

class PyMotifCounterException(Exception):
    pass
    
class PyMotifCounterException_InvalidParamValue(PyMotifCounterException):
    pass

class Parameter:
    """
    Represents a parameter that is used to pass data to an external program.
    """
    def __init__(self,name, \
                 alias = none, \
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

    def _validate(self):
        """
        Ensures that the parameter conforms to its specification
        """
        if self._validation_expr.match(str(self._value)) is None and self._is_required:
            raise PyMotifCounterException_InvalidParamValue(f"Expected {self._validation_expr}, received {self._value}")
        else:
            return True
        
    def __call__(self):
        if self._validate():
            return self.__repr__()
            
    def __repr__(self):
        return f"-{self._name} {str(self._value)}"
        
class MotifCountResultBase:
    def __init__(self, ctx):
        raise Exception("Not implemented")
        # # Process theoutput (if succesfull)
        # # TODO:HIGH, need to inspect the `err` and raise appropriate errors
        # outputData = self._output_parser.parseString(out)
        # D = pandas.DataFrame(columns=list(outputData["zscore"][0].keys()) + ["ave_rand_freq_sd", "ave_rand_conc_sd"], index = None)
        # for an_item in enumerate(outputData["zscore"]):
            # D.at[an_item[0], "gID"] = an_item[1]["gID"]
            # D.at[an_item[0], "freq"] = an_item[1]["freq"]
            # D.at[an_item[0], "conc"] = an_item[1]["conc"]
            # D.at[an_item[0], "f-ZScore"] = an_item[1]["f-ZScore"]
            # D.at[an_item[0], "f-pValue"] = an_item[1]["f-pValue"]
            # D.at[an_item[0], "c-ZScore"] = an_item[1]["c-ZScore"]
            # D.at[an_item[0], "c-pValue"] = an_item[1]["c-pValue"]
            # D.at[an_item[0], "ave_rand_freq"] = an_item[1]["ave_rand_freq"]["ave_rand_freq"]
            # D.at[an_item[0], "ave_rand_conc"] = an_item[1]["ave_rand_conc"]["ave_rand_conc"]
            # D.at[an_item[0], "ave_rand_freq_sd"] = an_item[1]["ave_rand_freq"]["sd"]
            # D.at[an_item[0], "ave_rand_conc_sd"] = an_item[1]["ave_rand_conc"]["sd"]
            
        # with open("adjMat.txt", "rt") as fd:
            # adj_mat_data = fd.read()
        # parsed_adjacency_results = self._adjacency_matrix_parser.parseString(adj_mat_data)
        # identified_motifs = {}
        # for an_item in parsed_adjacency_results:
            # identified_motifs[an_item["graphID"]] = an_item["G"]

        
class PyMotifCounterProcessBase:
    """
    Represents an external process.
    """
    
    def __init__(self, parameters = None, binary_location = None):
        self._parameters = parameters
        self._binary_location = binary_location
        
    def add_parameter(a_param):
        self._parameters.append(a_param)
        return self                
    
    def _before_run(self, a_graph):
        """
        Constructs a process context for a particular run.
        
        Notes:
            * Typically, obtain a network representation and add it to the context.
        """
        return None
        
    def _run(self, ctx, a_graph):
        """
        Actually calls the external binary and adds the return value to the context
        
        Notes:
            * Typically, create the process object and pass at least the network to it.
        """
        return ctx
        
    def _after_run(self, ctx, a_graph):
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
        ctx = self._before_run(a_graph)
        ctx = self._run(ctx, a_graph)
        ctx = after_run(ctx, a_graph) #ctx must also contain the entire file returned by the algorithm
        return MotifCountResultBase(ctx)  
        
class PyMotifCounterNetMode(PyMotifCounterProcessBase):
    def __init__(self):
        super().__init__()
        self.add_parameter(Parameter(name="s", \
                                     long_name="specify", \
                                     help_str="Specify length", \
                                     validation_expr=re.compile("[0-9]+")))
                                     


        

# class PyMotifNetMODECounter(PyMotifCounterProcessBase):
    # """
    # Represents a NetMODE call.
    # """
    # def __init__(self):
        # self.parameters.append(Parameter(name="k", help_str="Motif size", validation_exr=re.compile("3|4|5

if __name__ == "__main__":
    # v1 = Parameter(name="s", long_name="specify", help_str="Specify length", validation_expr=re.compile("[0-9]+"), is_required=False, param_value=23)
    # q = PyMotifCounterProcessCommon()
    q = PyMotifCounterProcessCommon()
    
    
    
