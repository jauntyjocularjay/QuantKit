from constants import Relationship as R, relationships_requiring_modifier
from fractions import Fraction
from typing import Union



class related_sample:
    base_alias: str

    def __init__(self, base_alias: str, relationship: R|None = None, modifier_alias: None|str = None ):
        if(modifier_alias is None and (relationship is R.UNION or relationship is R.INTERSECT or relationship is R.GIVEN)):
            return MissingEventModifierError()
        
        self.base_alias = base_alias.upper()
        self.relationship = relationship
        self.modifier_alias = modifier_alias.upper() if isinstance(modifier_alias, str) else None

    def __str__(self) -> str:
        if(self.relationship is None):
            return f'P({self.base_alias})'
        elif(self.relationship is R.PRIME):
            return f'P({self.base_alias}{self.relationship.value})'
        else:
            return f'P({self.base_alias}{self.relationship.value}{self.modifier_alias})'

class MissingEventModifierError(ValueError):
    def __init__(self):
        super().__init__(f'{related_sample} with a relationship: {relationships_requiring_modifier} require a modifier to be meaningful.')




class event_descriptor:
    ''' An event descriptor is used to map out or label an event or group of events by describing their outcome with a number and a str. 
    '''

    _symbol: str
    _coefficient: Union[int, float, Fraction]

    def __init__(self, coefficient: Union[int, float, Fraction], symbol: str) -> None:
        self._symbol = symbol
        self._coefficient = coefficient

    def __str__(self):
        return f'{self._coefficient}{self._symbol}'

    def __repr__(self) -> str:
        return self.__str__()

    def as_dict(self):
        return { self._symbol: self._coefficient }



class compound_event:
    ''' 
    '''
    def __init__(self, *descriptors):
        self.descriptors = tuple(descriptors)

    def __str__(self):
        return f'{(x for x in self.descriptors)}'

    def __repr__(self) -> str:
        return self.__str__()



event_a = related_sample('a')
event_a_prime = related_sample('a', R.PRIME)
event_b_given_a = related_sample('b', R.GIVEN, 'a')

print(event_a)
print(event_a_prime)
print(event_b_given_a)













event_space = {
    ('a', R.GIVEN, 'b')
}