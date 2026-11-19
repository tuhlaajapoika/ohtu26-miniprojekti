# Development notes

Notes about linting, formatting etc.

## Ruff

[Comparing Ruff and Pylint](https://pydevtools.com/handbook/explanation/how-do-ruff-and-pylint-compare/)

Ruff sorts imports through its linter, not formatter (`ruff format`).

To check and fix everything, including imports sort:

```shell
uv run ruff check --fix .
```

or only sort imports while excluding other checks:

```shell
uv run ruff check --select I --fix .
```

```shell
ruff check --fix .   # auto-fix common issues
ruff format .        # format code
pylint src/          # semantic analysis in CI
```
