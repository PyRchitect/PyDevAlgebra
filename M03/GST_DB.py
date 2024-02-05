import sqlalchemy as sa
import pandas as pd


driver='ODBC Driver 17 for SQL Server'
server='Marin-PC'
database='GST'
trusted_connection='yes'

connection_string = f'DRIVER={driver};'
connection_string+= f'SERVER={server};'
connection_string+= f'DATABASE={database};'
connection_string+= f'TRUSTED_CONNECTION={trusted_connection};'

connection_url = sa.engine.URL.create(
	"mssql+pyodbc",query={"odbc_connect":connection_string})

engine = sa.create_engine(connection_url)

query = 'SELECT TOP (10) * FROM NONFTL'
df = pd.read_sql(query,engine)
print(df)