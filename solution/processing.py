import numpy as np
from models import SimulationParameters, SimulationResult
from utils import generate_random_number, calculate_time

def process_iteration(params: SimulationParameters, iteration: int) -> SimulationResult:
    T = params.T
    num_channels = params.num_channels
    service_time = params.service_time
    alfa = params.alfa

    request_times = []
    service_end_times = np.zeros(num_channels)
    served_requests = 0
    rejected_requests = 0
    request_time = 0

    while request_time < T:
        rand_value = generate_random_number()
        inter_arrival_time = calculate_time(alfa, rand_value)
        request_time += inter_arrival_time

        if request_time > T:
            break

        available_server = np.argmin(service_end_times)
        if service_end_times[available_server] <= request_time:
            service_end_times[available_server] = request_time + service_time
            served_requests += 1
            serviced = 1
            rejected = 0
        else:
            rejected_requests += 1
            serviced = 0
            rejected = 1

        entry = {
            'index': len(request_times) + 1,
            'rand_value': round(rand_value, 4),
            'iba': round(inter_arrival_time, 4),
            'app_time': round(request_time, 4),
            'Обслужено': serviced,
            'Отказов': rejected,
        }

        for i in range(num_channels):
            key = f'server_{i + 1}'
            if serviced == 1 and available_server == i:
                entry[key] = round(service_end_times[i], 4)
            else:
                entry[key] = ''

        request_times.append(entry)

    return SimulationResult(iteration=iteration + 1, served_requests=served_requests, rejected_requests=rejected_requests, request_times=request_times)