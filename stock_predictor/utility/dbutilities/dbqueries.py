import psycopg2
from utility.dbutilities.dbproperties import *
import nsepy

from nsetools import Nse

nse = Nse()

# print(nse)
#
# all_stock_codes = nse.get_stock_codes(cached=True)
# print(all_stock_codes)
#
# index_codes = nse.get_index_list(cached=True)
# top_gainers = nse.get_top_gainers()
# nse.is_valid_code('infy')
#
#
# print(index_codes)


class db_queries(object):
    def __init__(self):
        self.database = database
        self.user = user
        self.password = 'sanjot111'
        self.host = host
        self.port = port

    def create_connection(self):
        conn = psycopg2.connect(database=self.database,
                                user=self.user,
                                password=self.password,
                                host=self.host,
                                port=self.port)
        print("Opened database successfully")
        return conn

    def close_conn(self,conn):
        conn.close()

    def exe(self,conn,query):
        cur = conn.cursor()
        cur.execute(query)
        return cur

        # rows = cur.fetchall()


    def df2db(self, df, table):
        engineurl = 'postgresql://'+self.user+':'+self.password+'@'+self.host+':'+self.port+'/'+self.database
        from sqlalchemy import create_engine
        engine = create_engine(engineurl)
        df.to_sql(table, engine)
        # conn.commit()

    def test(self):


        import pandas as pd

        df = pd.DataFrame(nse.get_stock_codes(cached=True))

        a = db_queries()
        conn = a.create_connection()
        query = '''CREATE TABLE StockList
              (ID INT PRIMARY KEY     NOT NULL,
              SYMBOL         TEXT     NOT NULL,    
              NAME           CHAR(50),
              INDFLAG        INT,
              FO_FLAG        INT);'''



        a.exe(conn,query)
        conn.commit()

        a.df2db(df, 'StockList', database, user, password, host, port)

