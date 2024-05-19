import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smo_rejection import run_simulation, calculate_mean_served_requests


def print_results(results, num_channels):
    """
    Выводит результаты симуляции в форматированном виде.

    ### Параметры:
    * `results (list[SimulationResult])` - Список объектов `SimulationResult`, содержащих результаты каждой итерации симуляции.
    * `num_channels (int)` - Количество каналов обслуживания (потоков).
    """
    import pandas as pd

    for result in results:
        print(f"\n------------------------------- Cимуляция номер: {result.iteration} -------------------------------")
        df = pd.DataFrame(result.request_times)
        print(df[['index', 'rand_value', 'iba', 'app_time', f'server_{1}', f'server_{2}', f'server_{3}', 'Обслужено', 'Отказов']].to_string(index=False))
        print(f"\nКоличество исполненных заявок: {result.served_requests}")
        print(f"Количество отказов: {result.rejected_requests}\n")

def main():
    T = 4
    num_channels = 3
    service_time = 0.5
    num_iterations = 2
    alfa = 5

    try:
        # Запуск симуляции с заданными параметрами
        results = run_simulation(T, num_channels, service_time, num_iterations, alfa)
        
        # Печать результатов симуляции
        print_results(results, num_channels)
        
        # Расчет и печать среднего числа обслуженных заявок
        a = calculate_mean_served_requests(results)
        print("\nВ качестве оценки искомого математического ожидания a – числа обслуженных заявок примем выборочную среднюю:")
        print(f"a = {a}")
    except Exception as e:
        # Обработка исключений
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
