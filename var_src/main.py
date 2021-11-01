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
import os
import re
import networkx
import subprocess
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
    
    def __init__(self, parameters = {}, binary_location = None):
        if binary_location is not None:
            if not os.path.exists(binary_location):
                raise ValueError(f"{binary_location} does not exist")
            
        self._parameters = parameters
        self._binary_location = binary_location
        
    def add_parameter(self, a_param):
        if a_param._name in self._parameters or a_param._alias in self._parameters:
            raise ValueError(f"Parameter {a_param._name / a_param._alias} already exists.")
            
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
        self._validate_parameters()
        ctx = self._before_run(a_graph)
        ctx = self._run(ctx, a_graph)
        ctx = self._after_run(ctx, a_graph) #ctx must also contain the entire file returned by the algorithm
        return ctx
        # return MotifCountResultBase(ctx)  
        
class PyMotifCounterNetMODE(PyMotifCounterProcessBase):
    def __init__(self):
        super().__init__(binary_location="../binaries/NetMODE/NetMODE")
        self.add_parameter(Parameter(name="k", \
                                     alias="motif_size", \
                                     help_str="k-node subgraphs (=3,4,5 or 6)", \
                                     validation_expr=re.compile("[3-6]")))
        self.add_parameter(Parameter(name="c", \
                                     alias="n_random", \
                                     help_str="Number of comparison graphs (An integer in [0, 2^31))", \
                                     validation_expr=re.compile("[0-9]+")))
        self.set_parameter_value("k", 3)
        self.set_parameter_value("c", 0)
                                     
    def _before_run(self, a_graph):
        # Obtain network representation
        # First of all, encode the node ID to a number. NetMODE works only with numeric nodes
        nodeid_to_num = dict(zip(a_graph.nodes(), range(1, a_graph.number_of_nodes()+1)))
        num_to_noded = {value:key for key, value in nodeid_to_num.items()}
        # Create the edge list, translate node ids and convert to string data in one call.
        netmode_input = f"{a_graph.number_of_nodes()}\n" + "".join(map(lambda x:f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\n", networkx.to_edgelist(a_graph)))
        return {"edge_list":netmode_input}
        
    def _run(self, ctx, a_graph):
        # Group parameters
        all_param_values = set(self._parameters.values())
        p_params = []
        for a_param_value in all_param_values:
            p_params.extend(a_param_value())
            
        import pdb
        pdb.set_trace()
        # Create the process object
        # p = subprocess.Popen([f"{self._binary_location}NetMODE", "-k", f"{self._knodesize}", "-e", f"{self._edge_random_method}", "-c", f"{self._nrandom}"], universal_newlines=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = subprocess.Popen([self._binary_location] + p_params, universal_newlines=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Call the process
        out, err = p.communicate(input = ctx["edge_list"], timeout=320)
        
        ret_ctx = {}
        ret_ctx.update(ctx)
        ret_ctx.update({"proc_response":out, \
                        "proc_error":err})
        return ret_ctx        

# class PyMotifNetMODECounter(PyMotifCounterProcessBase):
    # """
    # Represents a NetMODE call.
    # """
    # def __init__(self):
        # self.parameters.append(Parameter(name="k", help_str="Motif size", validation_exr=re.compile("3|4|5

if __name__ == "__main__":
    # v1 = Parameter(name="s", long_name="specify", help_str="Specify length", validation_expr=re.compile("[0-9]+"), is_required=False, param_value=23)
    q = PyMotifCounterNetMODE()
    # q = PyMotifCounterProcessCommon()
    g = networkx.watts_strogatz_graph(64,4,0.8)
    z = q(g)
    
    
    
