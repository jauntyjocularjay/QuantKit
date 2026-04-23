from pytilities.validation import *
from outcome import outcome as Outcome


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