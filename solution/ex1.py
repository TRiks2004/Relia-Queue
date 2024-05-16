import random
from dataclasses import dataclass
from string import ascii_uppercase
from typing import List

@dataclass
class Element:
    probability: float

@dataclass
class Block:
    elements: List[Element]

    @property
    def num_elements(self) -> int:
        return len(self.elements)

    @property
    def element_probabilities(self) -> List[float]:
        return [element.probability for element in self.elements]

@dataclass
class BlockSystem:
    blocks: List[Block]

    def blocks_system(self, num_blocks: int) -> float:
        block_probabilities = []
        for block in self.blocks[:num_blocks]:
            block_probability = 1
            for p in block.element_probabilities:
                block_probability *= 1 - (1 - p)
            block_probability = 1 - block_probability
            block_probabilities.append(block_probability)

        p_system = 1
        for p in block_probabilities:
            p_system *= p

        return p_system

    def simulate_system(self, num_trials: int) -> float:
        successes = 0
        total_elements = sum(block.num_elements for block in self.blocks)
        letters = list(ascii_uppercase[:total_elements])
        table_header = f"{'Номер теста':^12}|" + "|".join(f"{'Элемент ' + letter:^12}" for letter in letters) + f"|{'Блок 1':^8}|{'Блок 2':^8}|{'Результат':^10}"
        table_rows = [table_header, "-" * len(table_header)]

        for trial in range(num_trials):
            block_results = []
            row = f"{trial + 1:^12}|"
            letter_index = 0
            for block in self.blocks:
                block_elements = [random.random() <= p for p in block.element_probabilities]
                block_success = any(block_elements)
                block_results.append(block_success)
                row += "|".join(f"{int(element):^12}" for element in block_elements)
                letter_index += block.num_elements

            trial_success = all(block_results)
            successes += int(trial_success)
            result = "Успех" if trial_success else "Неудача"
            row += f"|{int(block_results[0]):^8}|{int(block_results[1]):^8}|{result:^10}"
            table_rows.append(row)

        table_rows.append("-" * len(table_header))

        p_star = successes / num_trials
        return p_star, "\n".join(table_rows)

# Примеры значений
element1 = Element(probability=0.9)
element2 = Element(probability=0.8)
element3 = Element(probability=0.7)
block1 = Block(elements=[element1, element2, element3])

element4 = Element(probability=0.6)
element5 = Element(probability=0.5)
block2 = Block(elements=[element4, element5])

block_system = BlockSystem(blocks=[block1, block2])

p_analytical = block_system.blocks_system(num_blocks=2)

num_trials = 10
p_star, table = block_system.simulate_system(num_trials)

absolute_error = abs(p_star - p_analytical)

print(table)