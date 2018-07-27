from utility.dbutilities import dbqueries as dbq
from utility.dbutilities.dbproperties import *
import nsepy
import psycopg2
from nsetools import Nse
import pandas as pd
import property as p

stockfoldpath=p.stockdata




### create table
def createstocktable(conn):
    query = '''CREATE TABLE IF NOT EXISTS SymbolList
          (ID            INT   NOT NULL,
          SYMBOL         VARCHAR(30)     NOT NULL,
          NAME           CHAR(50),
          INDFLAG        INT,
          FO_FLAG        INT);'''

symbol_query = '''CREATE TABLE IF NOT EXISTS SymbolList
      (ID INT PRIMARY KEY     NOT NULL,
      SYMBOL         VARCHAR(30)     NOT NULL,    
      NAME           CHAR(50),
      INDFLAG        INT,
      FO_FLAG        INT);'''

stock_data_query = '''CREATE TABLE StockData (
    Date               DATETIME     NOT NULL,
    Symbol             VARCHAR (50) NOT NULL,
    Series             CHAR (2),
    Prev_Close         REAL,
    Open               REAL,
    High               REAL,
    Low                REAL,
    Last               REAL,
    Close              REAL,
    VWAP               REAL,
    Volume             BIGINT,
    Turnover           NUMERIC,
    Trades             NUMERIC,
    Deliverable_Volume NUMERIC,
    Deliverble         NUMERIC,
    Inserttimestamp    DATETIME     DEFAULT (CURRENT_TIMESTAMP) 
                                    NOT NULL ON CONFLICT ROLLBACK,
    Updatetimestamp    DATETIME     DEFAULT (CURRENT_TIMESTAMP),
    PRIMARY KEY (
        Date,
        Symbol
    )
);

CREATE TRIGGER UpdateTimestamp
         AFTER UPDATE
            ON StockData
      FOR EACH ROW
BEGIN
    INSERT INTO StockData (
                              UpdatedTimestamp
                          )
                          VALUES (
                              datetime('now') 
                          );
END;
'''

def listtriggers(triger,table):
    return 'SELECT name FROM sqlite_master WHERE ' \
           'type = {0} AND tbl_name = {1};.' \
           'format(triger,table)'


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
def createstocktable(query,conn):
    try:
        dbobj.exe(conn,query)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

def createDerivativeTable (conn):
    query = '''CREATE TABLE IF NOT EXISTS DerivativeData
              (ID            SERIAL      NOT NULL,
              INSTRUMENT     VARCHAR(30),
              SYMBOL         VARCHAR(30)     NOT NULL,
              EXPIRY_DT      VARCHAR(30),
              STRIKE_PR      numeric   ,
              OPTION_TYP     VARCHAR(5),
              OPEN           numeric,
              HIGH           numeric,
              LOW            numeric,
              CLOSE          numeric,
              SETTLE_PR      numeric,
              CONTRACTS      numeric,
              VAL_INLAKH     numeric,
              OPEN_INT       numeric,
              CHG_IN_OI      numeric,
              Date           Varchar(30) ,
              Unnamed15    Varchar(10),
              PRIMARY KEY(INSTRUMENT, SYMBOL,EXPIRY_DT,STRIKE_PR ,OPTION_TYP,Date));'''

# createstocktable(delete_query_index_table)
    createstocktable(query_Index_data)


    try:
        dbobj.exe(conn, query)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

# createDerivativeTable()
query_table_exist= "SELECT id from SymbolList"
def check_table(conn,query_table_exist=query_table_exist):

    try:
        dbobj.exe(conn,query_table_exist)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def writeCodesToCSV():
    nse = Nse()
    Index_Name = nse.get_index_list() # this return only name
    all_stock_codes = list(nse.get_stock_codes(cached=True).keys())
    all_stock_name = list(nse.get_stock_codes(cached=True).values())

    codes = [('SYMBOL', all_stock_codes),
             ('NAME', all_stock_name)]

    symbolDF = pd.DataFrame.from_items(codes)
    symbolDF['INDFLAG'] = 0
    symbolDF['FO_FLAG'] = 0

    symbolDF.to_csv(p.symbollist)




def insertSymbolListInTabel():
    import csv
    with open('symbolList.csv', 'r') as f:
        # Notice that we don't need the `csv` module.

        # reder = csv.reader(f)
        # for row in reder :
        #   next(f)
        #  print(row)
        next(f)  # Skip the header row.
        cur.copy_from(f, 'SymbolList', sep=',')





def inserDerivativeDataInTable():
    dbobj = dbq.db_queries()
    conn = dbobj.create_connection()
    cur = conn.cursor()
    import os
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(p.optiondata) if  f.endswith('.csv')]
    #print(onlyfiles)
    for file1 in onlyfiles:
        if '2018_7'in file1:

            fileName = os.path.join(p.optiondata, file1)
            print(fileName)
            with open(fileName, 'r') as f:
                # Notice that we don't need the `csv` module.
                next(f)  # Skip the header row.
                cur.copy_from(f, 'derivativeData', sep=',')
                conn.commit()
    conn.close()


if __name__ == '__main__':
    writeCodesToCSV()

    # dbobj = dbq.db_queries()
    # conn = dbobj.create_connection()
    #
    # cur = conn.cursor()
    # check_table()

    # insertSymbolListInTabel()
    # conn.commit()

    #inserDerivativeDataInTable()

    # try:
    #     conn.commit()
    #     conn.close()
    # except Exception as e:
    #     print(e)
    #
