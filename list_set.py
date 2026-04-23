
from ..pytilities.validation import *
from collections.abc import Iterable


class ListSet(list):
    ''' 
    '''
    lookup_set: set

    def __init__(self, *arg):
        arg_set = set(arg)
        arg_list = list(arg_set)

        super().__init__(arg_list)
        self.lookup_set = arg_set


    # append(x) — Adds an item to the end.
    def append(self, value):
        validate_uniqueness(self,value)
        super().append(value)
        self.lookup_set = set(super())

    # insert(i, x) — Inserts an item at a given position.
    def insert(self, i, value):
        validate_uniqueness(self, value)
        super().insert(i, value)
        self.lookup_set = set(super())

    # extend(iterable) — Adds all items from an iterable.
    def extend(self, iterable_values: Iterable):

        for value in iterable_values:
            if value not in self:
                super().append(value)
                self.lookup_set.add(value)
