from __future__ import annotations

import argparse
import importlib
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

CLI_MODULES = {
    "drcutils.cli.data_cli": "drc-data",
    "drcutils.cli.doe_cli": "drc-doe",
    "drcutils.cli.doe_analysis_cli": "drc-doe-analyze",
    "drcutils.cli.power_cli": "drc-power",
    "drcutils.cli.repro_cli": "drc-repro",
    "drcutils.cli.stats_cli": "drc-stats",
}


def _iter_parsers(parser: argparse.ArgumentParser) -> list[argparse.ArgumentParser]:
    parsers = [parser]
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for subparser in action.choices.values():
                parsers.extend(_iter_parsers(subparser))
    return parsers


def _iter_non_help_actions(parser: argparse.ArgumentParser) -> list[argparse.Action]:
    actions: list[argparse.Action] = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for subparser in action.choices.values():
                actions.extend(_iter_non_help_actions(subparser))
            continue
        if action.dest == "help" or action.help == argparse.SUPPRESS:
            continue
        actions.append(action)
    return actions


@pytest.mark.parametrize(("module_name", "command_name"), CLI_MODULES.items())
def test_cli_help_smoke(module_name: str, command_name: str) -> None:
    cmd = [sys.executable, "-m", module_name, "--help"]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(cmd, env=env, check=False, capture_output=True, text=True)

    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
    assert command_name in result.stdout


@pytest.mark.parametrize(("module_name", "command_name"), CLI_MODULES.items())
def test_cli_parser_contract(module_name: str, command_name: str) -> None:
    module = importlib.import_module(module_name)
    parser = module._build_parser()

    assert parser.prog == command_name
    for target_parser in _iter_parsers(parser):
        assert target_parser.description
    for action in _iter_non_help_actions(parser):
        assert action.help


def test_cli_commands_are_documented() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    script_names = sorted(pyproject["project"]["scripts"])
    docs_text = (
        Path("README.md").read_text(encoding="utf-8")
        + "\n"
        + Path("docs/cli_standards.rst").read_text(encoding="utf-8")
    )

    for script_name in script_names:
        assert script_name in docs_text
