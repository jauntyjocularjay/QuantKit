from enum import Enum

class Symbol(Enum):
    UNION = '∪'         # Equivalent to the || operator meaning either, or
    OR = '∨'            # Equivalent to the || operator meaning either, or
    INTERSECT = '∩'     # Equivalent to the && operator
    AND = '∧'           # Equivalent to the && operator
    GIVEN = '|'         # AKA conditional or given
    COMPLEMENT = '`'
    INDEPENDENT = '⊥'
    DEPENDENT = '⊤'
    XOR = '⊻'           # Exclusive OR, this or that but not both, mutually exclusive

OUTCOME = 'outcome'
ALL_OUTCOMES = 'all_outcomes'
DESIRED_OUTCOMES = 'desired_outcomes'
FAIR_PROBABILITY = 'fair_probability'
FAIR_COMPLEMENT = 'fair_complement'
PROBABILITY = 'probability'
COMPLEMENT = 'complement'

class EventType(Enum):
    DEPENDENT = 'dependent'
    INDEPENDENT = 'independent'
    MUTUAL_EXCLUSIVE = 'mutually_exlusive'

class Relationship(Enum):
    UNION = '∪'
    INTERSECT = '∩'
    GIVEN = '|'
    PRIME = '`'

relationships_requiring_modifier = [Relationship.UNION, Relationship.INTERSECT, Relationship.GIVEN]
