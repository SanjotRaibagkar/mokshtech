import psycopg2
import nsepy
import sqlite3
from sqlite3 import Error
import pandas as pd
from utility.dbutilities.csv2sqlite.csv2sqlite import convert
from utility.dbutilities import  dbproperties as dbp
import property as p
from nsetools import Nse
import os

nse = Nse()

# print(nse)
#
#all_stock_codes = nse.get_stock_codes(cached=True)
# print(all_stock_codes)
#
# index_codes = nse.get_index_list(cached=True)
# top_gainers = nse.get_top_gainers()
# print(nse.is_valid_code('PILIND'),'print')
#
#
# print(index_codes)


class db_queries(object):
    def __init__(self):
        self.database = dbp.database
        self.user = dbp.user
        self.password = dbp.password
        self.host = dbp.host
        self.port = dbp.port

    def create_connection_postgress(self):
        conn = psycopg2.connect(database=self.database,
                                user=self.user,
                                password=self.password,
                                host=self.host,
                                port=self.port)
        print("Opened database successfully")
        return conn

    def create_connection(self,db_file=dbp.database):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            import traceback
            print("dbqueries 1 ",traceback.extract_stack())
            print(e)
        finally:
            return conn

    def close_conn(self,conn):
        try:
            conn.close()
            print("connection close")
        except Exception as e:
            print("dbqueries 2",e)

    def exe(self,conn,query):
        cur = conn.cursor()
        cur.execute(query)
        return cur

    def df2db_posgress(self, df, table):
        engineurl = 'postgresql://'+self.user+':'+self.password+'@'+self.host+':'+self.port+'/'+self.database
        from sqlalchemy import create_engine
        engine = create_engine(engineurl)
        df.to_sql(table, engine)


    def uploadData(self,x,table,cur):
        print(x)
        try:
            with open(x, 'r') as f:
                # Notice that we don't need the `csv` module.
                next(f)  # Skip the header row.
                cur.copy_from(f, table, sep=',')
                conn.commit()
        except Exception as e:
            print(x,e)
        finally:
            pass
            conn.commit()

    def abc(self):

        stocklist = []
        indlist = []
        dirpath = p.stockdata
        for a, b, c in os.walk(dirpath):
            indlist = ['FTSE100', 'INDIAVIX', 'NIFTYCPSE', 'NIFTY', 'NIFTYIT', 'BANKNIFTY', 'NIFTYMID50', 'NIFTYPSE',
                       'NIFTYINFRA']
            c = list(set(c) - set(indlist))
            for files in c:
                # files=files+'.csv'
                if not files.startswith("symbolList.csv"):
                    stocklist.append(os.path.join(dirpath, files))
            for files in indlist:
                if not files.startswith("symbolList.csv"):
                    indlist.append(os.path.join(dirpath, files))

        stocklist = pd.Series(stocklist)
        indlist = pd.Series(indlist)

        def upload_StockData(db, table):
            stocklist.apply(convert, args=(db, table,))
            indlist.apply(uploadData)



    def df_sql(self,df,table,con):
        try:
            df.to_sql(name=table,con=con,if_exists='append')
            con.commit()
        except Exception as e:
            print(e," dbqueries 3 ")
        finally:
            return con

