from dataclasses import dataclass

@dataclass
class SimulationParameters:
    T: float
    num_channels: int
    service_time: float
    num_iterations: int
    alfa : int

@dataclass
class SimulationResult:
    iteration: int
    served_requests: int
    rejected_requests: int
    request_times: list
