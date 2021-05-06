import sys
import argparse
from pathlib import Path


def format_file(fs: str, extension: str):
    p = Path(fs)
    if p.suffix in {".yaml", ".yml"}:
        if p.suffix != extension:
            p.replace(p.with_suffix(extension))
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--ext",
        type=str,
        help="file extension for yaml files",
        default="yaml",
        choices=["yml", "yaml"],
    )
    parser.add_argument("file", help="files", nargs="*")

    args = parser.parse_args()

    if not args.file:
        parser.error("requires at least one file")

    ret = False

    for file in args.file:
        ret |= format_file(file, "." + args.ext)
    return ret


if __name__ == "__main__":
    sys.exit(main())
