import re
from typing import Any

from ruamel.yaml import CommentToken
from ruamel.yaml.emitter import Emitter

pattern1 = re.compile("\n{3,}")
# pattern2 = re.compile("\n +")
pattern3 = re.compile("# *")


class RemoveMultiEmptyLineEmitter(Emitter):
    def __init__(
        self,
        *args,
        indent=None,
        **kwargs,
    ):
        if indent is None:
            indent = 2
        super().__init__(*args, indent=indent, **kwargs)
        self.best_map_indent = indent
        self.sequence_dash_offset = indent
        self.best_sequence_indent = indent * 2
        self.allow_space_break = True

    def write_plain(self, text, split=True):  # type: (Any, Any) -> None
        super().write_plain(text, False)

    def write_comment(self, comment: CommentToken, *args, **kwargs):
        """write line break or comment with line break"""
        line_break_num = 2
        if comment.value.startswith("#"):
            line_break_num = 3
        stripped = comment.value.strip()

        if stripped:
            leading = ""
            if comment.value.startswith("\n"):
                leading = "\n"
                indent = (self.indent or 0) - 2
                if self.mapping_context:
                    indent += 2
                if stripped == "#":
                    comment.value = "\n"
                else:
                    comment.value = (
                        leading + " " * indent + "# " + comment.value.lstrip("\n# ")
                    )
            else:
                comment.value = pattern3.sub("# ", comment.value)
                if comment.value.strip() == "#":
                    comment.value = comment.value.lstrip("# ")

            if not self.column:
                indent = self.indent or 0
                if self.mapping_context or self.sequence_context:
                    indent += 2
                comment.value = (
                    leading + " " * indent + "# " + comment.value.lstrip("\n# ")
                )

        comment.value = pattern1.sub("\n" * line_break_num, comment.value)

        if self.column:
            if comment.value.strip():
                comment.start_mark.column = self.column + 2
        else:
            comment.start_mark.column = 0

        super().write_comment(comment, *args, **kwargs)
