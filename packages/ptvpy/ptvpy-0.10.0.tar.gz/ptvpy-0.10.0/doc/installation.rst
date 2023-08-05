.. highlight:: none

.. _installation:

===============
Installation
===============


With pip
========

PtvPy is available_ on the Python Package Index.
To install, simply open a command line prompt where pip_ is available and type::

    pip install ptvpy


.. _available: https://pypi.org/project/ptvpy/
.. _pip: https://pip.pypa.io/en/stable/


With conda
==========

If you haven't yet installed the `Anaconda distribution`_ (or its lightweight version
miniconda_) please do so before continuing.
PtvPy and some of its dependencies are not available in Anaconda's official
repositories.
Therefore we need to append the community managed repository `conda forge`_ to its
search path with the command::

    conda config --append channels conda-forge

Then you can simply install PtvPy with::

    conda install ptvpy

.. _Anaconda distribution: https://www.anaconda.com/download/
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _conda forge: https://conda-forge.org/


Install latest unreleased version
=================================

If you want to install the latest unreleased version of PtvPy you can clone the
files with git::

    git clone https://gitlab.com/tud-mst/ptvpy.git

Then install the package by pointing pip_ at the source files::

    pip install ptvpy/

.. warning::

   This method is only recommended if you want to test the latest unreleased features
   of PtvPy.