# Packaged binaries

`PyMotifCounter` auto-discovers binaries from the following packages (provided that they can be reached via your `PATH`
environment variable):

* `mfinder`
* `fanmod-cmd`
* `NetMODE`

If you have one or more of those binaries setup already, the `PyMotifCounter` module will automatically discover each 
one at runtime when it is required.

# What if I don't have any of those installed?
`PyMotifCounter` can help with obtaining, compiling and even packaging these binaries for you. Please note however 
that the following steps would have to be executed **BEFORE** installing the python package itself.

This directory contains three (mostly empty) sub-directories (`mfinder`, `NetMODE`, `fanmod-cmd`), one for each binary.
When you first obtain the package, each sub-directory contains two files:

1. A bash script prefixed with `fetch_`
2. A `readme.md` file with detailed information about obtaining and compiling each binary.

For **all** of the binaries included here, the process is exactly the same and is demonstrated here using `mfinder` *as 
an example*:

1. `> cd mfinder`
2. `> ./fetch_mfinder.sh`
3. `> cd mfinder1.21` (Version 1.21 at the time of writing)
4. `> make all`

At the end of this process, a binary will have been created in the default location expected by `PyMotifCounter`. 

The default locations for each binary that the `PyMotifCounter` `setup.py` expects at installation are described in the 
`binaries/binaries_to_install.json` (one array entry for each binary target).

Therefore, to make sure that `PyMotifCounter` **includes** one or more of these binaries with its installation, then
follow this process:

1. Checkout `PyMotifCounter` from [this repository](https://github.com/aanastasiou/pymotifcounter)
2. **First** fetch and compile each binary as outlined above
3. **Then** navigate to the base directory (that contains the `setup.py`) and run `> pip install ./`

# Notes
If you are adding a new binary to `pymotifcounter`, add its path relative to the `binaries/` directory and it will 
be included in the list of executables to get installed in the local interpreter's `bin/` directory as part of the 
installation process.