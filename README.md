# Sanitiser

Clear sensitive words from text input.

## Install

```sh
uv tool install sanitiser/
```

## Run

Can be run with a file input:

```sh
uvx sanitiser example.org > clean_example.org
```

or with piped text:

```sh
cat example.org | uvx sanitiser
```

## Configuration

Sensitive words are stored in yaml files.
The program looks for files in the following locations:

- `src/sanitiser/maps`
- `~/.local/share/sanitiser/maps`
- `./maps`

A typical configuration file contains a map:

```yaml
# src/sanitiser/maps/example.yaml
---
example:
- usernames:
    my_username: me
- passwords:
    abc123: xxx
    123abc: XXX
    '@example.com': '@ex.co'
```

With this configuration file, `my_username`, `abc123` and `123abc` would be
replaced by `user`, `xxx` and `XXX` respectively.
