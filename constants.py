from enum import Enum

class Symbol(Enum):
    UNION = '∪'         # Equivalent to the || operator
    OR = '∨'            # Equivalent to the || operator
    INTERSECT = '∩'     # Equivalent to the && operator
    AND = '∧'           # Equivalent to the && operator
    GIVEN = '|'         # AKA conditional or given

OUTCOME = 'outcome'
ALL_OUTCOMES = 'all_outcomes'
DESIRED_OUTCOMES = 'desired_outcomes'
FAIR_PROBABILITY = 'fair_probability'
FAIR_COMPLEMENT = 'fair_complement'
PROBABILITY = 'probability'
COMPLEMENT = 'complement'

class Event(Enum):
    DEPENDENT = 'dependent'
    INDEPENDENT = 'independent'
    MUTUAL_EXCLUSIVE = 'mutually_exlusive'