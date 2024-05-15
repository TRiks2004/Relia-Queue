import math
import random
from dataclasses import dataclass

@dataclass
class Iteration:
    index: int
    rand_value: float
    interval_between_apps: float
    app_time: float
    server_times: list[float]

@dataclass
class Answer:
    iterations: list[Iteration]
    expected_value: float

@dataclass
class Queue:
    results: list[Answer]
    average_value: float 

def round_value(value, decimals=4):
    return round(value, decimals)

def interval_between_apps(alpha, rand_value):
    return round_value(-1 / alpha * math.log(rand_value))

def max_row(lst):
    return max(lst)

def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed_matrix = []

    for col in range(cols):
        new_row = []
        for row in range(rows):
            new_row.append(matrix[row][col])
        transposed_matrix.append(new_row)

    return transposed_matrix

def max_columns(lst):
    return [max_row(row) for row in transpose(lst)]

def generate_random_number():
    number = round_value(random.uniform(0, 1))
    if number == 0:
        return generate_random_number()
    else:
        return number

def sum_expected_values(lst):
    return sum([answer.expected_value for answer in lst])

def simulate_queue(service_time, max_time, alpha, num_threads=1, num_iterations=1):
    answers: list[Answer] = []
    
    for iteration in range(num_iterations):
        iterations: list[Iteration] = []
        current_time = 0
        rand_value = 0
        interval = 0
        servers = []
        server_row_count = 0
        app_count = 0
        
        while current_time <= max_time:
            servers.append([])
            
            for _ in range(num_threads):
                servers[-1].append(0)
            
            column_max_values = max_columns(servers)
            
            for index, value in enumerate(column_max_values):
                if current_time >= value:
                    servers[server_row_count][index] = round_value(current_time + service_time)
                    break
            else:
                if index + 1 < len(servers[server_row_count]):
                    servers[server_row_count][index + 1] = round_value(current_time + service_time)
                else:
                    min_column_max = min(column_max_values)
                    current_time = min_column_max
                    servers[server_row_count][column_max_values.index(min_column_max)] = round_value(current_time + service_time)
                    
            server_row_count += 1
            
            iterations.append(
                Iteration(
                    index=app_count, 
                    rand_value=rand_value, 
                    interval_between_apps=interval, 
                    app_time=current_time, 
                    server_times=servers[-1]
                )
            )
            
            rand_value = generate_random_number()
            interval = interval_between_apps(alpha, rand_value)
            current_time = round_value(current_time + interval)
            app_count += 1
        
        answers.append(Answer(iterations[:], app_count - 1))
    
    return Queue(answers, round_value(sum_expected_values(answers) / len(answers)))

# Пример использования
queue = simulate_queue(
    service_time=0.5, 
    max_time=10, 
    alpha=5,
    num_threads=3,
    num_iterations=7
)
