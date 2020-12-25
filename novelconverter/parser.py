# -*- coding: utf-8 -*-
# author: @RShirohara

import json
import re

from .util import Processor

_PARA = re.compile(
    r'\{"type": (?P<text>.*?)\}'
)


def build_inlineparser():
    """Build the default inline parsers."""
    parser = InlineParser()
    # parser.reg.add(item, name, priority)
    return parser


def build_blockparser():
    """Build the default block parsers."""
    parser = BlockParser()
    # parser.reg.add(parser.newpage, "newpage", 60)
    # parser.reg.add(parser.header, "header", 50)
    # parser.reg.add(parser.code_block, "code_block", 40)
    # parser.reg.add(parser.item_list, "item_list", 30)
    # parser.reg.add(parser.quote, "quote", 20)
    parser.reg.add(parser.para, "para", 10)
    return parser


class InlineParser(Processor):
    """Parse strings into a JSON-formatted string.

    Example:
        {"type": "parser name", "content": [content]}

    In most cases, the 0th element in "content" will be output if the
    corresponding "Renderer" does not exist.
    """

    def bold(self, source):
        """Bold text

        Example:
            {"type": "bold", "content": ["text"]}
        """
        pass

    def code_inline(self, source):
        """Code block in line

        Example:
            {"type": "code_inline", "content", ["text"]}
        """

    def image(self, source):
        """Image

        Example:
            {"type": "image", "content", ["text", "link"]}
        """
        pass

    def link(self, source):
        """Hyper link

        Example:
            {"type": "link", "content": ["text", "link"]}
        """
        pass

    def ruby(self, source):
        """Ruby text

        Example:
            {"type": "ruby", "content": ["text", "ruby"]}
        """
        pass

    def tcy(self, source):
        """Tate chu Yoko

        Example:
            {"type": "tcy", "content": ["text"]}
        """
        pass


class BlockParser(Processor):
    """Parse a JSON-formatted string into a dict object."""

    def para(self, source):
        """Paragraph

        Returns:
            dict: {
                "type": "para",
                "content": ["content strings"]
            }
        """
        _in_list = []
        for i in source.splitlines():
            _match = _PARA.search(i)
            if _match:
                _in_list.append([
                    _PARA.sub(r'",{"type": \g<text>},"', i)
                ])
            else:
                _in_list.append(i)
        _content = str(_in_list).replace("\'", '"')
        _new = "{" + f'"type": "para", "content": {_content}' + "}"
        return json.loads(_new)

    def header(self, source):
        """Header

        Returns:
            dict: {
                "type": "header",
                "content": ["Header name", level]
            }
        """
        pass

    def code_block(self, source):
        """Code block

        Returns:
            dict: {
                "type": "code_block",
                "content": [["content strings"], "language"]
            }
        """
        pass

    def item_list(self, source):
        """Item list

        Returns:
            dict: {
                "type": "item_list",
                "content": [["content strings"], [level]]
            }
        """
        pass

    def quote(self, source):
        """Quote

        Returns:
            dict: {
                "type": "quote",
                "content": [["content strings"], [level]]
            }
        """
        pass

    def newpage(self, source):
        """New page

        Returns:
            dict: {"type": "newpage"}
        """
        pass
