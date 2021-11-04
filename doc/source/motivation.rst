==========
Motivation
==========

This package was born out of necessity to obtain motif counts of networks that were
generated from a variety of sources, most commonly as `networkx` objects.

The motivation to create this project was twofold:

1. Over the years, I frequently found myself having to use one or more of these programs 
   from within Python over large graph data sets and had to deal with all their special 
   points separately. This includes the round-trip of having to:
      1. Convert a given network to the format that is suitable for a given motif count algorithm
      2. Raise the process and feed it parameters and the network at its input
      3. Collect the output
      4. Parse the output in a computable form (a step usually referred to as "Marshalling").
   
2. Some of these programs represent really excellent work from the point of view of 
   establishing and analysing the counting algorithms. Unfortunately, as the time 
   goes by and code remains unmaintained it also becomes difficult to use effectively, 
   for someone who sets off from zero knowledge.
   
The broad aim of this piece of work is to offer Python *bindings* to the underlying 
data structures and code for each one of these algorithms.

The objective at this stage of development is to provide an interface at process level 
that abstracts away each algorithm's input, output and parameters.

All that the user interacts with is a top level Python object that returns the motif 
distribution in a way that makes it easy to use these results further within a Python 
based data analysis ecosystem.
