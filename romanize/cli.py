#!/usr/bin/env python3
"""Romanize Thai text."""

import sys
from argparse import ArgumentParser

from pythainlp.transliterate import romanize, transliterate

CORE_ENGINES = ("royin",)
ML_ENGINES = ("thai2rom", "thai2rom_onnx", "tltk")
DEFAULT_TEXT = "สวัสดี"


def _available(engine: str) -> bool:
    try:
        from importlib import import_module

        module = {
            "thai2rom": "torch",
            "thai2rom_onnx": "onnxruntime",
            "tltk": "tltk",
        }[engine]
        import_module(module)
        return True
    except ImportError:
        return False


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(prog="romanize", description="Romanize Thai text.")
    parser.add_argument("text", nargs="?", default=DEFAULT_TEXT)
    parser.add_argument(
        "engines", nargs="*", choices=CORE_ENGINES + ML_ENGINES
    )
    parser.add_argument("--iso", action="store_true", help="also print ISO 11940 transliteration")
    args = parser.parse_args(argv)

    engines = args.engines or list(CORE_ENGINES)
    multiple = len(engines) > 1

    for e in engines:
        if e in ML_ENGINES and not _available(e):
            print(f"skipped {e}: not installed", file=sys.stderr)
            continue
        try:
            result = romanize(args.text, engine=e)
            print(f"{e}: {result}" if multiple else result)
        except Exception as exc:
            print(f"{e}: ERROR {exc}", file=sys.stderr)

    if args.iso:
        try:
            print(transliterate(args.text, engine="iso_11940"))
        except Exception as exc:
            print(f"iso_11940: ERROR {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())