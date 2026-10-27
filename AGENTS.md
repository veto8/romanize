# AGENTS.md — romanize

## What this is
A Python (Poetry) CLI that gives the true pronunciation of text in any language: IPA from kaikki/Wiktionary lexicons (`lexicons/<lang>.tsv`), with royin romanization fallback for Thai and pass-through for other languages.

## Stack
- Python >= 3.10, Poetry
- `pythainlp` (runtime dep: `word_tokenize` for Thai segmentation, `romanize` for the Thai royin fallback)

## Run
```bash
poetry install
poetry run romanize "สวัสดี"            # -> sa˨˩.wat̚˨˩.diː˧  (IPA from lexicons/th.tsv)
poetry run romanize "สวัสดีครับ"
poetry run romanize --lang fr "bonjour monsieur"
poetry run romanize --lexicon path.tsv "..."   # override the lexicon file
poetry run romanize --engine thai2rom_onnx ... # change the Thai fallback engine
```

Language behavior:
- `--lang <code>` picks `lexicons/<code>.tsv` and the tokenizer.
- Word splitting: whitespace by default; Thai (`th`) uses pythainlp `word_tokenize` (registry `TOKENIZERS` in `cli.py` — add entries for other no-space scripts).
- Lookup-first: lexicon IPA wins; Thai OOV → royin fallback; other languages OOV → pass through.
- Missing lexicon → warn to stderr and pass through.

Lexicon:
- Dumps live in `dumps/`, lexicons in `lexicons/<code>.tsv`.
- Thai: `poetry run romanize-lexicon dumps/kaikki.org-dictionary-Thai.jsonl -o lexicons/th.tsv`
- Any language: download its dump from `kaikki.org/dictionary/<Language>/` into `dumps/`, build to `lexicons/<code>.tsv`; `./ask.sh` task 6 browses the kaikki list interactively, task 7 batch-adds a fixed common list (English, French, German, Japanese, Chinese, Korean, Spanish, Russian, Portuguese, Italian), task 8 refreshes the Thai dump.
- `ask.sh` menu tasks 1-12 cover install/run/build/test/venv/update/status/cleanup; `dumps/` and `lexicons/` are gitignored.

## Structure
- `romanize/cli.py` — CLI entry (`romanize.cli:main`, console script `romanize`); loads `lexicons/<lang>.tsv` (word→IPA), tokenizes via pythainlp (th) / whitespace, looks up each token, royin-fallbacks unknown Thai words
- `romanize/lexicon.py` — build-time tool (`romanize-lexicon` console script): `word\tIPA` TSV from a kaikki.org Wiktionary dump (NDJSON or JSON list)
- `romanize/__init__.py` — package docstring
- `dumps/` — downloaded kaikki JSONL dumps (gitignored)
- `lexicons/` — per-language word→IPA TSVs (gitignored)
- `pyproject.toml` — Poetry config; `[project.optional-dependencies]` map ML engines to importable modules
- `romanize.svg` / `README.md` — logo + docs
- LICENSE — GPLv3 (mirrors github.com/myridia/romanize)

## Conventions
- No comments in code unless asked.
- Verify: `python -m py_compile romanize/cli.py`.
- Lookup-first: lexicon (true IPA) wins; pythainlp `romanize` is only the fallback for out-of-lexicon tokens. Missing lexicon file → warn to stderr and fall back to royin.
- Commits are done by the user only.