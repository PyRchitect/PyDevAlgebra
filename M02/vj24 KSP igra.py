import random as rn

class Player():
	def __init__(self,player_type=None,player_name=None):
		self.player_type = player_type
		self.player_name = player_name
		self.move = 0
		self.score = 0

def evaluate(players):
	m1 = int(players[0].move)
	m2 = int(players[1].move)
	
	# STATES:
	# 1 - kamen
	# 2 - skare
	# 3 - papir

	# GAMES:
	# 1 > 2
	# 2 > 3
	# 3 > 1

	if m1 == m2:
		return "izjednaceno"

	if (m1 == 1 and m2 == 2) or (
		m1 == 2 and m2 == 3) or (
		m1 == 3 and m2 == 1):
		players[0].score+=1
		return f"pobjeda {players[0].player_name}"

	if (m1 == 1 and m2 == 3) or (
		m1 == 2 and m2 == 1) or (
		m1 == 3 and m2 == 2):
		players[1].score+=1
		return f"pobjeda {players[1].player_name}"

def play(players):
	
	player_turn = 0
	print("\nIGRA:")

	while True:
		print(f"> potez ({players[player_turn].player_name}): ",end='')

		if players[player_turn].player_type == 'H':
			move_flag = False
			while not move_flag:
				players[player_turn].move = input()
				if int(players[player_turn].move) not in [1,2,3]:
					print("Pogresan unos!")
				else:
					move_flag = True
					
		else:			
			players[player_turn].move = rn.randint(1,3)
			if players[0].player_type == 'C' and players[1].player_type == 'H':
				print('#')
			else:
				print(players[player_turn].move)

		if player_turn == 1:
			print("\nPOTEZI: ")
			print(f"> {players[0].player_name}: {players[0].move}")
			print(f"> {players[1].player_name}: {players[1].move}")
			
			print(f"\nREZULTAT:")
			print(evaluate(players))
			break
		else:
			player_turn = 1

def main():

	new_players = True
	new_game = True

	def initialize_players():
		players = [Player(x) for x in range(2)]

		for (index,player) in enumerate(players):
			
			type_flag = False
			while not type_flag:
				player.player_type = input(f"Igrac ({index+1}): (H)uman or (C)omputer? ")
				if player.player_type not in ['h','H','c','C']:
					print("Pogresan unos!")
				else:
					type_flag = True

			name_flag = False
			while not name_flag:
				player.player_name = input("Ime igraca? ")
				if not player.player_name:
					print("Igrac mora imati ime!")
				else:
					name_flag = True

		return players

	while new_game:

		if new_players:
			players = initialize_players()

		print(f"\n{players[0].player_name} VS {players[1].player_name}")

		print("1 - kamen")
		print("2 - skare")
		print("3 - papir")

		play(players)
		
		print("\nSCORE:")
		print(f"> {players[0].player_name}: {players[0].score}")
		print(f"> {players[1].player_name}: {players[1].score}")

		game_flag = False
		while not game_flag:
			new_game = input("\n> nova igra? (Y/N) ")
			if not new_game in ['y','Y','n','N']:
				print("Pogrešan unos!")
			else:
				game_flag = True

		if new_game in ['n','N']:
			new_game = False
			continue

		player_flag = False
		while not player_flag:
			new_players = input("\n> novi igraci? (Y/N) ")
			if not new_players in ['y','Y','n','N']:
				print("Pogrešan unos!")
			else:
				player_flag = True

		if new_players in ['n','N']:
			new_players = False

main()