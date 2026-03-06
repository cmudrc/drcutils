Brand Utilities
===============

Overview
--------

Brand assets and image helpers for DRC identity workflows.

Palette
-------

Canonical brand colors are exposed in ``drcutils.brand.COLORS`` and named
constants:

.. image:: _static/brand/palette_swatches.png
   :alt: DRC color swatches for black, dark teal, teal, blue, orange, and red.
   :width: 100%
   :align: center

.. list-table::
   :header-rows: 1

   * - Name
     - Hex
   * - ``BLACK``
     - ``#000000``
   * - ``DARK_TEAL``
     - ``#1A4C49``
   * - ``TEAL``
     - ``#4D8687``
   * - ``BLUE``
     - ``#57B7BA``
   * - ``ORANGE``
     - ``#EA8534``
   * - ``RED``
     - ``#DF5127``

Logo Samples
------------

.. image:: _static/brand/logo_horizontal_full.png
   :alt: DRC horizontal full-color logo.
   :width: 85%
   :align: center

.. image:: _static/brand/logo_stacked_full.png
   :alt: DRC stacked full-color logo.
   :width: 50%
   :align: center

.. image:: _static/brand/logo_symbol_full.png
   :alt: DRC symbol full-color logo.
   :width: 30%
   :align: center

.. image:: _static/brand/logo_horizontal_on_black_preview.png
   :alt: DRC horizontal on-black-only logo rendered on a dark background.
   :width: 85%
   :align: center

Typography Guidance
-------------------

- Primary family: ``Magdelin`` (headers, all caps).
- Secondary family: ``Zilla Slab`` (body text).
- Use ``get_matplotlib_font_fallbacks()`` for plotting-friendly fallback stacks.

Asset Resolver Examples
-----------------------

.. code-block:: python

   from drcutils.brand import (
       get_circle_graphic_path,
       get_gradient_paths,
       get_logo_path,
       get_pattern_path,
       get_scribble_path,
   )

   symbol_white = get_logo_path("symbol", "white")
   stacked_on_black = get_logo_path("stacked", "full", on_black=True)
   pattern = get_pattern_path("grey")
   gradients = get_gradient_paths()
   circle = get_circle_graphic_path("blue")
   scribble = get_scribble_path("thick", "dark_teal")

Watermark Example
-----------------

.. code-block:: python

   from drcutils.brand import watermark

   watermark(
       "artifacts/figure.png",
       output_filepath="artifacts/figure_watermarked.png",
       logo_layout="stacked",
       logo_variant="auto",
       on_black="auto",
       box=[0.02, 0.02, 0.12, None],
   )

Variant Matrix
--------------

- ``horizontal`` logo variants: ``full``, ``black``, ``dark_teal``, ``red``, ``white``.
- ``stacked`` logo variants: ``full``, ``black``, ``dark_teal``, ``red``, ``white``.
- ``symbol`` logo variants: ``full``, ``black``, ``dark_teal``, ``blue``, ``teal``,
  ``orange``, ``red``, ``white``.
- ``on_black=True`` uses dedicated high-contrast logos for ``horizontal``,
  ``stacked``, and ``symbol`` layouts.

API Reference
-------------

.. automodule:: drcutils.brand
   :members:
