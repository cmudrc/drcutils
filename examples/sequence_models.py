"""Example sequence-model workflow for grammar tokens and text embeddings."""

from __future__ import annotations

import numpy as np

from drcutils.sequence import (
    decode_hmm,
    fit_discrete_hmm,
    fit_markov_chain,
    fit_text_gaussian_hmm,
)


def _toy_text_embedder(texts: list[str]) -> np.ndarray:
    """Encode text into simple deterministic features for demonstration."""
    rows: list[list[float]] = []
    for text in texts:
        tokens = text.lower().split()
        rows.append(
            [
                float(len(tokens)),
                float(sum(len(token) for token in tokens)),
                float("robot" in tokens),
                float("camera" in tokens),
            ]
        )
    return np.asarray(rows, dtype=float)


def main() -> None:
    """Run the token and text sequence-model examples."""
    grammar_sequences = [
        ["S", "NP", "VP", "END"],
        ["S", "NP", "VP", "PP", "END"],
        ["S", "ADV", "VP", "END"],
    ]
    chain = fit_markov_chain(grammar_sequences, smoothing=1.0)
    print("Markov states:", chain.to_dict()["states"])

    try:
        discrete_hmm = fit_discrete_hmm(grammar_sequences, n_states=3, seed=0)
        print("Discrete HMM transition matrix:\n", discrete_hmm.transmat)
    except ImportError as exc:
        print(exc)
        print("Skipping discrete HMM example because optional sequence deps are missing.")

    texts = [
        "robot arm grasps block",
        "robot arm releases block",
        "camera tracks arm motion",
        "camera loses tracking briefly",
    ]
    try:
        gaussian_hmm = fit_text_gaussian_hmm(
            texts,
            n_states=2,
            embedder=_toy_text_embedder,
            seed=0,
        )
        decoded = decode_hmm(gaussian_hmm, _toy_text_embedder(texts))
        print("Gaussian HMM decoded states:", decoded.states.tolist())
    except ImportError as exc:
        print(exc)
        print("Skipping Gaussian HMM example because optional sequence deps are missing.")


if __name__ == "__main__":
    main()
