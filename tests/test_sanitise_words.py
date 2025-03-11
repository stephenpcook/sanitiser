from sanitiser.sanitise_words import flatten_to_strings


def test_flatten_to_strings_single_dict():
    d = {"k": "v", "k2": "v2"}

    out = list(flatten_to_strings(d))
    expected_out = [("k", "v"), ("k2", "v2")]

    assert out == expected_out


def test_flattened_dict_of_dict():
    d = {"d": {"k": "v"}}

    out = list(flatten_to_strings(d))
    expected_out = [("k", "v")]

    assert out == expected_out


def test_flattened_dict_of_dict_multiple():
    d = {"d1": {"k": "v"}, "d2": {"k2": "v2"}}

    out = list(flatten_to_strings(d))
    expected_out = [("k", "v"), ("k2", "v2")]

    assert out == expected_out


def test_flattened_list_of_dict():
    d = {"l1": [{"d1": {"k": "v"}}, {"d2": {"k2": "v2"}}]}

    out = list(flatten_to_strings(d))
    expected_out = [("k", "v"), ("k2", "v2")]

    assert out == expected_out
