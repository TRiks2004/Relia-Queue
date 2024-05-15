import unittest
from smo_rejection import Event, poisson_process

class TestPoissonProcess(unittest.TestCase):

    def test_poisson_process_expected_number_of_events(self):
        """Проверяет, что количество сгенерированных событий соответствует ожидаемому значению."""
        rate = 5
        time = 10
        expected_number_of_events = rate * time
        events = poisson_process(rate, time)
        self.assertEqual(len(events), expected_number_of_events)

    def test_poisson_process_return_type(self):
        """Проверяет правильный тип возвращаемого значения."""
        rate = 10
        time = 20
        events = poisson_process(rate, time)
        self.assertIsInstance(events, list)
        for event in events:
            self.assertIsInstance(event, Event)

    def test_poisson_process_events_generated(self):
        """Проверяет, что события были сгенерированы."""
        rate = 10
        time = 20
        events = poisson_process(rate, time)
        self.assertTrue(events)

    def test_poisson_process_event_times_within_duration(self):
        """Проверяет, что время всех событий находится в пределах заданной продолжительности."""
        rate = 10
        time = 20
        events = poisson_process(rate, time)
        for event in events:
            self.assertLessEqual(event.time, time)

    def test_poisson_process_zero_rate(self):
        """Проверяет обработку нулевой интенсивности потока."""
        rate = 0
        time = 20
        with self.assertRaises(ValueError):
            poisson_process(rate, time)

    def test_poisson_process_negative_rate(self):
        """Проверяет обработку отрицательной интенсивности потока."""
        rate = -5
        time = 20
        with self.assertRaises(ValueError):
            poisson_process(rate, time)

    def test_poisson_process_zero_time(self):
        """Проверяет обработку нулевой продолжительности симуляции."""
        rate = 10
        time = 0
        with self.assertRaises(ValueError):
            poisson_process(rate, time)

    def test_poisson_process_negative_time(self):
        """Проверяет обработку отрицательной продолжительности симуляции."""
        rate = 10
        time = -20
        with self.assertRaises(ValueError):
            poisson_process(rate, time)

if __name__ == '__main__':
    unittest.main()
