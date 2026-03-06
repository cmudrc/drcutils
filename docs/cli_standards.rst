CLI Standards
=============

Purpose
-------

The command-line interfaces in ``drcutils`` are expected to remain stable,
self-documenting, and script-friendly. This page defines the minimum contract
for every CLI entrypoint.

Parser Contract
---------------

- Each CLI module must expose a ``_build_parser()`` helper.
- Parsers must set a concrete ``prog`` value that matches the installed command.
- Every parser and subparser must provide a ``description``.
- Every user-facing argument must include a non-empty ``help`` string.
- CLI errors should produce a concise stderr message and a non-zero exit code.

Output Contract
---------------

- Commands whose primary output is stdout should print structured dictionary
  results as JSON.
- File-writing commands must create parent directories when needed.
- Successful commands return ``0``.
- Input/validation/runtime failures return ``2``.

Command Catalog
---------------

- ``drc-doe``: DOE table generation for full, LHS, and fractional two-level designs.
- ``drc-doe-analyze``: main-effect summaries and optional screening model outputs.

Contributor Workflow
--------------------

Run the quality gates before opening a PR:

.. code-block:: bash

   make qa
   make docs-build

``tests/test_cli_standards.py`` enforces parser/help/documentation requirements to
prevent command drift.
