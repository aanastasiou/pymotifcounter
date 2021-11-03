"""
A wrapper around binary processes to automate network motif analysis

:author: Athanasios Anastasiou
:date: Nov 2021
"""

from .exceptions import *
import os
import pathlib

def discover_binaries_folder():
    """
    Attempts to auto-discover the binaries folder.
    
    Notes:
        * This function allows for the module to be installed in development mode as well as "standalone".
          The difference there is in the location where the binaries are installed to.
    """
    bins_available_dev = {"mfinder":"mfinder/mfinder1.21/mfinder", \
                          "NetMODE":"NetMODE/NetMODE", \
                          "fanmod":"fanmod-cmd/fanmod_cmd"}
                          
    bins_available_full = {"mfinder":"mfinder", \
                           "NetMODE":"NetMODE", \
                           "fanmod":"fanmod_cmd"}
    bins_folder = "binaries/"
    # The value of module_root depends on where the module is installed in and consequently where the binaries folder
    # would be located.
    module_root = pathlib.Path(os.path.abspath(__file__)).parent
    dev_mode_path = module_root.parent.joinpath(bins_folder)
    full_mode_path = module_root.parent.parent.parent.parent.joinpath(bins_folder)
    binaries_path, bins_available = (full_mode_path, bins_available_full) if full_mode_path.exists() else (dev_mode_path, bins_available_full) if dev_mode_path.exists() else (None, None)
    existing_bins = dict(filter(lambda x:binaries_path.joinpath(x[1]).exists(), bins_available.items())) if binaries_path is not None else None
    return (binaries_path, existing_bins, module_root)
    
    
BINARIES_ROOT_FOLDER, EXISTING_BINS, MOD_ROOT  = discover_binaries_folder()
