===============
Developer notes
===============

Work In Progress


Overview
========

.. mermaid::
    :caption: High level class overview

    graph LR
        A("Input <br/> (A Networkx Graph)")
        B("External Process <br/> (An executable)")
        C("Parameters <br/> (Motif size, sampling method, ...)")
        D("Output <br/> (Motif enumeration as DataFrame)")

        A --> B
        C --> B
        B --> D

Typical process flowchart
=========================

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


.. mermaid::
    :caption: A high level view of the project's design.

    classDiagram
        class PyMotifCounterParameter
        
        class PyMotifCounterOutputTransformerBase
        
        class PyMotifCounterInputTransformerBase
        
        
        class PyMotifCounterProcessBase
        PyMotifCounterProcessBase : -str _binary_location
        
        PyMotifCounterProcessBase o-- PyMotifCounterInputTransformerBase:_input_transformer
        PyMotifCounterProcessBase o-- PyMotifCounterOutputTransformerBase:_output_transformer
        PyMotifCounterProcessBase *-- "0..*" PyMotifCounterParameter:_parameters
        
        

Parameters
==========

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

3. ``PGD``
    * Websites:
        * `One <https://github.com/nkahmed/PGD>`_
        * `Two <http://nesreenahmed.com/graphlets/>`_
        * `Three <http://graphlets.org/>`_

