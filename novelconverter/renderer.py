# -*- coding: utf-8 -*-
# author: @RShirohara

from copy import copy

from . import util


def build_renderer():
    """Build the default renderers."""
    renderer = Renderer()
    renderer.reg.add(renderer.code_inline, "code_inline", 120)
    renderer.reg.add(renderer.bold, "bold", 110)
    renderer.reg.add(renderer.image, "image", 100)
    renderer.reg.add(renderer.link, "link", 90)
    renderer.reg.add(renderer.ruby, "ruby", 80)
    renderer.reg.add(renderer.tcy, "tcy", 70)
    renderer.reg.add(renderer.newpage, "newpage", 60)
    renderer.reg.add(renderer.header, "header", 50)
    renderer.reg.add(renderer.code_block, "code_block", 40)
    renderer.reg.add(renderer.item_list, "item_list", 30)
    renderer.reg.add(renderer.quote, "quote", 20)
    renderer.reg.add(renderer.para, "para", 10)
    return renderer


class Renderer(util.Processor):
    """Renders the ElementTree into a formatted string."""

    def _render_nest(self, source):
        if type(source) == list:
            for i in range(len(source)):
                source[i] = self._render_nest(source[i])
        if type(source) == dict:
            if "content" in source.keys():
                source["content"] = self._render_nest(source["content"])
            source = self.reg[source["type"]](source)
        return source

    def _join_nest(self, source, cat1="", cat2=""):
        if type(source) == list:
            for i in range(len(source)):
                source[i] = self._join_nest(source[i], cat1=cat2)
            return cat1.join(source)
        return source

    def run(self, tree):
        result = copy(tree.root.block)
        for i in range(len(tree)):
            result[i] = self._render_nest(result[i])
        return [r for r in result if r]

    def para(self, source):
        """Paragraph"""
        return self._join_nest(source["content"], "\n", "")

    def header(self, source):
        """Header"""
        return source["content"][0]

    def code_block(self, source):
        """Code block"""
        return self._join_nest(source["content"][0], "\n", "")

    def item_list(self, source):
        """Item list"""
        return self._join_nest(source["content"][0], "\n", "")

    def quote(self, source):
        """Quote"""
        return self._join_nest(source["content"][0], "\n", "")

    def newpage(self, source):
        """New page"""
        pass

    def bold(self, source):
        """Bold text"""
        return source["content"][0]

    def code_inline(self, source):
        """Code block in line"""
        return source["content"][0]

    def image(self, source):
        """Image link"""
        return source["content"][0]

    def link(self, source):
        """Hyper link"""
        return source["content"][0]

    def ruby(self, source):
        """Ruby text"""
        return source["content"][0]

    def tcy(self, source):
        """Tate chu Yoko"""
        return source["content"][0]
