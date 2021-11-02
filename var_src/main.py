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
import pyparsing
import pandas

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
        

class PyMotifCounterResultBase:
    def __init__(self):
        pass
        
    def __call__(self, a_ctx, a_graph):
        """
        Actually performs the conversion and returns a dataframe of results.
        """
        return None

       
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
        self._result_transformer = PyMotifCounterResultBase() 
        
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
        return self._result_transformer(ctx, a_graph)

        
class PyMotifCounterResultNetMODE(PyMotifCounterResultBase):
    @staticmethod
    def _get_parser():
        """
        Returns a parser that is used to transform the output of a given algorithm 
        to computable form.
        
        Notes:
            * This is usually a pyparsing parser.
        """
        float_num = pyparsing.Regex(r"([+-]?)(nan|([0-9]*)\.([0-9]+))").setParseAction(lambda s, l ,t:float(t[0]))
        int_num = pyparsing.Regex(r"[0-9]+").setParseAction(lambda s,l,t:int(t[0]))
        gID = (pyparsing.Suppress("gID:") + int_num("gID"))
        freq = (pyparsing.Suppress("freq:") + int_num("freq"))
        ave_rand_freq = pyparsing.Group(pyparsing.Suppress("ave_rand_freq:") + float_num("ave_rand_freq") + pyparsing.Suppress("(sd:") + float_num("sd") + pyparsing.Suppress(")"))("ave_rand_freq")
        conc = (pyparsing.Suppress("conc:") + float_num("conc"))
        ave_rand_conc = pyparsing.Group(pyparsing.Suppress("ave_rand_conc:") + float_num("ave_rand_conc") + pyparsing.Suppress("(sd:") + float_num("sd") + pyparsing.Suppress(")"))("ave_rand_conc")
        fzscore = (pyparsing.Suppress("f-ZScore:") + float_num("f-ZScore"))
        fpvalue = (pyparsing.Suppress("f-pValue:") + float_num("f-pValue"))
        czscore = (pyparsing.Suppress("c-ZScore:") + float_num("c-ZScore"))
        cpvalue = (pyparsing.Suppress("c-pValue:") + float_num("c-pValue"))
        row_data = pyparsing.Group(gID + freq + ave_rand_freq + conc + ave_rand_conc + fzscore + fpvalue + czscore + cpvalue)
        data_parsing = (pyparsing.Suppress(r"calc Z-Score") + pyparsing.ZeroOrMore(row_data))("zscore")
        return data_parsing
            
    def __init__(self):
        self._parser = self._get_parser()
        
    def __call__(self, a_ctx, a_graph):
        # Process theoutput (if succesfull)
        # TODO:HIGH, need to inspect the `err` and raise appropriate errors
        outputData = self._parser.parseString(a_ctx["proc_response"])
        ret_dataframe = pandas.DataFrame(columns=list(outputData["zscore"][0].keys()) + ["ave_rand_freq_sd", "ave_rand_conc_sd"], index = None)
        for an_item_idx, an_item in enumerate(outputData["zscore"]):
            ret_dataframe.at[an_item_idx, "gID"] = an_item["gID"]
            ret_dataframe.at[an_item_idx, "freq"] = an_item["freq"]
            ret_dataframe.at[an_item_idx, "conc"] = an_item["conc"]
            ret_dataframe.at[an_item_idx, "f-ZScore"] = an_item["f-ZScore"]
            ret_dataframe.at[an_item_idx, "f-pValue"] = an_item["f-pValue"]
            ret_dataframe.at[an_item_idx, "c-ZScore"] = an_item["c-ZScore"]
            ret_dataframe.at[an_item_idx, "c-pValue"] = an_item["c-pValue"]
            ret_dataframe.at[an_item_idx, "ave_rand_freq"] = an_item["ave_rand_freq"]["ave_rand_freq"]
            ret_dataframe.at[an_item_idx, "ave_rand_conc"] = an_item["ave_rand_conc"]["ave_rand_conc"]
            ret_dataframe.at[an_item_idx, "ave_rand_freq_sd"] = an_item["ave_rand_freq"]["sd"]
            ret_dataframe.at[an_item_idx, "ave_rand_conc_sd"] = an_item["ave_rand_conc"]["sd"]
        return ret_dataframe    
        # with open("adjMat.txt", "rt") as fd:
            # adj_mat_data = fd.read()
        # parsed_adjacency_results = self._adjacency_matrix_parser.parseString(adj_mat_data)
        # identified_motifs = {}
        # for an_item in parsed_adjacency_results:
            # identified_motifs[an_item["graphID"]] = an_item["G"]
        
class PyMotifCounterNetMODE(PyMotifCounterProcessBase):
    def __init__(self):
        # Build the base model
        super().__init__(binary_location="../binaries/NetMODE/NetMODE")
        # Exchange the result transformer
        self._result_transformer = PyMotifCounterResultNetMODE()
        # Add the right parameters        
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
        
    def _after_run(self, ctx, a_graph):
        """
        Performs any cleanup after the process has run and produced results.
        
        Notes:
            * NetMODE creates an adjacency matrix file in the CWD with all 
              the adjacency matrices of the motifs it enumerated. This is 
              not strictly needed because the adjacency matrix can be inferred 
              by the motif's ID.
        """
        if os.path.exists("adjMat.txt"):
            os.remove("adjMat.txt")
        return ctx

if __name__ == "__main__":
    # v1 = Parameter(name="s", long_name="specify", help_str="Specify length", validation_expr=re.compile("[0-9]+"), is_required=False, param_value=23)
    q = PyMotifCounterNetMODE()
    # q = PyMotifCounterProcessCommon()
    g = networkx.watts_strogatz_graph(64,4,0.8)
    z = q(g)
    
    
    
