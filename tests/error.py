import sys
import os

# Добавляем в системный путь директорию на один уровень выше текущего файла
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from smo_rejection import run_simulation,round_value, calculate_time
from smo_rejection import (
    ServiceTimeNegative, 
    NumIterationsNegative, NumIterationsIsZero,
    MaxTimeNegative,
    NumChannelsIsZero, NumChannelsNegative,
    AlphaIsZero, AlphaNegative
)

class ErrorInputParametres(unittest.TestCase):
    """
    Тестовый класс для проверки функции run_simulation на корректную обработку ошибок.
    """
    
    def test_service_time_negative(self):
        """
        Проверка вызова исключения ServiceTimeNegative при отрицательном времени обслуживания.
        """
        self.assertRaises(ServiceTimeNegative, run_simulation, 1, 2, -3, 4, 5)
                
    def test_num_iterations_negative(self):
        """
        Проверка вызова исключения NumIterationsNegative при отрицательном количестве итераций.
        """
        self.assertRaises(NumIterationsNegative, run_simulation, 1, 2, 3, -4, 5)
        
    def test_num_iterations_is_zero(self):
        """
        Проверка вызова исключения NumIterationsIsZero при нулевом количестве итераций.
        """
        self.assertRaises(NumIterationsIsZero, run_simulation, 1, 2, 3, 0, 5)

    def test_num_channels_negative(self):
        """
        Проверка вызова исключения NumChannelsNegative при отрицательном количестве каналов.
        """
        self.assertRaises(NumChannelsNegative, run_simulation, 1, -2, 3, 4, 5)
        
    def test_num_channels_is_zero(self):
        """
        Проверка вызова исключения NumChannelsIsZero при нулевом количестве каналов.
        """
        self.assertRaises(NumChannelsIsZero, run_simulation, 1, 0, 3, 4, 5)
        
    def test_max_time_negative(self):
        """
        Проверка вызова исключения MaxTimeNegative при отрицательном максимальном времени.
        """
        self.assertRaises(MaxTimeNegative, run_simulation, -1, 2, 3, 4, 5)
        
    def test_alpha_is_zero(self):
        """
        Проверка вызова исключения AlphaIsZero при нулевом значении альфа.
        """
        self.assertRaises(AlphaIsZero, run_simulation, 1, 2, 3, 4, 0)
    
    def test_alpha_negative(self):
        """
        Проверка вызова исключения AlphaNegative при отрицательном значении альфа.
        """
        self.assertRaises(AlphaNegative, run_simulation, 1, 2, 3, 4, -5)

class TestUtilityFunctions(unittest.TestCase):

    def test_round_value(self):
        """
        Тестирует функцию round_value на корректность округления до 4 знаков после запятой.
        """
        self.assertEqual(round_value(3.14159265), 3.1416)
        self.assertEqual(round_value(2.718281828), 2.7183)
        self.assertEqual(round_value(1.23456789), 1.2346)
        self.assertEqual(round_value(0.99999999), 1.0000)
        self.assertEqual(round_value(0.00000001), 0.0000)

    def test_calculate_time(self):
        """
        Тестирует функцию calculate_time на корректность вычисления времени между двумя последовательными заявками.
        """
        self.assertEqual(calculate_time(2, 0.5), 0.3466)
        self.assertEqual(calculate_time(1, 0.1), 2.3026)
        self.assertEqual(calculate_time(5, 0.9), 0.0210)
        self.assertEqual(calculate_time(10, 0.01), 0.4605)

if __name__ == "__main__":
    unittest.main()
