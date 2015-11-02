.. Reframe documentation master file, created by
   sphinx-quickstart on Fri Oct 30 10:35:07 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Reframe Documentation
=====================

Reframe is a simple relational algebra implementation.  It allows you to experiment with relational
operators in Python.   The relational operators provided in Reframe use an object oriented notation.  That
is  ``relation.operator()``  In keeping with relational algebra all operators return a relation.  This
allows you to chain together operators in a pipeline:  ``relation.operator().operator().operator()``



.. automodule:: reframe
    :members:
    :undoc-members:


Implementation Notes
====================

Reframe is built on top of Pandas DataFrames.  In many cases the relational operators are very thin
layers over regular Pandas operators.  In other cases more convoluted wrappers have been created to
preserve the relation.operator() --> relation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

