import random
from dataclasses import dataclass
from string import ascii_uppercase
from typing import List, Literal

from enum import Enum

## Вариант 1. Система состоит из двух блоков, соединенных последовательно. 
#  Система отказывает при отказе хотя бы одного блока. Первый блок содержит три элемента: А, В, С, а второй – два элемента: D, E. 
#  Элементы каждого блока соединены параллельно. Блок отказывает при одновременном отказе всех элементов, входящих в него. 
#  Вероятности безотказной работы элементов Р(А), Р(В), Р(С), Р(D), P(E) вводит пользователь.

class Element:
    def __init__(self, probability: float):
        self.probability = probability


class MethodConnection(Enum):
    Sequentially = 'sequentially'
    Parallelly = 'parallelly'


class Block():

    def __init__(self, *elements: Element, connections: MethodConnection = MethodConnection.Parallelly):
        self.elements = elements
        self.connections = connections
    
    def probability_trouble_free_parallelly(self):
        
        probability = 1
        for element in self.elements:
           
            probability *= 1 - element.probability
            
        
        return probability
    
    def probability_trouble_free_sequentially(self):
        
        probability = 1
        for element in self.elements:
            print(f'{element.probability = }')
            probability *= element.probability
            print(f'{probability = }')
        
        return probability
    
    def probability_trouble_free(self):
        match self.connections:
            case MethodConnection.Parallelly:
                return self.probability_trouble_free_parallelly()
            case MethodConnection.Sequentially:
                return self.probability_trouble_free_sequentially()

class BlockSystem():
    
    # (1−P(A))⋅(1−P(B))⋅(1−P(C))
    
    def __init__(self, *blocks: Block, connections: MethodConnection = MethodConnection.Sequentially):
        self.blocks = blocks
        self.connections = connections
    
    def probability_trouble_free_parallelly(self):
        
        probability = 1
        for block in self.blocks:
            probability *= 1 - block.probability_trouble_free()
        
        return probability
    
    def probability_trouble_free_sequentially(self):
        
        probability = 1
        for block in self.blocks:
            print(f'\t{block.probability_trouble_free() = }')
            probability *= block.probability_trouble_free()
            print(f'\t{probability = }')
        
        return probability
    
    
    def probability_trouble_free(self):
        match self.connections:
            case MethodConnection.Sequentially:
                return self.probability_trouble_free_parallelly()
            case MethodConnection.Parallelly:
                return self.probability_trouble_free_sequentially()
        

# Примеры значений
element1 = Element(probability=0.9)
element2 = Element(probability=0.85)
element3 = Element(probability=0.95)
block1 = Block(element1, element2, element3, connections=MethodConnection.Sequentially)

element4 = Element(probability=0.8)
element5 = Element(probability=0.75)
block2 = Block(element4, element5, connections=MethodConnection.Sequentially)

block_system = BlockSystem(block1, block2, connections=MethodConnection.Sequentially)

p_analytical = block_system.probability_trouble_free()

print(p_analytical)


# num_trials = 10
# p_star, table = block_system.simulate_system(num_trials)

# absolute_error = abs(p_star - p_analytical)

# print(table)