"""Extract a Thai word -> IPA lexicon from a kaikki.org Wiktionary dump."""

import argparse
import json
import sys


def _entries(path: str):
    with open(path, encoding="utf-8") as f:
        if f.read(1) == "[":
            f.seek(0)
            yield from json.load(f)
            return
        f.seek(0)
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def _ipas(entry: dict):
    for sound in entry.get("sounds") or []:
        ipa = sound.get("ipa")
        if ipa:
            yield ipa.strip().strip("/[]")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="romanize-lexicon", description="Build word\\tIPA TSV from kaikki.org Wiktionary data."
    )
    parser.add_argument("input", help="kaikki.org Thai dump (NDJSON or JSON list)")
    parser.add_argument(
        "-o", "--output", default="lexicon.tsv", help="output TSV (default: lexicon.tsv)"
    )
    args = parser.parse_args(argv)

    words: dict[str, str] = {}
    for entry in _entries(args.input):
        word = entry.get("word")
        if not word or word in words:
            continue
        ipas = list(dict.fromkeys(_ipas(entry)))
        if ipas:
            words[word] = " | ".join(ipas)

    with open(args.output, "w", encoding="utf-8") as f:
        for word in sorted(words):
            f.write(f"{word}\t{words[word]}\n")

    print(f"{len(words)} words -> {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())