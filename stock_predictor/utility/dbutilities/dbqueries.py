
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
import datetime
import property as p

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

    def create_connection(self,db_file=dbp.sqlmokshtechdb):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            # shz: fix error with non-ASCII input
            # conn.text_factory = str
            print(sqlite3.version)
            return conn
        except Error as e:
            import traceback
            print("dbqueries 1 ",traceback.extract_stack())
            print(e)


    def close_conn(self,conn):
        try:
            conn.close()
            print("connection close")
        except Exception as e:
            print("dbqueries 2",e)

    def exec(self,conn,query):
        cur = conn.cursor()
        cur.execute(query)
        return cur


    def df2db_posgress(self, df, table):
        engineurl = 'postgresql://'+self.user+':'+self.password+'@'+self.host+':'+self.port+'/'+self.database
        from sqlalchemy import create_engine
        engine = create_engine(engineurl)
        df.to_sql(table, engine)


    def csv_sql(self,table,csvfile,con):
        try:
            con = convert(csvfile,dbpath=self.database,table=table,conn=con)
            con.commit()
        except Exception as e:
            import stack_trace
            print('dbqueries 6',stack_trace,e)
        finally:
            return con


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





    def dbqueriesdf_sql(self,df,table,con,csvfile='xyz.csv'):
        try:
            df.to_sql(name=table,con=con,if_exists='append',index=False)
            con.commit()
        except Exception as e:
            print(e," dbqueries 3 ")
            print("retrying")
            con = convert(table, csvfile, con)
            con.commit()
            print("retry succeed")
        finally:
            return con

def getlatestDerivative():
        try:
            db = os.path.join(p.sqldb, 'mokshtechdatabase.db')
            dbqo = db_queries()
            query = dbp.latest_derivative_query
            con = dbqo.create_connection(db_file=db)
            cur = con.cursor()
            rows = cur.execute(query)
            rows = rows.fetchall()[0][0]
            rows_y = int(rows[:4])
            rows_d = int(rows[6:8])
            rows_m = int('0' + rows[4:6])
            rows = datetime.date(rows_y, rows_m, rows_d)
            # if len(rows)>8:
            #     pass
            # placde holder for mins
            latestday = datetime.datetime.strptime(str(rows + datetime.timedelta(1)), '%Y-%m-%d').strftime('%d-%b-%Y')
            print('latest_start_day',latestday)
            con.close()
            return latestday
        except Exception as e:
            print(e)

def getlatestStockDate():

    db = os.path.join(p.sqldb, 'mokshtechdatabase.db')
    dbqo = db_queries()
    query = dbp.min_max_symbol_date_query
    con = dbqo.create_connection(db_file=db)
    cur = con.cursor()
    rows = cur.execute(query)
    rows = rows.fetchall()
    return rows

if __name__ == '__main__':
    getlatestStockDate()
# uploadStockData.upload_OptionsData()
