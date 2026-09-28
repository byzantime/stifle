# Agent notes

## Comments and docstrings

Python code in this repo is gated by stifle itself, using its default
deletion categories:

- no own-line comments, trailing comments or orphan strings (bare string
  expressions that are not docstrings);
- the built-in pragma keeps are allowed (`# noqa`, `# type:`,
  `# pragma:`, …);
- docstrings are at most 7 content lines (`max-doc-lines` in
  `[tool.stifle]` in `pyproject.toml`).

Test samples that deliberately contain comments live inside string literals,
so they are not affected.

The gate runs the working-tree stifle (`uv run stifle`), so a change to
stifle itself also changes the gate that checks it.

## Local commands

```console
uv run stifle check src tests    # the gate
uv run stifle format src tests   # strip violations, then hand-shorten any
                                 # docstring still flagged
uv run pytest
uv run ruff check .
```
