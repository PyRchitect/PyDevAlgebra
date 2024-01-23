import os

import arg_testing
import datetime

from interface import Interface

class Bank():
	title = 'pyBank'

	BUSINESS = 'business'
	PERSONAL = 'personal'

	acc_type = {
		BUSINESS:'BA',
		PERSONAL:'PA'}

	def __init__(self,
			  clients=None,
			  acc_taken=None,
			  ids_taken=None):

		self.clients = clients or {}
		self.acc_taken = acc_taken or {}
		self.ids_taken = ids_taken or []
	
	def client_add(self,client:'Client'):
		self.clients[client.client_id]=client

	def client_remove(self,client:'Client'):
		self.clients.pop(client.client_id)
		self.ids_taken.remove(client.client_id)

		(client_type,first_num,second_num,n) = client.acc.split('-')
	
	def client_list(self):
		Interface.SimpleMessage("Popis klijenata:")
	
	def generate_client_id(self):
		# find hole algorithm !
		n = max(self.ids_taken) + 1
		return n

	def generate_acc_number(self,fn,sn):
		def find_first_hole(L,value):
			try:
				return L.index(value)
			except ValueError:
				return None

		if fn in self.acc_taken:
			if sn in self.acc_taken[fn]:

				hole = find_first_hole(self.acc_taken[fn][sn],0)
				if hole:
					self.acc_taken[fn][sn][hole] = 1
				else:
					hole = len(self.acc_taken[fn][sn])
					self.acc_taken[fn][sn].append(1)
			else:
				hole = 0
				self.acc_taken[fn][sn] = [1]
		else:
			hole = 0
			self.acc_taken[fn] = {sn: [1]}
			
		return hole


class Client():

	def __init__(self,
			  client_type=None,
			  client_id=None,
			  name=None,
			  OIB=None,
			  address=None,
			  city=None,
			  postal=None,
			  acc=None):

		if client_type not in Bank.acc_type:
			raise ValueError(f"tipovi klijenta: {[v for v in Bank.acc_type.values]}")

		self.client_type = client_type
		self.client_id = client_id or Bank.generate_client_id()

		self.name = name
		self.OIB = OIB
		self.adress = address
		self.city = city
		self.postal = postal

		self.acc = acc or Account(Bank.generate_acc_number(self))

	def account_add(self):
		...	

	def account_remove(self):
		...	
	
	def account_list(self):
		...

class Account():

	EUR = 'EUR'
	HRK = 'HRK'
	currencies = [EUR,HRK]

	DEPOSIT = 'deposit'
	WITHDRAW = 'withdraw'
	actions = [DEPOSIT,WITHDRAW]

	def __init__(self,
			  acc_number,
			  acc_currency=None,
			  funds=None,
			  transactions=None):

		if acc_currency not in Account.currencies:
			raise ValueError(f"Currencies: {Account.currencies}")
		
		self.acc_currency = acc_currency or 'EUR'
		self.acc_number = acc_number
		self.funds = funds or 0
		self.transactions = transactions or []
	
	def funds_add(self,funds):
		self.transactions.append((Account.DEPOSIT,funds))
		self.funds += funds
	
	def funds_remove(self,funds):		
		if self.funds - funds < 0:
			raise ValueError("Nedostatan saldo!")
		else:
			self.transactions.append((Account.WITHDRAW,funds))
			self.funds -= funds

	def transactions_list(self):
		Interface.SimpleMessage("Transakcije po računu:")
		for t in self.transactions:
			Interface.SimpleMessage(t)

class Menus():

	class MainMenu():

		def __init__(self):
			...


def cls_check():
	return 'cls' if os.name =='nt' else 'clear'

def main():
	...

if __name__ == '__main__':
	main()