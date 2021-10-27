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
from dataclasses import dataclass
import re

class PyMotifCounterException(Exception):
    pass
    
class PyMotifCounterException_InvalidParamValue(PyMotifCounterException):
    pass

@dataclass(repr=False)
class Parameter:
    """
    Represents a parameter that is used to pass data to an external program.
    """
    name: str
    long_name: str
    help_str: str
    validation_expr: re.Pattern
    is_required: bool
    param_value: str = None
    
    def _validate(self):
        """
        Ensures that the parameter conforms to its specification
        """
        if self.validation_expr.match(str(self.param_value)) is None and self.is_required:
            raise PyMotifCounterException_InvalidParamValue(f"Expected {self.validation_expr}, received {self.param_value}")
        else:
            return True
        
    def __call__(self):
        if self._validate():
            return self.__repr__()
            
    def __repr__(self):
        return f"-{self.name} {str(self.param_value)}"
        
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

        

@dataclass(repr=False)
class PyMotifCounterProcessBase:
    """
    Represents an external process.
    """
    parameters: list[Parameter]
    binarylocation: str
    
    def _before_run(self, a_graph):
        """
        Constructs a process context for a particular run.
        """
        # # Obtain network representation
        # # First of all, you have to encode the node ID to a number. NetMODE works only with numeric nodes
        # nodeid_to_num = dict(zip(G.nodes(), range(1, G.number_of_nodes()+1)))
        # num_to_noded = {value:key for key, value in nodeid_to_num.items()}
        # # Create the edge list, translate node ids and convert to string data in one call.
        # netmode_input = f"{G.number_of_nodes()}\n" + "".join(map(lambda x:f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\n", networkx.to_edgelist(G)))
        return None
        
    def _run(self, ctx, a_graph):
        """
        Actually calls the external binary and adds the return value to the context
        """
        # # Create the process object
        # p = subprocess.Popen([f"{self._netmode_binary_dir}NetMODE", "-k", f"{self._knodesize}", "-e", f"{self._edge_random_method}", "-c", f"{self._nrandom}"], universal_newlines=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # # Call the process
        # out, err = p.communicate(input = netmode_input, timeout=320)
        return ctx
        
    def _after_run(self, ctx, a_graph):
        """
        Performs any clean up required and returns the context.
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


class PyMotifNetMODECounter(PyMotifCounterProcessBase):
    """
    Represents a NetMODE call.
    """
    def __init__(self):
        self.parameters.append(Parameter(name="k", help_str="Motif size", validation_exr=re.compile("3|4|5
if __name__ == "__main__":
    v1 = Parameter(name="s", long_name="specify", help_str="Specify length", validation_expr=re.compile("[0-9]+"), is_required=False, param_value=23)
    
    
    
