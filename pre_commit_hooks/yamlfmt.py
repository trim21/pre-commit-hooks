import argparse
import os
import sys
from io import StringIO
from ruamel import yaml

from pre_commit_hooks._yaml_dumper import RemoveMultiEmptyLineRoundTripDumper


def round_trip(sin):
    y = yaml.round_trip_load(sin, preserve_quotes=False)
    return yaml.round_trip_dump(
        y,
        Dumper=RemoveMultiEmptyLineRoundTripDumper,
        allow_unicode=True,
        block_seq_indent=2,
        top_level_colon_align=False,
    )


def format_file(fs, write):
    ret = 0
    with open(fs, "r+", encoding="utf8", newline="") as f:
        before = f.read()
        s = StringIO(initial_value=before)
        s.seek(0)
        after = round_trip(s).rstrip("\n") + "\n"
        if before != after:
            return 1
        if write:
            f.seek(0)
            f.write(after)
            f.truncate()
        else:
            print(after)
    return ret


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--write",
        help="overwrite file with formatted output",
        action="store_true",
    )
    parser.add_argument("file", help="file to parse", nargs="*")

    args = parser.parse_args()

    if not args.file:
        parser.error("write requires at least one file")

    ret = False

    for file in args.file:
        ret |= format_file(file, args.write)
    return ret


if __name__ == "__main__":
    sys.exit(main())
