import random

def round_value(number):
    """
    Округляет заданное число до 4 знаков после запятой.

    ### Параметры:
    - `number` (float): Число для округления.

    ### Возвращает:
    `float`: Число, округленное до 4 знаков после запятой.
    """
    return round(number, 4)


def generate_random_number():
    """
    Генерирует случайное число в диапазоне (0, 1] с округлением до 4 знаков после запятой.
    Если сгенерировано 0, повторяет генерацию.

    ### Возвращает:
    `float`: Случайное число в диапазоне (0, 1].
    """
    number = round_value(random.uniform(0, 1))
    if number == 0:
        return generate_random_number()
    else:
        return number