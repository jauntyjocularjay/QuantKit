from multiprocessing import Value

from ..pytilities.validation import *
from outcome import outcome as Outcome



class ListSet(list):
    ''' 
    '''

    def __init__(self, *arg):
        arg_set = set(arg)
        arg_list = list(arg_set)
        super().__init__(arg_list)


    # append(x) — Adds an item to the end.
    def append(self, value):
        validate_uniqueness(self,value)
        super().append(value)

    # insert(i, x) — Inserts an item at a given position.
    def insert(self, i, value):
        validate_uniqueness(self, value)
        super().insert(i, value)

    # extend(iterable) — Adds all items from an iterable.
    def extend(self, i, values: Sequence):
        for x in values:
            if self.count(x) > 0: continue
            else: self.append(x)


class Probability:
    '''
    '''
    def __init__(self, sample_space: set):
        Probability.is_set_of_outcomes(sample_space)
        self._sample_space = sample_space

    @classmethod
    def is_set_of_outcomes(cls, outcomes):
        validate_as(outcomes, set)

        for x in outcomes:
            validate_as(x, Outcome)

    @property
    def sample_space(self):
        return self._sample_space

    