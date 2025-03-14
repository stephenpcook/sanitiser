import toml

from sanitiser import __version__


def test_version_in_file_matches_toml():
    with open("pyproject.toml") as f:
        version_toml = toml.load(f)["project"]["version"]

    assert version_toml == __version__
