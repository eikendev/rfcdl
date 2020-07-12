from rfcdl.util import *


def test_clean_string():
    assert clean_string("  test ") == "test"
