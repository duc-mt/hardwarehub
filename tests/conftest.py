"""Shared pytest fixtures.

Several tests exercise code that reads/writes database/users.csv and
database/database.csv using hardcoded relative paths. `isolated_project`
copies those files into a temp directory and chdirs into it for the
duration of the test, so nothing here ever mutates the real files under
version control.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def isolated_project(tmp_path, monkeypatch):
    shutil.copytree(PROJECT_ROOT / "database", tmp_path / "database")
    monkeypatch.chdir(tmp_path)
    return tmp_path
