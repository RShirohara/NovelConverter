#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: RShirohara

import argparse
import inspect
import sys

import novelconverter

_EXTENSION = (
    "markdown",
    "ddmarkdown",
    "pixiv"
)


def get_args():
    _parser = argparse.ArgumentParser(
        description=novelconverter.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    _parser.add_argument(
        "from_format", type=str, help="Format of the original text"
    )
    _parser.add_argument(
        "to_format", type=str, help="Format of the output text"
    )
    _parser.add_argument(
        "-o", "--output", type=str, help="File path of the output text"
    )
    _parser.add_argument(
        "-i", "--input", type=str, help="File path of the original text"
    )
    args = _parser.parse_args()
    return args


def load_data(path):
    if path:
        with open(path, "r") as _f:
            source = _f.read()
    else:
        source = sys.stdin.read()
    return source


def export_data(source, path):
    if path:
        with open(path, "w") as _f:
            _f.write(source)
    else:
        print(source)


def load_extension(ext_name, proc_name):
    # ext_nameが存在しているか確認
    if ext_name not in _EXTENSION:
        raise ValueError(f"No extension named {ext_name} exists.")
    ext = eval(f"novelconverter.extension.{ext_name}")
    _in_processor = [
        x[0] for x in inspect.getmembers(ext, inspect.isfunction)
    ]
    processor = {
        x.replace("build_", ""): eval(f"ext.{x}", {"ext": ext})
        for x in _in_processor
    }
    # proc_nameが存在するかを確認
    if proc_name not in processor.keys():
        sys.stderr.write(f"No processor named {proc_name} exists.\n")
        return novelconverter.util.Processor()
    return processor[proc_name]()


class NovelConverter(novelconverter.NovelConverter):
    def build_registry(self, from_form, to_form):
        self.tree.ip = load_extension(from_form, "inlineparser")
        self.tree.bp = load_extension(from_form, "blockparser")
        self.renderer = load_extension(to_form, "renderer")
        self.preprocessor = load_extension(from_form, "preprocessor")
        self.postprocessor = load_extension(to_form, "postprocessor")


def main():
    args = get_args()
    nv = NovelConverter()
    nv.build_registry(args.from_format, args.to_format)
    source = load_data(args.input)
    result = nv.convert(source)
    export_data(result, args.output)


if __name__ == "__main__":
    main()
