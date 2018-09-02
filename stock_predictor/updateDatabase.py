import multiprocessing
import pandas as pd
import numpy as np
from multiprocessing import Pool

from utility import getsymboldata
from optionvaluecalculation.OptionChain import nseoptionchain
# def test():
#     num_cores = multiprocessing.cpu_count()
#     a,b = [nseoptionchain.appendData(),getsymboldata.run_getsymboldata()]
#     pool = Pool(num_cores)
#     print(pool)
#     exit(1)
#     pa =pool.apply(a)
#     pb =pool.apply(b)
#     pool.close()
#     pool.join()
#     return pa,pb
#
# test()

years_series=pd.Series([2018])
if __name__ == '__main__':
    # nseoptionchain.appendData()
    getsymboldata.run_getsymboldata()


