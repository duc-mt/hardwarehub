"""
==============================================================================
Module Name:   conftest.py
Description:   Source module conftest.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 conftest.py [options]
Notes:         Requires Python 3.8+
==============================================================================
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
