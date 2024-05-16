import random
from enum import Enum
from abc import ABC, abstractmethod

class MethodConnection(Enum):
    Parallel = 'parallel'
    Serial = 'serial'

class Component(ABC):
    probability: float

    @abstractmethod
    def calculate_probability_simulated(self) -> bool:
        pass

    @abstractmethod
    def component_to_string_parallel(self) -> str:
        pass
    
    @abstractmethod
    def component_to_string_serial(self) -> str:
        pass

class Element(Component):
    
    def __init__(self, probability: float):
        self.probability = probability
        self.calculate_probability_simulated = lambda: random.random() < probability

    def component_to_string_parallel(self) -> str:
        return f'1 - {self.probability}'

    def component_to_string_serial(self) -> str:
        return f'{self.probability}'
    
class Block(Component):
    
    def __init__(self, *components: Component, connection: MethodConnection):
       self.components = components
       self.connection = connection
       
       self.probability = self.calculate_probability_analytical()
       
    def calculate_probability_by_method_analytical(self, probability):
        match self.connection:
            case MethodConnection.Parallel:
                return 1 - probability
            case MethodConnection.Serial:
                return probability
    
    def calculate_probability_analytical(self):
        probability = 1
        for component in self.components:
            probability *= self.calculate_probability_by_method_analytical(component.probability)
        
        return self.calculate_probability_by_method_analytical(probability)
    
    def simulated_probability(self, num_trials) -> float:
        count = 0
        
        for _ in range(num_trials):    
            simulated = self.calculate_probability_simulated()
            if simulated:
                count += 1

        return count / num_trials
            
    def calculate_probability_by_method_simulated(self, prob_one, prob_two):
        match self.connection:
            case MethodConnection.Parallel:
                return prob_one or prob_two
            case MethodConnection.Serial:
                return prob_one and prob_two
    
    def calculate_probability_simulated(self):
        probability = self.components[0].calculate_probability_simulated()
        for component in self.components[1:]:
            probability = self.calculate_probability_by_method_simulated(probability, component.calculate_probability_simulated())
        
        return probability
    
    def component_to_string_connection(self, component: Component) -> str:
        match self.connection:
            case MethodConnection.Parallel:
                return component.component_to_string_parallel()
            case MethodConnection.Serial:
                return component.component_to_string_serial()
    
    def component_to_string_parallel(self) -> str:
        return f"1 - {" * ".join(self.component_to_string_connection(component) for component in self.components)}" 

    def component_to_string_serial(self) -> str:
        return f"{" * ".join(self.component_to_string_connection(component) for component in self.components)}"

# Ввод данных пользователем
element_1 = Element(probability=0.8)
element_2 = Element(probability=0.85)
element_3 = Element(probability=0.6)

block_1 = Block(element_1, element_2, connection=MethodConnection.Parallel)

print(f'----- block_1 -----')
print(f'{block_1.probability = }')
print(f'{block_1.simulated_probability(100) = }')

block_2 = Block(element_3, connection=MethodConnection.Parallel)

print(f'\n----- block_2 -----')
print(f'{block_2.probability = }')
print(f'{block_2.simulated_probability(100) = }')

block_all = Block(block_1, block_2, connection=MethodConnection.Serial)

print(f'\n----- block_all -----')
print(f'{block_all.probability = }')
print(f'{block_all.simulated_probability(100) = }')
