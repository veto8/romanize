#!/usr/bin/env python3
"""Pronunciation from Wiktionary IPA: true for any language, lexical fallback."""

import os
import re
import sys
from argparse import ArgumentParser

from pythainlp.tokenize import word_tokenize
from pythainlp.transliterate import romanize

THAI_RE = re.compile(r"[\u0E00-\u0E7F]")
TRIM = ' .,!?;:"\'()[]{}\u00AB\u00BB\u201C\u201D\u2018\u2019\u2013\u2014\u2026'
DEFAULT_TEXT = "สวัสดี"
DEFAULT_LANG = "th"
LEXICONS_DIR = "lexicons"


def _thai_tokens(text: str) -> list[str]:
    return [t for t in word_tokenize(text, keep_whitespace=False) if t.strip()]


def _word_tokens(text: str) -> list[str]:
    return [t.strip(TRIM) for t in text.split() if t.strip()]


TOKENIZERS = {"th": _thai_tokens}


def load_lexicon(path: str) -> dict[str, str]:
    words: dict[str, str] = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                word, _, ipa = line.rstrip("\n").partition("\t")
                if word:
                    words[word] = ipa
    except OSError:
        return {}
    return words


def pronounce(text: str, lexicon: dict[str, str], lang: str, engine: str) -> str:
    tokenizer = TOKENIZERS.get(lang, _word_tokens)
    out = []
    for token in tokenizer(text):
        if token in lexicon:
            out.append(lexicon[token])
        elif lang == "th" and THAI_RE.search(token):
            out.append(romanize(token, engine=engine))
        else:
            out.append(token)
    return " ".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(
        prog="romanize",
        description="True pronunciation (IPA) from Wiktionary lexicons, in any language.",
    )
    parser.add_argument("text", nargs="?", default=DEFAULT_TEXT)
    parser.add_argument("--lang", default=DEFAULT_LANG, help="language code (default: th)")
    parser.add_argument(
        "--lexicon", default="", help="lexicon TSV (default: <lexicons>/<lang>.tsv)"
    )
    parser.add_argument(
        "--engine", default="royin", help="Thai fallback romanization engine (default: royin)"
    )
    args = parser.parse_args(argv)

    path = args.lexicon or os.path.join(LEXICONS_DIR, f"{args.lang}.tsv")
    lexicon = load_lexicon(path)
    if not lexicon:
        print(f"warning: no lexicon at {path}, passing unknown words through", file=sys.stderr)

    print(pronounce(args.text, lexicon, args.lang, args.engine))
    return 0


if __name__ == "__main__":
    sys.exit(main())