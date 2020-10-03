from pre_commit_hooks.find_trailing_comma import _find_danger, find_in_file


def test_basic_file(tmpdir):
    p = tmpdir / "test.py"
    with p.open("w", encoding="utf-8") as f:
        f.write("a = 1,")
    assert find_in_file(p)


def test_basic():
    assert _find_danger("a = 1,")


def test_tuple_multi_element():
    assert not _find_danger("a = (1, 2, 3, )")


def test_tuple_in_brackets():
    assert not _find_danger("a = (1, )")


def test_tuple_in_getitem():
    assert _find_danger("h = [[1], [2]][1, ]")


def test_not_ok_in_dict():
    assert not _find_danger("d = {'1': 1, '2': 2}")


def test_not_in_list():
    assert not _find_danger("c = [1, 2, 3, 4, ]")


def test_not_in_tuple():
    assert not _find_danger("a = (1, 2)")


def test_tuple_as_first_tuple_element():
    assert _find_danger("g = (1, ),")
