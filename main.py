import math
import random

from dataclasses import dataclass

@dataclass
class Iter:
    item: int
    random_count: float
    
    time_between_applications: float
    
    applications_time: float
    
    server: list
    


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
    return round(random.uniform(0, 1), 4)



def simulate_queue(t1, t2, alpha, threads=1):
    
    random.seed(100)
    
    iter_list: list[Iter] = []
    
    time = 0
    random_count = 0
    tba = 0
    
    servers = []  # Четыре канала обслуживания
    servers_count_row = 0
    
    c = 0 
    
    while time <= t2:
         
        servers.append([])
        
        for _ in range(threads):
            servers[-1].append(0)
        
        
        column_max = max_item_columns(servers)
        # print(column_max)
        
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
        
        iter_list.append(Iter(
            item=c, 
            random_count=random_count, 
            time_between_applications=tba, 
            applications_time=time, 
            server=servers[-1]
        ))
        
    
        random_count = random_number_generator()
        tba = time_between_applications(alpha, random_count)
        time = round(time + tba, 4)
        
        c += 1
    
    
    
    # table = PrettyTable()

    # # Определяем основные столбцы
    # main_columns = ['item', 'random_count', 'time_between_applications', 'applications_time']
    # for col in main_columns:
    #     table.add_column(col, [getattr(obj, col) for obj in iter_list])

    # # Определяем максимальную длину списка server
    # max_server_length = max(len(obj.server) for obj in iter_list)

    # # Добавляем столбцы для элементов server
    # for i in range(max_server_length):
    #     table.add_column(f'server_{i+1}', [obj.server[i] if i < len(obj.server) else None for obj in iter_list])

    # # Выводим таблицу
    # print(table)
    
            
    # print(*iter_list, sep='\n')