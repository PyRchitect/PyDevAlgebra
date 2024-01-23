import arg_testing
from interface import Interface

class Bank():

	BUSINESS = 'business'
	PERSONAL = 'personal'

	acc_name_prefix = {
		Bank.BUSINESS:'BA',
		Bank.PERSONAL:'BA'}

	def __init__(self,clients,accounts):
		self.clients = clients or {}
		self.accounts = accounts or {}
	
	def add_client(self,client):
		...
	
	def generate_account_number(self,client):
		...

class Client():

	def __init__(self,name,surname,OIB,address):
		self.name = name
		self.surname = surname
		self.OIB = OIB
		self.adress = address