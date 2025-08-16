# Contributing

Thanks for considering a contribution to **ai-energy-saver**!

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
````

## Tests & Lint

```bash
pytest -q
ruff check .
```

## Adding a Provider

1. Implement the relevant base class in `providers/*/base.py`.
2. Add unit tests (reuse contract tests in `tests/contracts`).
3. Update `README.md` with usage instructions.

## Adding an Adapter

1. Create `adapters/my_adapter.py` with a `load()` function returning a DataFrame.
2. Provide a small synthetic example in `examples/`.

## Code of Conduct

This project follows the Contributor Covenant (see `CODE_OF_CONDUCT.md`).