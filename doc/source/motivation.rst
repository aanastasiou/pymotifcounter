=======================
Why ``PyMotifCounter``?
=======================

This package was born out of a necessity to obtain motif counts of networks that were
generated from a variety of sources and were generally available as ``networkx`` objects.

The motivation to create it was twofold:

1. To provide an interface to key motif counting algorithms, to the extent that would
   allow a user to simply call the binary with a ``networkx`` object and receive a
   **computable** version of the motif distribution.

2. To preserve the code of these counters



The interface aspect
====================

Suppose that you have a set of networks whose node id's are arbitrary **strings** (or country names, or EEG
electrode names, or state names or more generally *anything other than an integer id*) and you wanted to see what motifs
it is composed of. Suppose also that you wanted to perform this enumeration using ``mfinder`` [#]_.

If you are working with Python you are probably using `networkx <https://networkx.org/>`_ to work with disparate
graphs an expect that you could get the motif distribution in **computable** form be able to use it further in other
calculations.

To obtain a single motif distribution using (for example) ``mfinder``, you have to go through the following steps:

1. If you don't have ``mfinder``, you need to obtain it, compile it and install it to your system.
2. Provided that you dealt with step #1:
    1. The ``mfinder`` binary is called as ``> mfinder network.el -s 3 -r 1000`` where:
          * ``network.el`` is *a file* containing the *edge list* representation of your network
            *in a particular format* expected by ``mfinder``
                * ``mfinder`` expects the edge list file to be listing one edge in each line with the format:
                  ``Source Node ID, Target Node ID, Weight``, where the node IDs **must be numeric** and ``Weight``,
                  as it is not used, should have the value of ``1``.
          * ``-s 3`` is the motif size to enumerated; and
          * ``-r 1000`` is the number of random networks to generate for statistical testing purposes
    2. At the end of step 2.1, you get a **file** with the filename ``[123456]_OUT.txt`` where ``[123456]`` are the
       first 6 characters of the input file (``network.el``), that contains the motif enumeration along with other
       information associated with it that looks like the following.

       .. literalinclude:: resources/mfinder_out.txt

To apply this process to a set of networks, you can now:

1. Handle the analysis *without* Python by:
    * Writing an intermediate script that converts all of your networks to a bunch of files in edge-list format; then
    * Writing a bash script that scans these files and sends them to ``mfinder`` (including the specific enumeration
      parameters); then
    * Writing another script (possibly involving ``sed, awk`` or even a parser in Python) to scan the result files and
      creates something like a CSV file which you would then use for further analysis.

2. Handle the analysis *with* Python by:
    * Using ``networkx`` to convert the network to a file; then
    * Sending this file and the parameters to the ``mfinder`` binary; then
    * Parsing the output of that file to get the enumeration.

The first option leaves a large margin for error as we now have to juggle a number of scripts
(and a directory structure) to perform and analyse the data from each set of computational experiments
we want to run.

The second option is slightly better but it still requires handling the conversion from and to
the intermediate stages and calling the external process.

The code maintenance aspect
===========================

Suppose now that you decided that no road is easier than the other and you now have a working solution.

Years pass, your solution is still working but you now decide to extend the code that produces the binary, or you
want to automate the installation process, or you want to perform any additional steps that augment the original
functionality in any way.

You download the code base and try to compile it but you realise that things have moved on, certain libraries are not
available any more or bugs have been found with the versions that were originally linked to a given motif counter.

Or, as it did happen with one of the binaries packaged along with ``PyMotifCounter``, the original source code is no
more available (i.e. the whole website has vanished)...

Now what?



The ``PyMotifCounter`` module
=============================

Having abstracted ``mfinder``, it was a relatively small step to create models that
abstract the same process across a number of different motif counting algorithms, each one able to produce its own
kind of unique feature for a given network.

The primary objective of ``PyMotifCounter`` at this stage is to provide an interface to external processes that
abstract away each algorithm's input, output and parameters and enable a complete motif enumeration workflow
*using Python end-to-end*.

All that the user interacts with is a top level Python object that accepts a ``networkx`` network and returns the motif
distribution in a ``pandas.DataFrame``, thus making it easier to use these results further within a Python
based network data analysis ecosystem.

.. mermaid::
    :caption: Typical flowchart of ``PyMotifCounter`` operation.

    flowchart TB
        A["Network (networkx)"];
        B["Transform to method (process) dependent representation"];
        C["Check parameter validity"]
        D["Run external process"];
        E["Collect output"]
        F["Transform output to computable form (DataFrame)"];
        G["Return results (DataFrame)"];

        subgraph Python
        A --> B
        subgraph PyMotifCounter
        B --> C
        E --> F
        end
        F --> G
        end

        subgraph System
        C --> D
        D --> E
        end

        style A fill:#ddcbbc
        style G fill:#ddcbbc
        style D fill:#E83B3C, color:#BBBBBB

        style B fill:#2b9c90
        style C fill:#2b9c90
        style E fill:#2b9c90
        style F fill:#2b9c90


Outlook
=======

One limitation of ``PyMotifCounter`` is the use of ``subprocess.popen()`` to call an external process that handles
the actual motif enumeration. Although it is possible to optimise this invocation of an external process at the
operating system level so that it is nearly instantaneous, this method is associated with a longer processing
overhead than actually packaging the C/C++ code that was used to write them, in a proper Python binding.

And this is exactly, the broader aim of ``PyMotifCounter``, to offer true Python bindings to the underlying
data structures and code for each one of these algorithms.

Until then, if you are looking for a convenient way to get computable forms of a network's motif distribution,
have a look at the:

* :ref:`Examples <Detailed Examples>`
* :ref:`Detailed API documentation <api>`
* :ref:`Developer notes <dev notes>`


.. [#] ``mfinder`` is one of the motif enumerators supported by ``PyMotifCounter``.