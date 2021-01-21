import numpy as np
import csv
import time
import platform
from scipy.io import loadmat
from cvxpy.interface import matrix_utilities
from cvxopt import sparse, matrix, cholmod
from scipy import linalg
import psutil
from memory_profiler import memory_usage

# Global variables
INPUT_DIRECTORY = '/Users/'
MATRICES_NAMES = ['ex15', 'shallow_water1', 'apache2', 'parabolic_fem', 'G3_circuit', 'cfd1', 'cfd2', 'StocF-1465', 'Flan_1565']
OUTPUT_PATH = INPUT_DIRECTORY + '/data_python_' + platform.system().lower() + '.csv'
CSV_HEADER = ['Environment', 'System', 'Matrix name', 'Elapsed time (s)', 'Memory (MB)', 'Relative error']

def resolve(matrix_name):
    A = matrix_utilities.sparse2cvxopt(loadmat(INPUT_DIRECTORY + matrix_name)['Problem']['A'][0][0])

    start_memory = psutil.swap_memory()[1] / (1024 * 1024)

    xe = matrix(np.ones([A.size[0], 1]))
    b = sparse(A * xe)

    end_memory = max(memory_usage((cholmod.splinsolve, (A, b)))) + (psutil.swap_memory()[1] / (1024 * 1024))

    start_time = time.time()

    x = cholmod.splinsolve(A, b)

    end_time = time.time()

    error = linalg.norm(x - xe) / linalg.norm(xe)

    return (end_time - start_time), (end_memory - start_memory), error

def cholesky_python():
    with open(OUTPUT_PATH, 'w', newline='\n') as data:
        write_data = csv.writer(data, quoting=csv.QUOTE_ALL)
        write_data.writerow(CSV_HEADER)
        
        for matrix_name in MATRICES_NAMES:
            time, memory, error = resolve(matrix_name)

            write_data.writerow(['Python', platform.system(), matrix_name, time, memory, error])
            print("Environment: {}\nSystem: {}\nMatrix: {}\nElapsed time: {} s\nMemory: {} MB\nRelative error: {}\n".format('Python', platform.system(), matrix_name, time, memory, error))

if __name__ == '__main__':
    cholesky_python()