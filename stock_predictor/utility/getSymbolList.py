from nsetools import Nse
import pandas as pd
from property import*
def  getstockList():
    des_file = symbollist
    nse = Nse()
    all_stock_code = nse.get_stock_codes(cached=True)
    all_stock_codes = pd.DataFrame(list(all_stock_code.items()),columns=["SYMBOL","NAME OF COMPANY"])
    all_stock_codes.drop(all_stock_codes.index[0],inplace=True)
    Symbols = all_stock_codes['SYMBOL'].tolist()
    isvalid=list(map(lambda x : nse.is_valid_code(x),Symbols))
    all_stock_codes['isactve']=isvalid
    all_stock_codes['FUT']=False
    all_stock_codes['IDX']=False
    return all_stock_codes

def get_idxlist():

    all_stock_codes.to_csv(des_file)