#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from novelconverter import NovelConverter
from novelconverter.renderer import build_renderer
from novelconverter.tree import ElementTree


class TestRenderer(unittest.TestCase):
    """Test class of novelconverter.renderer."""

    def setUp(self):
        self.renderer = build_renderer()
        self.tree = ElementTree()

    # Add renderer function

    def test_para(self):
        source = {
            "type": "para",
            "content": [
                "t1",
                "t2",
                ["t3", "t4", "t5"],
                "t6",
            ]
        }
        result = "t1\nt2\nt3t4t5\nt6"
        self.assertEqual(result, self.renderer.reg["para"](source))

    def test_run(self):
        self.tree.root.block = [
            {
                "type": "para",
                "content": [
                    "t1",
                    "t2",
                    [
                        "t3",
                        {"type": "ruby", "content": ["t4-1", "t4-2"]},
                        "t5",
                    ],
                    "t6"
                ]
            },
            {
                "type": "header",
                "content": ["Test 1", 1]
            }
        ]
        result = [
            "t1\nt2\nt3t4-1t5\nt6",
            "Test 1"
        ]
        self.assertEqual(result, self.renderer.run(self.tree))


if __name__ == "__main__":
    unittest.main()
