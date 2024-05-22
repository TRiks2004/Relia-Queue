import json
from system_reliability.components.block import Block
from system_reliability.components.element import Element

from system_reliability.enums import MethodConnection

from dataclasses import asdict

# Ввод данных пользователем
element_a = Element(probability=0)
element_b = Element(probability=0.85)
element_c = Element(probability=0)
element_d = Element(probability=0.6)
element_e = Element(probability=0.3)

block_1 = Block(element_a, connection=MethodConnection.Parallel)
block_2 = Block(element_c, connection=MethodConnection.Serial)

block_all = Block(block_1, block_2, connection=MethodConnection.Serial)

def custom_serializer(obj):
    if isinstance(obj, MethodConnection):
        return obj.value
    if hasattr(obj, '__dataclass_fields__'):
        return asdict(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

simulation_results = block_all.calculate()

print(simulation_results.analytical_results)
# print(json.dumps(simulation_results, default=custom_serializer, indent=4))