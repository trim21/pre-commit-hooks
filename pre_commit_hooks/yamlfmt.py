import sys
import difflib
import argparse
from io import StringIO
from textwrap import dedent

from ruamel import yaml

from pre_commit_hooks._yaml_dumper import (
    ForceNoneRepresenter,
    RemoveMultiEmptyLineEmitter,
)


def _round_trip(sin, indent: int, width: int):
    inst = yaml.YAML(typ="rt", pure=True)
    inst.width = width  # type: ignore
    inst.old_indent = indent  # type: ignore
    inst.sequence_indent = indent * 2  # type: ignore
    inst.sequence_dash_offset = indent
    inst.map_indent = indent  # type: ignore
    inst.Emitter = RemoveMultiEmptyLineEmitter
    inst.Representer = ForceNoneRepresenter
    y = inst.load(sin)

    with StringIO() as stream:
        inst.dump(y, stream)
        return stream.getvalue()


def round_trip(sin, indent: int, width: int):
    after = _round_trip(sin, indent, width)
    return after
    again = _round_trip(after, indent, width)

    while after != again:
        after = again
        again = _round_trip(after, indent, width)

    return again


def format_file(fs, write, indent: int, width: int):
    ret = 0
    with open(fs, encoding="utf8", newline="\n") as f:
        before = f.read()
    after = (
        "\n".join(
            dedent(round_trip(before.replace("\r\n", "\n"), indent, width))
            .strip(" \n")
            .splitlines(),
        ).strip()
        + "\n"
    )
    if before != after:
        if write:
            print(f"fixing {fs}")
        else:
            print(
                "".join(
                    difflib.unified_diff(
                        before.splitlines(True),
                        after.splitlines(True),
                    ),
                )
            )
        ret = 1
    if write:
        if ret:
            with open(fs, "w", encoding="utf8", newline="\n") as f:
                f.write(after)
    return ret


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--write",
        help="overwrite file with formatted output",
        action="store_true",
    )
    parser.add_argument(
        "--indent",
        type=int,
        help="indent",
        default=2,
    )
    parser.add_argument(
        "--width",
        type=int,
        help="best width",
        default=100,
    )
    parser.add_argument("file", help="file to parse", nargs="*")

    args = parser.parse_args()

    if not args.file:
        parser.error("write requires at least one file")

    ret = False

    for file in args.file:
        ret |= format_file(file, args.write, args.indent, args.width)
    return ret


if __name__ == "__main__":
    sys.exit(main())
