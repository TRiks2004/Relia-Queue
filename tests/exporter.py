import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smo_rejection import run_simulation, export_to_pdf, export_to_excel

def main():
    T = 4
    num_channels = 3
    service_time = 0.5
    num_iterations = 10
    alfa = 5

    results = run_simulation(T, num_channels, service_time, num_iterations, alfa)
    export_to_pdf(results, "simulation_results.pdf")
    export_to_excel(results, "simulation_results.xlsx")
    

if __name__ == "__main__":
    main()
