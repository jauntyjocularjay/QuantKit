
from pytilities.validation import *
from collections.abc import Iterable
from typing import Union, Any



class unique_list(list):
    ''' 
    '''
    lookup_set: set

    def __init__(self, *arg):
        arg_set = set(arg)
        arg_list = list(arg_set)

        super().__init__(arg_list)
        self.lookup_set: set = arg_set


    # append(x) — Adds an item to the end.
    def append(self, value):
        if value in self.lookup_set: return
        super().append(value)
        self.lookup_set.add(value)

    # insert(i, x) — Inserts an item at a given position.
    def insert(self, i, value):
        if value in self.lookup_set: return
        super().insert(i, value)
        self.lookup_set.add(value)

    # extend(iterable) — Adds all items from an iterable.
    def extend(self, iterable_values: Iterable):
        for value in iterable_values:
            if value not in self.lookup_set:
                super().append(value)
                self.lookup_set.add(value)

    # TODO Test and finish
    def __setitem__(self, key: Union[int, slice], value_to_set: Union[Any, Iterable[Any]]):
        if isinstance(key, slice) and isinstance(value_to_set, Iterable):
            values = list(value_to_set)
            self.set_slice(key, values)
        elif isinstance(key, int) and isinstance(value_to_set, Iterable):
            self.set_iterable_at(key, value_to_set)
        elif isinstance(key, int):
            self.set_single(key, value_to_set)

    # TODO Test and finish
    def set_single(self, index: int, value: Any):
        if value in self.lookup_set:
            return
        else:
            self.insert(index,value)
            self.lookup_set.add(value)

    # TODO Test and finish
    def set_iterable_at(self, index: int, value_iterable: Iterable[Any]):
        value_list = list(value_iterable)

        for x in value_list:
            if x in self.lookup_set:
                value_list.remove(x)

        super().__setitem__(index, value_list)
        self.lookup_set.add(x)

    # TODO Test and finish
    def set_slice(self, slic: slice, value_iterable: Iterable[Any]):
        value_list = list(value_iterable)

        for x in value_list:
            if x in self.lookup_set:
                value_list.remove(x)

        slic = slice(slic.start, slic.stop-1, slic.step)
        super().__setitem__(slic, value_list)
        pass

