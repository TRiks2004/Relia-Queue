import math
import random
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed


@dataclass
class Iteration:
    index: int
    random_value: float
    interval_between_apps: float
    application_time: float
    server_times: list[float]

@dataclass
class Answer:
    iterations: list[Iteration]
    expected_value: float

@dataclass
class Queue:
    results: list[Answer]
    average_value: float 


class NumIterationsNegative(Exception):
    pass 

class NumIterationsIsZero(Exception):
    pass 

class NumThreadsNegative(Exception):
    pass

class NumThreadsIsZero(Exception):
    pass

class AlphaIsZero(Exception):
    pass

class AlphaNegative(Exception):
    pass

class ServiceTimeNegative(Exception):
    pass

class MaxTimeNegative(Exception):
    pass

def round_value(value, decimals=4):
    return round(value, decimals)

def interval_between_apps(alpha, random_value):
    return round_value(-1 / alpha * math.log(random_value))

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

def process_iteration(service_time, max_time, alpha, num_threads):
    iterations: list[Iteration] = []
    current_time = 0
    random_value = 0
    interval = 0
    servers = []
    server_row_count = 0
    application_count = 0

    while current_time <= max_time:
        servers.append([0] * num_threads)
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
                index=application_count,
                random_value=random_value,
                interval_between_apps=interval,
                application_time=current_time,
                server_times=servers[-1]
            )
        )

        random_value = generate_random_number()
        interval = interval_between_apps(alpha, random_value)
        current_time = round_value(current_time + interval)
        application_count += 1

    return Answer(iterations[:], application_count - 1)

def simulate_queue(service_time, max_time, alpha, num_threads=1, num_iterations=1):
    if num_iterations < 0:
        raise NumIterationsNegative
    elif num_iterations == 0:
        raise NumIterationsIsZero
    
    if num_threads < 0:
        raise NumThreadsNegative
    elif num_threads == 0:
        raise NumThreadsIsZero
    
    if alpha == 0:
        raise AlphaIsZero
    elif alpha < 0:
        raise AlphaNegative
    
    if service_time < 0:
        raise ServiceTimeNegative

    if max_time < 0:
        raise MaxTimeNegative
    
    print("Симуляция началась")
    
    answers: list[Answer] = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_iteration, service_time, max_time, alpha, num_threads) for _ in range(num_iterations)]
        
        for future in as_completed(futures):
            answers.append(future.result())
    
    return Queue(answers, round_value(sum_expected_values(answers) / len(answers)))
