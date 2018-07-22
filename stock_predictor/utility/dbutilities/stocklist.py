from utility.dbutilities import dbqueries as dbq
from utility.dbutilities.dbproperties import *
import nsepy
import psycopg2
from nsetools import Nse
import pandas as pd
import property as p

stockfoldpath=p.stockdata


dbobj = dbq.db_queries()
conn = dbobj.create_connection()


### create table
def createstocktable(conn=conn):
    query = '''CREATE TABLE IF NOT EXISTS SymbolList
          (ID            INT   NOT NULL,
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
def createDerivativeTable (conn=conn):
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

    try:
        dbobj.exe(conn, query)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

createDerivativeTable()
query_table_exist= "SELECT id from SymbolList"
def check_table(conn=conn,query_table_exist=query_table_exist):

    try:
        dbobj.exe(conn,query_table_exist)
    except Exception as e:
        print(e)
    finally:
        conn.close()

# check_table()

#all_stock_codes = list(nse.get_stock_codes(cached=True).keys())

# df = pd.Series(all_stock_codes)

# dbobj.df2db(df, 'SymbolList')

# for i in range(1,2):
#     query_insert = "INSERT INTO SymbolList VALUES ({0}, {1},'NAV', 0, 0)".format(i,str(all_stock_codes[i]))
#     dbobj.exe(conn,query_insert)


    conn.commit()
try:
    conn.close()
except Exception as e:
    print(e)


def writeCodesToCSV():

    nse = Nse()
    print(type(nse.get_stock_codes(cached=True)))
    print(nse.get_stock_codes(cached=True))
    smbollDic = nse.get_stock_codes(cached=True)
    all_stock_codes = list(nse.get_stock_codes(cached=True).keys())
    all_stock_name = list(nse.get_stock_codes(cached=True).values())

    codes = [('SYMBOL', all_stock_codes),
             ('NAME', all_stock_name)]

    print(codes)

    symbolDF = pd.DataFrame.from_items(codes)
    print(symbolDF.head())

    symbolDF['INDFLAG'] = 0
    symbolDF['FO_FLAG'] = 0
    # symbolDF.set_index('SYMBOL', inplace= True)


    symbolDF.to_csv('symbolList.csv')


#writeCodesToCSV()


cur = conn.cursor()


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


#insertSymbolListInTabel()
conn.commit()


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



inserDerivativeDataInTable()

