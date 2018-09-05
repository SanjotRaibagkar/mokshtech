import numpy as np
from multiprocessing import cpu_count, Pool, freeze_support
import pandas as pd
cores = cpu_count()  # Number of CPU cores on your system
partitions = cores  # Define as many partitions as you want


def parallelize(data, func,partitions):
    freeze_support()

    data_split = np.array_split(data, partitions)

    pool = Pool(cores)
    data = pd.concat(pool.map(func, data_split))
    pool.close()
    pool.join()
    return data