import sqlalchemy as sa
import pandas as pd

from enum import Enum

class DBMC():

	class constants(Enum):
		DRIVER='ODBC Driver 17 for SQL Server'
		SERVER='Marin-PC'
		DATABASE='GST'
		TRUSTED_CONNECTION='yes'
	
	def __init__(self):
		self.__engine = sa.create_engine(DBMC.__create_conn_URL(),echo=True)
	
	@staticmethod
	def __create_conn_string():
		cs = ''
		cs+= f'DRIVER={DBMC.constants.DRIVER.value};'
		cs+= f'SERVER={DBMC.constants.SERVER.value};'
		cs+= f'DATABASE={DBMC.constants.DATABASE.value};'
		cs+= f'TRUSTED_CONNECTION={DBMC.constants.TRUSTED_CONNECTION.value};'
		return cs
	
	@staticmethod
	def __create_conn_URL():
		return sa.engine.URL.create(
			"mssql+pyodbc",query={"odbc_connect":DBMC.__create_conn_string()}
		)

	def process_query(self,query:'str',show:'bool'=True):
		df = pd.read_sql(query,self.__engine)
		print(df) if show else print()
	
	def create_table(self,name,*data):
		meta = sa.MetaData()
		table = sa.Table(name,meta,*data)
		meta.create_all(self.__engine)
	
	def insert_into_table(self,table_name,data):
		meta = sa.MetaData()
		meta.reflect(bind=self.__engine,only=[table_name])		
		table = meta.tables[table_name]
		print(table.columns)
		conn = self.__engine.connect()
		conn.execute(table.insert(),data)

def backup():
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

	query = 'SELECT TOP (10) [PLU],[CATEGORY],[COMMODITY],[VARIETY],[SIZE] FROM NONFTL ORDER BY [PLU]'
	df = pd.read_sql(query,engine)
	print(df)

if __name__ == '__main__':
	db = DBMC()
	
	# query = 'SELECT TOP (10) [PLU],[CATEGORY],[COMMODITY],[VARIETY],[SIZE] FROM NONFTL ORDER BY [PLU]'
	# db.process_query(query)

	# name = 'CUSTOMERS'
	# data = (
	# 	sa.Column('id',sa.Integer,primary_key=True),
	# 	sa.Column('firstName',sa.String),
	# 	sa.Column('lastName',sa.String))
	
	# db.create_table(name,*data)

	data = []
	data.append({'firstName':'Marin','lastName':'Pirsic'})
	db.insert_into_table('CUSTOMERS',data)

	# backup()