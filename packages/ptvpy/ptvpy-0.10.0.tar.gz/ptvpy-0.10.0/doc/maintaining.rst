.. highlight:: none

.. _Maintaining:

===========
Maintaining
===========

This guide is aimed at maintainers of PtvPy who have commit access to the repository
on GitLab and describes common maintenance and administration tasks.

.. contents:: Content
   :local:

----


.. _Releasing a new version:

Releasing a new version
=======================

When creating a new release make sure that the release notes in the :ref:`Changelog`
give a good overview over the changes compared to the previous release.
Then update the section headline for the new release as being the "latest", fill in the
current date, commit these changes and push them so that the continuous integration
can check them.

Before continuing check:

- There are no pending tasks in ``TODO.rst`` for this release.
- The HTML documentation builds and renders correctly.
- All commands and their output in the documentation are up to date.
- The test suite passes in with ``pytest --doctest-modules``.
- The distribution archives build correctly with::

    python setup.py sdist bdist_wheel

If everything is in order create a new signed and annotated
tag with ::

    git tag -s "v<release version>"

which marks the actual release.
It is mandatory to sign tags (use the ``-s`` flag).
Tags follow the naming schema "vA.B.C" where A, B and C mark the numbers of the current
`semantic version`_, e.g. the release with the version 1.0.2 should be tagged "v1.0.2".

.. _semantic version: https://semver.org/spec/v2.0.0.html

If you are satisfied push this tag to the upstream repository with::

    git push upstream "v<release version>"

Following this, the continuous integration on GitLab should run the test suite (again),
create the distribution archives and update the online documentation.
After this is done, download the job artifacts containing the distribution archives for
the current release and upload them to the `test instance of PyPI`_ with::

    twine upload --repository-url https://test.pypi.org/legacy/ <path to archive folder>/*

.. _test instance of PyPI: https://packaging.python.org/guides/using-testpypi/

Before continuing check the following points:

- The project page on TestPyPI shows all meta data correctly.
- You can download and install the package into a working environment and the test suite
  passes.

After you have verified that everything works as indented you can upload the
distributions to the real PyPI instance by omitting the ``--repository-url`` flag.
