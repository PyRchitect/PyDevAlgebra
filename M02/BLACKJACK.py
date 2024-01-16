import pandas as pd
import numpy as np
import random as rn

class Game():
	max_players = 8
	max_decks = 8
	display_separator = "- "*10

	def __init__(self):

		self.number_of_players = 0	# set through init_players
		self.players = self.init_players()

		self.number_of_decks = self.init_decks()

		self.move_count = 0

		data = [[self.decks for _ in Cards.ranks] for _ in Cards.suits]
		self.available_cards = Cards(data)

		# # # TEST

		print("U ŠPILU:")
		print(Game.display_separator)
		print("ACES LOW:")
		print(self.available_cards.status)
		self.available_cards.aces_lh_switch()
		print(Game.display_separator)
		print("ACES HIGH:")
		print(self.available_cards.status)
		print(Game.display_separator)
		print(f"POINTS: {self.available_cards.calculate_points()}")

		for i,p in enumerate(self.players):
			print(f"\n{i+1}. IGRAC ({p.player_name}, {p.player_type}):")
			print(Game.display_separator)
			print("ACES LOW:")
			print(p.dealt_cards.status)
			p.dealt_cards.aces_lh_switch()
			print(Game.display_separator)
			print("ACES HIGH:")
			print(p.dealt_cards.status)
			print(Game.display_separator)
			print(f"POINTS: {p.dealt_cards.calculate_points()}")
		
		# # # TEST
			
	def init_players(self):
		players = []
		
		np_test = False
		while np_test == False:
			try:
				np = int(input("> Broj igraca [#]: "))
				assert np>=1 and np<=Game.max_players
			except:
				print("Pogresan unos!")
			else:
				np_test = True
			finally:
				print(Game.display_separator)
		
		for p in range(np):
			print(f"\n{p+1}. IGRAČ:")

			pn_test = False
			while pn_test == False:
				try:
					pn = input("> Ime igraca [""]: ")
					assert pn
				except:
					print("Pogresan unos!")
				else:
					pn_test = True
				finally:
					print(Game.display_separator)
			
			pt_test = False
			while pt_test == False:
				try:
					pt = input("> Tip igraca [H,C]: ")
					assert pt.upper() in ["H","C"]
				except:
					print("Pogresan unos!")
				else:
					pt_test = True
				finally:
					print(Game.display_separator)

			players.append(Player(pn,pt))
		
		self.number_of_players = np

		return players
	
	def init_decks(self):

		d_test = False
		while d_test == False:
			try:
				d = int(input("> Broj deckova [#]: "))
				assert d>=1 and d<=Game.max_decks
			except:
				print("Pogresan unos!")
			else:
				self.decks = d
				d_test = True
			finally:
				print(Game.display_separator)

	def deal(self):
		...
	
	def evaluate(self,player):
		...

class Cards():
	suits = list(range(1,4+1))
	sd = ["C","D","H","S"]
	# clubs, diamonds, hearts, spades
		
	ranks = list(range(1,13+1))
	# ranks basic range npr. za indeksiranje ili ako će trebati
	rd_al = ["A"] + [str(x) for x in range(2,11)] + ["J","Q","K"]
	# ranks display: aces low > A=1, 2-10, J=11, Q=12, K=13
	rd_ah = [str(x) for x in range(2,11)] + ["J","Q","K","A"]
	# ranks display: aces high > 2-10, J=10, Q=11, K=12, A=13
	rp_al = list(range(1,11)) + [10]*3
	# ranks points: aces low > A=1, 2-10, J,Q,K=10
	rp_ah = list(range(2,11)) + [10]*4
	# ranks points: aces high > 2-10, J,Q,K,A=10

	def __init__(self,R,aces=0):
		# aces flag: 0 - low, 1 - high
		if aces not in [0,1]:
			raise ValueError("Aces flag - pogresan unos! [0,1]")
		elif aces == 0:
			cols=Cards.rd_al
		elif aces == 1:
			cols=Cards.rd_ah
		self.aces_lh = aces

		self.status = pd.DataFrame.from_records(data=R,columns=cols,index=Cards.sd)
		pd.set_option('display.max_columns',13)
		pd.set_option('display.max_rows',4)
	
	def aces_lh_switch(self):
		col = self.status.pop("A")

		if self.aces_lh == 0:
			self.status.insert(len(self.status.columns),col.name,col) # move to end
			self.aces_lh = 1
		else:			
			self.status.insert(0,col.name,col) # move to beginning
			self.aces_lh = 0
	
	def cards_in_deck(self):
		return np.sum(self.status.values)

	def calculate_points(self):
		# aces flag: 0 - low, 1 - high
		if self.aces_lh == 0:
			cols=Cards.rp_al
		elif self.aces_lh == 1:
			cols=Cards.rp_ah

		status_points = pd.DataFrame.from_records(data=self.status.values,columns=cols,index=Cards.sd)

		s = 0
		for i in range(status_points.shape[1]):
			c = status_points.iloc[:,i]
			print(f"cn:{c.name}")
			print(f"cv:{c.values}")
			print(f"sum:{sum(c.values)}")
			s+=c.name*sum(c.values)
		
		return s

class Player():
	def __init__(self,player_name,player_type):
		self.player_name = player_name
		self.player_type = player_type

		data = [[0 for _ in Cards.ranks] for _ in Cards.suits]
		self.dealt_cards = Cards(data)

def play(new_game):
	...

def main():
	print("BLACKJACK")
	
	new_game = Game()

	while True:
		print(Game.display_separator)
		print("[0] - izlaz")
		print("[1] - igra")
		
		c_test = False
		while c_test == False:
			try:
				odabir = int(input("Odabir [0,1] "))
				assert odabir in [0,1]
			except:
				print("Pogrešan unos!")
				c_test = False
			else:
				c_test = True
			finally:
				print(Game.display_separator)

		if odabir == 0:
			print("Hvala i doviđenja.")
			break

		if odabir == 1:
			play(new_game)

		# elif odabir == ...

main()