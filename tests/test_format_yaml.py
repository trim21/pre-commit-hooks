import pytest

from pre_commit_hooks.yamlfmt import format_file

_INDENT = 2
_WIDTH = 88


@pytest.fixture()
def format_yaml(tmpdir):
    def format_f(content):
        p = tmpdir / "test.yaml"
        with open(p, "w+", encoding="utf-8") as f:
            f.write(content)
        format_file(p, True, _INDENT, _WIDTH)
        with open(p, encoding="utf-8") as f:
            return f.read()

    return format_f


def test_object_space(format_yaml):
    assert "a: 1\n" == format_yaml("a:  1")


def test_list_indent(format_yaml):
    assert """
a:
  - a
  - b
  - c
""".lstrip() == format_yaml(
        """
a:
- a
- b
- c
""",
    )


def test_comment_space_after_hash_1(format_yaml):
    assert "a: 1  # 233\n" == format_yaml("a: 1 #  233")


def test_comment_space_after_hash_2(format_yaml):
    assert "a: 1  # 233\n" == format_yaml("a: 1 #233")


def test_comment_space_before_hash(format_yaml):
    assert "a: 1  # 233\n" == format_yaml("a: 1     # 233")


def test_remove_empty_comment(format_yaml):
    assert "a: 1\n" == format_yaml("a: 1 #")
