Metrics
=======

Metrics is a Python package for computing various software metrics from the source code. This package can compute:

* **raw** metrics (various LOC, blank lines, different line averages and line percentages, etc.)
* **Halstead** metrics
* **McCabe's** complexity (cyclomatic complexity)
* **Henry-Kafura** Information Flow metrics (module complexity)

Usage
-----

Metrics package can be used from command line or programmatically. Here's a code example of using package API::

   import metrics

   metrics.foo('source_file.c') # returns a value

A command line usage example is shown below::

   $ metrics cc source_file.c
   source_file.c
      F 356:0 func1
      F 1093:0 func2

   Average complexity: F (724.5)

Detailed documantation for how package can be used is at https://metrics.readthedocs.org/.

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Lisence
-------

`MIT <https://choosealicense.com/licenses/mit/>`_

