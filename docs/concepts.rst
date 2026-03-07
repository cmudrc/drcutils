Concepts
========

Shared Utility Layer
--------------------

``drcutils`` centralizes recurring helper functions used across DRC projects so
branding, figure export, and runtime checks are implemented once.

Brand Consistency
-----------------

Brand asset paths, palette constants, and watermark behavior are packaged as
reusable code to keep visual outputs consistent across studies.

Figure Export Conventions
-------------------------

Figure export helpers standardize preset dimensions and output targets so lab
artifacts are easier to compare and reuse in papers, slides, and reports.

Runtime Portability
-------------------

Runtime detection helpers (for example notebook and Colab checks) reduce
environment-specific branching in downstream scripts.

Small, Stable Surface
---------------------

The package favors a compact, practical API aimed at internal workflows rather
than a large public framework.
