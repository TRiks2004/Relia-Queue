import sys
import math
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smo_over_queue.models import Answer
import unittest
from smo_over_queue import simulate_queue
from smo_over_queue.exceptions import (
    ServiceTimeNegative, 
    NumThreadsNegative, NumThreadsIsZero,
    NumIterationsNegative, NumIterationsIsZero,
    MaxTimeNegative,
    AlphaIsZero, AlphaNegative
)
from smo_over_queue.utils import (
    round_value,
    interval_between_apps,
    max_row,
    transpose,
    max_columns,
    generate_random_number,
    sum_expected_values
)


class ErrorSimulateQueueTest(unittest.TestCase):
    """
    Тесты для исключений, возникающих при некорректных входных данных в функции simulate_queue.
    """

    def test_service_time_negative(self):
        """Проверка, что возникает исключение ServiceTimeNegative при отрицательном времени обслуживания."""
        self.assertRaises(ServiceTimeNegative, simulate_queue, -1, 2, 3, 4, 5)
        
    def test_num_threads_negative(self):
        """Проверка, что возникает исключение NumThreadsNegative при отрицательном количестве потоков."""
        self.assertRaises(NumThreadsNegative, simulate_queue, 1, 2, 3, -4, 5)
        
    def test_num_threads_is_zero(self):
        """Проверка, что возникает исключение NumThreadsIsZero при количестве потоков, равном нулю."""
        self.assertRaises(NumThreadsIsZero, simulate_queue, 1, 2, 3, 0, 5)
        
    def test_num_iterations_negative(self):
        """Проверка, что возникает исключение NumIterationsNegative при отрицательном количестве итераций."""
        self.assertRaises(NumIterationsNegative, simulate_queue, 1, 2, 3, 4, -5)
        
    def test_num_iterations_is_zero(self):
        """Проверка, что возникает исключение NumIterationsIsZero при количестве итераций, равном нулю."""
        self.assertRaises(NumIterationsIsZero, simulate_queue, 1, 2, 3, 4, 0)
        
    def test_max_time_negative(self):
        """Проверка, что возникает исключение MaxTimeNegative при отрицательном максимальном времени."""
        self.assertRaises(MaxTimeNegative, simulate_queue, 1,    -2, 3, 4, 5)
        
    def test_alpha_is_zero(self):
        """Проверка, что возникает исключение AlphaIsZero при значении alpha, равном нулю."""
        self.assertRaises(AlphaIsZero, simulate_queue, 1, 2, 0, 4, 5)
    
    def test_alpha_negative(self):
        """Проверка, что возникает исключение AlphaNegative при отрицательном значении alpha."""
        self.assertRaises(AlphaNegative, simulate_queue, 1, 2, -3, 4, 5)


class FunctionsTest(unittest.TestCase):
    """
    Тесты для утилитарных функций, используемых в проекте.
    """

    def test_round_value(self):
        """
        Проверка функции round_value.
        Ожидается, что значения будут округлены до указанного количества десятичных знаков.
        """
        self.assertAlmostEqual(round_value(123.456789, 2), 123.46, places=2)
        self.assertAlmostEqual(round_value(123.451789, 3), 123.452, places=3)
        self.assertAlmostEqual(round_value(123, 2), 123.00, places=2)

    def test_interval_between_apps(self):
        """
        Проверка функции interval_between_apps.
        Ожидается, что интервал между заявками будет рассчитан корректно на основе alpha и случайного значения.
        """
        alpha = 2.0
        random_value = 0.5
        expected_interval = -1 / alpha * math.log(random_value)
        self.assertAlmostEqual(interval_between_apps(alpha, random_value), round_value(expected_interval), places=4)

    def test_max_row(self):
        """
        Проверка функции max_row.
        Ожидается, что будет возвращено максимальное значение из списка.
        """
        lst = [1, 3, 5, 2, 4]
        self.assertEqual(max_row(lst), 5)
        
    def test_transpose(self):
        """
        Проверка функции transpose.
        Ожидается, что матрица будет транспонирована (строки заменены на столбцы).
        """
        matrix = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        expected_transposed = [
            [1, 4],
            [2, 5],
            [3, 6]
        ]
        self.assertEqual(transpose(matrix), expected_transposed)

    def test_max_columns(self):
        """
        Проверка функции max_columns.
        Ожидается, что будут возвращены максимальные значения для каждого столбца матрицы.
        """
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(max_columns(matrix), [7, 8, 9])

    def test_generate_random_number(self):
        """
        Проверка функции generate_random_number.
        Ожидается, что будет сгенерировано случайное число в диапазоне (0, 1] с округлением до 4 знаков.
        """
        random_number = generate_random_number()
        self.assertTrue(0 < random_number <= 1)
        self.assertAlmostEqual(round_value(random_number, 4), random_number, places=4)

    def test_sum_expected_values(self):
        """
        Проверка функции sum_expected_values.
        Ожидается, что будет корректно рассчитана сумма ожидаемых значений из списка объектов Answer.
        """
        answers = [
            Answer(expected_value=10, iterations=1),
            Answer(expected_value=20, iterations=1),
            Answer(expected_value=30, iterations=1)
        ]
        self.assertEqual(sum_expected_values(answers), 60)
