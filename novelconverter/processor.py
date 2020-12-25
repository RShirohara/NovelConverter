# -*- coding: utf-8 -*-
# author: @RShirohara


from . import util


def build_preprocessor():
    """Build the default preprocessors."""
    processor = PreProcessor()
    # processor.reg.add(function, name, priority)
    return processor


def build_postprocessor():
    """Build the default postprocessors."""
    processor = PostProcessor()
    # processor.reg.add(function, name, priority)
    return processor


class PreProcessor(util.Processor):
    """Process a strings before running parser."""
    pass


class PostProcessor(util.Processor):
    """Process a strings after running renderer."""
    pass
