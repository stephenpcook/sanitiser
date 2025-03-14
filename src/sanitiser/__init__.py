import argparse
import re
import sys
from pathlib import Path
from typing import TextIO

from sanitiser.handle_links import strip_links
from sanitiser.sanitise_words import get_word_maps
from sanitiser.version import __version__

__all__ = ["__version__", "main", "sanitise_text"]


def sanitise_text(
    infile: TextIO, word_map: dict[str, str], *, remove_hyperlinks: bool = True
) -> None:
    """Remove sensitive words and links from a file."""
    patterns = []
    for k, v in word_map.items():
        patterns.append((re.compile(rf"{k}", re.IGNORECASE), v))
    with infile as f:
        for line in f:
            if remove_hyperlinks:
                line = strip_links(line)
            for pat, repl in patterns:
                line = re.sub(pat, repl, line)
            print(line, end="")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--hyperlinks", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument("--word-map-directory", type=Path, action="append")

    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )

    args = parser.parse_args()

    word_map = dict(get_word_maps())

    sanitise_text(args.infile, word_map, remove_hyperlinks=not args.hyperlinks)
