from multiprocessing.pool import Pool
import numpy as np
from cvxopt import cholmod, matrix, sparse
from cvxpy.interface import matrix_utilities
import time
from scipy import io
import psutil

def memory_watch():
    start = str(int(time.time()))
    virtual_start = (psutil.virtual_memory().used) / (1024 * 1024)
    swap_start = (psutil.swap_memory().used) / (1024 * 1024)
    sampling_frequence = 10

    while True:
        virtual = (psutil.virtual_memory().used) / (1024 * 1024) - virtual_start
        swap = (psutil.swap_memory().used) / (1024 * 1024) - swap_start

        memory = virtual + swap

        with open(start + '.txt', 'a') as txt:
            txt.write(str(memory) + ', ')
            
        time.sleep(sampling_frequence)

def main():
    matrices = ['StocF-1465.mat', 'Flan_1565.mat']

    for matrix_name in matrices:
        A = matrix_utilities.sparse2cvxopt(io.loadmat(matrix_name)['Problem']['A'][0][0])
        xe = matrix(np.ones([A.size[0], 1]))
        b = sparse(A * xe)

        pool = Pool(processes=1)
        pool.apply_async(memory_watch)
        time.sleep(5)

        cholmod.splinsolve(A, b)

        pool.terminate()
        pool.join()

if __name__ == '__main__':
    main()
