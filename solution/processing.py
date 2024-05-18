from models import SimulationParameters, SimulationResult
from utils import generate_random_number, calculate_time

def process_iteration(params: SimulationParameters, iteration: int) -> SimulationResult:
    """
    Выполняет одну итерацию симуляции обслуживания заявок.

    ### Параметры:
    * `params (SimulationParameters)` - Параметры симуляции.
    * `iteration (int)` - Номер текущей итерации.

    ### Возвращаемое значение:
    * `SimulationResult` - Объект, содержащий результаты текущей итерации симуляции.

    ### Описание:
    Функция моделирует процесс поступления и обслуживания заявок в системе с несколькими каналами обслуживания (потоками).
    На каждом шаге времени генерируется случайное значение, на основе которого рассчитывается интервал времени до следующей заявки.
    Если в момент поступления заявки есть свободный канал обслуживания, заявка обслуживается, иначе она отклоняется.
    Функция отслеживает время занятости каждого канала обслуживания и статистику обслуженных и отклоненных заявок.
    Результаты итерации сохраняются в объекте `SimulationResult`, который возвращается функцией.
    """
    T = params.T  # Время окончания симуляции
    num_channels = params.num_channels  # Количество каналов обслуживания
    service_time = params.service_time  # Время обслуживания одной заявки
    alfa = params.alfa  # Параметр для расчета времени между заявками

    request_times = []  # Список для хранения времени поступления заявок и состояния каналов
    service_end_times = [0] * num_channels  # Время окончания обслуживания на каждом канале
    served_requests = 0  # Счетчик обслуженных заявок
    rejected_requests = 0  # Счетчик отклоненных заявок
    request_time = 0  # Время поступления текущей заявки

    while request_time < T:
        # Генерация случайного значения и расчет времени до следующей заявки
        rand_value = generate_random_number()
        inter_arrival_time = calculate_time(alfa, rand_value)
        request_time += inter_arrival_time

        if request_time > T:
            break

        # Поиск свободного канала или канала, который освободится раньше всех
        available_server = service_end_times.index(min(service_end_times))
        if service_end_times[available_server] <= request_time:
            # Если канал свободен, обслуживаем заявку
            service_end_times[available_server] = request_time + service_time
            served_requests += 1
            serviced = 1
            rejected = 0
        else:
            # Если канал занят, отклоняем заявку
            rejected_requests += 1
            serviced = 0
            rejected = 1

        # Создание записи о текущей заявке
        entry = {
            'index': len(request_times) + 1,
            'rand_value': round(rand_value, 4),
            'iba': round(inter_arrival_time, 4),
            'app_time': round(request_time, 4),
            'Обслужено': serviced,
            'Отказов': rejected,
        }

        # Запись времени окончания обслуживания для каждого канала
        for i in range(num_channels):
            key = f'server_{i + 1}'
            if serviced == 1 and available_server == i:
                entry[key] = round(service_end_times[i], 4)
            else:
                entry[key] = ''

        # Добавление записи в список всех заявок
        request_times.append(entry)

    # Возврат результатов итерации
    return SimulationResult(iteration=iteration + 1, served_requests=served_requests, rejected_requests=rejected_requests, request_times=request_times)