NetworkDisk: On disk graph manipulation
=======================================

NetworkDisk provides a way to manipulate graphs on disk.
The goal is to be as much as possible compatible with (Di)Graph objects of the  `NetworkX <https://networkx.org/>`_ package
but lifting memory requirement and providing persistence of the Graph.

We aim to manage full retro-compatibility with NetworkX core methods to ensure
that most algorithms will work at is.
Some algorithms are not adapted to work with on-disk graph and will thus have poor performances.
Some will be fast enough to be use at is.


Audience
--------

The target audience for NetworkDisk are users of NetworkX that want to manipulate database graphs
without worrying about the database specific technology nor learning a new database related language.
No knowledge on database is required for simple use of this module. A good knowledge of the backend
will be require for advance usage and tuning of the performance.

Pro and cons
------------

There are several motivations to use database graphs rather than in-memory graphs.

1. Lack of resource: The graph is too large to hold in RAM.
2. Persistence requirements and graph sharing: The graph should be saved on disk. You might combine `networkx` and `pickle` modules for that instead, but *NetworkDisk* do save the graph automatically avoiding version conflict and allowing a DB user to directly access the graph DB. Also, loading a graph does not require any parsing nor pre-processing.
3. Transaction support: You don't want graph alteration performed by a failing algorithm to be kept.
4. Concurrency control: You want many user to access the same graph.
5. Symbolic manipulation of subgraphs: You may want to transform the Graph implicitly without actually computing the transformation.

The main drawback of using `NetworkDisk` rather than `NetworkX` is the performance loss. For direct graph manipulation, the expected penalty
is of one order of magnitude (at least ten times slower) and for complex graph algorithms the penalty can be much worse.

Recommended Usage
-----------------

For very large graph, we recommend to use NetworkDisk to extract subgraph small enough to hold in RAM and to manipulate
them as classical NetworkX graph. For this reason, we took a particular attention to allow to extract subgraph efficiently
as well as to export a NetworkDisk graph to NetworkX efficiently.


Designing algorithms for NetworkDisk
------------------------------------

It is possible to adapt standard graph algorithms to be used efficiently on disk. It requires a specific attention
to memory management as well as avoiding as much as possible repeated call to the Backend.

Graph algorithms that requires either to copy or to go through all the graph to build a dedicated DataStructure in RAM
should be avoided. Graph exploration algorithms (shortest path, random walk for instance) should have usable performance.

Schemas
-------

NetworkDisk can be think as a dedicated `ORM <https://fr.wikipedia.org/wiki/Mapping_objet-relationnel>`_ for NetworkX.
That is, a mapping from the structure underlying NetworkX graphs to a relational database. This mapping has to reduces
the cost penalty to perform many disk access.

In the code base of NetworkDisk, we do not enforce one specific schema mapping.
It can be adapted to already existing database. It is however a complicated task to design a schema mapping that
provides a correct implementation Backend.  Therefore, some default fixed schemas are proposed as ready to use.

RoadMap
-------

MultiGraph and MultiDiGraph
^^^^^^^^^^^^^^^^^^^^^^^^^^^

NetworkX implementation provides classes for MultiDiGraph and MultiGraph.
We do not provides them yet. Some specific work has to be done to adapt the current
schema of Graph and DiGraph to those situation.

Other Database Engine
^^^^^^^^^^^^^^^^^^^^^

So far, NetworkDisk only support SQLite local Dabatabase. A `PostgreSQL <https://www.postgresql.org/>`_
version is on the top of the "TODO" list of the project. Other database engine are possible and will
be easily adapted.

At its core, NetworkDisk was built with flexibility of the backend technology in minds. Adapting
from SQLite to other backend requires some routine work. The core difficulties is to provides
adjusted graph mapping that take benefits of the engine specificity.

For instance, PostgreSQL nice support for JSON datatype, could improve a lot performances.

Cache Policy
^^^^^^^^^^^^

A crude Cache policy is provided in NetworkDisk without any control either on the memory consumption
nor on any time limit to discard cached elements.

Abstract cache policy with some reasonable based implementation could be added to improve this states.

Bulk cache warmup could also be of interest to start without an empty cache without having to perform
ridiculous amount of small query. 

NoSQL relational Engines
^^^^^^^^^^^^^^^^^^^^^^^^
Storing graphs in a Graph Database Engine is also a possibility. If the data-model
fits, it could benefits of many graph-dedicated optimization. Other type of DataBase
could help as well (for instance distributed Key-Value stores paired with indexation engines).

A full study system per system is required and will be the subject of further works.

Indexable data fields
^^^^^^^^^^^^^^^^^^^^^

NetworkX doesn't provides any indexation properties nor any data-graph operator.
Some dedicated work even on NetworkX base classes could be performed.

Graph transformation and Regular Path Queries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the key feature of NetworkDisk (compared to standard graph database) is the possibility
to perform graph transformations through query rewriting.
The performance of such a transformation depends of the inner complexity of the rewriting,
the efficiency of the query optimizer, and the possibility of complex indexation approach.

A completely flexible approach to those operations is thus doomed and it should be consider separately
for each backend.



Free software
-------------

NetworkDisk is free software; you can redistribute it and/or modify it under the
terms of the `3-clause BSD License`.  We welcome contributions.
Join us on `GitLab <https://gitlab.inria.fr/guillonb/networkdisk>`_.
