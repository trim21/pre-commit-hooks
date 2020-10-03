from pathlib import Path

import poetry.utils
import poetry.poetry
from poetry.factory import Factory


def main() -> int:
    if not current_repo().locker.is_fresh():
        return 1
    return 0


def current_repo() -> poetry.poetry.Poetry:
    return Factory().create_poetry(Path.cwd())


if __name__ == "__main__":
    exit(main())
