import pandas as pd

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from abc import ABC,abstractmethod
from enum import Enum

Base = sa.orm.declarative_base()

# allow only one instance of core classes
class singleton_class:
	def __init__(self,aClass):
		self.aClass = aClass
		self.instance = None
	def __call__(self,*args,**kwargs):
		if self.instance == None:
			self.instance = self.aClass(*args,**kwargs)
		return self.instance
	def __getattr__(self,attrname):
		return getattr(self.aClass,attrname)

@singleton_class	
class DBEngine():
	@staticmethod
	def create_conn_string():
		cs = ''
		cs+= f'DRIVER={DBMC.ConnParams.DRIVER.value};'
		cs+= f'SERVER={DBMC.ConnParams.SERVER.value};'
		cs+= f'DATABASE={DBMC.ConnParams.DATABASE.value};'
		cs+= f'TRUSTED_CONNECTION={DBMC.ConnParams.TRUSTED_CONNECTION.value};'
		return cs
	
	@staticmethod
	def create_conn_URL():
		return sa.engine.URL.create(
			"mssql+pyodbc",query={"odbc_connect":DBEngine.create_conn_string()})
	
	def __init__(self,echo=False):
		self._engine = sa.create_engine(DBEngine.create_conn_URL(),echo=echo)
	def __get__(self,instance,owner):
		return self._engine
	def __set__(self,instance,value,echo=False):
		raise AttributeError('cannot change engine!')
	def __delete__(self,instance):
		raise AttributeError('cannot delete engine!')

@singleton_class	
class DBMeta():
	def __init__(self):
		self._meta = sa.MetaData()
	def __get__(self,instance,owner):
		return self._meta
	def __set__(self,instance,value):
		raise AttributeError('cannot change meta!')
	def __delete__(self,instance):
		raise AttributeError('cannot delete meta!')

@singleton_class	
class DBSession():
	def __init__(self):
		self._session = sessionmaker(bind=DBMC.engine)()
	def __get__(self,instance,owner):
		return self._session
	def __set__(self,instance,value):
		raise AttributeError('cannot change session!')
	def __delete__(self,instance):
		raise AttributeError('cannot delete session!')

class DBMC():

	class ConnParams(Enum):
		DRIVER='ODBC Driver 17 for SQL Server'

		from platform import node
		SERVER = node()
		# SERVER='Marin-PC'
		# SERVER='NEFORMALNI-23'

		DATABASE='GST'
		TRUSTED_CONNECTION='yes'
	
	engine = None
	meta = None
	session = None

	def __init__(self):

		DBMC.engine = DBEngine()
		DBMC.meta = DBMeta()
		DBMC.session = DBSession()

		self.tables = {
			'FTL_JOINED':		FTL_JOINED(),
			'PRODUCTS':			PRODUCTS(),
			'INVENTORY':		INVENTORY(),
			'VENDORS':			VENDORS(),
			'ORDERS_VENDORS':	ORDERS_VENDORS(),
			'CUSTOMERS':		CUSTOMERS(),
			'ORDERS_CUSTOMERS':	ORDERS_CUSTOMERS()}
	
	def create_new_table(self,table_name,data):
		self.meta.reflect(self.engine)
		if table_name in self.meta.tables: return

		# (CORE) insert new table into DB using meta:
		# table = sa.Table(table_name,self.meta,*(v for v in data.values()))
		# try:
		# 	self.meta.create_all(self.engine)
		# except:
		# 	raise RuntimeError("DB error!")

		# (ORM) insert new table into DB using class and engine:
		# fill neccessary data for table creation
		classdict = {
			'__tablename__':table_name,
			'__mapper_args__' : {"concrete": True,}
			}
		classdict.update(data)
		TableClass = type(table_name,(DBTable,),classdict)
		TableClass.__table__.create(bind=self.engine)
		self.tables[table_name] = TableClass()

# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_declaring_mapping.htm
class DBTable(Base):

	# to be changed in inherited classes:
	__tablename__ = ''
	templateId = sa.Column(sa.Integer,primary_key=True)

	def __init__(self):
		self.DBEngine = DBMC.engine
		if not self.DBEngine:
			raise RuntimeError("DB not initialized!")
		self.DBMeta = DBMC.meta
		# self.__DBBase = DBMC.get_base()
		self.DBSession = DBMC.session
		self.columns = self.get_columns()

	def get_columns(self):
		self.DBMeta.reflect(bind=self.DBEngine,only=[self.__class__.__tablename__])
		return self.DBMeta.tables[self.__class__.__tablename__].columns.keys()	

	def check_columns(self,data):
		for k in data:
			if k not in self.columns:
				raise LookupError("invalid column name!")

	def select_from_table(self,columns='*',lookup_data:'dict'={},sep='',raw:'bool'=False):
		self.check_columns(columns) if columns!='*' else True
		query_columns = ','.join(columns) + ' FROM ' + self.__class__.__tablename__

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
			
			with self.DBEngine.connect() as conn:
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
			result = pd.read_sql(query,self.DBEngine)
		
		return result

	def lookup_by_values(self,columns='*',lookup_data:'dict'={},sep='',raw:'bool'=False):
		return self.select_from_table(columns,lookup_data,sep,raw)
	
	def lookup_by_keys(self,columns=[],lookup_data:'dict'={}):
		...
	
	def insert_into_table(self,data):
		self.DBMeta.reflect(bind=self.DBEngine,only=[self.__class__.__tablename__])
		table = self.DBMeta.tables[self.__class__.__tablename__]
		with self.DBEngine.connect() as conn:
			conn.execute(table.insert(),data)
			conn.commit()
	
	def append_entries(self,data):		
		for entry in data:
			self.check_columns(entry)
		
		self.insert_into_table(data)

class FTL_JOINED(DBTable):
	__tablename__ = 'FTL_JOINED'
	__mapper_args__ = {"concrete": True,}

	fsmaFTL = sa.Column(sa.VARCHAR(10))
	PLU = sa.Column(sa.INTEGER,primary_key=True)
	category = sa.Column(sa.VARCHAR(50))
	commodity = sa.Column(sa.VARCHAR(50))
	variety = sa.Column(sa.VARCHAR())
	size = sa.Column(sa.VARCHAR(50))
	measurementsNA = sa.Column(sa.VARCHAR(200))
	measurementsRoW = sa.Column(sa.VARCHAR(100))
	restrictions = sa.Column(sa.VARCHAR(250))
	botanicalName = sa.Column(sa.VARCHAR(100))
	aka = sa.Column(sa.VARCHAR())
	notes = sa.Column(sa.VARCHAR())
	revDate = sa.Column(sa.VARCHAR(50))
	dateAdded = sa.Column(sa.VARCHAR(50))
	GPC = sa.Column(sa.VARCHAR(20))

class PRODUCTS(DBTable):
	__tablename__ = 'PRODUCTS'
	__mapper_args__ = {"concrete": True,}

	productId = sa.Column(sa.INTEGER,primary_key=True)
	PLU = sa.Column(sa.INTEGER)
	productVendorId = sa.Column(sa.INTEGER)
	buyPrice = sa.Column(sa.FLOAT)
	holdPrice = sa.Column(sa.FLOAT)
	sellPrice = sa.Column(sa.FLOAT)

class INVENTORY(DBTable):
	__tablename__ = 'INVENTORY'
	__mapper_args__ = {"concrete": True,}

	inventoryId = sa.Column(sa.INTEGER,primary_key=True)
	productId = sa.Column(sa.INTEGER)
	qtyInStock = sa.Column(sa.INTEGER)
	qtyReStock = sa.Column(sa.INTEGER)
	dateAdded = sa.Column(sa.DATE)

class VENDORS(DBTable):
	__tablename__ = 'VENDORS'
	__mapper_args__ = {"concrete": True,}

	vendorId = sa.Column(sa.INTEGER,primary_key=True)
	vendorName = sa.Column(sa.VARCHAR(100))
	vendorAddress = sa.Column(sa.VARCHAR(100))
	vendorPostalCode = sa.Column(sa.CHAR(5))
	vendorCity = sa.Column(sa.VARCHAR(50))
	vendorOIB = sa.Column(sa.CHAR(11))
	vendorWebsite = sa.Column(sa.VARCHAR(100))

class ORDERS_VENDORS(DBTable):
	__tablename__ = 'ORDERS_VENDORS'
	__mapper_args__ = {"concrete": True,}

	orderVendorId = sa.Column(sa.INTEGER,primary_key=True)
	vendorId = sa.Column(sa.INTEGER)
	productId = sa.Column(sa.INTEGER)
	productQty = sa.Column(sa.INTEGER)
	totalPrice = sa.Column(sa.FLOAT)

