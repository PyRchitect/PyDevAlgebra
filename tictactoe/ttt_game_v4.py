import math

P1 = 'X' # maximizer
P2 = 'O' # minimizer
P3 = '-' # prazna

def initialize():
	return [[P3 for x in range(3)] for y in range(3)]

def show(board):
	board_display = ''

	for i in range(3):
		board_display+='\n| '
		for j in range(3):
			board_display+=f'{board[i][j]} | '

	print(board_display[1:])

def update(board,row,col,mark):
	if board[row][col]==P3:
		board[row][col]=mark
		return board

	raise TypeError

def is_moves_left(board):
	# vraća true/false ako se može/ne može igrati još poteza
	# testira ima li praznih ćelija, ako nađe neku vraća true

	for i in range(3):
		for j in range(3):
			if (board[i][j] == P3):
				return True

	return False

def evaluate(board):
	# evaluation function: tko pobjeđuje? b[3][3] je TTT ploča
	# MOŽE SE OPTIMIZIRATI I SKRATITI, ali nebitno je za sada

	for row in range(3): # Rows
		if (board[row][0] == board[row][1] and board[row][1] == board[row][2]):
			if (board[row][0] == P1):
				return 1
			if (board[row][0] == P2):
				return -1

	for col in range(3): # Cols
		if (board[0][col] == board[1][col] and board[1][col] == board[2][col]):
			if (board[0][col] == P1):
				return 1
			if (board[0][col] == P2):
				return -1

	if (board[0][0] == board[1][1] and board[1][1] == board[2][2]): # Diag(\)
		if (board[0][0] == P1):
			return 1
		if (board[0][0] == P2):
			return -1

	if (board[0][2] == board[1][1] and board[1][1] == board[2][0]): # Diag(/)
		if (board[0][2] == P1):
			return 1
		if (board[0][2] == P2):
			return -1

	return 0 # ako si tu, nitko nije pobijedio

def minimax(board, depth, is_max):
	# minimax function: gleda sve načine na koje se
	# ploča može razviti i vraća vrijednost ploče
	score = evaluate(board)
	if (score == 1):
		return score # Maximizer je pobijedio
	if (score ==-1):
		return score # Minimizer je pobijedio
	# nema više poteza, nitko nije pobijedio > neriješeno
	if (not is_moves_left(board)):
		return 0

	if is_max: # Ako je Maximizer na potezu
		best = -math.inf
		for i in range(3):
			for j in range(3):
				if (board[i][j]==P3): # ćelija prazna?
					board[i][j] = P1 # napravi potez
					# minimax rekurzivno > odaberi max vrijednost
					best = max(best,minimax(board,depth + 1,not is_max))
					board[i][j] = P3 # vrati potez nakon testa
		return best

	else:  # Ako je Minimizer na potezu
		best = math.inf
		for i in range(3):
			for j in range(3):
				if (board[i][j] == P3): # ćelija prazna?
					board[i][j] = P2 # napravi potez
					# minimax rekurzivno > odaberi min vrijednost
					best = min(best, minimax(board, depth + 1, not is_max))
					board[i][j] = P3 # vrati potez nakon testa
		return best

def find_best_move(board):
	# vraća najbolji potez prema minimax algoritmu
	# za sada: P1 je 'X', čovjek, maximizer | P2 je 'O', kompjuter, minimizer
	best_score = math.inf
	best_move = None
	# evaluate minimax function za sve prazne ćelije, vrati optimalnu
	for i in range(3):
		for j in range(3):
			if board[i][j] == P3: # ćelija prazna?
				board[i][j] = P2 # napravi potez
				score = minimax(board, 0, True) # evaluate
				board[i][j] = P3 # vrati potez nakon testa
				# ako je vrijednost veća od trenutnog najboljeg, ažuriraj
				if (score < best_score):
					best_move = (i, j)
					best_score = score

	# TEST
	# print("Vrijednost najboljeg poteza: ", bestScore)
	# TEST
	print()
	return best_move

def play(name_player,name_opponent):

	def move_check(move,board):
		# input_check = lambda x,y : (x in [0,1,2] and y in [0,1,2])
		def input_check(x,y):
			return (x in [0,1,2] and y in [0,1,2])

		try:
			row = int(move.split(' ')[0])
			col = int(move.split(' ')[1])
		except ValueError:
			return (False, "Pogrešan unos!")

		if (not input_check(row,col)):
			return (False, "Potez van ploče!")

		if board[row][col]!=P3:
			return (False, "Polje nije prazno!")

		return (True,(row,col))

	def move_display(move,board,player_name,player):
		(row,col) = move[1]
		board = update(board,row,col,player)
		show(board)
		score = evaluate(board)

		if score != 0:
			return (True,board,f"pobjeda {player_name}!")

		if is_moves_left(board):
			return (False,board,"slijedeci potez ...")

		return (True,board,"izjednaceno!")

	board = initialize()
	move_count = 1
	show(board)

	print("\nUPUTA: potez se unosi u obliku (red, [0-2]) (stupac, [0-2]).")

	win_flag = False
	while not win_flag:
		# prvi igra čovjek (za sada)
		move = input(f"\n> {move_count}. potez ({name_player}): ")
		move = move_check(move,board)

		if not move[0]:
			# neuspješno unesen potez
			print(move[1])
			continue
		else:
			# uspješno unesen potez
			(win_flag,board,poruka) = move_display(move,board,name_player,P1)
			print(poruka)

		if win_flag:
			break

		# drugi igra kompjuter (za sada)
		print(f"> {move_count}. potez ({name_opponent}): ")
		move = (True,find_best_move(board))
		(win_flag,board, poruka)= move_display(move,board,name_opponent,P2)
		print(poruka)

		if win_flag:
			break

		move_count += 1

class Player():
	def __init__(self,player_type=None,player_name=None):
		self.player_type = player_type
		self.player_name = player_name

	@staticmethod
	def assign_value(msg,expected_type,check_list,err_msg):
		parameter = None
		while not parameter:
			parameter = expected_type(input(msg))

			if (len(parameter) == 0) or (check_list and (not parameter in check_list)):
				parameter = None
				print(err_msg)
				continue

		return parameter

def main():
	# name_player = input("unesi ime igraca: ")

	def initialize_players(num_players):
		players = [Player() for x in range(num_players)]

		for (player,index) in enumerate(players):
			player.player_type = Player.assign_value(
				f"Igrac ({index}): (H)uman or (C)omputer? ",str,['H','C'],"Pogresan unos!")
			player.player_name = Player.assign_value(
				"Ime igraca? ",str,[],"Igrac mora imati ime!")

		return players

	players = initialize_players(2)

	name_player = "Gary"
	name_opponent = "DeepToe"
	print(f"\n{players[0].player_name} VS {players[1].player_name}\n")
	
	new_game = True
	while new_game:
		play(players)
		# TO DO: running score
		ask_new_game = input("\n> nova igra? (Y/N) ").upper()
		if ask_new_game == 'N':
			new_game = False
		elif ask_new_game == 'Y':
			new_game = True
		else:
			# TO DO: malo pametnije
			print("Greška! Izlaz.")
			new_game = False

main()
