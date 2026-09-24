# AGENTS.md — romanize

## What this is
A Python (Poetry) CLI that romanizes Thai text using pythainlp's transliteration engines, plus ISO 11940.

## Stack
- Python >= 3.10, Poetry
- `pythainlp` (runtime dep; optional ML engines: `torch`, `onnxruntime`, `tltk`)

## Run
```bash
poetry install          # base; -E thai2rom / thai2rom_onnx / tltk for ML engines
poetry run romanize "สวัสดี"
poetry run romanize "สวัสดี" thai2rom_onnx
```

## Structure
- `romanize/cli.py` — CLI entry (`romanize.cli:main`, console script `romanize`)
- `romanize/__init__.py` — package docstring
- `pyproject.toml` — Poetry config; `[project.optional-dependencies]` map ML engines to importable modules
- `romanize.svg` / `README.md` — logo + docs
- LICENSE — GPLv3 (mirrors github.com/myridia/romanize)

## Conventions
- No comments in code unless asked.
- Verify: `python -m py_compile romanize/cli.py`.
- Engines: `CORE_ENGINES = ("royin",)`, `ML_ENGINES = ("thai2rom", "thai2rom_onnx", "tltk")`. ML engines are auto-skipped (with a notice) when their module isn't installed — do not hard-fail.
- Commits are done by the user only.