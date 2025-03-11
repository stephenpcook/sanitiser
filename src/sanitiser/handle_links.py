import re


def strip_links(text: str) -> str:
    """Replace links in text.

    >>> strip_links("[[https://www.example.org][example]] http://x.org")
    '[[link]] link'
    """
    text = strip_orgmode_links(text)
    return strip_raw_links(text)


def strip_raw_links(text: str) -> str:
    """Replace raw links in text.

    >>> strip_raw_links("https://www.example.org")
    'link'
    """
    return re.sub(r"http(s)?:\/\/\S*", "link", text)


def strip_orgmode_links(text: str) -> str:
    """Replace org-mode links in text.

    >>> strip_orgmode_links("[[https://www.example.org][example]]")
    '[[link]]'
    """
    return re.sub(r"\[\[[^\]]*\](\[[^\]]*\])?\]", "[[link]]", text)
