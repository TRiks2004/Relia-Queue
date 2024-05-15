from dataclasses import dataclass
import random

@dataclass
class Event:
    time: float
    description: str

@dataclass
class SimulationResult:
    average_served: float
    average_refusal: float
    all_events: list

def poisson_process(rate, time):
    events = []
    t = 0
    while True:
        delta_t = random.expovariate(rate)
        t += delta_t
        if t > time:
            break
        events.append(Event(t, "ЗАЯВКА"))
    return events

def simulate_queue(arrival_times, service_time, num_channels):
    served = 0
    refusal = 0
    channels = [0] * num_channels
    events = []
    for arrival in arrival_times:
        events.append(Event(arrival.time, "ЗАЯВКА"))
        free_channel = next((i for i, t in enumerate(channels) if t <= arrival.time), None)
        if free_channel is not None:
            channels[free_channel] = arrival.time + service_time
            served += 1
            events.append(Event(channels[free_channel], f"Обслуживание завершено в канале {free_channel}"))
        else:
            refusal += 1
            events.append(Event(arrival.time, "Все каналы заняты. Произошел отказ."))
    return served, refusal, events

def run_simulation(rate, service_time, time, num_channels, num_runs):
    all_results = []
    for _ in range(num_runs):
        total_served = 0  # Исправлено: объявляем переменные перед циклом симуляции
        total_refusal = 0
        total_events = []
        arrival_times = poisson_process(rate, time)
        served, refusal, events = simulate_queue(arrival_times, service_time, num_channels)
        total_served += served
        total_refusal += refusal
        average_served = total_served  # Исправлено: переносим расчет среднего вне цикла
        average_refusal = total_refusal
        all_results.append(SimulationResult(average_served, average_refusal, events))
    return all_results

# Входные данные
rate = 5
service_time = 0.5
time = 4
num_channels = 3
num_runs = 1

# Запуск симуляции
simulation_results = run_simulation(rate, service_time, time, num_channels, num_runs)

print("Подробный вывод:")
for i, result in enumerate(simulation_results, start=1):
    print(f"\nСимуляция #{i}:")
    for event in result.all_events:
        print(f"Событие в момент времени {event.time}: {event.description}")
    print(f"Математическое ожидание числа обслуженных заявок за {time} минут: {result.average_served:.2f}")
    print(f"Математическое ожидание числа отказов за {time} минут: {result.average_refusal:.2f}")

# Вычисление средних значений по всем симуляциям
total_served = sum(result.average_served for result in simulation_results) / len(simulation_results)
total_refusal = sum(result.average_refusal for result in simulation_results) / len(simulation_results)
print("\nСредние значения по всем симуляциям:")
print(f"Среднее математическое ожидание числа обслуженных заявок за {time} минут: {total_served:.2f}")
print(f"Среднее математическое ожидание числа отказов за {time} минут: {total_refusal:.2f}")
