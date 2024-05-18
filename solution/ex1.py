import random
from enum import Enum
from abc import ABC, abstractmethod
from typing import TypedDict


class MethodConnection(Enum):
    Parallel = 'parallel'
    Serial = 'serial'

class Component(ABC):
    probability_analytical: float

    @abstractmethod
    def calculate_probability_simulated(self) -> bool:
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass



class ElementDict(TypedDict):
    type_component: str
    probability_analytical: float
    random_value: float
    probability: float


class BlockDict(TypedDict):
    type_component: str
    connection: str
    probability: bool
    components: list[ElementDict]

class SimulationResult(TypedDict):
    success_count: int
    num_trials: int
    probability: float
    details: list[BlockDict | ElementDict]


class Element(Component):
    
    random_value: float
    
    def __init__(self, probability: float):
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

class Block(Component):
    
    def __init__(self, *components: Component, connection: MethodConnection):
        self.components = components
        self.connection = connection
        self.probability_analytical = self.calculate_probability_analytical()
    
    block_main = None
    block_step: str = None  
    simulated_step: int = None 
    simulated_results = []
       
    def calculate_probability_by_method_analytical(self, probability):
        match self.connection:
            case MethodConnection.Parallel:
                return 1 - probability
            case MethodConnection.Serial:
                return probability
    
    def calculate_probability_analytical(self):
        probability = 1
        for component in self.components:
            probability *= self.calculate_probability_by_method_analytical(component.probability_analytical)
        
        return self.calculate_probability_by_method_analytical(probability)
    
    def simulated_probability(self, num_trials) -> SimulationResult:
        success_count = 0
        
        for trial in range(num_trials):            
            is_successful = self.calculate_probability_simulated()
            
            if is_successful:
                success_count += 1
                
            self.simulated_results.append(self.to_dict())
            
        return SimulationResult(
            success_count=success_count,
            num_trials=num_trials,
            probability=success_count / num_trials,
            details=self.simulated_results
        )
            
    def calculate_probability_by_method_simulated(self, prob_one: bool, prob_two: bool) -> bool:
        match self.connection:
            case MethodConnection.Parallel:
                return prob_one or prob_two
            case MethodConnection.Serial:
                return prob_one and prob_two
    
    def calculate_probability_simulated(self) -> bool:    
        probability = 1 if self.connection == MethodConnection.Serial else 0 
        
        for component in self.components:
            probability = self.calculate_probability_by_method_simulated(probability, component.calculate_probability_simulated())
        
        self.probability_simulated = probability
        
        return probability
    
    def to_dict(self) -> BlockDict:
        return BlockDict(
            type_component=self.__class__.__name__,
            connection=self.connection.value,
            probability=self.probability_simulated,
            components=[component.to_dict() for component in self.components],
        )
    
import json

# Ввод данных пользователем
element_a = Element(probability=0.8)
element_b = Element(probability=0.85)
element_c = Element(probability=0.6)
element_d = Element(probability=0.6)
element_e = Element(probability=0.3)

block_1 = Block(element_a, element_b, connection=MethodConnection.Parallel)

block_2 = Block(element_c, element_d, connection=MethodConnection.Parallel)

block_all = Block(block_1, block_2, connection=MethodConnection.Serial)

def custom_serializer(obj):
    if isinstance(obj, MethodConnection):
        return obj.value
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

simulation_results = block_all.simulated_probability(2)
print(json.dumps(simulation_results, default=custom_serializer, indent=4))

print(simulation_results['details'][0]['components'][0]['type_component'])