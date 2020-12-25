# -*- coding: utf-8 -*-
# author: @RShirohara

from .parser import build_blockparser, build_inlineparser
from .renderer import build_renderer
from .processor import build_postprocessor, build_preprocessor
from .util import ElementTree


class NovelConverter:
    """A Novel Converter.

    Convert syntax for multiple Web-Novel sites.

    Examples:
        novelconv = NovelConverter()
        novelconv.build_registry()
        result = novelconv.convert(source)
    """

    def __init__(self):
        self.tree = ElementTree(self)

    def build_registry(self):
        """Build default registry."""
        self.inlineparser = build_inlineparser()
        self.blockparser = build_blockparser()
        self.renderer = build_renderer()
        self.preprocessor = build_preprocessor()
        self.postprocessor = build_postprocessor()

    def convert(self, source):
        """Convert syntax.

        Args:
            source (str): source strings
        """
        source = self.preprocessor.run(source)
        self.tree.parse(source)
        result = "\n\n".join(self.renderer.run(self.tree))
        return self.postprocessor.run(result)
