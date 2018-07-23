import os
from datetime import timedelta, datetime

import property as p
from utility.dbutilities import dbqueries as dbq
from utility.dbutilities.dbproperties import *
import nsepy
import psycopg2
from nsetools import Nse
import pandas as pd



dbobj = dbq.db_queries()
conn = dbobj.create_connection()
cur = conn.cursor()

latest_derivative_query = "SELECT max(to_date(Date, 'DD Mon YYYY'))  from derivativeData;"


def get_latest_dates(query,conn,path):
    if path == p.optiondata:
        try:
            cur = dbobj.exe(conn, query)
            rows = cur.fetchall()[0][0]
            latestday = datetime.strptime(str(rows+timedelta(1)), '%Y-%m-%d').strftime('%d-%b-%Y')
            return latestday
        except Exception as e:
            print('Error',e)

def get_prev_day(query,conn):
    try:
        cur = dbobj.exe(conn, query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print('Error',e)

datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%d-%b-%Y')


latestday_der = get_latest_dates(latest_derivative_query,conn,p.optiondata)

# prev_day = latestday.days - timedelta(days=1)
# print(latestday,prev_day)
# count_query = '''SELECT count(*)  from derivativeData where Date = {0};'''.format(str(latestday))
#
# count_pk = get_prev_day(count_query,conn)
#print(count_pk)