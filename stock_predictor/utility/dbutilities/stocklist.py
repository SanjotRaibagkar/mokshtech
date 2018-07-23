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

symbol_query = '''CREATE TABLE IF NOT EXISTS SymbolList
      (ID INT PRIMARY KEY     NOT NULL,
      SYMBOL         VARCHAR(30)     NOT NULL,    
      NAME           CHAR(50),
      INDFLAG        INT,
      FO_FLAG        INT);'''

stock_data_query = '''CREATE TABLE IF NOT EXISTS StockData
        (Date   VARCHAR(12) NOT NULL,
        Symbol  VARCHAR(50) NOT NULL,
        Series  CHAR(2),
        Prev_Close  REAL,
        Open    REAL,
        High    REAL,
        Low     REAL,
        Last    REAL,
        Close   REAL,
        VWAP    REAL,
        Volume  BIGINT,
        Turnover    numeric,
        Trades  numeric,
        Deliverable_Volume  numeric,
        Deliverble     numeric,
        PRIMARY KEY (Date, Symbol));'''

query_delete_stock = "DROP TABLE StockData;"
query_Index_data = '''CREATE TABLE IF NOT EXISTS IndexData
        (Date   VARCHAR(12) NOT NULL,
        Open    REAL,
        High    REAL,
        Low     REAL,
        Close   REAL,
        Volume  BIGINT,
        Turnover    REAL,
        Symbol  VARCHAR(50) NOT NULL,

        PRIMARY KEY (Date, Symbol));'''


query_derivative_alter = '''
ALTER TABLE derivativeData
ADD COLUMN Inserttimesamp TIMESTAMP DEFAULT NOW(),
ADD COLUMN UpdatedTimestamp TIMESTAMP;
	
	
CREATE OR REPLACE FUNCTION update_UpdatedTimestamp_column()
RETURNS TRIGGER AS $derivativeData$
BEGIN
   NEW.UpdatedTimestamp = now(); 
   RETURN NEW;
END;
$derivativeData$ language 'plpgsql';

CREATE TRIGGER update_derivativeData_UpdatedTimestamp BEFORE UPDATE
    ON derivativeData FOR EACH ROW EXECUTE PROCEDURE 
    update_UpdatedTimestamp_column();'''

delete_query_index_table= '''DROP TABLE IndexData;'''
### create table
def createstocktable(query,conn=conn):
    try:
        dbobj.exe(conn,query)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

# createstocktable(query_derivative_alter)

query_table_exist= "SELECT id from SymbolList"
def check_table(conn=conn,query_table_exist=query_table_exist):

    try:
        dbobj.exe(conn,query_table_exist)
    except Exception as e:
        print(e)
    finally:
        conn.close()

check_table()

# all_stock_codes = list(nse.get_stock_codes(cached=True).keys())
# # df = pd.Series(all_stock_codes)
#
# # dbobj.df2db(df, 'SymbolList')
#
# for i in range(1,2):
#     query_insert = "INSERT INTO SymbolList VALUES ({0}, {1},'NAV', 0, 0)".format(i,str(all_stock_codes[i]))
#     dbobj.exe(conn,query_insert)


try:
    conn.close()
except Exception as e:
    print(e)