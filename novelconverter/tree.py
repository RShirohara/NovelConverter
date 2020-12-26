# -*- coding: utf-8 -*-
# author: @RShirohara

import dataclasses
import typing
from collections.abc import Iterable

from .__meta__ import __version__ as nv_ver
from .util import Processor


class _Metadata(typing.TypedDict):
    title: str
    author: str


@dataclasses.dataclass
class _TreeRoot:
    block: list[dict] = dataclasses.field(default_factory=list, init=False)
    meta: _Metadata = dataclasses.field(init=False)
    version: str = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.block = [{}]
        self.meta = _Metadata()
        self.version = nv_ver


@dataclasses.dataclass
class ElementTree:
    """A ElementTree object have syntax and contents."""

    root: _TreeRoot = dataclasses.field(init=False)
    ip: Processor = dataclasses.field(init=False)
    bp: Processor = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.root = _TreeRoot()

    def __contains__(self, item: dict) -> bool:
        return item in self.root.block

    def __getitem__(self, key: typing.Union[slice, str]) -> dict:
        # reference tree[start:stop]
        if isinstance(key, slice):
            return self.root.block[key.start:key.stop]
        return self.root.block[key]

    def __iter__(self) -> Iterable:
        return iter(self.root.block)

    def __len__(self) -> int:
        return len(self.root.block)

    def _get_meta(self, source: str) -> None:
        # TODO #4
        pass

    def clear(self) -> None:
        """Cleanup ElementTree."""
        self.root = _TreeRoot()

    def parse(self, source: str) -> None:
        """Parse a JSON-formatted string into a Tree object.

        Args:
            source (str): JSON-formatted string
        """

        self.clear()
        _cache = []
        for i in [s for s in source.split("\n\n") if s]:
            if "meta" in self.bp.reg:
                _meta = self.bp.reg["meta"](i)
                if _meta:
                    self.root.meta = _meta
                    _cache.remove(i)
                    self.bp.reg.delete("meta")
                    break
            _cache.append(i)
        for c in _cache:
            _i = len(self.root.block) - 1
            if "code_block" in self.bp.reg:
                _match = self.bp.reg["code_block"](c)
                if _match:
                    self.root.block.insert(_i, _match)
                    continue
                self.bp.reg.delete("code_block")
            c = self.ip.run(c)
            for rb in self.bp.reg:
                if "type" in self.root.block[_i]:
                    break
                _result = rb(c)
                if not _result:
                    continue
                self.root.block.insert(_i, _result)
        self.root.block = [r for r in self.root.block if r]
