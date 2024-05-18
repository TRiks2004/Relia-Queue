import numpy as np
import random
import math

def round_value(number: float) -> float:
    """Округляет заданное число до 4 знаков после запятой."""
    return round(number, 4)

def generate_random_number():
    """Генерирует случайное число в диапазоне (0, 1] с округлением до 4 знаков после запятой."""
    while True:
        number = round_value(np.random.rand())
        if number > 0:
            return number

def calculate_time(alfa: int, number: float) -> float:
    """Возвращает время между двумя последовательными заявками."""
    return round_value((-1/alfa) * np.log(number))

def calculate_mean_served_requests(results):
    total_served_requests = [result.served_requests for result in results]
    return np.mean(total_served_requests)

def print_results(results, num_channels):
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