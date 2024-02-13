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
	
	def __init__(self):
		DBMC.__engine = DBMC.__create_engine(echo=False)

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
		self.columns = self.get_columns()
	
	@abstractmethod
	def get_table_name(self): return None

	def get_columns(self):
		meta = sa.MetaData()
		meta.reflect(bind=self.__DBEngine,only=[self.__table_name])
		return meta.tables[self.__table_name].columns.keys()	

	def check_columns(self,data):
		for k in data:
			if k not in self.columns:
				raise LookupError("invalid column name!")

	def select_from_table(self,condition:'str'=''):
		query = 'SELECT * FROM ' + self.__table_name
		query+= ' WHERE ' + condition if condition else ''
		df = pd.read_sql(query,self.__DBEngine)
		return df

	def lookup_by_values(self,lookup_data:'dict'):
		self.check_columns(lookup_data)

		separator = " AND "
		condition = ""
		for k,v in lookup_data.items():
			condition += separator + f"{k} IN ({','.join(map(str,v))})"

		return self.select_from_table(condition[len(separator):])
	
	def insert_into_table(self,data):
		meta = sa.MetaData()
		meta.reflect(bind=self.__DBEngine,only=[self.__table_name])
		table = meta.tables[self.__table_name]
		with self.__DBEngine.connect() as conn:
			result = conn.execute(table.insert(),data)
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

	def append_entries(self,data):
		# if exists in inventory
		DBTable.append_entries(data)
		# update inventory? SQL trigger?
		# if at restock level restock inventory?



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
		db.tables["TEST"].insert_into_table(data)

	def test_select():
		condition = "testVar1 = 'testVal11'"
		df = db.tables["TEST"].select_from_table(condition)
		print(df)
	
	# test_create()
	# test_insert()
	# test_select()
		
	def get_product():
		print("\n> lookup by productId (1,2,3)")
		print(db.tables['PRODUCTS'].lookup_by_values({'productId':[1,2,3]}))

		print("\n> lookup by PLU (3000)")
		print(db.tables['PRODUCTS'].lookup_by_values({'PLU':[3000]}))

		print("\n> lookup by vendorId (1)")
		print(db.tables['PRODUCTS'].lookup_by_values({'productVendorId':[1]}))

		print("\n> lookup by price (2.00)")
		print(db.tables['PRODUCTS'].lookup_by_values({'price':[2.00]}))

		print("\n> lookup by productId (1,2,3) and price (2.00)")
		print(db.tables['PRODUCTS'].lookup_by_values({'productId':[1,2,3],'price':[2.00]}))
	
	# get_product()

	def add_product():

		print("\n> lookup by vendorId (1)")
		print(db.tables['PRODUCTS'].lookup_by_values({'productVendorId':[1]}))

		data = []
		data.append({
			'PLU':3012,
			'productVendorId':1,
			'price':3.00})
		data.append({
			'PLU':3320,
			'productVendorId':1,
			'price':2.60})
		db.tables['PRODUCTS'].append_entries(data)

		print("\n> lookup by vendorId (1)")
		print(db.tables['PRODUCTS'].lookup_by_values({'productVendorId':[1]}))
	
	# add_product()
		
	def get_vendor():
		print("\n> lookup by vendorID (1)")
		print(db.tables['VENDORS'].lookup_by_values({'vendorId':[1]}))

		print("\n> lookup by vendorName (Farmeraj d.o.o.)")
		print(db.tables['VENDORS'].lookup_by_values({'vendorName':["'Farmeraj d.o.o.'"]}))

		print("\n> lookup by vendorAddress (Slavonska avenija 7)")
		print(db.tables['VENDORS'].lookup_by_values({'vendorAddress':["'Slavonska avenija 7'"]}))

		print("\n> lookup by vendorPostalCode (10000) and vendorCity (Zagreb)")
		print(db.tables['VENDORS'].lookup_by_values({'vendorPostalCode':[10000],'vendorCity':["'Zagreb'"]}))
	
	# get_vendor()

	def add_vendor():

		print("\n> select all")
		print(db.tables['VENDORS'].select_from_table())

		data = []
		data.append({
			'vendorName':"Biovega d.o.o.",
			'vendorAddress':"Majstorska 1E",
			'vendorPostalCode': 10000,
			'vendorCity': "Zagreb",
			'vendorOIB': 84586153335,
			'vendorWebsite':"https://www.biobio.hr/"})
		data.append({
			'vendorName':"Podravka d.d.",
			'vendorAddress':"Ante Starčevića 32",
			'vendorPostalCode': 48000,
			'vendorCity': "Koprivnica",
			'vendorOIB': 18928523252,
			'vendorWebsite':"https://www.podravka.hr/"})
		db.tables['VENDORS'].append_entries(data)

		print("\n> select all")
		print(db.tables['VENDORS'].select_from_table())
	
	# add_vendor()

	def get_customer():
		print("\n> lookup by customerId (1)")
		print(db.tables["CUSTOMERS"].lookup_by_values({'customerId':[1]}))
		
		print("\n> lookup by customerName (Dubravkin put)")
		print(db.tables["CUSTOMERS"].lookup_by_values({'customerName':["'Dubravkin put'"]}))

		print("\n> lookup by customerAddress")
		print(db.tables["CUSTOMERS"].lookup_by_values({'customerAddress':["'Dubravkin put 2'"]}))

		print("\n> lookup by customerPostalCode (10000) and customerCity (Zagreb)")
		print(db.tables["CUSTOMERS"].lookup_by_values({'customerPostalCode':[10000],'customerCity':["'Zagreb'"]}))

	# get_customer()

	def add_customer():

		print("\n> select all")
		print(db.tables['CUSTOMERS'].select_from_table())

		data = []
		data.append({
			'customerName':"Takenoko",
			'customerAddress':"Masarykova 22",
			'customerPostalCode':10000,
			'customerCity':"Zagreb",
			'customerOIB':"79733218169",
			'customerWebsite':"https://www.takenoko.hr/"
		})
		data.append({
			'customerName':"ManO2",
			'customerAddress':"Radnička cesta 50",
			'customerPostalCode':10000,
			'customerCity':"Zagreb",
			'customerOIB':"86637426089",
			'customerWebsite':"https://mano2.hr/"})
		db.tables['CUSTOMERS'].append_entries(data)

		print("\n> select all")
		print(db.tables['CUSTOMERS'].select_from_table())
	
	# add_customer()
		
	def get_order_vendor():
		print("\n> lookup by orderId (1)")
		print(db.tables["ORDERS_VENDORS"].lookup_by_values({'orderId':[1]}))

		print("\n> lookup by vendorId (1)")
		print(db.tables["ORDERS_VENDORS"].lookup_by_values({'vendorId':[1]}))

		print("\n> lookup by productId (10)")
		print(db.tables["ORDERS_VENDORS"].lookup_by_values({'productId':[10]}))

		print("\n> lookup by productQty (100)")
		print(db.tables["ORDERS_VENDORS"].lookup_by_values({'productQty':[100]}))
	
	# get_order_vendor()

	def add_order_vendor():

		print("\n> select all")
		print(db.tables['ORDERS_VENDORS'].select_from_table())

		data = []
		data.append({
			'vendorId':9,
			'productId':5,
			'productQty':200})
		data.append({
			'vendorId':9,
			'productId':2,
			'productQty':50})
		db.tables['ORDERS_VENDORS'].append_entries(data)

		print("\n> select all")
		print(db.tables['ORDERS_VENDORS'].select_from_table())
	
	# add_order_vendor()

	# get_order_customer()

	def get_order_customer():
		print("\n> lookup by orderId (1)")
		print(db.tables["ORDERS_CUSTOMERS"].lookup_by_values({'orderId':[1]}))

		print("\n> lookup by customerId (1)")
		print(db.tables["ORDERS_CUSTOMERS"].lookup_by_values({'customerId':[1]}))

		print("\n> lookup by productId (10)")
		print(db.tables["ORDERS_CUSTOMERS"].lookup_by_values({'productId':[10]}))

		print("\n> lookup by productQty (10)")
		print(db.tables["ORDERS_CUSTOMERS"].lookup_by_values({'productQty':[10]}))
	
	# get_order_customer()
		
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

	add_order_customer()