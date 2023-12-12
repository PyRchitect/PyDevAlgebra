# https://www.geeksforgeeks.org/introduction-to-evaluation-function-of-minimax-algorithm-in-game-theory/

# evaluation function for Tic Tac Toe Game
# Returns a value based on who is winning
# b[3][3] is the Tic-Tac-Toe board
 
def evaluate(b):
	
	for row in range(0, 3): # Checking for Rows
		if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
			if b[row][0] == 'x': return 10
			elif b[row][0] == 'o': return -10
	
	for col in range(0, 3): # Checking for Columns
		if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
			if b[0][col]=='x': return 10
			elif b[0][col] == 'o': return -10
	
	if b[0][0] == b[1][1] and b[1][1] == b[2][2]: # Checking for Diagonal1
		if b[0][0] == 'x': return 10
		elif b[0][0] == 'o':return -10
	
	if b[0][2] == b[1][1] and b[1][1] == b[2][0]: # Checking for Diagonal2	
		if b[0][2] == 'x': return 10
		elif b[0][2] == 'o': return -10
	
	return 0 # if none of them have won

# Driver code 
if __name__ == "__main__":
	board = [['x', '-', 'o'], 
			['-', 'x', 'o'], 
			['-', '-', '-']]
	value = evaluate(board)
	print("The value of this board is", value)

	board = [['x', '-', 'o'], 
			['-', 'x', 'o'], 
			['-', '-', 'o']]
	value = evaluate(board)
	print("The value of this board is", value)
	board = [['x', '-', 'o'], 
			['-', 'x', 'o'], 
			['-', '-', 'x']]
	
	value = evaluate(board)  
	print("The value of this board is", value)