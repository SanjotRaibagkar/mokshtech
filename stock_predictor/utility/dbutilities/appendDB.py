import os
from datetime import timedelta, datetime

import property as p
from utility.dbutilities import dbqueries as dbq
from utility.dbutilities.dbproperties import *
import nsepy
import psycopg2
from nsetools import Nse
import pandas as pd



latest_derivative_query = "SELECT max(to_date(Date, 'DD Mon YYYY'))  from derivativeData;"

min_max_symbol_date_query = "SELECT min(to_date(maxSymbolDate, 'DD Mon YYYY')) from " \
                            "(SELECT max(to_date(Date, 'DD Mon YYYY'))" \
                            "  from StockData where SYMBOL in " \
                            "(SELECT Distinct SYMBOL  from StockData) as maxSymbolDate)"


try:
    dbobj = dbq.db_queries()
    conn = dbobj.create_connection()
    cur = conn.cursor()
except Exception as e:
    print("DB not connected")

def get_latest_dates(query,conn):
        try:
            cur = dbobj.exe(conn, query)
            rows = cur.fetchall()[0][0]
            latestday = datetime.strptime(str(rows+timedelta(1)), '%Y-%m-%d').strftime('%d-%b-%Y')
            return latestday
        except Exception as e:
            print('Error',e)


def get_latest(x):
    if x == 'latestday_der':
        try:
            return get_latest_dates(latest_derivative_query, conn)
        except Exception as e:
            print("DB not connected")
    elif x == 'latestday_stock':
        try:
            return get_latest_dates(min_max_symbol_date_query, conn)
        except Exception as e:
            print("DB not connected")
    else:
        return '2018-12-7'#'2015-01-01'





def get_prev_day(query,conn):
    try:
        cur = dbobj.exe(conn, query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print('Error',e)

datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%d-%b-%Y')

if __name__ == '__main__':
    pass
    print(get_latest('latestday_stock'))