class CUSTOMERS(DBTable):
	__tablename__ = 'CUSTOMERS'
	__mapper_args__ = {"concrete": True,}

	customerId = sa.Column(sa.INTEGER,primary_key=True)
	customerName = sa.Column(sa.VARCHAR(100))
	customerAddress = sa.Column(sa.VARCHAR(100))
	customerPostalCode = sa.Column(sa.CHAR(5))
	customerCity = sa.Column(sa.VARCHAR(50))
	customerOIB = sa.Column(sa.CHAR(11))
	customerWebsite = sa.Column(sa.VARCHAR(100))

class ORDERS_CUSTOMERS(DBTable):
	__tablename__ = 'ORDERS_CUSTOMERS'
	__mapper_args__ = {"concrete": True,}

	orderId = sa.Column(sa.Integer,primary_key=True)

	customerId = sa.Column(sa.INTEGER)
	productId = sa.Column(sa.INTEGER)
	productQty = sa.Column(sa.INTEGER)
	totalPrice = sa.Column(sa.FLOAT)

if __name__ == '__main__':
	db = DBMC()

	def test_create():
		name = 'TEST'
		data = {
			'testId':sa.Column(sa.Integer,primary_key=True),
			'testVar1':sa.Column(sa.String),
			'testVar2':sa.Column(sa.String)}
		db.create_new_table(name,data)

	def test_insert():
		data = []
		data.append({'testVar1':'testVal11','testVar2':'testVal21'})
		data.append({'testVar1':'testVal12','testVar2':'testVal22'})
		db.tables["TEST"].insert_into_table(data)

	def test_select():
		print(db.tables["TEST"].lookup_by_values(lookup_data={'testVar1':["'testVal11'"]}))

	# test_create()
	# test_insert()
	# test_select()

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
		
		print("\n> lookup (productId,productQty,totalPrice) by productID (5) and productQty (10) keys")
		# print(db.tables["ORDERS_CUSTOMERS"].lookup_by_keys
	
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

	# add_order_customer()

	def list_db():	
		
		print("\n> select all")

		print("FTL_JOINED")
		print(db.tables['FTL_JOINED'].select_from_table())

		print("PRODUCTS")
		print(db.tables['PRODUCTS'].select_from_table())

		print("INVENTORY")
		print(db.tables['INVENTORY'].select_from_table())

		print("VENDORS")
		print(db.tables['ORDERS_VENDORS'].select_from_table())

		print("ORDERS_VENDORS")
		print(db.tables['ORDERS_VENDORS'].select_from_table())

		print("CUSTOMERS")
		print(db.tables['CUSTOMERS'].select_from_table())

		print("ORDERS_CUSTOMERS")
		print(db.tables['ORDERS_CUSTOMERS'].select_from_table())

	# list_db()

	def add_vendors():

		print("\nVENDORS")
		print(db.tables['VENDORS'].select_from_table())

		data = []
		# data.append({
		# 	'vendorName':			'',
		# 	'vendorAddress':		'',
		# 	'vendorPostalCode':		'',
		# 	'vendorCity':			'',
		# 	'vendorOIB':			'',
		# 	'vendorWebsite':		'',
		# 	})
		# data.append({
		# 	'vendorName':			'Biovega d.o.o.',
		# 	'vendorAddress':		'Majstorska 1E',
		# 	'vendorPostalCode':		'10000',
		# 	'vendorCity':			'Zagreb',
		# 	'vendorOIB':			'84586153335',
		# 	'vendorWebsite':		'https://www.biobio.hr/',
		# 	})
		# data.append({
		# 	'vendorName':			'Podravka d.d.',
		# 	'vendorAddress':		'Ante Starčevića 32',
		# 	'vendorPostalCode':		'48000',
		# 	'vendorCity':			'Koprivnica',
		# 	'vendorOIB':			'18928523252',
		# 	'vendorWebsite':		'https://www.podravka.hr/',
		# 	})
		# data.append({
		# 	'vendorName':			'Animus Grupa d.o.o.',
		# 	'vendorAddress':		'Slavonska avenija 7',
		# 	'vendorPostalCode':		'10000',
		# 	'vendorCity':			'Zagreb',
		# 	'vendorOIB':			'14553621354',
		# 	'vendorWebsite':		'https://mojezrno.com/',
		# 	})
		# data.append({
		# 	'vendorName':			'GEKOS NATURA d.o.o. za usluge',
		# 	'vendorAddress':		'Ulica Grada Mainza 23',
		# 	'vendorPostalCode':		'10000',
		# 	'vendorCity':			'Zagreb',
		# 	'vendorOIB':			'94068269434',
		# 	'vendorWebsite':		'https://vocarna.hr/',
		# 	})
		# data.append({
		# 	'vendorName':			'OPG VESELIĆ - ORGANIC AGRICULTURE',
		# 	'vendorAddress':		'Novo Selo Palanječko, Vukovarska 24',
		# 	'vendorPostalCode':		'44202',
		# 	'vendorCity':			'Topolovac',
		# 	'vendorOIB':			'12214924795',
		# 	'vendorWebsite':		'https://www.eko-veselic.com/',
		# 	})
		# data.append({
		# 	'vendorName':			'TER d.o.o.',
		# 	'vendorAddress':		'Medarska 69',
		# 	'vendorPostalCode':		'10000',
		# 	'vendorCity':			'Zagreb',
		# 	'vendorOIB':			'35210351014',
		# 	'vendorWebsite':		'https://ter.hr/',
		# 	})
		# data.append({
		# 	'vendorName':			'ZKM d.o.o.',
		# 	'vendorAddress':		'Jadranska cesta 47',
		# 	'vendorPostalCode':		'23000',
		# 	'vendorCity':			'Zadar',
		# 	'vendorOIB':			'57976587442',
		# 	'vendorWebsite':		'http://www.zkm.hr/',
		# 	})
		# data.append({
		# 	'vendorName':			'LINI PLAC d.o.o. za trgovinu i usluge ',
		# 	'vendorAddress':		'Ferenščica I 102',
		# 	'vendorPostalCode':		'10000',
		# 	'vendorCity':			'Zagreb',
		# 	'vendorOIB':			'33815062701',
		# 	'vendorWebsite':		'https://plac.hr/',
		# 	})
		# db.tables['VENDORS'].append_entries(data)

		# print("\nVENDORS")
		# print(db.tables['VENDORS'].select_from_table())

	# add_vendors()
		
	def add_customer():

		print("\nCUSTOMERS")
		print(db.tables['CUSTOMERS'].select_from_table())

		data = []
		# data.append({
		# 	'customerName':			'',
		# 	'customerAddress':		'',
		# 	'customerPostalCode':	'',
		# 	'customerCity':			'',
		# 	'customerOIB':			'',
		# 	'customerWebsite':		'',
		# 	})
		data.append({
			'customerName':			'Carpaccio',
			'customerAddress':		'Teslina 14',
			'customerPostalCode':	'10000',
			'customerCity':			'Zagreb',
			'customerOIB':			'83706912258',
			'customerWebsite':		'https://ristorantecarpaccio.hr/',
			})
		data.append({
			'customerName':			'Rougemarin',
			'customerAddress':		'Frane Folnegovića 10',
			'customerPostalCode':	'10000',
			'customerCity':			'Zagreb',
			'customerOIB':			'20822976890',
			'customerWebsite':		'https://www.rougemarin.hr/',
			})
		data.append({
			'customerName':			'Lari i Penati',
			'customerAddress':		'Petrinjska 42a',
			'customerPostalCode':	'10000',
			'customerCity':			'Zagreb',
			'customerOIB':			'88529228879',
			'customerWebsite':		'http://www.laripenati.hr/',
			})
		data.append({
			'customerName':			'Boban',
			'customerAddress':		'Gajeva 9',
			'customerPostalCode':	'10000',
			'customerCity':			'Zagreb',
			'customerOIB':			'53656152979',
			'customerWebsite':		'http://www.boban.hr/',
			})
		data.append({
			'customerName':			'BOTA-ŠARE d.o.o.',
			'customerAddress':		'Ulica kralja Zvonimira 124',
			'customerPostalCode':	'10000',
			'customerCity':			'Zagreb',
			'customerOIB':			'74950041813',
			'customerWebsite':		'https://www.bota-sare.hr/',
			})
		data.append({
			'customerName':			'IZAKAYA',
			'customerAddress':		'Selska 90b',
			'customerPostalCode':	'10000',
			'customerCity':			'Zagreb',
			'customerOIB':			'07919388411',
			'customerWebsite':		'https://www.izakaya.hr/',
			})
		db.tables['CUSTOMERS'].append_entries(data)

		print("\nCUSTOMERS")
		print(db.tables['CUSTOMERS'].select_from_table())

	# add_customer()