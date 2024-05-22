import unittest
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Теперь используем абсолютные импорты
from tests.error import ErrorSimulateQueueTest, FunctionsTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ErrorSimulateQueueTest))
    suite.addTest(unittest.makeSuite(FunctionsTest))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
