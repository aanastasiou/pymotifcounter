.. _dev notes:

===============
Developer notes
===============

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


.. mermaid::
    :caption: A high level view of the project's design.

    classDiagram
        class PyMotifCounterParameter
        
        class PyMotifCounterOutputTransformerBase
        
        class PyMotifCounterInputTransformerBase
        
        
        class PyMotifCounterBase
        PyMotifCounterBase : -str _binary_location
        
        PyMotifCounterBase o-- PyMotifCounterInputTransformerBase:_input_transformer
        PyMotifCounterBase o-- PyMotifCounterOutputTransformerBase:_output_transformer
        PyMotifCounterBase *-- "0..*" PyMotifCounterParameter:_parameters

        class PyMotifCounterMfinder

        class PyMotifCounterNetMODE

        class PyMotifCounterFanmod

        PyMotifCounterMfinder --|> PyMotifCounterBase
        PyMotifCounterNetMODE --|> PyMotifCounterBase
        PyMotifCounterFanmod --|> PyMotifCounterBase


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


Parameters
==========


``mfinder``
-----------

.. literalinclude:: resources/mfinder_params.txt


``fanmod_cmd``
--------------

.. literalinclude:: resources/fanmod_params.txt


``NetMODE``
-----------

.. literalinclude:: resources/netmode_params.txt


``PGD``
-------

.. literalinclude:: resources/pgd_params.txt


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



Other algorithms
================

1. ``ORCA`` `website <https://github.com/thocevar/orca>`_
    * Also see `this <https://github.com/qema/orca-py>`_
2. `Hypergraphlets <http://www0.cs.ucl.ac.uk/staff/natasa/group-page.html>`_

3. ``PGD``
    * Websites:
        * `One <https://github.com/nkahmed/PGD>`_
        * `Two <http://nesreenahmed.com/graphlets/>`_
        * `Three <http://graphlets.org/>`_

