Installation
============

Package Install
---------------

.. code-block:: bash

   pip install drcutils

Editable Install
----------------

.. code-block:: bash

   git clone https://github.com/cmudrc/drcutils.git
   cd drcutils
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -e ".[dev]"

Maintainer Shortcut
-------------------

.. code-block:: bash

   make dev

Notes
-----

``drcutils`` is primarily intended for internal lab use, where shared utility
behavior across repositories matters more than a broad public API surface.
