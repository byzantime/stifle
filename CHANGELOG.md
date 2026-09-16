# Changelog

## 1.0.0 — 2026-09-16

### Renamed

The package has been renamed from **censor** to **stifle** for PyPI
availability. All imports, CLI entry-point names, and `[tool.censor]`
config table keys have changed to `stifle`. See the breaking changes
section below.

### Breaking changes

- **Package rename**: `import censor` → `import stifle`. The PyPI name
  is now `stifle`; `pip install stifle`.
- **CLI entry point**: `censor` → `stifle` (`stifle check ...`,
  `stifle format ...`).
- **Config table**: `[tool.censor]` in `pyproject.toml` must now be
  `[tool.stifle]`; the bare top-level `[stifle]` form is also accepted.
  There is no backward-compatible `[tool.censor]` alias.

### Added

- MIT license file and SPDX `license` field in `pyproject.toml`.
- `CHANGELOG.md` (this file).
- `project.urls` (Repository, Changelog) in `pyproject.toml`.

### Stable

- Version bumped from `0.1.0` to `1.0.0`.
- Classifier changed from *Development Status :: 4 - Beta* to
  *Development Status :: 5 - Production/Stable*.

## 0.1.0 — 2026-08-23 to 2026-08-27

First public beta, developed incrementally across several iterations.

### Added

- **Comment stripper** (`_core.py`): tokenization-based engine that
  deletes whole lines or truncates at a trailing comment's start column.
  Only ever removes comments; never regenerates code.
- **Target categories**: `OWN_LINE`, `TRAILING`, `DOCSTRINGS`,
  `ORPHAN_STRINGS` with repeatable `--delete`/`--skip` flags replacing
  the earlier mode enum.
- **Verification gate**: comment modes compare significant token
  streams; docstring and orphan-string modes compare normalized ASTs.
  Any mismatch leaves the file untouched.
- **Safety preserves**: shebang, PEP 263 coding declarations, and
  tool pragmas (`# noqa`, `# fmt:`, `# type:`, etc.) survive by
  default; `--no-default-keeps` disables.
- **Orphan-string detection**: bare string literals after assignments
  (PEP 224 attribute docstrings, dead prose) are deleted by default.
- **CLI** (`_cli.py`): `check`/`format` (alias `strip`) subcommands
  inspired by ruff/black conventions; `--fix`, `--check`, `--diff`
  flags; recursive `*.py` discovery skipping `.git`/`.venv`/`__pycache__`
  etc.; `ProcessPoolExecutor` parallelism; atomic in-place writes;
  exit codes 0/1/2.
- **Pyproject config**: `[tool.censor]` table with black-style
  discovery (`--config PATH`, `--isolated`); keys: `delete`, `skip`,
  `keep`, `default-keeps`, `exclude`.
- **`--max-doc-lines`**: check-only flag reporting docstrings longer
  than N content lines; counts interior blanks separately; never
  rewrites docstrings.
- **Blank-run normalization**: removing an own-line comment collapses
  blank-line runs to the longest pre-existing run (capped at 2) so
  removing a comment never leaves doubled blanks.
- **Library API**: `strip_source()`, `verify()`, `docstring_violations()`,
  `DocstringViolation` named tuple.
- **Test suite**: unit tests covering all categories, trailing/own-line
  comments, sole-docstring bodies, pragma keeps, CRLF/BOM/non-UTF-8
  files, syntax errors, symlink handling, CLI subcommands and flags,
  and config discovery/validation; stdlib fuzz corpus asserting every
  file verifies and stripping is idempotent.
- **Lint tooling**: black (line-length 80, target py311) and ruff with
  curated rule set (E/F/I/C90 baseline plus RUF006, B023, S110, B904,
  PLW0603, RUF012, B905, RUF100, SIM105).
