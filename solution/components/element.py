import random
from .component import Component
from ..exceptions import ConstrainElementUp, ConstrainElementDown

from ..date.element_dict import ElementDict

class Element(Component):
    
    random_value: float
    
    def __init__(self, probability: float):
        
        if probability > 1:
            raise ConstrainElementUp
        elif probability < 0:
            raise ConstrainElementDown
        
        self.probability_analytical = probability
        
    def calculate_probability_simulated(self) -> bool:
        self.random_value = random.random()
        return self.random_value < self.probability_analytical

    def to_dict(self) -> ElementDict:
        return ElementDict(
            type_component=self.__class__.__name__,
            probability_analytical=self.probability_analytical,
            random_value=self.random_value,
            probability=self.random_value < self.probability_analytical
        )
