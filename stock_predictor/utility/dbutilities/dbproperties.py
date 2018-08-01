import os
import property as p
database = "mokshtechdatabase"
user = "postgres"
password = "xxxxxxx"
# host = "117.228.34.133"
port = "5432"
host="xxxxxxxx"

sqlmokshtechdb = os.path.join(p.sqldb,'mokshtechdatabase.db')

latest_derivative_query = "SELECT max(to_date(Date, 'DD Mon YYYY'))  from derivativeData;"

min_max_symbol_date_query = "SELECT min(to_date(maxSymbolDate, 'DD Mon YYYY')) from " \
                            "(SELECT max(to_date(Date, 'DD Mon YYYY'))" \
                            "  from StockData where SYMBOL in " \
                            "(SELECT Distinct SYMBOL  from StockData) as maxSymbolDate)"

# Server [localhost]:
# Database [postgres]: mokshtechdatabase
# Port [5432]:
# Username [postgres]:postgres
