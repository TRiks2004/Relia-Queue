from dataclasses import dataclass

@dataclass
class ElementDict:
    type_component: str
    probability_analytical: float
    random_value: float
    probability: bool