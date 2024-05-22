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
    
    def test_service_time_negative(self):
        self.assertRaises(ServiceTimeNegative, simulate_queue, -1, 2, 3, 4, 5)
        
    def test_num_threads_negative(self):
        self.assertRaises(NumThreadsNegative, simulate_queue, 1, 2, 3, -4, 5)
        
    def test_num_threads_is_zero(self):
        self.assertRaises(NumThreadsIsZero, simulate_queue, 1, 2, 3, 0, 5)
        
    def test_num_iterations_negative(self):
        self.assertRaises(NumIterationsNegative, simulate_queue, 1, 2, 3, 4, -5)
        
    def test_num_iterations_is_zero(self):
        self.assertRaises(NumIterationsIsZero, simulate_queue, 1, 2, 3, 4, 0)
        
    def test_max_time_negative(self):
        self.assertRaises(MaxTimeNegative, simulate_queue, 1, -2, 3, 4, 5)
        
    def test_alpha_is_zero(self):
        self.assertRaises(AlphaIsZero, simulate_queue, 1, 2, 0, 4, 5)
    
    def test_alpha_negative(self):
        self.assertRaises(AlphaNegative, simulate_queue, 1, 2, -3, 4, 5)

class FunctionsTest(unittest.TestCase):

    def test_round_value(self):
        self.assertAlmostEqual(round_value(123.456789, 2), 123.46, places=2)
        self.assertAlmostEqual(round_value(123.451789, 3), 123.452, places=3)
        self.assertAlmostEqual(round_value(123, 2), 123.00, places=2)

    def test_interval_between_apps(self):
        alpha = 2.0
        random_value = 0.5
        expected_interval = -1 / alpha * math.log(random_value)
        self.assertAlmostEqual(interval_between_apps(alpha, random_value), round_value(expected_interval), places=4)

    def test_max_row(self):
        lst = [1, 3, 5, 2, 4]
        self.assertEqual(max_row(lst), 5)
        
    def test_transpose(self):
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
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(max_columns(matrix), [7, 8, 9])

    def test_generate_random_number(self):
        random_number = generate_random_number()
        self.assertTrue(0 < random_number <= 1)
        self.assertAlmostEqual(round_value(random_number, 4), random_number, places=4)

    def test_sum_expected_values(self):
        answers = [
            Answer(expected_value=10, iterations=1),
            Answer(expected_value=20, iterations=1),
            Answer(expected_value=30, iterations=1)
        ]
        self.assertEqual(sum_expected_values(answers), 60)
