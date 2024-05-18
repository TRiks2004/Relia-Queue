import random
from enum import Enum
from abc import ABC, abstractmethod

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

class Element(Component):
    
    random_value: float
    
    def __init__(self, probability: float):
        self.probability_analytical = probability
        
    
    def calculate_probability_simulated(self) -> bool:
        self.random_value = random.random()
        return self.random_value < self.probability_analytical


    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'probability_analytical': self.probability_analytical,
            'random_value': self.random_value,
            'probability': self.random_value < self.probability_analytical
        }

    
class Block(Component):
    
    def __init__(self, *components: Component, connection: MethodConnection):
       self.components = components
       self.connection = connection
       
       self.probability_analytical = self.calculate_probability_analytical()
    
    
    block_main = None
    block_step: str = None  
    simulated_step: int = None 
    simulated = {}

    
       
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
    
    def simulated_probability(self, num_trials) -> float:
        count = 0
        
        for _ in range(num_trials):            
            simulated_chek = self.calculate_probability_simulated()
            
            if simulated_chek:
                count += 1
                
            self.simulated[_] = self.to_dict()
            
        
        return {
            'count': count,
            'num_trials': num_trials,
            'probability': count / num_trials,
            'ditails': self.simulated
        }
            
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
    
    
    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'connection': self.connection.value,
            'probability': self.probability_simulated,
            'components': [component.to_dict() for component in self.components],
        }
    
import json

# Ввод данных пользователем
element_1 = Element(probability=0.8)
element_2 = Element(probability=0.85)
element_3 = Element(probability=0.6)
element_4 = Element(probability=0.6)
element_5 = Element(probability=0.3)

block_1 = Block(element_1, element_2, connection=MethodConnection.Parallel)

# print(f'----- block_1 -----')
# print(f'{block_1.probability = }')

block_2 = Block(element_3, element_4, connection=MethodConnection.Parallel)

# print(f'\n----- block_2 -----')
# print(f'{block_2.probability = }')

block_all = Block(block_1, element_5,  block_2, connection=MethodConnection.Serial)

print(f'\n----- block_all -----')
# print(f'{block_all.probability = }')

def custom_serializer(obj):
    if isinstance(obj, MethodConnection):
        return obj.value
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

all_ = block_all.simulated_probability(1)
print(json.dumps(all_, default=custom_serializer, indent=4))
 







