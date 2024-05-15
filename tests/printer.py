import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from smo_over_queue import Answer, Iteration, Queue
from smo_over_queue import simulate_queue

from prettytable import PrettyTable

def print_table(iterations: list[Iteration]):
    table = PrettyTable()
    
    table.field_names = ['index', 'rand_value', 'iba', 'app_time'] + [f'server_{i+1}' for i in range(len(iterations[0].server_times))]
    
    for iteration in iterations:
        row = [
            iteration.index, 
            iteration.random_value, 
            iteration.interval_between_apps, 
            iteration.application_time
        ] + ['' if t == 0 else str(t) for t in iteration.server_times]
        
        table.add_row(row)
    
    return table

def print_sq(queue: Queue):
    for i, answer in enumerate(queue.results[:3]):
        name_iter = f' Итерация номер: {i+1} '
        print(f'{name_iter :-^75}')
        print(print_table(answer.iterations))
        print()
        print(f'Количество исполненных заявок: {answer.expected_value}')
        print()
    
    print("..." * 25)
    print()
    
    print('Среднее количество исполненных заявок:', end=' ')
    
    if len(queue.results) <= 6:
        results_str = " + ".join(str(answer.expected_value) for answer in queue.results)
        print(f"{results_str} = {queue.average_value}")
    else:
        first_results = " + ".join(str(answer.expected_value) for answer in queue.results[:3])
        last_results = " + ".join(str(answer.expected_value) for answer in queue.results[-3:])
        print(f"{first_results} + ... + {last_results} = {queue.average_value}")

sq = simulate_queue(
    service_time=0.5, 
    max_time=4, 
    alpha=5,
    num_threads=3,
    num_iterations=10
)

print_sq(sq)
