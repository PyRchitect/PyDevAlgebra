import sqlalchemy as sa
import pandas as pd

from abc import ABC,abstractmethod
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
	
	# makes engine available for other classes:
	# references only dialect,driver,server and DB
	# referenced by all child classes (ie. tables)
	__engine = None
	
	def __init__(self):
		DBMC.__engine = DBMC.__create_engine(echo=True)

		self.tables = {
			'PRODUCTS':			PRODUCTS(),
			'INVENTORY':		INVENTORY(),
			'VENDORS':			VENDORS(),
			'ORDERS_VENDORS':	ORDERS_VENDORS(),
			'CUSTOMERS':		CUSTOMERS(),
			'ORDERS_CUSTOMERS':	ORDERS_CUSTOMERS()}
	
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

	@staticmethod
	def __create_engine(echo=False):
		return sa.create_engine(DBMC.__create_conn_URL(),echo=echo)

	@staticmethod
	def get_engine(): return DBMC.__engine
	
	def create_new_table(self,table_name,*data):
		meta = sa.MetaData()
		# insert new table into DB:
		table = sa.Table(table_name,meta,*data)
		try:
			meta.create_all(self.__engine)
		except:
			raise RuntimeError("DB error!")

		# get table name method (abstractmethod requirement):
		def get_table_name(self): return table_name
		classdict = {'get_table_name':get_table_name}
		# create new subclass of DBTable:
		TableClass = type(table_name,(DBTable,),classdict)
		# add to tables dictionary:
		self.tables[table_name] = TableClass()

class DBTable(ABC):

	def __init__(self):
		self.__DBEngine = DBMC.get_engine()
		if not self.__DBEngine:
			raise RuntimeError("DB not initialized!")
		
		self.__table_name = self.get_table_name()
	
	@abstractmethod
	def get_table_name(self): return None

	def __select_from_table(self,condition:'str'):
		query = 'SELECT * FROM ' + self.__table_name + ' WHERE ' + condition
		df = pd.read_sql(query,self.__DBEngine)
		return df
	
	def __insert_into_table(self,data):
		meta = sa.MetaData()
		meta.reflect(bind=self.__DBEngine,only=[self.__table_name])
		table = meta.tables[self.__table_name]
		with self.__DBEngine.connect() as conn:
			result = conn.execute(table.insert(),data)
			conn.commit()

class PRODUCTS(DBTable):

	# def __init__(self):
	# 	super()
	
	def get_table_name(self): return 'PRODUCTS'
	
	def get_by_id(self,productId):
		condition = f"productId IN ({','.join(map(str,productId))})"
		return self._DBTable__select_from_table(condition)
	
	def get_by_vendor(self,productVendorId:'list'):
		condition = f"productVendorId IN ({','.join(map(str,productVendorId))})"
		return self._DBTable__select_from_table(condition)
	
	def get_by_id_and_vendor(self,productId:'list',productVendorId:'list'):
		condition = f"productId IN ({','.join(map(str,productId))})"
		condition+= " AND "
		condition+= f"productVendorId IN ({','.join(map(str,productVendorId))})"
		return self._DBTable__select_from_table(condition)
	
	def add_new_product(self,productId:'list',productVendorId:'list',price:'float'):
		productData = {'productId':productId,'productVendorId':productVendorId,'price':price}
		super().__insert_into_table(self,productData)

class INVENTORY(DBTable):
	def update_inventory(self): ...
	def get_table_name(self): return 'INVENTORY'

class VENDORS(DBTable):	
	def get_vendor(self): ...
	def get_table_name(self): return 'VENDORS'

class ORDERS_VENDORS(DBTable):	
	def get_order_vendor(self): ...
	def get_table_name(self): return 'ORDERS_VENDORS'

class CUSTOMERS(DBTable):
	def get_customer(self): ...
	def get_table_name(self): return 'CUSTOMERS'	

class ORDERS_CUSTOMERS(DBTable):	
	def get_order_customer(self): ...
	def get_table_name(self): return 'ORDERS_CUSTOMERS'



if __name__ == '__main__':
	db = DBMC()

	def test_create():
		name = 'TEST'
		data = (
			sa.Column('testId',sa.Integer,sa.Identity(),primary_key=True),
			sa.Column('testVar1',sa.String),
			sa.Column('testVar2',sa.String))	
		db.create_new_table(name,*data)

	def test_insert():
		data = []
		data.append({'testVar1':'testVal11','testVar2':'testVal21'})
		data.append({'testVar1':'testVal12','testVar2':'testVal22'})
		db.tables["TEST"]._DBTable__insert_into_table(data)

	def test_select():
		condition = "testVar1 = 'testVal11'"
		df = db.tables["TEST"]._DBTable__select_from_table(condition)
		print(df)
	
	# test_create()
	# test_insert()
	# test_select()
		
	def get_product():
		df = db.tables['PRODUCTS'].get_by_id_and_vendor([1,2,3],[1])
		print(df)
	
	get_product()
		
	