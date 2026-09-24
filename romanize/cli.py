#!/usr/bin/env python3
"""Romanize Thai text."""

import sys

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
    args = list(argv) if argv is not None else sys.argv[1:]
    text = DEFAULT_TEXT

    if args and not args[0].startswith("-"):
        text = args.pop(0)

    engine = args[0] if args else None
    engines = (engine,) if engine else CORE_ENGINES

    for e in engines:
        if e in ML_ENGINES and not _available(e):
            print(f"romanize({text!r}, engine={e!r}): skipped (not installed)")
            continue
        try:
            print(f"romanize({text!r}, engine={e!r}):", romanize(text, engine=e))
        except Exception as exc:
            print(f"romanize({text!r}, engine={e!r}): ERROR {exc}")

    try:
        print(f"transliterate({text!r}, engine='iso_11940'):", transliterate(text, engine="iso_11940"))
    except Exception as exc:
        print(f"transliterate({text!r}, engine='iso_11940'): ERROR {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())