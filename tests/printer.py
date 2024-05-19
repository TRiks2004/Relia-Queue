import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smo_rejection import run_simulation, calculate_mean_served_requests, export_to_pdf

def main():
    T = 4
    num_channels = 3
    service_time = 0.5
    num_iterations = 2
    alfa = 5

    results = run_simulation(T, num_channels, service_time, num_iterations, alfa)
    export_to_pdf(results, "simulation_results.pdf")

if __name__ == "__main__":
    main()
