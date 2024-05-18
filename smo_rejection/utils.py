import random
import math

def round_value(number: float) -> float:
    """
    Округляет заданное число до 4 знаков после запятой.

    ### Параметры:
    * `number (float)` - Число, которое нужно округлить.

    ### Возвращаемое значение:
    * `float` - Округленное число с 4 знаками после запятой.
    """
    return round(number, 4)

def generate_random_number():
    """
    Генерирует случайное число в диапазоне (0, 1] с округлением до 4 знаков после запятой.

    ### Возвращаемое значение:
    * `float` - Случайное число в диапазоне (0, 1] с 4 знаками после запятой.
    """
    while True:
        number = round_value(random.random())
        if number > 0:
            return number

def calculate_time(alfa: int, number: float) -> float:
    """
    Возвращает время между двумя последовательными заявками.

    ### Параметры:
    * `alfa (int)` - Параметр для расчета интервалов между заявками.
    * `number (float)` - Случайное число, использованное для расчета интервала.

    ### Возвращаемое значение:
    * `float` - Время между двумя последовательными заявками с 4 знаками после запятой.
    """
    return round_value(-1/alfa * math.log(number))

def calculate_mean_served_requests(results):
    """
    Вычисляет среднее количество обслуженных заявок по результатам симуляции.

    ### Параметры:
    * `results (list[SimulationResult])` - Список объектов `SimulationResult`, содержащих результаты каждой итерации симуляции.

    ### Возвращаемое значение:
    * `float` - Среднее количество обслуженных заявок с 4 знаками после запятой.
    """
    total_served_requests = [result.served_requests for result in results]
    return round_value(sum(total_served_requests) / len(total_served_requests))

def print_results(results, num_channels):
    """
    Выводит результаты симуляции в форматированном виде.

    ### Параметры:
    * `results (list[SimulationResult])` - Список объектов `SimulationResult`, содержащих результаты каждой итерации симуляции.
    * `num_channels (int)` - Количество каналов обслуживания (потоков).
    """
    import pandas as pd

    for result in results:
        print(f"\n---------------------------- Cимуляция номер: {result.iteration} ----------------------------")
        df = pd.DataFrame(result.request_times)

        # Удаление дубликатов значений серверов
        for i in range(1, len(df)):
            for j in range(num_channels):
                server_key = f'server_{j + 1}'
                if df.at[i, server_key] == df.at[i - 1, server_key] or df.at[i, server_key] == '':
                    df.at[i, server_key] = ''

        print(df[['index', 'rand_value', 'iba', 'app_time', f'server_{1}', f'server_{2}', f'server_{3}', 'Обслужено', 'Отказов']].to_string(index=False))
        print(f"\nКоличество исполненных заявок: {result.served_requests}")
        print(f"Количество отказов: {result.rejected_requests}\n")