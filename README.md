# Single Bet Placement test suite

## Deliverables

| File | Description |
|---|---|
| [docs/test_plan.md](docs/test_plan.md) | Prioritized test scenarios |
| [docs/bug_reports.md](docs/bug_reports.md) | Execution results & defects |
| `tests/` | Automation framework + tests |
| [docs/strategy.md](docs/strategy.md) | Test strategy & scale-up recommendations |

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation) (dependency & venv manager).
  Poetry can also provide the interpreter: `poetry python install 3.12`
- Desktop Chrome (for UI tests)
- [Allure CLI](https://allurereport.org/docs/install/) — `brew install allure`

## Setup

```bash
poetry install            # creates .venv, installs deps, installs the pre-commit hook
cp .env.example .env
# edit .env and set USER_ID=<your-user-id> (USER_ID env var has higher priority than .env)
```

Run commands inside the environment with `poetry run <cmd>`, or open a shell
with `poetry env activate` (then run `pytest` directly).

## Linting & formatting

[Ruff](https://docs.astral.sh/ruff/) handles linting and formatting, enforced
on commit via a [pre-commit](https://pre-commit.com/) hook).

```bash
make lint     # ruff check + ruff format --check (read-only gate)
make format   # ruff check --fix + ruff format (apply fixes)
poetry run pre-commit run --all-files   # run all hooks against the whole tree
```

## Run tests locally

```bash
make test-local           # all tests → opens Allure report
make test-local mark=api  # API tests only
make test-local mark=ui   # UI tests only
```


## Run tests in Github Actions

1. **Actions** → **"Run tests"** (triggered manually).
2. The Allure report is published to GitHub Pages:
   **https://arcamael.github.io/sporty-tech-task/**.

## Dependency management

Dependencies are declared in `pyproject.toml` and pinned in `poetry.lock`.

```bash
poetry add <pkg>          # add a runtime dependency
poetry add --group test <pkg>   # add a test-only dependency
poetry update             # refresh the lock file within constraints
make lock                 # re-lock and reinstall after editing pyproject.toml
```
