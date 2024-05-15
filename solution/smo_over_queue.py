import math
import random

from dataclasses import dataclass

@dataclass
class Iter:
    item: int
    random_count: float
    time_between_applications: float
    applications_time: float
    server: list[float]

@dataclass
class Answer:
    iters: list[Iter]
    mathematical_expectations: float

@dataclass
class Queue:
    answers: list[Answer]
    average: float 

    
def time_between_applications(alpha, random_count):
    return round(-1 / alpha * math.log(random_count), 4)
    
def max_item_row(lst):
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

def max_item_columns(lst):
    return [max_item_row(row) for row in transpose(lst)]
        
        
def random_number_generator():
    
    if (number := round(random.uniform(0, 1), 4)) == 0:
        return random_number_generator()
    else:
        return number

def sum_answer(lst):
    return sum([i.mathematical_expectations for i in lst])


def simulate_queue(t1, t2, alpha, threads=1, iterations=1):
    
    answer_list: list[Answer] = []
    
    for _ in range(iterations):
        print(f"iteration {_}")
        iter_list: list[Iter] = []
        time = 0
        random_count = 0
        tba = 0
        
        servers = []
        servers_count_row = 0
        
        c = 0 
        while time <= t2:
            
            servers.append([])
            
            for _ in range(threads):
                servers[-1].append(0)
            
            
            column_max = max_item_columns(servers)
            
            for i, j in enumerate(column_max):
                if time >= j:
                    servers[servers_count_row][i] = round(time + t1, 4)
                    break
            else:
                if i + 1 < len(servers[servers_count_row]):
                    servers[servers_count_row][i + 1] = round(time + t1, 4)
                else:
                    column_max_min = min(column_max)
                    time = column_max_min
                    
                    servers[servers_count_row][column_max.index(column_max_min)] = round(time + t1, 4)
                    
            servers_count_row += 1
            
            iter_list.append(
                Iter(
                    item=c, 
                    random_count=random_count, 
                    time_between_applications=tba, 
                    applications_time=time, 
                    server=servers[-1]
                )
            )
            
        
            random_count = random_number_generator()
            tba = time_between_applications(alpha, random_count)
            time = round(time + tba, 4)
            
            c += 1
        
        answer_list.append(Answer(iter_list[:], c - 1))
    
    
    return Queue(answer_list, round(sum_answer(answer_list) / len(answer_list), 4))
    
queue = simulate_queue(1, 10, 5, 2, 100)