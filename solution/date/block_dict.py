from dataclasses import dataclass
from typing import List

@dataclass
class BlockDict:
    type_component: str
    connection: str
    probability: bool
    components: List