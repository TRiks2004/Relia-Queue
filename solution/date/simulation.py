from dataclasses import dataclass
from typing import List
from ..date.element_dict import ElementDict
from ..date.block_dict import BlockDict

@dataclass
class SimulationResult:
    success_count: int
    num_trials: int
    probability: float
    details: List[ElementDict | BlockDict]
