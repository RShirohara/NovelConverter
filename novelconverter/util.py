# -*- coding: utf-8 -*-
# author: @RShirohara

import dataclasses
import typing
from types import FunctionType


class _PriorityItem(typing.NamedTuple):
    """A Priority item used in Registry."""

    name: str
    priority: int


class Processor:
    def __init__(self):
        self.reg = Registry()

    def run(self, source):
        for r in self.reg:
            source = r(source)
        return source


@dataclasses.dataclass
class Registry:
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
    _priority: list[_PriorityItem] = dataclasses.field(init=False)
    _is_sorted: bool = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self._data = {}
        self._priority = []
        self._is_sorted = False

    def __contains__(self, item: typing.Union[str, int]) -> _PriorityItem:
        if isinstance(item, str):
            return item in self._data.keys()
        return item in self._data.values()

    def __iter__(self):
        self._sort()
        return iter([self._data[k] for k, v in self._priority])

    def __getitem__(self, key: typing.Union[slice, str, int]) -> dict:
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

    def __len__(self) -> int:
        return len(self._priority)

    def _sort(self) -> None:
        """Sort the registry by priority."""
        if not self._is_sorted:
            self._priority.sort(key=lambda item: item.priority, reverse=True)
            self._is_sorted = True

    def get_index(self, name: str) -> FunctionType:
        """Return the index of the given name.

        Args:
            name (str): index name
        Returns:
            function: function
        """
        if name in self:
            self._sort()
            return self._priority.index(
                [x for x in self._priority if x.name is name][0]
            )
        raise ValueError(f"No item named {name} exists.")

    def add(self, item: FunctionType, name: str, priority: int) -> None:
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

    def delete(self, name: str, strict: bool = True) -> None:
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
