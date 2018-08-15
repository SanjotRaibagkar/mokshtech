import multiprocessing
import pandas as pd
import numpy as np
from multiprocessing import Pool


def parallelize_dataframe(num_partitions, Series, func, **kwargs):
    num_cores = multiprocessing.cpu_count()
    splitlit = [np.array_split(Series, num_partitions)]
    pool = Pool(num_cores)
    Series = pd.concat(pool.map(func, splitlit))
    pool.close()
    pool.join()
    return Series

def square(x,n):
    res = x ** n
    return res

def arg_decorrator(func):
    print(func)
    def infunc(*args,**kwargs):
        pass

    return func

# @arg_decorrator
def test_func(data):
    #print("Process working on: ", data)
    data["square"] = data["col"].apply(square,args=(2,))
    return data



df = pd.DataFrame({'col': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]})





def test():
    testres = test_func(df)
    return testres

if __name__ == '__main__':
    # test = parallelize_dataframe(5,df, test_func)
    testres = test()
    print(testres)
