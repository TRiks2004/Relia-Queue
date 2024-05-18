from simulation import run_simulation
from utils import calculate_mean_served_requests, print_results

def main():
    T = 4
    num_channels = 3
    service_time = 0.5
    num_iterations = 2
    alfa = 5

    try:
        results = run_simulation(T, num_channels, service_time, num_iterations,alfa)
        print_results(results, num_channels)
        a = calculate_mean_served_requests(results)
        print(f"\nВ качестве оценки искомого математического ожидания a – числа обслуженных заявок примем выборочную среднюю:")
        print(f"a = {a}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
