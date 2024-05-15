import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .error import ErrorSimulateQueueTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ErrorSimulateQueueTest))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())