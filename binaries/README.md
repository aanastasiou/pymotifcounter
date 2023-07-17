# Packaged binaries

`PyMotifCounter` includes the following algorithms:

* `mfinder`
    * A couple of minor changes to ``mfinder`` are also applied here. The resulting binary that ``PyMotifCounter`` uses
      is slightly different than the one produced by the original source code.
* `fanmod-cmd`
* `NetMODE`
* `pgd`


# What if I want to recompile or modify the code of those binaries?
`PyMotifCounter` can help with obtaining, compiling and even re-packaging these binaries for you. 

For more information please see https://pymotifcounter.readthedocs.io/en/latest/installation.html

# Notes
If you are adding a new binary to `pymotifcounter`, add its path relative to the `binaries/` directory.
