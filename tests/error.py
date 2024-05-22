import sys
import os
from unittest.mock import Mock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from smo_rejection import run_simulation,round_value, calculate_time, calculate_mean_served_requests
from smo_rejection import (
    ServiceTimeNegative, 
    NumIterationsNegative, NumIterationsIsZero,
    MaxTimeNegative,
    NumChannelsIsZero, NumChannelsNegative,
    AlphaIsZero, AlphaNegative,
    MaxAlfha,MaxNumChannels,MaxNumIteration,MaxServiceTime,MaxSimulationTime
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

    def test_alpha_big(self):
        """
        Проверка вызова исключения MaxAlfha при большом значении альфа.
        """
        self.assertRaises(MaxAlfha, run_simulation, 1, 2, 3, 4, 101)

    def test_num_iteration_big(self):
        """
        Проверка вызова исключения MaxNumIteration при большом значении числа итераций.
        """
        self.assertRaises(MaxNumIteration, run_simulation, 1, 2, 3, 100100, 5)

    def test_num_channels_big(self):
        """
        Проверка вызова исключения MaxNumChannels при большом значении числа каналов.
        """
        self.assertRaises(MaxNumChannels, run_simulation, 1, 10, 3, 4, 5)

    def test_service_time_big(self):
        """
        Проверка вызова исключения MaxServiceTime при большом значении времени обслуживания.
        """
        self.assertRaises(MaxServiceTime, run_simulation, 1, 2, 1010, 4, 5)

    def test_simulation_time_big(self):
        """
        Проверка вызова исключения MaxSimulationTime при большом значении времени симуляции.
        """
        self.assertRaises(MaxSimulationTime, run_simulation, 100100, 2, 3, 4, 5)


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
        self.assertEqual(calculate_time(5, 0.9), 0.0211)
        self.assertEqual(calculate_time(10, 0.01), 0.4605)

class TestCalculateMeanServedRequests(unittest.TestCase):
    def test_single_result(self):
        """
        Тест на то, что функция возвращает правильное значение при передаче одного результата.
        """
        mock_result = Mock(served_requests=100)
        results = [mock_result]
        mean_served_requests = calculate_mean_served_requests(results)
        self.assertEqual(mean_served_requests, 100.0)

    def test_multiple_results(self):
        """
        Тест на то, что функция возвращает правильное значение при передаче нескольких результатов.
        """
        mock_result1 = Mock(served_requests=100)
        mock_result2 = Mock(served_requests=200)
        mock_result3 = Mock(served_requests=150)
        results = [mock_result1, mock_result2, mock_result3]
        mean_served_requests = calculate_mean_served_requests(results)
        self.assertEqual(mean_served_requests, 150.0)

    def test_rounding(self):
        """
        Тест на то, что функция правильно округляет результат до 4 знаков после запятой.
        """
        mock_result1 = Mock(served_requests=100.12345)
        mock_result2 = Mock(served_requests=200.67890)
        results = [mock_result1, mock_result2]
        mean_served_requests = calculate_mean_served_requests(results)
        self.assertEqual(mean_served_requests, 150.4012)


if __name__ == "__main__":
    unittest.main()
