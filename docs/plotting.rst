Plot Styling
============

Overview
--------

Use ``drcutils.visualization.plotting`` to apply a consistent DRC visual language across
Matplotlib, pandas plotting, optional Seaborn themes, and Plotly templates.

Matplotlib Quick Start
----------------------

.. code-block:: python

   import matplotlib.pyplot as plt

   from drcutils.visualization import use_plot_style

   use_plot_style(context="paper")

   fig, ax = plt.subplots()
   ax.plot([0, 1, 2], [0, 1, 4], label="trend")
   ax.set_xlabel("Time")
   ax.set_ylabel("Score")
   ax.legend()

Style File Usage
----------------

.. code-block:: python

   import matplotlib.pyplot as plt

   from drcutils.visualization import get_plot_style_path

   plt.style.use(get_plot_style_path())

Temporary Context
-----------------

.. code-block:: python

   from drcutils.visualization import plot_style_context

   with plot_style_context(context="talk"):
       ...

Seaborn and pandas
------------------

.. code-block:: python

   import pandas as pd
   import seaborn as sns

   from drcutils.visualization import use_plot_style

   use_plot_style(context="notebook", seaborn=True)

   sns.lineplot(data=pd.DataFrame({"x": [0, 1], "y": [1, 3]}), x="x", y="y")
   pd.DataFrame({"value": [1, 2, 3]}).plot()

Install Seaborn support with ``pip install drcutils[seaborn]`` or
``pip install drcutils[visualization]``.

Plotly Template
---------------

.. code-block:: python

   import plotly.graph_objects as go

   from drcutils.visualization import get_plotly_template

   fig = go.Figure()
   fig.update_layout(template=go.layout.Template(get_plotly_template()))

API Reference
-------------

.. automodule:: drcutils.visualization.plotting
   :members:
