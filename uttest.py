import unittest
from unittest.mock import patch
from system_reliability.components.block import Block
from system_reliability.components.element import Element
from system_reliability.enums import MethodConnection
from system_reliability.exceptions import ConstrainElementUp, ConstrainElementDown

class TestBlock(unittest.TestCase):
    """
    Класс для тестирования функциональности класса Block.
    """

    def setUp(self):
        """
        Настройка экземпляров Element для использования в тестах.
        """
        self.element1 = Element(0.8)
        self.element2 = Element(0.6)

    def test_calculate_probability_analytical(self):
        """
        Тестирование метода calculate_probability_analytical класса Block.
        Проверяет корректность расчета вероятности при параллельном и последовательном соединениях.
        """
        # Проверка параллельного соединения
        block = Block(self.element1, self.element2, connection=MethodConnection.Parallel)
        self.assertEqual(block.probability_analytical, 0.92)

        # Проверка последовательного соединения
        block = Block(self.element1, self.element2, connection=MethodConnection.Serial)
        self.assertEqual(block.probability_analytical, 0.48)

    def test_calculate_probability_by_method_simulated(self):
        """
        Тестирование метода calculate_probability_by_method_simulated класса Block.
        Проверяет корректность расчета вероятности при параллельном и последовательном соединениях.
        """
        # Проверка параллельного соединения
        block = Block(self.element1, self.element2, connection=MethodConnection.Parallel)
        result = block.calculate_probability_by_method_simulated(True, False)
        self.assertTrue(result)

        # Проверка последовательного соединения
        block = Block(self.element1, self.element2, connection=MethodConnection.Serial)
        result = block.calculate_probability_by_method_simulated(True, False)
        self.assertFalse(result)

    @patch('system_reliability.components.element.random.random')
    def test_calculate_probability_simulated(self, mock_random):
        """
        Тестирование метода calculate_probability_simulated класса Block.
        Проверяет корректность расчета вероятности при параллельном и последовательном соединениях.
        Использует mock для имитации возвращаемых значений функции random.random().
        """
        # Проверка параллельного соединения
        mock_random.side_effect = [0.7, 0.5]  # Вероятность для element1 и element2
        block = Block(self.element1, self.element2, connection=MethodConnection.Parallel)
        result = block.calculate_probability_simulated()
        self.assertTrue(result)

        # Проверка последовательного соединения
        mock_random.side_effect = [0.9, 0.5]  # Вероятность для element1 и element2
        block = Block(self.element1, self.element2, connection=MethodConnection.Serial)
        result = block.calculate_probability_simulated()
        self.assertFalse(result)

    def test_to_dict_analytical(self):
        """
        Тестирование метода to_dict_analytical класса Block.
        Проверяет корректность формирования формулы расчета вероятности при параллельном соединении.
        """
        block = Block(self.element1, self.element2, connection=MethodConnection.Parallel)
        formula = block.to_dict_analytical(MethodConnection.Parallel)
        self.assertEqual(formula, '(1 - (1 - 0.8) * (1 - 0.6))')

    def test_get_formula_analytical(self):
        """
        Тестирование метода get_formula_analytical класса Block.
        Проверяет корректность формирования формулы расчета вероятности при параллельном и последовательном соединениях.
        """
        # Проверка параллельного соединения
        formula = Block.get_formula_analytical(0.5, MethodConnection.Parallel)
        self.assertEqual(formula, '(1 - 0.5)')

        # Проверка последовательного соединения
        formula = Block.get_formula_analytical(0.5, MethodConnection.Serial)
        self.assertEqual(formula, '0.5')

class TestElement(unittest.TestCase):
    """
    Класс для тестирования функциональности класса Element.
    """

    def test_init_valid(self):
        """
        Тестирование инициализации экземпляра Element с корректным значением вероятности.
        """
        element = Element(0.8)
        self.assertEqual(element.probability_analytical, 0.8)

    def test_init_invalid_up(self):
        """
        Тестирование инициализации экземпляра Element с некорректным значением вероятности (больше 1).
        Ожидается вызов исключения ConstrainElementUp.
        """
        with self.assertRaises(ConstrainElementUp):
            Element(1.1)

    def test_init_invalid_down(self):
        """
        Тестирование инициализации экземпляра Element с некорректным значением вероятности (меньше 0).
        Ожидается вызов исключения ConstrainElementDown.
        """
        with self.assertRaises(ConstrainElementDown):
            Element(-0.1)

    @patch('system_reliability.components.element.random.random')
    def test_calculate_probability_simulated(self, mock_random):
        """
        Тестирование метода calculate_probability_simulated класса Element.
        Проверяет корректность расчета вероятности.
        Использует mock для имитации возвращаемых значений функции random.random().
        """
        mock_random.return_value = 0.7
        element = Element(0.8)
        result = element.calculate_probability_simulated()
        self.assertTrue(result)

        mock_random.return_value = 0.9
        result = element.calculate_probability_simulated()
        self.assertFalse(result)

    def test_to_dict_analytical(self):
        """
        Тестирование метода to_dict_analytical класса Element.
        Проверяет корректность формирования формулы расчета вероятности при параллельном соединении.
        """
        element = Element(0.8)
        formula = element.to_dict_analytical(MethodConnection.Parallel)
        self.assertEqual(formula, '(1 - 0.8)')

if __name__ == '__main__':
    unittest.main()