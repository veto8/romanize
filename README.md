<img src="romanize.svg" alt="romanize" width="120">

# romanize

True pronunciation from real Wiktionary lexicons, **in any language** — type a word and get its actual IPA, straight from the [kaikki](https://kaikki.org) dictionary dumps. Unknown words pass through (or fall back to royin romanization for Thai).

```
$ romanize "สวัสดี"
sa˨˩.wat̚˨˩.diː˧
```

## Quick start

```bash
poetry install
poetry run romanize "สวัสดี"
```

## Usage

```bash
romanize                        # default sample, Thai (สวัสดี)
romanize "<Thai text>"          # IPA from the Thai lexicon
romanize --lang fr "bonjour"    # any language with a lexicon in lexicons/<code>.tsv
romanize "<text>" --lexicon /path/lexicon.tsv   # explicit lexicon file
romanize "<Thai text>" --engine thai2rom  # Thai fallback engine (default royin)
```

How it works per word: look it up in the language's `lexicons/<code>.tsv` → print its IPA. Not found → Thai words get royin romanization; all other languages pass the word through unchanged. Word splitting is whitespace-based, except Thai which uses pythainlp's tokenizer. Examples:

```
$ romanize "สวัสดีครับ"
sa˨˩.wat̚˨˩.diː˧ kʰrap̚˦˥

$ romanize --lang fr "bonjour monsieur"
bɔ̃.ʒuʁ mə.sjø
```

## ask.sh

`./ask.sh` is the command hub for the project:

| # | Task |
|---|---|
| 1 | Install - `poetry install` |
| 2 | Run - romanize a text (language + text) |
| 3 | Build Thai lexicon - word→IPA from the Thai kaikki dump |
| 4 | Test - py_compile + run the default sample |
| 5 | Enter venv shell |
| 6 | Add language - pick from the kaikki language list, download + build its lexicon |
| 7 | Add common languages - download + build a fixed list of languages |
| 8 | Update Thai dump - re-download the kaikki Thai dump |
| 9 | Run examples |
| 10 | Status - venv, dumps, lexicons |
| 11 | Clean bytecode |
| 12 | Remove lexicons + dumps (destructive) |
| 0 | Exit |

## The lexicon

`lexicons/<language>.tsv` maps words to IPA (`word \t IPA`), built from the free kaikki/Wiktionary dump for that language. Raw kaikki dumps live in `dumps/` (Thai: `dumps/kaikki.org-dictionary-Thai.jsonl`, ~17.5k words):

```bash
mkdir -p dumps
curl -o dumps/kaikki.org-dictionary-Thai.jsonl https://kaikki.org/dictionary/Thai/kaikki.org-dictionary-Thai.jsonl
poetry run romanize-lexicon dumps/kaikki.org-dictionary-Thai.jsonl -o lexicons/th.tsv
```

Any language works the same — or use `./ask.sh` task `6`, which fetches the full kaikki language list, lets you pick one (by number or name), then downloads + builds `lexicons/<code>.tsv`. Task `7` batch-adds common languages (English, French, German, Japanese, Chinese, Korean, Spanish, Russian, Portuguese, Italian). Dumps and generated TSVs are gitignored.

## Structure

- `romanize/cli.py` — CLI: loads `lexicons/<lang>.tsv`, tokenizes (pythainlp for Thai, whitespace otherwise), looks up + falls back
- `romanize/lexicon.py` — `romanize-lexicon` builder (kaikki dump → TSV, any language)
- `romanize/__init__.py` — package docstring
- `dumps/` — raw kaikki JSONL downloads (gitignored)
- `lexicons/` — per-language word→IPA TSVs (gitignored)
- `ask.sh` — command menu (see above)
- `pyproject.toml` — Poetry packaging
- `romanize.svg` — logo

## Conventions

- No comments in code unless asked.
- Verify: `python -m py_compile romanize/cli.py`.
- Commits are done by the user only.