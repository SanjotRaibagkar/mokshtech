import os
from datetime import timedelta, datetime

import property as p
from utility.dbutilities import dbqueries as dbq
from utility.dbutilities.dbproperties import *
import nsepy
import psycopg2
from nsetools import Nse
import pandas as pd






try:
    dbobj = dbq.db_queries()
    conn = dbobj.create_connection()
    cur = conn.cursor()
except Exception as e:
    print("DB not connected")

def get_latest_dates(query,conn):
        try:
            print(conn)
            cur = dbobj.exe(conn, query)
            rows = cur.fetchall()
            print(len(rows),rows)
            latestday = datetime.strptime(str(rows+timedelta(1)), '%Y-%m-%d').strftime('%d-%b-%Y')
            return latestday
        except Exception as e:
            print('Error',e)


def get_latest(x):
    if x == 'latestday_der':
        try:
            late_date =  get_latest_dates(latest_derivative_query, conn)
            print(type(late_date))
            exit(1)

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
    print(get_latest('latestday_der'))

