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
		# update dict with table columns received
		classdict.update(data)
		# create new subclass of DBTable:
		TableClass = type(table_name,(DBTable,),classdict)
		# create the table in db:
		TableClass.__table__.create(bind=self.engine)
		# add to tables dictionary:
		self.tables[table_name] = TableClass()

# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_declaring_mapping.htm
class DBTable(Base):

	# to be changed on init:
	__tablename__ = ''
	templateId = sa.Column(sa.Integer,primary_key=True)

	def __init__(self):
		DBTable.__tablename__ = self.__class__.__tablename__
		self.DBEngine = DBMC.engine
		if not self.DBEngine:
			raise RuntimeError("DB not initialized!")
		self.DBMeta = DBMC.meta
		# self.__DBBase = DBMC.get_base()
		self.DBSession = DBMC.session
		self.columns = self.get_columns()

	def get_columns(self):
		self.DBMeta.reflect(bind=self.DBEngine,only=[DBTable.__tablename__])
		return self.DBMeta.tables[DBTable.__tablename__].columns.keys()	

	def check_columns(self,data):
		for k in data:
			if k not in self.columns:
				raise LookupError("invalid column name!")

	def select_from_table(self,columns='*',lookup_data:'dict'={},sep='',raw:'bool'=False):
		self.check_columns(columns) if columns!='*' else True
		query_columns = ','.join(columns) + ' FROM ' + DBTable.__tablename__

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
		self.DBMeta.reflect(bind=self.DBEngine,only=[DBTable.__tablename__])
		table = self.DBMeta.tables[DBTable.__tablename__]
		with self.DBEngine.connect() as conn:
			conn.execute(table.insert(),data)
			conn.commit()
	
	def append_entries(self,data):		
		for entry in data:
			self.check_columns(entry)
		
		self.insert_into_table(data)

class PRODUCTS(DBTable):
	__tablename__ = 'PRODUCTS'
	__mapper_args__ = {"concrete": True,}

	productId = sa.Column(sa.Integer,primary_key=True)

class INVENTORY(DBTable):
	__tablename__ = 'INVENTORY'
	__mapper_args__ = {"concrete": True,}

	inventoryId = sa.Column(sa.Integer,primary_key=True)

class VENDORS(DBTable):
	__tablename__ = 'VENDORS'
	__mapper_args__ = {"concrete": True,}

	vendorId = sa.Column(sa.Integer,primary_key=True)

class ORDERS_VENDORS(DBTable):
	__tablename__ = 'ORDERS_VENDORS'
	__mapper_args__ = {"concrete": True,}

	orderVendorId = sa.Column(sa.Integer,primary_key=True)

class CUSTOMERS(DBTable):
	__tablename__ = 'CUSTOMERS'
	__mapper_args__ = {"concrete": True,}

	customerId = sa.Column(sa.Integer,primary_key=True)

class ORDERS_CUSTOMERS(DBTable):
	__tablename__ = 'ORDERS_CUSTOMERS'
	__mapper_args__ = {"concrete": True,}

	orderId = sa.Column(sa.Integer,primary_key=True)

	customerId = sa.Column(sa.Integer)
	productId = sa.Column(sa.Integer)
	productQty = sa.Column(sa.Integer)
	totalPrice = sa.Column(sa.Float)

if __name__ == '__main__':
	db = DBMC()

	def test_create():
		name = 'TEST'
		data = {
			'testId':sa.Column(sa.Integer,primary_key=True),
			'testVar1':sa.Column(sa.String),
			'testVar2':sa.Column(sa.String)}
		# data = {
		# 	'testId':sa.Column('testId',sa.Integer,sa.Identity(),primary_key=True),
		# 	'testVar1':sa.Column('testVar1',sa.String),
		# 	'testVar2':sa.Column('testVar2',sa.String)}
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