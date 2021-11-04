"""

    Implements the mfinder concrete counter.

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


class PyMotifCounterResultmfinder(PyMotifCounterResultBase):
    def __init__(self):
        self._res = None
        
    def __call__(self, a_ctx):
        return a_ctx["proc_response"]
        
class PyMotifCounterNetworkmfinderRep(PyMotifCounterNetworkRepBase):
    def __call__(self, a_graph):
        # Obtain network representation
        # First of all, encode the node ID to a number.
        nodeid_to_num = dict(zip(a_graph.nodes(), range(1, a_graph.number_of_nodes()+1)))
        num_to_noded = {value:key for key, value in nodeid_to_num.items()}
        # Create the edge list
        return "".join(map(lambda x:f"{nodeid_to_num[x[0]]}\t{nodeid_to_num[x[1]]}\t1\n", networkx.to_edgelist(a_graph)))


class PyMotifCountermfinder(PyMotifCounterProcessBase):
    def __init__(self, binary_location = None):
        # Build the base model
        # TODO: HIGH, if the binary_location is None, this should raise an exception when an attempt is made to run.
        # TODO: HIGH, this can be abstracted further to a function that performs autodiscovery of the binary's location
        # TODO: HIGH, the validation can be a function
        # TODO: MID, add the output file name and use it when it is specified
        super().__init__(binary_location=binary_location or "mfinder")
        # Exchange the input transformer
        self._input_transformer = PyMotifCounterNetworkmfinderRep()
        # Exchange the result transformer
        self._output_transformer = PyMotifCounterResultmfinder()
        # Add the right parameters        
        self.add_parameter(Parameter(name="s", \
                                     alias="motif_size", \
                                     help_str="Motif size to search", \
                                     validation_expr=re.compile("[3-4]")))
        self.add_parameter(Parameter(name="r", \
                                     alias="n_random", \
                                     help_str="Number of random networks to generate", \
                                     validation_expr=re.compile("[0-9]+")))
        self.set_parameter_value("s", 3)
        self.set_parameter_value("r", 0)
                                     
    def _run(self, ctx):
        # Group parameters
        # TODO: HIGH, this step can be abstracted
        all_param_values = set(self._parameters.values())
        p_params = []
        for a_param_value in all_param_values:
            p_params.extend(a_param_value())
            
        # TODO: LOW, it is probably easy to make mfinder work with stdin/stdout as a binary
        # TODO: HIGH, this needs exception handling
        # mfinder works off of a file, so first save the input representation down to a file in temporary storage
        tmp_fileno, tmp_filename = tempfile.mkstemp()
        ctx["temporary_filename"] = tmp_filename
        with os.fdopen(tmp_fileno, "wt") as fd:
            fd.write(ctx["transformed_graph"])
        p_params = [tmp_filename] + p_params
        # Create the process object
        # TODO: HIGH, this needs exception handling for timeout
        p = subprocess.Popen([self._binary_location] + p_params, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Call the process
        out, err = p.communicate(timeout=320)
        # mfinder will write a file in the same directory
        split_tmp_filename = os.path.split(tmp_filename)
        split_tmp_filename_ext = os.path.splitext(split_tmp_filename[1])
        split_tmp_out_filename = f"{split_tmp_filename[0]}/{split_tmp_filename_ext[0][:7]}_OUT.txt"
        with open(split_tmp_out_filename, "rt") as fd:
            out = fd.read()
        
        ret_ctx = {}
        ret_ctx.update(ctx)
        ret_ctx.update({"proc_response":out, \
                        "proc_error":err, \
                        "mfinder_output_file":split_tmp_out_filename})        
        return ret_ctx
        
    def _after_run(self, ctx):
        """
        Performs any cleanup after the process has run and produced results.
        
        Notes:
            * NetMODE creates an adjacency matrix file in the CWD with all 
              the adjacency matrices of the motifs it enumerated. This is 
              not strictly needed because the adjacency matrix can be inferred 
              by the motif's ID.
        """
        if os.path.exists(ctx["temporary_filename"]):
            os.remove(ctx["temporary_filename"])
            
        if os.path.exists(ctx["mfinder_output_file"]):
            os.remove(ctx["mfinder_output_file"])
        
        return ctx

