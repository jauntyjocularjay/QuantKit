from .stats import *



console.clear()

DATA_LIST = 'data_list'
SEQUENCE_MINIMUM = 'min'
SEQUENCE_MAXIMUM = 'max'
SEQUENCE_MEDIAN = 'median'
SEQUENCE_RANGE = 'range'
OUTLIERS = 'outliers'
Q1 = 'q1'
Q2 = 'q2'
Q3 = 'q3'
IQR = 'iqr'
TUKEY_FENCE = 'tukey_fence'

@dataclass(frozen=True)
class BoxPlot:
    q1: Union[float, int]
    median: Union[float, int]
    q3: Union[float, int]
    data_list: Sequence
    
    '''Represents a box plot summary for a numeric sequence (min, Q1, median, Q3, max).

    This class computes and stores the five-number summary required for a box plot:
        1. minimum, 
        2. first quartile (Q1)
        3. median (Q2)
        4. third quartile (Q3)
        5. maximum.
        6. ordered data list
        7. iqr
        8. range
     - Quartiles are calculated using the specified method ('exclusive' or 'inclusive').
     - If a tuple or set is passed as the sequence it will be automatically converted to an ordered 
      list.
    - In the case of sets, the original order will be lost. 

    Parameters:
        data_list (Sequence): A sequence of numeric values (length >= 4).
        quantile_method (Literal['exclusive', 'inclusive']): Method for quartile calculation.
            Defaults to 'exclusive'.

    Attributes:
        min (float): Minimum value in the data.
        q1 (float): First quartile (25th percentile).
        median (float): Median value (50th percentile).
        q3 (float): Third quartile (75th percentile).
        max (float): Maximum value in the data.
        data_list (list): Sorted list of the input data.

    Example:
        bp = BoxPlot([1, 2, 3, 4, 5, 6])
        print(bp.as_dict())
        # {min: 1, q1: 2.25, 'median': 3.5, q2: 3.5, q3: 4.75, max: 6}

    Notes:
        The __str__ method provides a compact, human-readable summary of the box plot:
            boxplot:    min * {min} ---- q1 [ {q1}     median | {median}     q3 ] {q3} ---- max * {max}]
        This is useful for quick inspection of the five-number summary in logs or printouts.
        For a traditional logging instead, use BoxPlot.as_dict() when you print the result.
    '''
    def __init__(self, data_list: Sequence, quantile_method: Literal['exclusive', 'inclusive'] = 'exclusive'):
        if data_list is None or not isinstance(data_list, Sequence):
            raise InvalidSequenceError
        if not sequence_are_numbers(data_list):
            raise NotNumericSequenceError
        if len(data_list) < 4:
            raise ValueError('argument must have at least length 4')

        data_list = sorted(data_list)
        quartiles = Statistics.quantiles(data_list, n=4, method = quantile_method)

        object.__setattr__(self, Q1, quartiles[0])
        object.__setattr__(self, SEQUENCE_MEDIAN, Statistics.median(data_list)) # aka q2
        object.__setattr__(self, Q3, quartiles[2])
        object.__setattr__(self, DATA_LIST, data_list)

    @property
    def min(self):
        ''' returns the first value within the Tukey Fence or the first value in a given sequence.

        Returns:
            num: either the first value within the Tukey Fence or the first value in the sequence.
        '''
        return next((x for x in self.data_list if x >= self.tukey_fence[SEQUENCE_MINIMUM]), self.data_list[0])

    @property
    def max(self):
        ''' returns the last value within the Tukey Fence or the last value in a given sequence.

        Returns:
            num: either the last value within the Tukey Fence or the last value in the sequence.
        '''
        return next((x for x in reversed(self.data_list) if x <= self.tukey_fence[SEQUENCE_MAXIMUM]), self.data_list[-1])

    @property
    def tukey_fence(self):
        return {
            SEQUENCE_MINIMUM: self.q1 - self.iqr * 1.5,
            SEQUENCE_MAXIMUM: self.q3 + self.iqr * 1.5
        }

    @property
    def range(self):
        return self.max - self.min

    @property
    def outliers(self):
        return [x for x in self.data_list if x < self.tukey_fence[SEQUENCE_MINIMUM] or x > self.tukey_fence[SEQUENCE_MAXIMUM]]

    @property
    def iqr(self):
        return self.q3 - self.q1

    @property
    def iqr_balance(self):
        left = self.median - self.q1
        right = self.q3 - self.median
        return (left - right) / self.iqr

    @property
    def whisker_balance(self):
        left = self.q1 - self.min
        right = self.max - self.q3
        return (left - right) / self.range

    def as_dict(self):
        return {
            SEQUENCE_MINIMUM: self.min,
            Q1: self.q1,
            SEQUENCE_MEDIAN: self.median,
            Q2: self.median,
            Q3: self.q3,
            SEQUENCE_MAXIMUM: self.max,
            TUKEY_FENCE: {
                SEQUENCE_MINIMUM: self.tukey_fence[SEQUENCE_MINIMUM], 
                SEQUENCE_MAXIMUM: self.tukey_fence[SEQUENCE_MAXIMUM]
            },
            DATA_LIST: self.data_list,
            OUTLIERS: self.outliers,
            IQR: self.iqr,
            SEQUENCE_RANGE: self.range
        }

    def __str__(self):
        return f'boxplot:    min * {self.min} ---- q1 [ {self.q1}     median | {self.median}     q3 ] {self.q3} ---- max * {self.max}]'

bp = BoxPlot([-1024, -512-64,-512, -512-128,136, 140, 178, 190, 205, 215, 217, 218, 232, 234, 240, 255, 270, 275, 290, 301, 303, 315, 317, 318, 326, 333, 343, 349, 360, 369, 377, 388, 391, 392, 398, 400, 402, 405, 408, 422, 429, 450, 475, 512, 1024])
pprint(bp.as_dict())