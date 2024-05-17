from exception import InvalidInputError, NumIterationsNegative, NumIterationsIsZero, NumChannelsNegative, NumChannelsIsZero, AlphaIsZero, AlphaNegative, ServiceTimeNegative, MaxTimeNegative
from models import SimulationParameters
from processing import process_iteration

def run_simulation(T: float, num_channels: int, service_time: float, num_iterations: int, alfa : int):
    if T <= 0:
        raise MaxTimeNegative("Максимальное время симуляции должно быть положительным числом.")
    if num_channels <= 0:
        raise NumChannelsNegative("Количество каналов должно быть положительным числом.")
    if num_channels == 0:
        raise NumChannelsIsZero("Количество каналов не может быть нулевым.")
    if service_time <= 0:
        raise ServiceTimeNegative("Время обслуживания должно быть положительным числом.")
    if num_iterations < 0:
        raise NumIterationsNegative("Количество итераций не может быть отрицательным.")
    if num_iterations == 0:
        raise NumIterationsIsZero("Количество итераций не может быть нулевым.")
    if alfa < 0:
        raise AlphaNegative("Альфа не может быть отрицательной")
    if alfa == 0:
        raise AlphaIsZero("Альфа не может быть равным нулю")
    
    params = SimulationParameters(T=T, num_channels=num_channels, service_time=service_time, num_iterations=num_iterations, alfa = alfa)
    results = []

    for iteration in range(num_iterations):
        result = process_iteration(params, iteration)
        results.append(result)

    return results
