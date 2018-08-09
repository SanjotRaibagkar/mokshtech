from datetime import timedelta, datetime
from utility.dbutilities.dbproperties import *
from utility.dbutilities import dbqueries as dbq


# try:
#     dbobj = dbq.db_queries()
#     conn = dbobj.create_connection()
#     cur = conn.cursor()
# except Exception as e:
#     print("DB not connected")




def get_latest_dates(query,conn):
        try:
            print(query)
            cur = conn.cursor()
            rows = cur.execute(query)
            rows = rows.fetchall()
            for i in rows:
                print(i)
            exit(1)
            latestday = datetime.strptime(str(rows+timedelta(1)), '%Y%m%d').strftime('%d-%b-%Y')
            return latestday
        except Exception as e:
            print('Error',e)


def get_latest(x):
    try:
        # dbqo = dbq.db_queries()
        # conn = dbqo.create_connection()
        # cur = conn.cursor()
        #
        # print(conn)
        if x == 'latestday_der':
            import os
            import property as p

            db = os.path.join(p.sqldb, 'mokshtechdatabase.db')
            table = 'DerivativeData'
            dbqo = dbq.db_queries()
            con = dbqo.create_connection()
            print(con)
            query = '''select max("Date") from (SELECT substr(Date,8,8)||
                  CASE substr(Date,4,3)
                     WHEN 'JAN' THEN 01
                     WHEN 'FEB' THEN 02
                     WHEN 'MAR' THEN 03
                     WHEN 'APR' THEN 04
                     WHEN 'May' THEN 05
                     WHEN 'JUN' THEN 06
                     WHEN 'JUL' THEN 07
                     WHEN 'AUG' THEN 08
                     WHEN 'SEP' THEN 09
                     WHEN 'OCT' THEN 10
                     WHEN 'NOV' THEN 11
                     WHEN 'DEC' THEN 12
                  END ||substr(Date,1,2) as Date FROM MaxpainIV);'''
            print(query)
            cur = con.cursor()
            rows = cur.execute(query)
            rows = rows.fetchall()
            for i in rows:
                print(i)

            con.close()
            print('done')

        elif x == 'latestday_stock':
            try:
                return get_latest_dates(min_max_symbol_date_query, conn)
            except Exception as e:
                print("DB not connected")
        else:
            return '2018-12-7'#'2015-01-01'
    except Exception as e:
        print(e, "DB not connected")





def get_prev_day(query,conn):
    try:
        cur = dbobj.exe(conn, query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print('Error',e)

datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%d-%b-%Y')

if __name__ == '__main__':
    def getlatest():
        try:
            import os
            import property as p

            db = os.path.join(p.sqldb, 'mokshtechdatabase.db')
            table = 'DerivativeData'
            dbqo = dbq.db_queries()
            con = dbqo.create_connection(db_file=db)
            print(con)
            # con = convert('prices_2018_8.csv',conn=con,dbpath=db,table=table)
            # con.commit()
            # con = convert('prices_2018_7.csv',conn=con,dbpath=db,table=table)
            # con.commit()
            # con = convert('prices_2018_1.csv',conn=con,dbpath=db,table=table)
            # con.commit()
            query = '''select max("Date") from (SELECT substr(Date,8,8)||
              CASE substr(Date,4,3)
                 WHEN 'JAN' THEN 01
                 WHEN 'FEB' THEN 02
                 WHEN 'MAR' THEN 03
                 WHEN 'APR' THEN 04
                 WHEN 'May' THEN 05
                 WHEN 'JUN' THEN 06
                 WHEN 'JUL' THEN 07
                 WHEN 'AUG' THEN 08
                 WHEN 'SEP' THEN 09
                 WHEN 'OCT' THEN 10
                 WHEN 'NOV' THEN 11
                 WHEN 'DEC' THEN 12
              END ||substr(Date,1,2) as Date FROM MaxpainIV);'''
            print(query)
            cur = con.cursor()
            rows = cur.execute(query)
            rows = rows.fetchall()
            for i in rows:
                print(i)

            con.close()
            print('done')
        except Exception as e:
            print(e)


    getlatest()

