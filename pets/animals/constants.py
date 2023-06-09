from enum import Enum
from typing import List, Tuple


class Species(Enum):
    Cat = "cat"
    Dog = "dog"
    Bunny = "bunny"

    @classmethod
    def as_list(cls) -> List[str]:
        return [e.value for e in Species]

    @classmethod
    def as_tuples(cls) -> List[Tuple[str, str]]:
        return [(e.value, e.name) for e in Species]


ALLOWED_SPECIES = [Species.Cat.value, Species.Dog.value]
