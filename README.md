<img src="romanize.svg" alt="romanize" width="120">

# romanize

Romanize Thai text — a CLI built on [pythainlp](https://github.com/PyThaiNLP/pythainlp) exposing its transliteration engines (royin, thai2rom, thai2rom_onnx, tltk) and ISO 11940 for easy testing/shell use.

## Install

```bash
poetry install
```

ML engines are optional extras:

```bash
poetry install -E thai2rom       # PyTorch
poetry install -E thai2rom_onnx  # onnxruntime
poetry install -E tltk           # tltk
```

## Usage

```bash
romanize                    # prints "swatdi" (default text, royin)
romanize "<Thai text>"      # prints the royin romanization
romanize "<Thai text>" thai2rom
romanize "<Thai text>" --iso thai2rom_onnx tltk
```

Prints just the romanized text (one line per engine). Add `--iso` for the lossless ISO 11940 transliteration. Uninstalled ML engines are skipped with a stderr notice instead of failing.

## Structure

- `romanize/cli.py` — CLI entry (`romanize.cli:main`)
- `romanize/__init__.py` — package docstring
- `pyproject.toml` — Poetry packaging, optional extras per engine

## Conventions

- No comments in code unless asked.
- Verify: `python -m py_compile romanize/cli.py`.
- Commits are done by the user only.