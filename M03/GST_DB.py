import sqlalchemy as sa
import pandas as pd

from enum import Enum

class DBMC():

	class constants(Enum):
		DRIVER='ODBC Driver 17 for SQL Server'
		from platform import node

		SERVER = node()
		# SERVER='Marin-PC'
		# SERVER='NEFORMALNI-23'

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
		# conn = self.__engine.connect()
		# conn.execute(table.insert(),data)
		with self.__engine.connect() as conn:
			result = conn.execute(table.insert(),data)
			conn.commit()

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

	def test_create():
		name = 'TEST'
		data = (
			sa.Column('testId',sa.Integer,primary_key=True),
			sa.Column('testVar1',sa.String),
			sa.Column('testVar2',sa.String))	
		db.create_table(name,*data)

	def test_insert():
		data = []
		data.append({'testVar1':'testVal1','testVar2':'testVal2'})
		db.insert_into_table('TEST',data)

	def test_select():
		query = 'SELECT * FROM TEST'
		db.process_query(query)
	
	test_create()
	test_insert()
	test_select()

	# backup()