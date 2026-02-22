"""Bootstrap and nonparametric testing helpers."""

from __future__ import annotations

from typing import Any

import numpy as np

from .templates import render_ci_text, render_np_test_text, render_permutation_text


def _as_array(values: Any, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float).reshape(-1)
    if arr.size == 0:
        raise ValueError(f"{name} must contain at least one value.")
    return arr


def _calc_stat(x: np.ndarray, y: np.ndarray | None, stat: str) -> float:
    if stat == "mean":
        return float(np.mean(x))
    if stat == "median":
        return float(np.median(x))
    if y is None:
        raise ValueError(f"stat '{stat}' requires y values.")
    if stat == "diff_means":
        return float(np.mean(x) - np.mean(y))
    if stat == "diff_medians":
        return float(np.median(x) - np.median(y))
    raise ValueError("stat must be one of: mean, median, diff_means, diff_medians")


def bootstrap_ci(
    x: Any,
    *,
    stat: str = "mean",
    y: Any | None = None,
    n_resamples: int = 10000,
    ci: float = 0.95,
    method: str = "percentile",
    seed: int = 0,
) -> dict[str, Any]:
    """Estimate a bootstrap confidence interval.

    Args:
        x: First sample.
        stat: Statistic name.
        y: Optional second sample for difference stats.
        n_resamples: Number of bootstrap draws.
        ci: Confidence level in ``(0, 1)``.
        method: ``percentile`` or ``bca``.
        seed: Random seed.

    Returns:
        A structured dictionary with estimate, interval, summary stats, and interpretation.
    """
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive.")
    if not (0.0 < ci < 1.0):
        raise ValueError("ci must be in (0, 1).")

    x_arr = _as_array(x, "x")
    y_arr = _as_array(y, "y") if y is not None else None

    if method == "bca":
        try:
            import statsmodels.api  # noqa: F401
            from scipy import stats as sp_stats
        except ImportError as exc:
            raise ImportError(
                "BCa method requires optional stats dependencies. "
                "Install with `pip install drcutils[stats]`."
            ) from exc
        alpha = 1.0 - ci
        if y_arr is None:
            stat_fun: Any
            if stat == "mean":
                stat_fun = np.mean
            elif stat == "median":
                stat_fun = np.median
            else:
                raise ValueError(f"stat '{stat}' requires y values.")
            bres = sp_stats.bootstrap(
                (x_arr,),
                stat_fun,
                confidence_level=ci,
                n_resamples=n_resamples,
                method="BCa",
                random_state=seed,
            )
            ci_low = float(bres.confidence_interval.low)
            ci_high = float(bres.confidence_interval.high)
            estimate = _calc_stat(x_arr, y_arr, stat)
            rng = np.random.default_rng(seed)
            samples = np.empty(n_resamples, dtype=float)
            n_x = x_arr.size
            for idx in range(n_resamples):
                boot_x = x_arr[rng.integers(0, n_x, size=n_x)]
                samples[idx] = _calc_stat(boot_x, None, stat)
        else:
            if stat not in {"diff_means", "diff_medians"}:
                raise ValueError(f"stat '{stat}' is not valid for two-sample BCa.")
            rng = np.random.default_rng(seed)
            samples = np.empty(n_resamples, dtype=float)
            n_x = x_arr.size
            n_y = y_arr.size
            for idx in range(n_resamples):
                boot_x = x_arr[rng.integers(0, n_x, size=n_x)]
                boot_y = y_arr[rng.integers(0, n_y, size=n_y)]
                samples[idx] = _calc_stat(boot_x, boot_y, stat)
            ci_low = float(np.quantile(samples, alpha / 2.0))
            ci_high = float(np.quantile(samples, 1.0 - alpha / 2.0))
            estimate = _calc_stat(x_arr, y_arr, stat)
        distribution_summary = {
            "n": int(samples.size),
            "std": float(np.std(samples, ddof=1)),
            "skew": float(
                ((samples - samples.mean()) ** 3).mean() / (np.std(samples) ** 3 + 1e-12)
            ),
        }
        return {
            "estimate": estimate,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "distribution_summary": distribution_summary,
            "method_used": method,
            "interpretation": render_ci_text(
                estimate=estimate,
                ci_low=ci_low,
                ci_high=ci_high,
                ci=ci,
                stat=stat,
            ),
        }
    if method != "percentile":
        raise ValueError("method must be one of: percentile, bca")

    rng = np.random.default_rng(seed)
    samples = np.empty(n_resamples, dtype=float)
    n_x = x_arr.size
    n_y = y_arr.size if y_arr is not None else 0
    for idx in range(n_resamples):
        boot_x = x_arr[rng.integers(0, n_x, size=n_x)]
        boot_y_opt = y_arr[rng.integers(0, n_y, size=n_y)] if y_arr is not None else None
        samples[idx] = _calc_stat(boot_x, boot_y_opt, stat)

    alpha = 1.0 - ci
    ci_low = float(np.quantile(samples, alpha / 2.0))
    ci_high = float(np.quantile(samples, 1.0 - alpha / 2.0))
    estimate = _calc_stat(x_arr, y_arr, stat)

    distribution_summary = {
        "n": int(samples.size),
        "std": float(np.std(samples, ddof=1)),
        "skew": float(((samples - samples.mean()) ** 3).mean() / (np.std(samples) ** 3 + 1e-12)),
    }

    return {
        "estimate": estimate,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "distribution_summary": distribution_summary,
        "method_used": method,
        "interpretation": render_ci_text(
            estimate=estimate, ci_low=ci_low, ci_high=ci_high, ci=ci, stat=stat
        ),
    }


