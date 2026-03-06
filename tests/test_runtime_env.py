from __future__ import annotations

import drcutils.runtime.env as env


def test_is_google_colab_true_and_false(monkeypatch) -> None:
    monkeypatch.setitem(env._modules, "google.colab", object())
    assert env.is_google_colab() is True

    monkeypatch.delitem(env._modules, "google.colab", raising=False)
    assert env.is_google_colab() is False


def test_is_notebook_colab_short_circuit(monkeypatch) -> None:
    monkeypatch.setattr(env, "is_google_colab", lambda: True)
    monkeypatch.setattr(
        env, "_get_ipython", lambda: (_ for _ in ()).throw(AssertionError("unused"))
    )

    assert env.is_notebook() is True


def test_is_notebook_shell_variants(monkeypatch) -> None:
    monkeypatch.setattr(env, "is_google_colab", lambda: False)

    class ZMQInteractiveShell:
        pass

    class TerminalInteractiveShell:
        pass

    class OtherShell:
        pass

    monkeypatch.setattr(env, "_get_ipython", lambda: ZMQInteractiveShell())
    assert env.is_notebook() is True

    monkeypatch.setattr(env, "_get_ipython", lambda: TerminalInteractiveShell())
    assert env.is_notebook() is False

    monkeypatch.setattr(env, "_get_ipython", lambda: OtherShell())
    assert env.is_notebook() is False


def test_is_notebook_name_error_path(monkeypatch) -> None:
    monkeypatch.setattr(env, "is_google_colab", lambda: False)

    def _raise_name_error() -> None:
        raise NameError("not defined")

    monkeypatch.setattr(env, "_get_ipython", _raise_name_error)
    assert env.is_notebook() is False
