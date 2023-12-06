import math

p1 = 'O' # maximizer
p2 = 'X' # minimizer
pn = '-' # prazna

def initialize():
	return [[pn for x in range(3)] for y in range(3)]

def show(board):
	board_display = ''

	for i in range(3):
		board_display+='\n| '
		for j in range(3):
			board_display+=f'{board[i][j]} | '

	print(board_display[1:])	

def update(board,row,col,mark):
	if board[row][col]==pn:
		board[row][col]=mark
		return board
	else:
		raise TypeError

def isMovesLeft(board): 
	# vraća true/false ako se može/ne može igrati još poteza
	# testira ima li praznih ćelija, ako nađe neku vraća true

	for i in range(3): 
		for j in range(3): 
			if (board[i][j] == pn): return True

	return False

def evaluate(board):
	# evaluation function: tko pobjeđuje? b[3][3] je TTT ploča
	# MOŽE SE OPTIMIZIRATI I SKRATITI, ali nebitno je za sada
	
	for row in range(3): # Rows
		if (board[row][0] == board[row][1] and board[row][1] == board[row][2]):
			if (board[row][0] == p1): return 1
			elif (board[row][0] == p2): return -1

	for col in range(3): # Cols
		if (board[0][col] == board[1][col] and board[1][col] == board[2][col]):
			if (board[0][col] == p1): return 1
			elif (board[0][col] == p2): return -1

	if (board[0][0] == board[1][1] and board[1][1] == board[2][2]): # Diag(\)
		if (board[0][0] == p1): return 1
		elif (board[0][0] == p2): return -1

	if (board[0][2] == board[1][1] and board[1][1] == board[2][0]): # Diag(/)
		if (board[0][2] == p1): return 1
		elif (board[0][2] == p2): return -1

	return 0 # ako si tu, nitko nije pobijedio

def minimax(board, depth, isMax):
	# minimax function: gleda sve načine na koje se ploča
	# može razviti i vraća vrijednost ploče
	score = evaluate(board)	
	if (score == 1): return score # Maximizer je pobijedio
	if (score ==-1): return score # Minimizer je pobijedio
	# nema više poteza, nitko nije pobijedio > neriješeno
	if (isMovesLeft(board) == False): return 0
	
	if (isMax): # Ako je Maximizer na potezu
		best = -math.inf
		for i in range(3):
			for j in range(3):
				if (board[i][j]==pn): # ćelija prazna?
					board[i][j] = p1 # napravi potez
					# minimax rekurzivno > odaberi max vrijednost 
					best = max(best,minimax(board,depth + 1,not isMax))
					board[i][j] = pn # vrati potez nakon testa
		return best
	
	else:  # Ako je Minimizer na potezu
		best = math.inf
		for i in range(3):		 
			for j in range(3):				
				if (board[i][j] == pn): # ćelija prazna?
					board[i][j] = p2 # napravi potez
					# minimax rekurzivno > odaberi min vrijednost
					best = min(best, minimax(board, depth + 1, not isMax))
					board[i][j] = pn # vrati potez nakon testa
		return best 

def findBestMove(board):
	# vraća najbolji potez prema minimax algoritmu
	bestScore = -math.inf
	bestMove = None
	# evaluate minimax function za sve prazne ćelije, vrati optimalnu
	for i in range(3):
		for j in range(3):			
			if board[i][j] == pn: # ćelija prazna?
				board[i][j] = p1 # napravi potez
				score = minimax(board, 0, False) # evaluate
				board[i][j] = pn # vrati potez nakon testa
				# ako je vrijednost veća od trenutnog najboljeg, ažuriraj
				if (score > bestScore):				 
					bestMove = (i, j) 
					bestScore = score

	# TEST
	# print("Vrijednost najboljeg poteza: ", bestScore) 
	# TEST
	print() 
	return bestMove

def play(name_player,name_opponent):		

	def move_check(move,board):
		input_check = lambda x,y : (x in [0,1,2] and y in [0,1,2])

		try:
			row = int(move.split(' ')[0])
			col = int(move.split(' ')[1])
		except:
			return (False, "Pogrešan unos!")
		
		if (not input_check(row,col)):
			return (False, "Potez van ploče!")

		if board[row][col]!=pn:
			return (False, "Polje nije prazno!")

		return (True,(row,col))

	def move_display(move,board,player_name,player):
		board = update(board,*move[1],player)
		show(board)
		score = evaluate(board)		
		
		if score != 0:			
			return (True,board,f"pobjeda {player_name}!")
		else:
			if isMovesLeft(board):
				return (False,board,"slijedeci potez ...")
			else:
				return (True,board,f"izjednaceno!")

	
	board = initialize()
	move_count = 1	
	show(board)

	print("\nUPUTA: potez se unosi u obliku (red, [0-2]) (stupac, [0-2]).")

	win_flag = False
	while win_flag == False:
		# prvi igra čovjek (za sada)
		move = input(f"\n> {move_count}. potez ({name_player}): ")
		move = move_check(move,board)

		if not move[0]:
			# neuspješno unesen potez
			print(move[1])
			continue
		else:
			# uspješno unesen potez
			(win_flag,board, poruka)= move_display(move,board,name_player,p2)
			print(poruka)
		
		if win_flag == True: break
		
		# drugi igra kompjuter (za sada)
		print(f"> {move_count}. potez ({name_opponent}): ")
		(row,col) = findBestMove(board)
		(win_flag,board, poruka)= move_display((True,(row,col)),board,name_opponent,p1)
		print(poruka)

		if win_flag == True: break

		move_count += 1	

def main():
	# name_player = input("unesi ime igraca: ")
	name_player = "Gary"
	name_opponent = "DeepToe"
	print(f"\n{name_player} VS {name_opponent}\n")
	# TO DO: čovjek P1 ili P2?
	new_game = True
	while new_game:
		play(name_player,name_opponent)
		# TO DO: running score
		ask_new_game = input("\n> nova igra? (Y/N) ")
		if ask_new_game == 'N':
			new_game = False
		elif ask_new_game == 'Y':
			new_game = True
		else:
			# TO DO: malo pametnije
			print("Greška! Izlaz.")
			new_game = False

main()