# Development notes

Notes about linting, formatting etc.

## Coverage

Run tests and create branch coverage report:

```shell
coverage run --branch -m pytest; coverage html; coverage report -m
```

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
