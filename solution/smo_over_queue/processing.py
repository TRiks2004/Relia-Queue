from models import Iteration, Answer
from utils import round_value, interval_between_apps, max_columns, generate_random_number

def process_iteration(service_time, max_time, alpha, num_threads):
    iterations: list[Iteration] = []
    current_time = 0
    random_value = 0
    interval = 0
    servers = []
    server_row_count = 0
    application_count = 0

    while current_time <= max_time:
        servers.append([0] * num_threads)
        column_max_values = max_columns(servers)

        for index, value in enumerate(column_max_values):
            if current_time >= value:
                servers[server_row_count][index] = round_value(current_time + service_time)
                break
        else:
            if index + 1 < len(servers[server_row_count]):
                servers[server_row_count][index + 1] = round_value(current_time + service_time)
            else:
                min_column_max = min(column_max_values)
                current_time = min_column_max
                servers[server_row_count][column_max_values.index(min_column_max)] = round_value(current_time + service_time)

        server_row_count += 1

        iterations.append(
            Iteration(
                index=application_count,
                random_value=random_value,
                interval_between_apps=interval,
                application_time=current_time,
                server_times=servers[-1]
            )
        )

        random_value = generate_random_number()
        interval = interval_between_apps(alpha, random_value)
        current_time = round_value(current_time + interval)
        application_count += 1

    return Answer(iterations[:], application_count - 1)
