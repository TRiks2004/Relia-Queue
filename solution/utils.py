import random
import math

def round_value(number : float) -> float:
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
    
def calculate_ln(number: float) -> float:
    """
    Возвращает результат натурального логарифма от случайного числа r_i с округлением до 4 знаков после запятой.
    
    ### Параметры:
    - `number` (float): Случайное число r_i 

    ### Возвращает:
    `float`: Число логарифмирования от случайно числа r_i 
    """
    return round_value(-math.log(number))

def calculate_time(alfa: int,number: float) -> float:
    """
    Возвращает время между двумя последовательными заявками.

    ##Параметры:
    - `alfa` (int): Число, задаваемое пользователем
    - `number` (float): Число, вычисляемое в функции calculate_ln

    ## Возвращает:
    `float` : Число подсчета времени
    """
    return (-1 / alfa) * number