import re

from ruamel.yaml import *
from ruamel.yaml.emitter import Emitter
from ruamel.yaml.serializer import Serializer

pattern1 = re.compile("\n{3,}")
pattern2 = re.compile("\n +")


class RemoveMultiEmptyLineEmitter(Emitter):
    def write_plain(self, text, split=True):  # type: (Any, Any) -> None
        super().write_plain(text, False)

    def write_comment(self, comment: CommentToken, *args, **kwargs):
        if self.column:
            comment.start_mark.column = self.column + 2
        else:
            comment.start_mark.column = 0
        comment.value = pattern1.sub("\n\n", comment.value)
        comment.value = pattern2.sub("\n", comment.value)
        comment.value = comment.value.lstrip(" ")
        super().write_comment(comment, *args, **kwargs)


class RemoveMultiEmptyLineRoundTripDumper(
    RemoveMultiEmptyLineEmitter, Serializer, RoundTripRepresenter, VersionedResolver
):
    def __init__(
        self,
        stream,
        default_style=None,
        default_flow_style=True,
        canonical=None,
        indent=None,
        width=None,
        allow_unicode=None,
        line_break=None,
        encoding=None,
        explicit_start=None,
        explicit_end=None,
        version=None,
        tags=None,
        block_seq_indent=None,
        top_level_colon_align=None,
        prefix_colon=None,
    ):
        # type: (StreamType, Any, Optional[bool], Optional[int], Optional[int], Optional[int], Optional[bool], Any, Any, Optional[bool], Optional[bool], Any, Any, Any, Any, Any) -> None  # NOQA
        RemoveMultiEmptyLineEmitter.__init__(
            self,
            stream,
            canonical=canonical,
            indent=indent,
            width=width,
            allow_unicode=allow_unicode,
            line_break=line_break,
            block_seq_indent=block_seq_indent,
            top_level_colon_align=top_level_colon_align,
            prefix_colon=prefix_colon,
            dumper=self,
        )
        self.best_map_indent = indent
        self.sequence_dash_offset = indent
        self.best_sequence_indent = indent * 2
        self.allow_space_break = True

        Serializer.__init__(
            self,
            encoding=encoding,
            explicit_start=explicit_start,
            explicit_end=explicit_end,
            version=version,
            tags=tags,
            dumper=self,
        )
        RoundTripRepresenter.__init__(
            self,
            default_style=default_style,
            default_flow_style=default_flow_style,
            dumper=self,
        )
        VersionedResolver.__init__(self, loader=self)
