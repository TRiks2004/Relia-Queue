from concurrent.futures import ProcessPoolExecutor, as_completed
from models import Queue, Answer
from exceptions import *
from utils import round_value, sum_expected_values
from simulation import process_iteration

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
