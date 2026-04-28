from constants import Relationship as R, relationships_requiring_modifier
from fractions import Fraction

class event:
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


event_a = event('a')
event_a_prime = event('a', R.PRIME)
event_b_given_a = event('b', R.GIVEN, 'a')

print(event_a)
print(event_a_prime)
print(event_b_given_a)


class MissingEventModifierError(ValueError):
    def __init__(self):
        super().__init__(f'{event} with a relationship: {relationships_requiring_modifier} require a modifier to be meaningful.')












event_space = {
    ('a', R.GIVEN, 'b')
}