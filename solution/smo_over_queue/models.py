from dataclasses import dataclass

@dataclass
class Iteration:
    index: int
    random_value: float
    interval_between_apps: float
    application_time: float
    server_times: list[float]

@dataclass
class Answer:
    iterations: list[Iteration]
    expected_value: float

@dataclass
class Queue:
    results: list[Answer]
    average_value: float
