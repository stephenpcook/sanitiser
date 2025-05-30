import re


def strip_links(text: str) -> str:
    """Replace links in text.

    >>> strip_links("[[https://example.org][example]] <http://example.com> http://example.net")
    'link link link'
    """
    text = strip_orgmode_links(text)
    text = strip_angle_bracket_links(text)
    return strip_raw_links(text)


def strip_raw_links(text: str) -> str:
    """Replace raw links in text.

    >>> strip_raw_links("https://www.example.org")
    'link'
    """
    return re.sub(r"http(s)?:\/\/\S*", "link", text)


def strip_angle_bracket_links(text: str) -> str:
    """Replace angle-bracket links in text.

    >>> strip_angle_bracket_links("<https://www.example.org>")
    'link'
    """
    return re.sub(r"<[^>]*>", "link", text)


def strip_orgmode_links(text: str) -> str:
    """Replace org-mode links in text.

    >>> strip_orgmode_links("[[https://www.example.org][example]]")
    'link'
    """
    return re.sub(r"\[\[[^\]]*\](\[[^\]]*\])?\]", "link", text)
