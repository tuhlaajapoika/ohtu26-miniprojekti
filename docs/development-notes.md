# Development notes

Notes about linting, formatting etc.

## Coverage

Run tests and create branch coverage report:

```shell
coverage run --branch -m pytest; coverage html; coverage report -m
```

or with `pytest-cov`:

```shell
# uses coverage.py
pytest --cov=src --cov-branch --cov-report=html src
# for both html and xml reports, use: --cov-report=html --cov-report=xml
```

### Coverage in VS Code

Install required vscode [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension if not installed. "Testing" icon should be visible in the sidepanel, right click and enable if not. Select "Run Tests with Coverage" and UI should show tests' status and coverage, both in the panel and in opened files.

## Ruff

[Comparing Ruff and Pylint](https://pydevtools.com/handbook/explanation/how-do-ruff-and-pylint-compare/)

Ruff sorts imports through its linter, not formatter (`ruff format`).

To check and fix everything, including imports sort, run:

```shell
uv run ruff check --fix .
# or when venv is active
ruff check --fix
```

To only sort imports and exclude other fixes, run:

```shell
uv run ruff check --select I --fix .
# or when venv is active
ruff check --select I --fix
```

```shell
ruff check --fix .   # auto-fix common issues
ruff format .        # format code
pylint src/          # semantic analysis in CI
```
