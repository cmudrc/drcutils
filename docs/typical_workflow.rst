Typical Workflow
================

1. Choose utility needs
-----------------------

Identify whether the task is primarily branding, visualization export, file
conversion, or runtime environment handling.

2. Import narrow helpers
------------------------

Import only the modules needed for the task (for example ``drcutils.brand`` or
``drcutils.viz``) to keep scripts explicit and readable.

3. Execute utility steps
------------------------

Run conversions, export figures, or apply branding assets as part of the
calling project workflow.

4. Capture artifacts
--------------------

Write generated files to a stable artifacts directory so downstream analysis
and reporting steps can consume them predictably.

5. Connect to sibling libraries
-------------------------------

Use these outputs in larger pipelines built with
``design-research-experiments`` and ``design-research-analysis``.
