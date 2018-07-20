from utility.dbutilities import dbqueries as dbq
from utility.dbutilities.dbproperties import *
import nsepy
import psycopg2
from nsetools import Nse
import pandas as pd

nse = Nse()

# df = pd.DataFrame(nse.get_stock_codes(cached=True))

dbobj = dbq.db_queries()
conn = dbobj.create_connection()

### create table
def createstocktable(conn=conn):
    query = '''CREATE TABLE IF NOT EXISTS SymbolList
          (ID INT PRIMARY KEY     NOT NULL,
          SYMBOL         VARCHAR(30)     NOT NULL,    
          NAME           CHAR(50),
          INDFLAG        INT,
          FO_FLAG        INT);'''


    try:
        dbobj.exe(conn,query)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

# createstocktable()

query_table_exist= "SELECT id from SymbolList"
def check_table(conn=conn,query_table_exist=query_table_exist):

    try:
        dbobj.exe(conn,query_table_exist)
    except Exception as e:
        print(e)
    finally:
        conn.close()

# check_table()

all_stock_codes = list(nse.get_stock_codes(cached=True).keys())
# df = pd.Series(all_stock_codes)

# dbobj.df2db(df, 'SymbolList')

for i in range(1,2):
    query_insert = "INSERT INTO SymbolList VALUES ({0}, {1},'NAV', 0, 0)".format(i,str(all_stock_codes[i]))
    dbobj.exe(conn,query_insert)


try:
    conn.close()
except Exception as e:
    print(e)