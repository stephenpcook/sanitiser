from sanitiser.handle_links import strip_orgmode_links


def test_strip_link():
    text = "[[http://www.example.org]]"

    stripped_text = strip_orgmode_links(text)
    expected_out = "[[link]]"

    assert stripped_text == expected_out


def test_strip_link_with_description():
    text_with_link = """
    Header:
    [[http://www.example.org]]
    [[http://x.example.org][x]]
    """

    expected_out = """
    Header:
    [[link]]
    [[link]]
    """

    assert strip_orgmode_links(text_with_link) == expected_out


def test_strip_link_two_on_one_line():
    text_with_link = """
    [[http://www.example.org]] [[http://x.example.org][x]]
    """

    expected_out = """
    [[link]] [[link]]
    """

    assert strip_orgmode_links(text_with_link) == expected_out
