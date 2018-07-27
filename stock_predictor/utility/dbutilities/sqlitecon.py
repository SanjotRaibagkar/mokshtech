import sqlite3
from sqlite3 import Error
from utility.dbutilities.dbqueries import *
import pandas as pd
from utility.dbutilities.csv2sqlite.csv2sqlite import convert
import property as p
from utility.dbutilities import  dbproperties as dbp

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        import traceback
        print(traceback.extract_stack())
        print(e)
    finally:
        return conn


def uploadData(x,table,cur):
    print(x)
    try:
        with open(x, 'r') as f:
            # Notice that we don't need the `csv` module.
            next(f)  # Skip the header row.
            cur.copy_from(f, table, sep=',')
            conn.commit()
            exit(1)
    except Exception as e:
        print(x,e)
    finally:
        pass
        conn.commit()


stocklist=[]
indlist = []
dirpath = p.stockdata
for a,b,c in os.walk(dirpath):
    indlist=['FTSE100','INDIAVIX','NIFTYCPSE','NIFTY','NIFTYIT','BANKNIFTY','NIFTYMID50','NIFTYPSE','NIFTYINFRA']
    c = list(set(c)-set(indlist))
    for files in c:
        #files=files+'.csv'
        if not files.startswith("symbolList.csv"):
            stocklist.append(os.path.join(dirpath,files))
    for files in indlist:
        if not files.startswith("symbolList.csv"):
            indlist.append(os.path.join(dirpath,files))


stocklist = pd.Series(stocklist)
indlist = pd.Series(indlist)


def upload_StockData(db,table):
    stocklist.apply(convert,args=(db,table,))
    indlist.apply(uploadData)



if __name__ == '__main__':
    pass
    upload_StockData(dbp.sqlmokshtechdb,'StockData')
