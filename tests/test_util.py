from rfcdl.util import clean_string


def test_clean_string():
    assert clean_string("  test ") == "test"
