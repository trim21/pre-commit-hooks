import sys
import difflib
import argparse
from io import StringIO
from textwrap import dedent

from ruamel import yaml

from pre_commit_hooks._yaml_dumper import RemoveMultiEmptyLineEmitter


def round_trip(sin, indent: int, width: int):
    inst = yaml.YAML(typ="rt", pure=True)
    inst.width = width
    inst.old_indent = indent
    inst.sequence_indent = indent * 2
    inst.sequence_dash_offset = indent
    inst.map_indent = indent * 2
    inst.Emitter = RemoveMultiEmptyLineEmitter
    y = inst.load(sin)

    with StringIO() as stream:
        inst.dump(y, stream)
        return stream.getvalue()


def format_file(fs, write, indent: int, width: int):
    ret = 0
    with open(fs, encoding="utf8", newline="\n") as f:
        before = f.read()
    with StringIO(initial_value=before.replace("\r\n", "\n"), newline="\n") as s:
        s.seek(0)
        after = (
            "\n".join(
                dedent(round_trip(s, indent, width)).strip(" \n").splitlines(),
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
