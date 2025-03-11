# Sanitise

Clear sensitive words from text input.

## Install

```sh
uv tool install sanitise/
```

## Run

Can be run with a file input:

```sh
uvx sanitise example.org > clean_example.org
```

or with piped text:

```sh
cat example.org | uvx sanitise
```

## Configuration

Sensitive words are stored in yaml files, by default in `src/sanitiser/maps`.
A typical configuration file contains a map:

```yaml
# src/sanitise/maps/example.yaml
---
example:
- usernames:
    my_username: me
- passwords:
    abc123: xxx
    123abc: XXX
```

With this configuration file, `my_username`, `abc123` and `123abc` would be
replaced by `user`, `xxx` and `XXX` respectively.
