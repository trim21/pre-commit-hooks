import difflib
from unittest import mock

import pytest

from pre_commit_hooks.yamlfmt import format_file

_INDENT = 2
_WIDTH = 88


@pytest.fixture()
def format_yaml(tmpdir):
    def format_f(content: str):
        p = tmpdir / "test.yaml"
        with open(p, "wb") as f:
            f.write(content.encode())
        format_file(p, True, _INDENT, _WIDTH)
        with open(p, "rb") as f:
            return f.read().decode()

    return format_f


def assert_string_eq(before, after):
    assert after == before, "".join(
        difflib.unified_diff(
            after.splitlines(True),
            before.splitlines(True),
        ),
    )


def test_object_space(format_yaml):
    assert format_yaml("a:  1") == "a: 1\n"


def test_line_break(format_yaml):
    assert format_yaml("a: 1\nb: 2\n") == "a: 1\nb: 2\n"


def test_line_break_2(format_yaml):
    assert format_yaml("a: 1\r\nb: 2\r\n") == "a: 1\nb: 2\n"


def test_list_indent(format_yaml):
    assert (
        format_yaml(
            """
a:
- a
- b
- c
""",
        )
        == """
a:
  - a
  - b
  - c
""".lstrip()
    )


def test_comment_space_after_hash_1(format_yaml):
    assert format_yaml("a: 1 #  233") == "a: 1  # 233\n"


def test_comment_space_after_hash_2(format_yaml):
    assert format_yaml("a: 1 #233") == "a: 1  # 233\n"


def test_comment_space_before_hash(format_yaml):
    assert format_yaml("a: 1     # 233") == "a: 1  # 233\n"


def test_remove_empty_comment(format_yaml):
    assert format_yaml("a: 1 #") == "a: 1\n"


def test_max_2_blank_line_1(format_yaml):
    expected = """
default_stages: [commit]


repos:
  - repo: https://github.com/Trim21/pre-commit-hooks
""".lstrip()
    actual = format_yaml(
        """
default_stages: [commit] #





repos:
- repo:  https://github.com/Trim21/pre-commit-hooks
""",
    )
    print(repr(expected), repr(actual))
    assert actual == expected


def test_max_2_blank_line_2(format_yaml):
    expected = """
default_stages: [commit]


repos:
  - repo: https://github.com/Trim21/pre-commit-hooks
""".lstrip()
    actual = format_yaml(
        """
default_stages: [commit]





repos:
- repo:  https://github.com/Trim21/pre-commit-hooks
""",
    )
    assert_string_eq(actual, expected)


def test_blank_line_2(format_yaml):
    assert_string_eq(
        format_yaml(
            """
default_stages: [commit]




repos:
  - repo: https://github.com/Trim21/pre-commit-hooks
    rev: 127181a2ddbbd90b309874c573c9c88550a93d64  # frozen: v0.2.0
    hooks:
      - id: yamlfmt
      - id: poetry-check-lock
      - id: find-trailing-comma

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: e1668fe86af3810fbca72b8653fe478e66a0afdc  # frozen: v3.2.0
    hooks:
      - id: check-case-conflict
      - id: check-ast
      - id: check-builtin-literals
""",
        ),
        """
default_stages: [commit]


repos:
  - repo: https://github.com/Trim21/pre-commit-hooks
    rev: 127181a2ddbbd90b309874c573c9c88550a93d64  # frozen: v0.2.0
    hooks:
      - id: yamlfmt
      - id: poetry-check-lock
      - id: find-trailing-comma

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: e1668fe86af3810fbca72b8653fe478e66a0afdc  # frozen: v3.2.0
    hooks:
      - id: check-case-conflict
      - id: check-ast
      - id: check-builtin-literals
""".lstrip(),
    )


def test_best_practice(tmpdir):
    p = tmpdir / "a.yaml"
    with open(p, "wb") as f:
        f.write(b"a: 1\nb: 2\n")
    assert not format_file(p, True, _INDENT, _WIDTH)


def test_format_file(tmpdir):
    p = tmpdir / "a.yaml"
    with open(p, "wb") as f:
        f.write(b"a: 1\nb: 2\n")
    with mock.patch("pre_commit_hooks.yamlfmt.round_trip") as m:
        m.return_value = "a: 1\nb: 2\n"
        assert not format_file(p, True, _INDENT, _WIDTH)


def test_top_array_with_indent(format_yaml):
    assert (
        format_yaml(
            """
  - id: yamlfmt
    name: format yaml

  - id: poetry-check-lock
    name: Check poetry.lock fresh
""",
        )
        == """
- id: yamlfmt
  name: format yaml

- id: poetry-check-lock
  name: Check poetry.lock fresh
""".lstrip()
    )


def test_comment_indent(format_yaml):
    assert_string_eq(
        format_yaml(
            """
# a comment
repos:
  - repo: https://github.com/Trim21/pre-commit-hooks
    rev: 1586f0d19e5685e59cbe827988f5360df0f334b5  # frozen: v0.3.0
    hooks:
# b comment
      - id: yamlfmt
      - id: poetry-check-lock
        #
      - id: find-trailing-comma
      - id: pretty-format-json
        args:
          - --no-ensure-ascii
               # check for file bigger than 500kb
          - --no-sort-keys
          - --indent
          - '2'
          - --autofix
# c comment
""",
        ),
        """\
# a comment
repos:
  - repo: https://github.com/Trim21/pre-commit-hooks
    rev: 1586f0d19e5685e59cbe827988f5360df0f334b5  # frozen: v0.3.0
    hooks:
      # b comment
      - id: yamlfmt
      - id: poetry-check-lock
      - id: find-trailing-comma
      - id: pretty-format-json
        args:
          - --no-ensure-ascii
          # check for file bigger than 500kb
          - --no-sort-keys
          - --indent
          - '2'
          - --autofix
          # c comment
""",
    )
