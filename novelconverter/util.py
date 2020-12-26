# -*- coding: utf-8 -*-
# author: @RShirohara

import dataclasses
import typing

from .__meta__ import __version__ as version


ProcVar = typing.TypeVar("Processor")
RegVar = typing.TypeVar("Registry")
PriItemVar = typing.TypeVar("PriorityItem")


class _PriorityItem(typing.NamedTuple):
    """A Priority item used in Registry."""

    name: str
    priority: int


class ElementTree:
    """A ElementTree that holds the syntax and contents."""

    def __init__(self, novelconv):
        self.nv = novelconv
        self.root = {
            "block": [{}],
            "meta": {},
            "NovelConv-Version": version,
        }

    def __contains__(self, item):
        return item in self.root["block"]

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.root["block"][key.start:key.stop]
        return self.root["block"][key]

    def __iter__(self):
        return iter(self.root["block"])

    def __len__(self):
        return len(self.root["block"])

    def __repr__(self):
        return f"<{self.__class__.__name__}({list(self)})>"

    def _get_meta(self, source):
        # TODO: #4
        pass

    def clear(self):
        """Cleanup ElementTree."""
        self.root["block"] = [{}]
        self.root["meta"] = {}

    def parse(self, source):
        """Parse a JSON-formatted string into a Tree object.

        Args:
            source (str): JSON-formatted string
        """
        self.clear()
        _cache = []
        for i in [s for s in source.split("\n\n") if s]:
            if "meta" in self.nv.blockparser.reg:
                _meta = self.nv.blockparser.reg["meta"](i)
                if _meta:
                    self.root["meta"] = _meta
                    _cache.remove(i)
                    self.nv.blockparser.reg.delete("meta")
                    break
            _cache.append(i)
        for c in _cache:
            _i = len(self.root["block"]) - 1
            if "code_block" in self.nv.blockparser.reg:
                _match = self.nv.blockparser.reg["code_block"](c)
                if _match:
                    self.root["block"].insert(_i, _match)
                    continue
                self.nv.blockparser.reg.delete("code_block")
            c = self.nv.inlineparser.run(c)
            for rb in self.nv.blockparser.reg:
                if "type" in self.root["block"][_i]:
                    break
                _result = rb(c)
                if not _result:
                    continue
                self.root["block"].insert(_i, _result)
        self.root["block"] = [r for r in self.root["block"] if r]


class Processor:
    def __init__(self):
        self.reg = Registry()

    def run(self, source):
        for r in self.reg:
            source = r(source)
        return source


@dataclasses.dataclass
class Registry(typing.Generic[PriItemVar]):
    """A priority sorted by registry.

    Use "add to add items and "delete" to remove items.
    A "Registry" instance it like a list when reading data.

    Examples:
        reg = Registry()
        reg.add(hoge(), "Hoge", 20)
        # by index
        item = reg[0]
        # by name
        item = reg["Hoge"]
    """

    _data: dict = dataclasses.field(init=False)
    _priority: list[PriItemVar] = dataclasses.field(init=False)
    _is_sorted: bool = dataclasses.field(init=False)

    def __post_init__(self):
        self._data = {}
        self._priority = []
        self._is_sorted = False

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._data.keys()
        return item in self._data.values()

    def __iter__(self):
        self._sort()
        return iter([self._data[k] for k, v in self._priority])

    def __getitem__(self, key):
        self._sort()
        # reference reg[start:stop]
        if isinstance(key, slice):
            reg = Registry()
            for k, v in self._priority[key]:
                reg.add(self._data[k], k, v)
            return reg
        # reference reg[index]
        if isinstance(key, int):
            return self._data[self._priority[key].name]
        # reference reg["itemname"]
        return self._data[key]

    def __len__(self):
        return len(self._priority)

    def _sort(self):
        """Sort the registry by priority."""
        if not self._is_sorted:
            self._priority.sort(key=lambda item: item.priority, reverse=True)
            self._is_sorted = True

    def get_index(self, name):
        """Return the index of the given name.

        Args:
            name (str): index name
        """
        if name in self:
            self._sort()
            return self._priority.index(
                [x for x in self._priority if x.name is name][0]
            )
        raise ValueError(f"No item named {name} exists.")

    def add(self, item, name, priority) -> None:
        """Add an item to the registry with the given name and priority.

        If an item is registered with a "name" which already exists, the
        existing item is replaced with the new item.

        Args:
            item (function): item
            name (str): item name
            priority (int): priority
        """
        if name in self:
            self.delete(name)
        self._is_sorted = False
        self._data[name] = item
        self._priority.append(_PriorityItem(name, priority))

    def delete(self, name, strict=True):
        """Delete an item to the registry with the given name.

        Args:
            name (str): item name
        """
        try:
            index = self.get_index(name)
            del self._priority[index]
            del self._data[name]
        except ValueError:
            if strict:
                raise
