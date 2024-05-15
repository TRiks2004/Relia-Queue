import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from smo_over_queue import simulate_queue
from smo_over_queue.exceptions import (
    ServiceTimeNegative, 
    NumThreadsNegative, NumThreadsIsZero,
    NumIterationsNegative, NumIterationsIsZero,
    MaxTimeNegative,
    AlphaIsZero, AlphaNegative
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