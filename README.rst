Proving 3-manifold groups are not left-orderable
================================================

The code in this directory is for proving that certain 3-mainfold
groups are *not* left-orderable. It has two main parts. The first is a
Python package called "quickdisorder" which depends only on "snappy",
though in addition, you will need the Python package for "cython" and
a working C compiler to build the package, since it includes a small C
extension for rapid matrix multiplication.

To install and run the basic tests do the following in this
directory::

  python -m pip install .
  python -m quickdisorder.test

After the second command, you should see something like::

  quickdisorder.double_group: TestResults(failed=0, attempted=5)
  quickdisorder.disorder: TestResults(failed=0, attempted=7)

Typical useage in Python::

  >>> import snappy, quickdisorder
  >>> M = snappy.Manifold('m003(-5, 1)')
  >>> quickdisorder.has_non_orderable_group(M)
  ... prints out proof of non-orderability ...

For further examples, please see the docstrings in the Python source
code, which is located in the subdirectory "src/python".

While the "quickdisorder" code is not rigorous, the subdirectory
"check_proof" contains BLAH
