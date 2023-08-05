Using miniff
============

As an executable
----------------

Standard workflows in ``miniff`` can be accessed by running::

    python -m miniff jobs.yml

where ``jobs.yml`` lists job parameters. For example::

    fit:
      prepare:
        fn_cells: fit-structures.json
      run:
        n_epochs: 10
        save: potentials.pt

    test-direct:
      prepare:
        fn_cells: test-structures.json
        potentials: potentials.pt

Root arguments specify what kind of workflow to perform: ``fit``, ``test-direct``, and others.
For each workflow, arguments are stored in three section corresponding to ``Workflow.__init__``,
``Workflow.prepare``, and ``Workflow.run``. If either of the section is absent the corresponding
workflow stage will still run with the default arguments. If multiple workflows are specified,
they will be invoked in the order they are present in the job file.

Arguments
"""""""""

The available arguments are specified in documentation of ``miniff.ml_util``.

As a library
------------

``miniff`` is a python library with a plain modular structure. Depending on the needs, it can
be used integrally or by individual pieces.

Workflows
"""""""""

TBD

Dataset construction
""""""""""""""""""""

TBD

Descriptors and potentials
""""""""""""""""""""""""""

TBD
