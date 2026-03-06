Sequence Modeling
=================

Overview
--------

``drcutils.sequence`` provides text-first sequence modeling utilities for:

- order-k Markov chains from discrete tokens,
- discrete-emission HMMs,
- Gaussian HMMs over dense embeddings.

Quick Start
-----------

.. code-block:: python

   from drcutils.sequence import (
       decode_hmm,
       fit_discrete_hmm,
       fit_markov_chain,
       fit_text_gaussian_hmm,
   )

   grammar_sequences = [
       ["S", "NP", "VP", "END"],
       ["S", "NP", "VP", "PP", "END"],
       ["S", "ADV", "VP", "END"],
   ]

   markov = fit_markov_chain(grammar_sequences, order=1, smoothing=1.0)
   discrete = fit_discrete_hmm(grammar_sequences, n_states=3, seed=0)

   texts = [
       "robot arm grasps block",
       "robot arm releases block",
       "camera tracks arm motion",
       "camera loses tracking briefly",
   ]
   gaussian = fit_text_gaussian_hmm(texts, n_states=2, seed=0)
   decoded = decode_hmm(gaussian, gaussian.means)

   print(markov.to_dict()["states"])
   print(discrete.to_dict()["n_states"])
   print(decoded.to_dict()["states"])

Optional Extras
---------------

Install sequence/HMM dependencies:

.. code-block:: bash

   pip install drcutils[seq]

Install text embedding dependencies:

.. code-block:: bash

   pip install drcutils[embeddings]

API Reference
-------------

.. automodule:: drcutils.sequence
   :members:
