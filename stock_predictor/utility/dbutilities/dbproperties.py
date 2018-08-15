import os
import property as p
database = "mokshtechdatabase.db"
user = "postgres"
password = "xxxxxxx"
# host = "117.228.34.133"
port = "5432"
host="xxxxxxxx"

sqlmokshtechdb = os.path.join(p.sqldb,'mokshtechdatabase.db')

indtable = 'IdxData'
nonindtable = 'StockData'


latest_derivative_query = '''select max("Date") from (SELECT substr(Date,8,8)||
              CASE substr(Date,4,3)
                 WHEN 'JAN' THEN '01'
                 WHEN 'FEB' THEN '02'
                 WHEN 'MAR' THEN '03'
                 WHEN 'APR' THEN '04'
                 WHEN 'May' THEN '05'
                 WHEN 'JUN' THEN '06'
                 WHEN 'JUL' THEN '07'
                 WHEN 'AUG' THEN '08'
                 WHEN 'SEP' THEN '09'
                 WHEN 'OCT' THEN '10'
                 WHEN 'NOV' THEN '11'
                 WHEN 'DEC' THEN '12'
              END ||substr(Date,1,2) as Date FROM MaxpainIV);'''

latest_symbol_derivative_data = '''
select max("Date") ,SYMBOL from (SELECT substr(Date,8,8)||
              CASE substr(Date,4,3)
                 WHEN 'JAN' THEN '01'
                 WHEN 'FEB' THEN '02'
                 WHEN 'MAR' THEN '03'
                 WHEN 'APR' THEN '04'
                 WHEN 'May' THEN '05'
                 WHEN 'JUN' THEN '06'
                 WHEN 'JUL' THEN '07'
                 WHEN 'AUG' THEN '08'
                 WHEN 'SEP' THEN '09'
                 WHEN 'OCT' THEN '10'
                 WHEN 'NOV' THEN '11'
                 WHEN 'DEC' THEN '12'
              END ||substr(Date,1,2) as Date,SYMBOL FROM MaxpainIV) GROUP BY  SYMBOL;
              '''

min_max_symbol_date_query = '''
Select Symbol, max(Date)
  as Date from IdxData
   GROUP BY Symbol
    HAVING Symbol in
     (select SYMBOL from SymbolList
       where isactve='True')
        union
         Select Symbol, max(Date)
          as Date from StockData
           GROUP BY Symbol
            HAVING Symbol in
             (select SYMBOL from SymbolList
              where isactve='True')
               order by Date;'''

# Server [localhost]:
# Database [postgres]: mokshtechdatabase
# Port [5432]:
# Username [postgres]:postgres

