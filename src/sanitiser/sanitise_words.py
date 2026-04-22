import logging
from collections import ChainMap
from collections.abc import Generator
from itertools import chain
from pathlib import Path

from yaml import safe_load

THIS_DIR = Path(__file__).parent

logger = logging.getLogger(__name__)


def get_config_dirs(config_paths: list[Path] | None = None) -> list[Path]:
    """Return config directories which exist."""
    DEFAULT_CONFIG_PATHS = [
        THIS_DIR / "maps",
        Path.home() / ".local/share/sanitiser/maps",
        Path.cwd() / "maps",
    ]
    if config_paths is None:
        config_paths = []

    for path in DEFAULT_CONFIG_PATHS:
        if path not in config_paths:
            config_paths.append(path)

    return list(filter(lambda f: f.exists() and f.is_dir(), config_paths))


def get_word_maps(custom_config_paths: list[Path] | None = None) -> ChainMap[str, str]:
    """Extract all word maps from all configuration locations."""
    config_paths = get_config_dirs(custom_config_paths)

    all_maps: ChainMap[str, str] = ChainMap()

    for path in config_paths:
        if not path.exists():
            continue
        maps = word_map_from_dir(path)
        if maps:
            all_maps = all_maps.new_child(maps)
    return all_maps


def get_config_files(custom_config_paths: list[Path] | None = None) -> list[Path]:
    """Get yaml files contained in a list of directories"""
    config_dirs = get_config_dirs(custom_config_paths)
    yaml_files = (chain(d.glob("*.yaml"), d.glob("*.yml")) for d in config_dirs)
    return list(chain.from_iterable(yaml_files))


def word_map_from_dir(root: Path | None = None) -> ChainMap[str, str]:
    """Extract all word maps from a directory of yaml files."""
    if root is None:
        root = THIS_DIR / "maps"
    word_maps: ChainMap[str, str] = ChainMap({})
    if not root.is_dir():
        msg = "Expected directory:"
        logger.error(msg)
        return word_maps
    for file in chain(root.glob("*.yml"), root.glob("*.yaml")):
        word_map = word_map_from_file(file)
        if word_map:
            word_maps = word_maps.new_child(word_map)
    return word_maps


def word_map_from_file(filename: Path) -> dict[str, str]:
    """Extract word maps from yaml file."""
    with open(filename) as f:
        contents = safe_load(f)
    if not isinstance(contents, dict):
        return {}
    return dict(flatten_to_strings(contents))


def flatten_to_strings(d: dict | list) -> Generator[tuple[str, str]]:
    """
    Take a nested dict of dicts-and-lists and return deepest string values.
    """
    if isinstance(d, list):
        d = {"": d}
    for k, v in d.items():
        if isinstance(v, str):
            yield (k, v)
        if isinstance(v, list):
            for item in filter(lambda x: isinstance(x, dict), v):
                yield from flatten_to_strings(item)
        if isinstance(v, dict):
            yield from flatten_to_strings(v)


if __name__ == "__main__":
    print(dict(word_map_from_dir()))
