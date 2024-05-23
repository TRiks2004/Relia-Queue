from pydantic import BaseModel


class SystemReliabilityElement(BaseModel):
    """
    Модель элемента системы надежности.

    Атрибуты:
        value (int): Значение элемента.
    """
    value: int


class SystemReliabilityBlock(BaseModel):
    """
    Модель блока системы надежности.

    Атрибуты:
        blockNumber (int): Номер блока.
        mode (str): Режим работы блока.
        elements (list[SystemReliabilityElement]): Список элементов блока.
    """
    blockNumber: int
    mode: str
    elements: list[SystemReliabilityElement]


class SystemReliabilityForm(BaseModel):
    """
    Модель формы системы надежности.

    Атрибуты:
        systemMode (str): Режим работы системы.
        blocks (list[SystemReliabilityBlock]): Список блоков системы.
    """
    systemMode: str
    blocks: list[SystemReliabilityBlock]


class SimulationInput(BaseModel):
    """
    Модель данных для представления входных параметров симуляции.

    Атрибуты:
        T (float): Продолжительность симуляции.
        num_channels (int): Количество каналов обслуживания.
        service_time (float): Время обслуживания.
        num_iterations (int): Количество итераций симуляции.
        alfa (int): Интенсивность потока заявок.
    """
    T: float
    num_channels: int
    service_time: float
    num_iterations: int
    alfa: int


class CFRUnlimitedParameters(BaseModel):
    """
    Модель параметров для симуляции CFRUnlimited.

    Атрибуты:
        serviceTime (float): Время обслуживания.
        maxSimulationTime (float): Максимальное время симуляции.
        alpha (float): Интенсивность потока заявок.
        channelCount (int): Количество каналов.
        iterationCount (int): Количество итераций симуляции.
    """
    serviceTime: float
    maxSimulationTime: float
    alpha: float
    channelCount: int
    iterationCount: int
