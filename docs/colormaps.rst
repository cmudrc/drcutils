Colormaps
=========

Overview
--------

DRC-branded Matplotlib colormaps.

Available Colormaps
-------------------

- ``drc_palette`` and ``drc_palette_r``
- ``drc_diverging`` and ``drc_diverging_r``
- ``drc_dark_diverging`` and ``drc_dark_diverging_r``
- ``drc_cool`` and ``drc_cool_r``
- ``drc_warm`` and ``drc_warm_r``

Quick Start
-----------

.. code-block:: python

   import matplotlib.pyplot as plt
   from drcutils.brand.colormaps import drc_diverging, drc_palette

   plt.imshow([[0, 1], [2, 3]], cmap=drc_diverging)
   plt.figure()
   plt.imshow([[0, 1], [2, 3]], cmap=drc_palette)
   plt.show()

Visual Previews
---------------

``drc_palette``

.. image:: _static/colormaps/drc_palette.png
   :alt: Preview of drc_palette colormap.
   :width: 100%

``drc_palette_r``

.. image:: _static/colormaps/drc_palette_r.png
   :alt: Preview of drc_palette_r colormap.
   :width: 100%

``drc_diverging``

.. image:: _static/colormaps/drc_diverging.png
   :alt: Preview of drc_diverging colormap.
   :width: 100%

``drc_diverging_r``

.. image:: _static/colormaps/drc_diverging_r.png
   :alt: Preview of drc_diverging_r colormap.
   :width: 100%

``drc_dark_diverging``

.. image:: _static/colormaps/drc_dark_diverging.png
   :alt: Preview of drc_dark_diverging colormap.
   :width: 100%

``drc_dark_diverging_r``

.. image:: _static/colormaps/drc_dark_diverging_r.png
   :alt: Preview of drc_dark_diverging_r colormap.
   :width: 100%

``drc_cool``

.. image:: _static/colormaps/drc_cool.png
   :alt: Preview of drc_cool colormap.
   :width: 100%

``drc_cool_r``

.. image:: _static/colormaps/drc_cool_r.png
   :alt: Preview of drc_cool_r colormap.
   :width: 100%

``drc_warm``

.. image:: _static/colormaps/drc_warm.png
   :alt: Preview of drc_warm colormap.
   :width: 100%

``drc_warm_r``

.. image:: _static/colormaps/drc_warm_r.png
   :alt: Preview of drc_warm_r colormap.
   :width: 100%

API Reference
-------------

.. automodule:: drcutils.brand.colormaps
   :members:
