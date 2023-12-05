# https://www.geeksforgeeks.org/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/

# function findBestMove(board):
#     bestMove = NULL
#     for each move in board :
#         if current move is better than bestMove
#             bestMove = current move
#     return bestMove

# function minimax(board, depth, isMaximizingPlayer):

#     if current board state is a terminal state :
#         return value of the board
    
#     if isMaximizingPlayer :
#         bestVal = -INFINITY 
#         for each move in board :
#             value = minimax(board, depth+1, false)
#             bestVal = max( bestVal, value) 
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

# Python3 program to find the next optimal move for a player 
player = 'x'
opponent = 'o'
empty = '-'

# This function returns true if there are moves 
# remaining on the board. It returns false if 
# there are no moves left to play. 
def isMovesLeft(board): 

	for i in range(3): 
		for j in range(3): 
			if (board[i][j] == empty): return True

	return False

# This is the evaluation function as discussed 
# in the previous article ( http://goo.gl/sJgv68 ) 
def evaluate(b) : 
	
	for row in range(3): # Checking for Rows
		if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
			if (b[row][0] == player): return 10
			elif (b[row][0] == opponent): return -10

	for col in range(3): # Checking for Cols
		if (b[0][col] == b[1][col] and b[1][col] == b[2][col]):
			if (b[0][col] == player): return 10
			elif (b[0][col] == opponent): return -10

	if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):  # Checking for Diag1
		if (b[0][0] == player): return 10
		elif (b[0][0] == opponent): return -10

	if (b[0][2] == b[1][1] and b[1][1] == b[2][0]): # Checking for Diag2 
		if (b[0][2] == player): return 10
		elif (b[0][2] == opponent): return -10

	return 0 # if none of them have won

# This is the minimax function. It considers all the possible ways
# the game can go and returns the value of the board
def minimax(board, depth, isMax) : 
	score = evaluate(board) 

	# If Maximizer has won the game return evaluated score
	if (score == 10): return score
	# If Minimizer has won the game return evaluated score
	if (score == -10): return score
	# If there are no more moves and no winner then it is a tie
	if (isMovesLeft(board) == False): return 0
	
	if (isMax): # If this maximizer's move
		best = -1000
		# Traverse all cells 
		for i in range(3):
			for j in range(3):
				if (board[i][j]==empty): # Check if cell is empty 
					board[i][j] = player # Make the move
					# Call minimax recursively and choose the maximum value 
					best = max(best,minimax(board,depth + 1,not isMax))
					board[i][j] = empty # Undo the move
		return best
	
	else: # If this minimizer's move
		best = 1000
		# Traverse all cells 
		for i in range(3):		 
			for j in range(3):				
				if (board[i][j] == empty): # Check if cell is empty									
					board[i][j] = opponent # Make the move 
					# Call minimax recursively and choose the minimum value 
					best = min(best, minimax(board, depth + 1, not isMax))					
					board[i][j] = empty # Undo the move
		return best 

# This will return the best possible move for the player
def findBestMove(board) : 
	bestVal = -1000
	bestMove = (-1, -1)
	# Traverse all cells, evaluate minimax function for
    # all empty cells and return the cell with optimal value. 
	for i in range(3):
		for j in range(3):			
			if (board[i][j]==empty): # Check if cell is empty				
				board[i][j] = player # Make the move
				# compute evaluation function for this move. 
				moveVal = minimax(board, 0, False)
				board[i][j] = empty # Undo the move

				# If the value of the current move is 
				# more than the best value, then update best/ 
				if (moveVal > bestVal):				 
					bestMove = (i, j) 
					bestVal = moveVal 

	print("The value of the best Move is :", bestVal) 
	print() 
	return bestMove 

def main():
    # Driver code 
    board = [ 
        [ 'x', 'o', 'x' ], 
        [ 'o', 'o', 'x' ], 
        [ '_', '_', '_' ] 
    ] 

    bestMove = findBestMove(board) 

    print("The Optimal Move is :") 
    print("ROW:", bestMove[0], " COL:", bestMove[1])

main()