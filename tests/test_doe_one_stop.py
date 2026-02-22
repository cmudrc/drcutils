from __future__ import annotations

from drcutils.doe import generate_doe


def test_generate_doe_has_expected_keys() -> None:
    result = generate_doe(
        kind="full",
        factors={"a": [0, 1], "b": [2, 3]},
        seed=1,
        randomize=True,
    )

    assert set(result.keys()) == {"design", "summary", "interpretation", "warnings"}
    assert result["summary"]["n_runs"] == 4