def permutation_test(
    x: Any,
    y: Any,
    *,
    stat: str = "diff_means",
    n_permutations: int = 20000,
    alternative: str = "two-sided",
    seed: int = 0,
) -> dict[str, Any]:
    """Run a two-sample permutation test.

    Args:
        x: First sample.
        y: Second sample.
        stat: Test statistic.
        n_permutations: Number of label shuffles.
        alternative: ``two-sided``, ``greater``, or ``less``.
        seed: Random seed.

    Returns:
        Structured result containing p-value and interpretation.
    """
    if n_permutations <= 0:
        raise ValueError("n_permutations must be positive.")
    if alternative not in {"two-sided", "greater", "less"}:
        raise ValueError("alternative must be one of: two-sided, greater, less")

    x_arr = _as_array(x, "x")
    y_arr = _as_array(y, "y")
    observed = _calc_stat(x_arr, y_arr, stat)

    rng = np.random.default_rng(seed)
    pooled = np.concatenate([x_arr, y_arr])
    n_x = x_arr.size
    perm_stats = np.empty(n_permutations, dtype=float)

    for idx in range(n_permutations):
        perm = rng.permutation(pooled)
        perm_stats[idx] = _calc_stat(perm[:n_x], perm[n_x:], stat)

    if alternative == "two-sided":
        p_value = float((np.abs(perm_stats) >= abs(observed)).mean())
    elif alternative == "greater":
        p_value = float((perm_stats >= observed).mean())
    else:
        p_value = float((perm_stats <= observed).mean())

    return {
        "p_value": p_value,
        "observed_stat": float(observed),
        "stat": stat,
        "alternative": alternative,
        "interpretation": render_permutation_text(
            p_value=p_value, stat_name=stat, alternative=alternative
        ),
    }


def rank_tests_one_stop(
    x: Any,
    y: Any | None = None,
    groups: Any | None = None,
    *,
    paired: bool | None = None,
    kind: str | None = None,
    alternative: str = "two-sided",
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Dispatch to an appropriate nonparametric rank test.

    Args:
        x: First sample or omnibus sample.
        y: Optional second sample.
        groups: Optional grouped samples for omnibus tests.
        paired: Optional paired/unpaired hint.
        kind: Explicit test kind override.
        alternative: Tail specification for two-sample tests.
        alpha: Reporting threshold.

    Returns:
        Structured test summary with effect size and interpretation.

    Raises:
        ImportError: If SciPy optional dependency is missing.
    """
    try:
        from scipy import stats as sp_stats
    except ImportError as exc:
        raise ImportError(
            "Nonparametric rank tests require scipy. Install with `pip install drcutils[stats]`."
        ) from exc

    x_arr = _as_array(x, "x")
    result: dict[str, Any]
    if kind is None:
        if groups is not None:
            kind = "friedman" if paired else "kruskal"
        elif y is not None:
            kind = "wilcoxon" if paired else "mannwhitney"
        else:
            raise ValueError("Provide y or groups to select a rank test.")

    effect_size: float | None = None
    guidance = [
        "Report exact sample sizes and handling of ties.",
        "Pair p-values with effect size and uncertainty context.",
        "Avoid causal claims from rank tests alone.",
    ]

    if kind == "mannwhitney":
        if y is None:
            raise ValueError("mannwhitney requires y.")
        y_arr = _as_array(y, "y")
        stat_val, p_value = sp_stats.mannwhitneyu(x_arr, y_arr, alternative=alternative)
        n1, n2 = x_arr.size, y_arr.size
        effect_size = 1.0 - 2.0 * float(stat_val) / float(n1 * n2)
        result = {"test": "mannwhitney", "statistic": float(stat_val), "p_value": float(p_value)}
    elif kind == "wilcoxon":
        if y is None:
            raise ValueError("wilcoxon requires y.")
        y_arr = _as_array(y, "y")
        stat_val, p_value = sp_stats.wilcoxon(x_arr, y_arr, alternative=alternative)
        n = x_arr.size
        max_w = n * (n + 1) / 2.0
        effect_size = 1.0 - 2.0 * float(stat_val) / max_w
        result = {"test": "wilcoxon", "statistic": float(stat_val), "p_value": float(p_value)}
    elif kind == "kruskal":
        if groups is None:
            raise ValueError("kruskal requires groups as list-like samples.")
        arrays = [_as_array(g, f"group_{idx}") for idx, g in enumerate(groups)]
        stat_val, p_value = sp_stats.kruskal(*arrays)
        n_total = int(sum(len(g) for g in arrays))
        k = len(arrays)
        effect_size = float((stat_val - k + 1) / (n_total - k)) if n_total > k else 0.0
        result = {"test": "kruskal", "statistic": float(stat_val), "p_value": float(p_value)}
    elif kind == "friedman":
        if groups is None:
            raise ValueError("friedman requires groups as repeated-measures samples.")
        arrays = [_as_array(g, f"group_{idx}") for idx, g in enumerate(groups)]
        stat_val, p_value = sp_stats.friedmanchisquare(*arrays)
        n = len(arrays[0])
        k = len(arrays)
        effect_size = float(stat_val / (n * (k - 1))) if n > 0 and k > 1 else 0.0
        result = {"test": "friedman", "statistic": float(stat_val), "p_value": float(p_value)}
    else:
        raise ValueError("kind must be one of: mannwhitney, wilcoxon, kruskal, friedman")

    result["effect_size"] = effect_size
    result["alpha"] = alpha
    result["interpretation"] = render_np_test_text(
        test_name=result["test"],
        p_value=result["p_value"],
        alpha=alpha,
        effect_size=effect_size,
    )
    result["reporting_guidance"] = guidance
    return result
