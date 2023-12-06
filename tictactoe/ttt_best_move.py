# https://www.geeksforgeeks.org/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/

# https://levelup.gitconnected.com/mastering-tic-tac-toe-with-minimax-algorithm-3394d65fa88f

# function findBestMove(board):
#     bestMove = NULL
#     for each move in board :
#         if current move is better than bestMove
#             bestMove = current move
#     return bestMove

# function minimax(board, depth, isMaximizingPlayer):

#     if current board state is a terminal state:
#         return value of the board
    
#     if isMaximizingPlayer :
#         bestVal = -INFINITY 
#         for each move in board :
#             value = minimax(board, depth+1, false)
#             bestVal = max(bestVal, value) 
#         return bestVal

#     else :
#         bestVal = +INFINITY 
#         for each move in board :
#             value = minimax(board, depth+1, true)
#             bestVal = min( bestVal, value) 
#         return bestVal

# function isMovesLeft(board):
#     for each cell in board:
#         if current cell is empty:
#             return true
#     return false

import math

px = 'X' # maximizer
po = 'O' # minimizer
pn = '-' # prazna

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
			if (board[row][0] == px): return 1
			elif (board[row][0] == po): return -1

	for col in range(3): # Cols
		if (board[0][col] == board[1][col] and board[1][col] == board[2][col]):
			if (board[0][col] == px): return 1
			elif (board[0][col] == po): return -1

	if (board[0][0] == board[1][1] and board[1][1] == board[2][2]): # Diag(\)
		if (board[0][0] == px): return 1
		elif (board[0][0] == po): return -1

	if (board[0][2] == board[1][1] and board[1][1] == board[2][0]): # Diag(/)
		if (board[0][2] == px): return 1
		elif (board[0][2] == po): return -1

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
					board[i][j] = px # napravi potez
					# minimax rekurzivno > odaberi max vrijednost 
					best = max(best,minimax(board,depth + 1,not isMax))
					board[i][j] = pn # vrati potez nakon testa
		return best
	
	else:  # Ako je Minimizer na potezu
		best = math.inf
		for i in range(3):		 
			for j in range(3):				
				if (board[i][j] == pn): # ćelija prazna?
					board[i][j] = po # napravi potez
					# minimax rekurzivno > odaberi min vrijednost
					best = min(best, minimax(board, depth + 1, not isMax))
					board[i][j] = pn # vrati potez nakon testa
		return best 

def findBestMove(board) : 
	# vraća najbolji potez prema minimax algoritmu
	bestScore = -math.inf
	bestMove = None
	# evaluate minimax function za sve prazne ćelije, vrati optimalnu
	for i in range(3):
		for j in range(3):			
			if board[i][j] == pn: # ćelija prazna?
				board[i][j] = px # napravi potez				
				score = minimax(board, 0, False) # evaluate
				# TEST
				print(i,j,board[i][j],score)
				# TEST
				board[i][j] = pn # vrati potez nakon testa
				# ako je vrijednost veća od trenutnog najboljeg, ažuriraj
				if (score > bestScore):				 
					bestMove = (i, j) 
					bestScore = score

	# TEST
	print("Vrijednost najboljeg poteza: ", bestScore) 
	# TEST
	print() 
	return bestMove

def main_test():
    # Driver code 
    board = [ 
        [px,po,px], 
        [po,po,px], 
        [pn,pn,pn]]

    bestMove = findBestMove(board) 

    print("The Optimal Move is :") 
    print("ROW:", bestMove[0], " COL:", bestMove[1])

main_test()