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

   pip install -e ".[seaborn]"
   pip install -e ".[plotly]"
   pip install -e ".[visualization]"

``seaborn`` adds the Seaborn theme bridge for the shared plotting helpers.
``plotly`` adds optional interactive visualization support.
``visualization`` installs both optional plotting extras together.

Version Note
------------

The package requires Python 3.12+ and is primarily maintained for internal lab
workflows where dependency consistency across sibling repositories is important.
