import sqlalchemy as sa
import pandas as pd

from abc import ABC,abstractmethod
from enum import Enum

class DBMC():

	class ConnParams(Enum):
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
	__meta = None
	
	def __init__(self):
		DBMC.__engine = DBMC.__create_engine(echo=False)
		DBMC.__meta = DBMC.get_meta()

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
		cs+= f'DRIVER={DBMC.ConnParams.DRIVER.value};'
		cs+= f'SERVER={DBMC.ConnParams.SERVER.value};'
		cs+= f'DATABASE={DBMC.ConnParams.DATABASE.value};'
		cs+= f'TRUSTED_CONNECTION={DBMC.ConnParams.TRUSTED_CONNECTION.value};'
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

	@staticmethod
	def get_meta(): return sa.MetaData()
	
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
		self.__DBMeta = DBMC.get_meta()
		if not self.__DBEngine:
			raise RuntimeError("DB not initialized!")
		
		self.__table_name = self.get_table_name()
		self.columns = self.get_columns()
	
	@abstractmethod
	def get_table_name(self): return None

	def get_columns(self):
		self.__DBMeta.reflect(bind=self.__DBEngine,only=[self.__table_name])
		return self.__DBMeta.tables[self.__table_name].columns.keys()	

	def check_columns(self,data):
		for k in data:
			if k not in self.columns:
				raise LookupError("invalid column name!")

	def select_from_table(self,columns='*',lookup_data:'dict'={},sep='',raw:'bool'=False):
		self.check_columns(columns) if columns!='*' else True
		query_columns = ','.join(columns) + ' FROM ' + self.__table_name

		if raw:
			# get raw selection (returns tuples using DBAPI)

			if sep=='':
				query_sep = lambda x: x
			elif sep=='AND':
				query_sep = sa.sql.and_
			elif sep=='OR':
				query_sep = sa.sql.or_
			else:
				raise ValueError("unknown condition separator!")
			
			with self.__DBEngine.connect() as conn:
				query = sa.sql.select(sa.sql.text(query_columns))
				if lookup_data:
					if len(lookup_data) == 1:
						(k,v) = lookup_data.popitem()
						query_text = sa.sql.text(f"{k} IN ({str(*v)})")
						query = query.where(query_text)
					else:
						query_list = [sa.sql.text(f"{k} IN ({','.join(map(str,v))})") for k,v in lookup_data.items()]					
						query = query.where(query_sep(*query_list))

				result = conn.execute(query).fetchall()
		else:
			# get formatted selection (returns pandas dataframe)
			sep = " " + sep + " "
			condition = ""
			for k,v in lookup_data.items():
				condition += sep + f"{k} IN ({','.join(map(str,v))})"

			query = 'SELECT ' + query_columns + (' WHERE ' + condition[len(sep):] if condition else '')
			result = pd.read_sql(query,self.__DBEngine)
		
		return result

	def lookup_by_values(self,columns='*',lookup_data:'dict'={},sep='',raw:'bool'=False):
		return self.select_from_table(columns,lookup_data,sep,raw)
	
	def insert_into_table(self,data):
		self.__DBMeta.reflect(bind=self.__DBEngine,only=[self.__table_name])
		table = self.__DBMeta.tables[self.__table_name]
		with self.__DBEngine.connect() as conn:
			conn.execute(table.insert(),data)
			conn.commit()
	
	def append_entries(self,data):		
		for entry in data:
			self.check_columns(entry)
		
		self.insert_into_table(data)

class PRODUCTS(DBTable):
	def get_table_name(self): return 'PRODUCTS'

class INVENTORY(DBTable):
	def get_table_name(self): return 'INVENTORY'

	def update_inventory(self): ...

class VENDORS(DBTable):
	def get_table_name(self): return 'VENDORS'

class ORDERS_VENDORS(DBTable):	
	def get_table_name(self): return 'ORDERS_VENDORS'

	def append_entries(self,data):
		# trigger at restock level
		DBTable.append_entries(data)
		# update inventory? SQL trigger?

class CUSTOMERS(DBTable):
	def get_table_name(self): return 'CUSTOMERS'	

class ORDERS_CUSTOMERS(DBTable):
	def get_table_name(self): return 'ORDERS_CUSTOMERS'

if __name__ == '__main__':
	db = DBMC()

	def get_order_customer():
		print("\n> lookup (productId,productQty,totalPrice) by productID (5) and productQty (10) df")
		print(db.tables["ORDERS_CUSTOMERS"].lookup_by_values(
			columns=['productId','productQty','totalPrice'],
			lookup_data={'productId':[5],'productQty':[10]},
			sep="AND",
			raw=False))
		print("\n> lookup (productId,productQty,totalPrice) by productID (5) and productQty (10) raw")
		print(db.tables["ORDERS_CUSTOMERS"].lookup_by_values(
			columns=['productId','productQty','totalPrice'],
			lookup_data={'productId':[5],'productQty':[10]},
			sep="AND",
			raw=True))
	
	get_order_customer()
		
	def add_order_customer():

		print("\n> select all")
		print(db.tables['ORDERS_CUSTOMERS'].select_from_table())

		data = []
		data.append({
			'customerId':3,
			'productId':5,
			'productQty':20})
		data.append({
			'customerId':3,
			'productId':2,
			'productQty':5})
		db.tables['ORDERS_CUSTOMERS'].append_entries(data)

		print("\n> select all")
		print(db.tables['ORDERS_CUSTOMERS'].select_from_table())

	# add_order_customer()