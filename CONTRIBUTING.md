# Contributing to hardwarehub

First off, thank you for considering contributing to hardwarehub! 

## Development Setup

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -e ".[dev]"`
4. Install pre-commit hooks: `pre-commit install`

## Pull Request Process

1. Ensure all tests pass: `pytest`
2. Ensure linting and typing pass: `ruff check .`, `ruff format .`, `mypy .` (this is automatically handled by pre-commit hooks).
3. Open a Pull Request!
