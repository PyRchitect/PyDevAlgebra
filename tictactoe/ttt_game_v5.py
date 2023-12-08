import math
import operator

NUM_PLAYERS = 2

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

def update(board,row,col,player):
	if board[row][col]==Player.marks[-1]:
		board[row][col]=Player.marks[player.player_index]
		return board

	raise TypeError

def is_moves_left(board):
	for i in range(3):
		for j in range(3):
			if (board[i][j] == Player.marks[-1]):
				return True

	return False

def evaluate(board):
	walk_direction = [[[1],[-1]],[[1],[0]],[[1],[1]],[[0],[1]]]
	def board_walk(board,x_pos,y_pos,dir): # direction [x][y]		
		return board[x_pos+dir[0]][y_pos+dir[1]]

	# rows, 
	# rows in transpose, 
	# 1st row in switch ii>i0 
	# 1st row in switch ii>i0 in transpose

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

def minimax(board,player_turn):

	score = evaluate(board)
	if (score != 0):
		return score # netko je pobijedio
	if (not is_moves_left(board)):
		return 0 # nema više poteza i nitko nije pobijedio > neriješeno

	if Player.minimax_setting[player_turn] == 'max': # Ako je Maximizer na potezu
		best = -math.inf
		best_func = max
	else: # Ako je Minimizer na potezu
		best = math.inf
		best_func = min

	for i in range(3):
		for j in range(3):
			if board[i][j] == Player.marks[-1]: # ćelija prazna?
				board[i][j] = Player.marks[player_turn] # napravi potez
				best = best_func(best,minimax(board,Player.switch_player(player_turn)))
				board[i][j] = Player.marks[-1] # vrati potez nakon testa

	return best

def find_best_move(board,player_turn):
	# vraća najbolji potez prema minimax algoritmu
	if Player.minimax_setting[player_turn] == 'max':
		best_score = -math.inf
		compare = operator.gt
	elif Player.minimax_setting[player_turn] == 'min':
		best_score = math.inf
		compare = operator.lt

	best_move = None
	# evaluate minimax function za sve prazne ćelije, vrati optimalnu
	for i in range(3):
		for j in range(3):
			if board[i][j] == Player.marks[-1]: # ćelija prazna?
				board[i][j] = Player.marks[player_turn] # napravi potez
				score = minimax(board,Player.switch_player(player_turn))
				board[i][j] = Player.marks[-1]	# vrati potez nakon testa
				if compare(score,best_score):	# ažuriraj ako je potez bolji
					best_move = (i, j)
					best_score = score

	return best_move

class Player():
	marks = ['X','O','-']
	# player 0 : 'X'
	# player 1 : 'O'
	# last(empty) : '-'
	minimax_setting = ['max','min']
	# player 0 : MAXIMIZER
	# player 1 : MINIMIZER

	def __init__(self,player_index,player_type=None,player_name=None):
		self.player_type = player_type
		self.player_name = player_name
		self.player_index = player_index

	@staticmethod
	def switch_player(index):
		return index +1 if index < NUM_PLAYERS-1 else 0

def play(players):

	def move_check(move,board):

		def board_check(x,y):
			return (x in [0,1,2] and y in [0,1,2])

		try:
			row = int(move.split(' ')[0])
			col = int(move.split(' ')[1])
		except ValueError:
			return (False, "Pogrešan unos!")

		if (not board_check(row,col)):
			return (False, "Potez van ploče!")

		if board[row][col]!=P3:
			return (False, "Polje nije prazno!")

		return (True,(row,col))

	def move_display(move,board,player):
		(row,col) = move
		board = update(board,row,col,player)
		show(board)
		score = evaluate(board)

		if score != 0:
			return (True,board,f"pobjeda {player.player_name}!")

		if is_moves_left(board):
			return (False,board,"slijedeci potez ...")

		return (True,board,"izjednaceno!")

	player_turn = 0
	move_count = 1

	board = initialize()
	show(board)

	print("\nUPUTA: potez se unosi u obliku (red, [0-2]) (stupac, [0-2]).")

	win_flag = False

	while not win_flag:
		print(f"\n> {move_count}. potez ({players[player_turn].player_name}): ",end='')

		if players[player_turn].player_type == 'H':
			(move_test,move) = move_check(input(),board)
			if not move_test:
				print(move)		# neuspješno unesen potez
				continue
		else:
			print()
			(move_test,move) = (True,find_best_move(board,player_turn))

		(win_flag,board,poruka) = move_display(move,board,players[player_turn])
		print(poruka)

		if win_flag:
			break

		player_turn = Player.switch_player(player_turn)
		move_count += 1

def assign_value(msg_input,expected_type,check_list,msg_error):

	parameter = None
	while not parameter:
		parameter = expected_type(input(msg_input))

		if (len(parameter) == 0) or (check_list and (not parameter in check_list)):
			parameter = None
			print(msg_error)
			continue

	return parameter

def main():

	def initialize_players():
		players = [Player(x) for x in range(NUM_PLAYERS)]

		for (index,player) in enumerate(players):
			player.player_type = assign_value(
				f"Igrac ({index+1}): (H)uman or (C)omputer? ",str,['h','H','c','C'],"Pogresan unos!")
			player.player_name = assign_value(
				"Ime igraca? ",str,[],"Igrac mora imati ime!")

		return players

	players = initialize_players()

	print(f"\n{players[0].player_name} VS {players[1].player_name}\n")

	new_game = True
	while new_game:
		play(players)

		new_game = assign_value("\n> nova igra? (Y/N) ",str,['y','Y','n','N'],"Pogrešan unos!")

		if new_game in ['n','N']:
			new_game = False

main()
