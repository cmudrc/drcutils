"""Text templates for reporting statistical utilities outputs."""

from __future__ import annotations


def render_ci_text(estimate: float, ci_low: float, ci_high: float, ci: float, stat: str) -> str:
    """Render conservative confidence-interval interpretation text."""
    return (
        f"The bootstrap {stat} estimate is {estimate:.4g}. "
        f"A {ci * 100:.1f}% interval spans [{ci_low:.4g}, {ci_high:.4g}], "
        "which describes uncertainty under the resampling assumptions."
    )


def render_permutation_text(p_value: float, stat_name: str, alternative: str) -> str:
    """Render permutation-test interpretation text."""
    return (
        f"The permutation test for {stat_name} produced p={p_value:.4g} ({alternative}). "
        "Interpret this as evidence against the null random-label model, not as proof of causality."
    )


def render_np_test_text(
    test_name: str, p_value: float, alpha: float, effect_size: float | None
) -> str:
    """Render rank-test interpretation text."""
    decision = "below" if p_value < alpha else "above"
    effect_txt = ""
    if effect_size is not None:
        effect_txt = f" Effect size estimate is {effect_size:.4g}."
    return (
        f"{test_name} returned p={p_value:.4g}, which is {decision} alpha={alpha:.3g}."
        f"{effect_txt} Use this with distribution checks and study context."
    )
