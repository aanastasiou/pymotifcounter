============
Design Notes
============

Motif counter offers a set of convenient bindings to existing binaries of motif counter
algorithms.

The aim of this project is to offer a low level link to the functionality of each codebase
(i.e. through FFI).

The objective of this version is to bring together a basic set of programs and offer a python
interface at a process level (i.e. through `popen`).

This is achieved by abstracting the inputs and outputs of each process, offering a high 
level interface which accepts a `networkx` graph and returns a motif / graphlet distribution.

The tools
=========

The following tools are included:

1. ``mfinder``
    * `Website <https://www.weizmann.ac.il/mcb/UriAlon/download/network-motif-software>`_
    * To compile ``mfinder`` in 2021, you have to add ``-fcommon`` to ``CFLAGS``.
        * See https://stackoverflow.com/questions/36209788/gcc-multiple-definition-of-error
    
2. ``fanmod``
    * `Website <https://github.com/aanastasiou/fanmod-cmd>`_
    * The original ``fanmod`` was operated *only* via a ``wxwidgets`` Graphical User 
      Interface (GUI). Subsequent work produced ``fanmod_cmd`` and that version 
      was used as the basis for the code that produces the ``fanmod_cmd`` binary
      used in this project.
    
3. ``NetMODE``
    * `Website <https://sourceforge.net/projects/netmode/>`_ 
    * `Paper <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0050093>`_
    
4. ``PGD``
    * Websites:
        * `One <https://github.com/nkahmed/PGD>`_ 
        * `Two <http://nesreenahmed.com/graphlets/>`_ 
        * `Three <http://graphlets.org/>`_


Parameters
----------

.. mermaid::
   :caption: A basic set of parameters required by all algorithms. These listings are driving the modelling at process level.
   
   classDiagram
      class MotifCounter
      MotifCounter : +int motif_size
      
      
      class mfinder 
      mfinder : Path input_file_path
      mfinder : Path output_file_path
      mfinder : int motif_size
      mfinder : bool is_nondirected
      mfinder : int n_random_nets
      
      class fanmod
      fanmod : Path input_file_path
      fanmod : Path output_file_path
      fanmod : bool is_directed
      fanmod : int motif_size
      fanmod : int n_random_nets
      
      class NetMODE
      NetMODE : stdin input_file
      NetMODE : stdout output_file
      NetMODE : int n_random_nets
      NetMODE : int method

      class pgd
      pgd : Path input_file_path
      pgd : stdout output_file
      
      
      
Requirements
^^^^^^^^^^^^

1. Must be possible to pass / define other parameters that a program might be accepting
    * Consider the way ``click`` options work
    
2. 
      

Inputs
======

Broadly speaking all programs expect an edge list format 
where nodes have unique numeric IDs. But, each program allows certain details 
to be passed along with the edgelist, depending on their specific objectives.


1. ``mfinder``
    * Expects an edge list of ``Source\tTarget\tWeight`` 
    * The edge list must be **TAB** delimited
    * The ``Weight`` *is not active* and should default to 1

2. ``fanmod_cmd``
    * Expects an edge list of ``Source Target``
    * Can also accept ....
    
3. ``NetMODE`` 
    * Expects an edge list of ``Source Target`` 
    * Listing has to begin with the number of edges expected present in the file.
    * The edge list must be **TAB** delimited.
   
4. ``PGD`` 
    * Expects an edge list of ``Source Target`` 
    * The edge list must be **COMMA** separated.


Outputs
=======

``mfinder``
-----------

.. literalinclude:: resources/mfinder_out.txt


``fanmod_cmd``
--------------

.. literalinclude:: resources/fanmod_out.txt


``NetMODE``
--------------

NetMODE produces both a file with results as well as a file with the 
adjacency matrices of the motifs it has detected.

.. literalinclude:: resources/netmode_out_1.txt

.. literalinclude:: resources/netmode_out_2.txt


``pgd``
-------

.. literalinclude:: resources/pgd_out.txt



Other Resources
===============

1. ``ORCA`` `website <https://github.com/thocevar/orca>`_
    * Also see `this <https://github.com/qema/orca-py>`_
2. `Hypergraphlets <http://www0.cs.ucl.ac.uk/staff/natasa/group-page.html>`_
