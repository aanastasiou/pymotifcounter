.. PyMotifCounter documentation master file, created by
   sphinx-quickstart on Wed Oct 20 13:10:29 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyMotifCounter's documentation!
==========================================

PyMotifCounter brings together a number of fast algorithms that enumerate network motifs.

The motivation to create this project was twofold:

1. Over the years, I frequently found myself having to use one or more of these programs 
   from within Python over large graph data sets and had to deal with all their special 
   points separately.
   
2. Some of these programs represent really excellent work from the point of view of 
   establishing and analysing the counting algorithms. Unfortunately, as the time 
   goes by and code remains unmaintained it also becomes difficult to use effectively.
   
The broad aim of this piece of work is to offer Python *bindings* to the underlying 
data structures and code for each one of these algorithms.

The objective at this stage of development is to provide an interface at process level 
that abstracts away each algorithm's input, output and parameters. 

All that the user interacts with is a top level Python object that returns the motif 
distribution in a way that makes it easy to use these results further within a Python 
based data analysis ecosystem.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   design_notes



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
