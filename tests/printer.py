import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from smo_rejection import run_simulation

from prettytable import PrettyTable

def print_simulation_results(results, T, num_channels, service_time, num_iterations, alfa):
    """
    Выводит результаты симуляции обслуживания заявок.

    Параметры:
    results (list[SimulationResult]): Список объектов `SimulationResult`, содержащих результаты каждой итерации симуляции.
    T (float): Общее время симуляции.
    num_channels (int): Количество каналов обслуживания (потоков).
    service_time (float): Время обслуживания одной заявки.
    num_iterations (int): Количество итераций симуляции.
    alfa (int): Параметр для расчета интервалов между заявками.
    """
    for i, result in enumerate(results[:3], start=1):
        print(f' Итерация номер: {i} '.center(75, '-'))

        table = PrettyTable()
        table.field_names = ['№', 'Случайное число', 'Интервал', 'Время заявки', 'Обслужено', 'Отказов'] + [f'Канал {j + 1}' for j in range(num_channels)]

        for j, entry in enumerate(result.request_times, start=1):
            row = [
                j,
                entry['rand_value'],
                entry['iba'],
                entry['app_time'],
                entry['Обслужено'],
                entry['Отказов']
            ]
            for k in range(num_channels):
                key = f'server_{k + 1}'
                row.append(entry.get(key, ''))

            table.add_row(row)

        print(table)
        print(f'Количество исполненных заявок: {result.served_requests}')
        print()

    if len(results) > 6:
        print('...' * 25)

    print('Среднее количество исполненных заявок:', end=' ')

    total_served_requests = sum(result.served_requests for result in results)
    average_served_requests = total_served_requests / len(results)

    if len(results) <= 6:
        served_requests_str = ' + '.join(str(result.served_requests) for result in results)
        print(f"{served_requests_str} = {average_served_requests:.4f}")
    else:
        first_results = ' + '.join(str(result.served_requests) for result in results[:3])
        last_results = ' + '.join(str(result.served_requests) for result in results[-3:])
        print(f"{first_results} + ... + {last_results} = {average_served_requests:.4f}")

results = run_simulation(T=4, num_channels=3, service_time=0.5, num_iterations=10, alfa=5)
print_simulation_results(results, T=4, num_channels=3, service_time=0.5, num_iterations=10, alfa=5)