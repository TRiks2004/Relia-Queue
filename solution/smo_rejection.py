from dataclasses import dataclass
import random

@dataclass
class Event:
    """
    Определение класса Event для представления события с двумя полями: время и описание
    """
    time: float
    description: str

@dataclass
class SimulationResult:
    """
    Определение класса SimulationResult для хранения результатов симуляции:
    среднее количество обслуженных заявок, среднее количество отказов и список всех событий
    """
    average_served: float
    average_refusal: float
    all_events: list

def validate_simulation_parameters(rate, service_time, time, num_channels, num_runs):
    """Проверяет корректность входных параметров для симуляции."""
    if rate <= 0:
        raise ValueError("Интенсивность потока (rate) должна быть положительным числом.")
    if service_time <= 0:
        raise ValueError("Время обслуживания (service_time) должно быть положительным числом.")
    if time <= 0:
        raise ValueError("Продолжительность симуляции (time) должна быть положительным числом.")
    if num_channels <= 0:
        raise ValueError("Количество каналов (num_channels) должно быть положительным числом.")
    if num_runs <= 0:
        raise ValueError("Количество запусков симуляции (num_runs) должно быть положительным числом.")


def poisson_process(rate: int, time: int) ->list[Event]:
    """
    Функция, реализующая пуассоновский поток событий с заданной 
    rate - интенсивностью,
    time - продолжительностью
    """
    validate_simulation_parameters(rate, service_time, time, num_channels, num_runs)
    events = []  # Список для хранения событий
    t = 0  # Начальное время
    while True:
        delta_t = random.expovariate(rate)  # Генерация времени до следующего события по экспоненциальному распределению
        t += delta_t  # Обновление времени
        if t > time:  # Проверка, не превышено ли общее время симуляции
            break
        events.append(Event(t, "ЗАЯВКА"))  # Добавление события в список
    return events

def simulate_queue(arrival_times: int, service_time: float, num_channels: int) -> tuple:
    """
    Функция, моделирующая обслуживание в очереди:
    arrival_times - времена поступления заявок, 
    service_time - время обслуживания,
    num_channels - количество каналов обслуживания
    """
    served = 0  # Счетчик обслуженных заявок
    refusal = 0  # Счетчик отказов
    channels = [0] * num_channels  # Список для хранения времен завершения обслуживания в каждом канале
    events = []  # Список для хранения всех событий
    for arrival in arrival_times:
        events.append(Event(arrival.time, "ЗАЯВКА"))  # Добавление события поступления заявки
        free_channel = next((i for i, t in enumerate(channels) if t <= arrival.time), None)  # Поиск свободного канала
        if free_channel is not None:  # Если найден свободный канал
            channels[free_channel] = arrival.time + service_time  # Обновление времени завершения обслуживания в канале
            served += 1  # Увеличение счетчика обслуженных заявок
            events.append(Event(channels[free_channel], f"Обслуживание завершено в канале {free_channel}"))  # Добавление события завершения обслуживания
        else:  # Если все каналы заняты
            refusal += 1  # Увеличение счетчика отказов
            events.append(Event(arrival.time, "Все каналы заняты. Произошел отказ."))  # Добавление события отказа
    return served, refusal, events  # Возвращение количества обслуженных и отказанных заявок, а также всех событий


def run_simulation(rate: int, service_time: float, time: int, num_channels: int, num_runs:int) -> list[SimulationResult]:
    """
    Функция, запускающая симуляцию несколько раз и собирающая результаты:
    rate - интенсивность пуассоновского потока, service_time - время обслуживания,
    time - продолжительность симуляции, num_channels - количество каналов,
    num_runs - количество запусков симуляции
    """

    # Проверка корректности входных данных
    validate_simulation_parameters(rate, service_time, time, num_channels, num_runs)

    all_results = []  # Список для хранения результатов симуляции
    for _ in range(num_runs):
        total_served = 0  # Счетчик общего числа обслуженных заявок
        total_refusal = 0  # Счетчик общего числа отказов
        total_events = []  # Список для хранения всех событий из всех запусков
        arrival_times = poisson_process(rate, time)  # Генерация времен поступления заявок
        served, refusal, events = simulate_queue(arrival_times, service_time, num_channels)  # Моделирование обслуживания
        total_served += served  # Обновление счетчика обслуженных заявок
        total_refusal += refusal  # Обновление счетчика отказов
        average_served = total_served  # Вычисление среднего числа обслуженных заявок
        average_refusal = total_refusal  # Вычисление среднего числа отказов
        all_results.append(SimulationResult(average_served, average_refusal, events))  # Добавление результатов в список
    return all_results  # Возвращение всех результатов симуляции


# Параметры симуляции
rate = 5  # Интенсивность пуассоновского потока
service_time = 0.5  # Время обслуживания
time = 4  # Продолжительность симуляции
num_channels = 3  # Количество каналов обслуживания
num_runs = 1  # Количество запусков симуляции

# Запуск симуляции и получение результатов
simulation_results = run_simulation(rate, service_time, time, num_channels, num_runs)

# Вывод результатов симуляции
print("Подробный вывод:")
for i, result in enumerate(simulation_results, start=1):
    print(f"\nСимуляция #{i}:")
    for event in result.all_events:
        print(f"Событие в момент времени {event.time}: {event.description}")
    print(f"Математическое ожидание числа обслуженных заявок за {time} минут: {result.average_served:.2f}")
    print(f"Математическое ожидание числа отказов за {time} минут: {result.average_refusal:.2f}")

# Вывод общих результатов симуляции
total_served = sum(result.average_served for result in simulation_results) / len(simulation_results)
total_refusal = sum(result.average_refusal for result in simulation_results) / len(simulation_results)
print("\nСредние значения по всем симуляциям:")
print(f"Среднее математическое ожидание числа обслуженных заявок за {time} минут: {total_served:.2f}")
print(f"Среднее математическое ожидание числа отказов за {time} минут: {total_refusal:.2f}")
