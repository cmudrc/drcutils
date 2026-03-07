Dependencies and Extras
=======================

Base Install
------------

.. code-block:: bash

   pip install drcutils

Development Install
-------------------

.. code-block:: bash

   pip install -e ".[dev]"

Optional Extras
---------------

Install optional visualization dependency groups as needed.

.. code-block:: bash

   pip install -e ".[plotly]"

Version Note
------------

The package requires Python 3.12+ and is primarily maintained for internal lab
workflows where dependency consistency across sibling repositories is important.
