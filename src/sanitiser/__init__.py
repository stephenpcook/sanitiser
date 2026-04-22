import argparse
import re
import sys
from pathlib import Path
from typing import TextIO

from sanitiser.handle_links import strip_links
from sanitiser.sanitise_words import get_config_dirs, get_config_files, get_word_maps
from sanitiser.version import __version__

__all__ = ["__version__", "main", "sanitise_text"]


def sanitise_text(
    infile: TextIO,
    word_map: dict[str, str],
    *,
    remove_hyperlinks: bool = True,
    no_output: bool = False,
) -> int:
    """Remove sensitive words and links from text and return change count.

    Prints to output to stdout and returns the number of lines changed."""
    patterns = []
    for k, v in word_map.items():
        patterns.append((re.compile(rf"{k}", re.IGNORECASE), v))
    with infile as f:
        lines_changed = 0
        for line in f:
            line_before_subs = line
            if remove_hyperlinks:
                line = strip_links(line)
            for pat, repl in patterns:
                line = re.sub(pat, repl, line)
            if line_before_subs != line:
                lines_changed += 1
            if not no_output:
                print(line, end="")
    return lines_changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--hyperlinks", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="return only the number of lines which would change",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="as for --count, and exit non-zero if changes required",
    )
    parser.add_argument("--word-map-directory", type=Path, action="append")
    parser.add_argument(
        "--show-map-paths",
        action="store_true",
        help="show all word map paths and files and exit",
    )
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )

    args = parser.parse_args()

    word_map_files = get_config_dirs(args.word_map_directory)

    if args.show_map_paths:
        print("Word map paths:")
        print("\n".join(str(p) for p in word_map_files))
        print("Word map files:")
        print("\n".join(str(f) for f in get_config_files(word_map_files)))
        return

    word_map = dict(get_word_maps(word_map_files))
    n_changes = sanitise_text(
        args.infile,
        word_map,
        remove_hyperlinks=not args.hyperlinks,
        no_output=args.count or args.check,
    )
    if args.count or args.check:
        print(n_changes)
    if args.check and n_changes > 0:
        exit(1)
