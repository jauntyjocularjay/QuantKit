from enum import Enum




UNION_SYM = '∪'         # Equivalent to the || operator
LOR_SYM = '∨'           # Equivalent to the || operator
INTERSECTION_SYM = '∩'  # Equivalent to the && operator
LAND_SYM = '∧'          # Equivalent to the && operator
GIVEN_SYM = '|'
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