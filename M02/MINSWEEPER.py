import os
import random as rn
import itertools as it

display_separator = '- '*10

width_min = 5
width_max = 30

height_min = 5
height_max = 30

class MBoard():
	empty = '-'
	zero = 0
	bomb = 'B'
	mark = 'M'

	palette = {
		0: '\x1b[38;5;245m',
		1: '\x1b[1;34;40m',
		2: '\x1b[1;32;40m',
		3: '\x1b[1;31;40m',
		4: '\x1b[1;33;40m',
		5: '\x1b[1;35;40m',
		6: '\x1b[1;37;40m',
		7: '\x1b[1;36;40m',
		8: '\x1b[1;30;40m',
		bomb: '\x1b[0;37;41m',
		mark: '\x1b[38;5;52m',
		empty: '\x1b[38;5;245m'
	}
	ENDC = '\x1b[0m'

	# [width,height,bombs] ; custom appends with key 'c'
	difficulty = {
		'b':(9,9,10),
		'i':(16,16,40),
		'e':(30,16,99)}

	def __init__(self,d_key):
		(self.width,self.height,bombs) = MBoard.difficulty[d_key]
		self.bombs_pos_all = []	# fill through board creation

		self.bombs_pos_found = []
		self.marks_pos_all = []

		self.active = self.init_board(MBoard.empty)
		self.board = self.create_board(bombs)
		self.test = 't'

	def display(self,board):
		board_display = ''

		board_display+='\n|   |'
		# naslovi stupaca
		for i in range(self.width):
			board_display+=f" {i:02d}|"

		for r in range(self.height):
			board_display+=f'\n| {r:02d}| '
			for c in range(self.width):
				value = board[r][c]
				color = MBoard.palette[value]
				board_display+=color + f'{value}' + MBoard.ENDC +' | '

		print(board_display[1:])
	
	def init_board(self,symbol):
		return [[symbol for _ in range(self.width)] for _ in range(self.height)]

	def create_board(self,bombs):
		# create board with zeroes
		board = self.init_board(MBoard.zero)
	
		# populate board with bombs
		distribution = [*it.product(range(self.height),range(self.width))]		
		self.bombs_pos_all = rn.sample(distribution,k=bombs)
		for b in self.bombs_pos_all:
			board[b[0]][b[1]] = MBoard.bomb

		# create perimeter around bombs
		for b in self.bombs_pos_all:
			for p in self.perimeter(b,type=8):
				if board[b[0]+p[0]][b[1]+p[1]] != MBoard.bomb:
					board[b[0]+p[0]][b[1]+p[1]] += 1

		return board	

	def perimeter(self,point,type=8):
		# point = [row,col]
		# type = 4 (only directions), 8 (with diagonals)
		if type not in [4,8]:
			raise ValueError("Incorrect type!")

		walk_direction = 	[				# [move_r, move_c]
								[-1,0],		# up,
								[0,1],		# right
								[1,0],		# down
								[0,-1]		# left
							]

		walk_diagonals = 	[				# [move_r, move_c]
								[-1,1],		# diag - up + right
								[1,1],		# diag - down + right
								[1,-1],		# diag - down + left
								[-1,-1]		# diag - up + left
							]

		test_direction = 	[										# test dir. per cell
								[[1,3],		[1,2,3],	[2,3]],		# [r,d],	[r,d,l],	[d,l]
								[[0,1,2],	[0,1,2,3],	[0,2,3]],	# [u,r,d],	[all],		[u,d,l]
								[[0,1],		[0,1,3],	[0,3]]		# [u,r],	[u,r,l],	[u,l]
							]										# walk_direction[d]

		test_diagonals = 	[										# test dir. per cell
								[[1],		[1,2],		[2]],		# [dr],		[dr,dl],	[dl]
								[[0,1],		[0,1,2,3],	[2,3]],		# [ur,dr],	[all],		[ul,dl]
								[[0],		[0,3],		[3]]		# [ur],		[ur,ul],	[ul]
							]										# walk_direction[d]

		# reduce coordinates to cases:		
		def get_position(coordinate,dimension):
			if coordinate == 0:
				return 0
			elif coordinate < dimension-1:
				return 1
			else:
				return 2
		
		p = [get_position(point[0],self.height),get_position(point[1],self.width)]

		available = []
		for d in test_direction[p[0]][p[1]]:
			available.append(walk_direction[d])
		if type == 8:
			for d in test_diagonals[p[0]][p[1]]:
				available.append(walk_diagonals[d])
		
		return available

	def get_bombs_remaining(self):
		return len(self.bombs_pos_all) - len(self.bombs_pos_found)

	def evaluate_move(self,r,c,t):

		v = self.board[r][c]
		a = self.active[r][c]

		if t == 0 and a == MBoard.empty:		# if dig
			self.active[r][c] = v
			if v == MBoard.bomb:
				return 'lost'
			if v > 0:
				return 'dig'
			else:
				# self.flood_fill([r,c])
				return 'flood'

		elif t == 1 and a == MBoard.empty:	# if mark
			self.active[r][c] = MBoard.mark
			if v == MBoard.bomb:
				self.bombs_pos_found.append([r,c])
				if self.get_bombs_remaining() == 0:
					return 'win'
				else:
					return 'bomb'
			else:
				return 'mark'
		
		elif t == 1 and a == MBoard.mark:
			self.active[r][c] = MBoard.empty
			return 'unmark'
	
	def flood_fill(self,point):
		...
		

def play(difficulty):
	mb = MBoard(difficulty)
	
	def show_board():
		os.system('cls')
		print("\nINICIJALIZIRANA PLOCA")
		mb.display(mb.board)
		print("> OTVORENA ZA TESTIRANJE")

		print("\nAKTIVNA PLOCA")
		mb.display(mb.active)
		print(f"> PREOSTALO BOMBI: {mb.get_bombs_remaining()}")

		print("MINESWEEPER")
		print(display_separator)
		print("> UPUTA: tip poteza [0]: iskopaj, [1]: (od)markiraj")
		print("> UPUTA: za izlaz iz igre unesi [x]")

	new_move = True
	while new_move == True:
		show_board()

		i_test=False
		while i_test == False:
			try:
				move = input("\n> unesi koordinate i tip poteza: [r c 0|1]:")
				if move.upper() =='X':
					new_move = False
					break

				move = move.split()

				assert len(move)==3
				(r,c,t) = map(int,move)
				assert r >= 0 and r < mb.height
				assert c >= 0 and c < mb.width
				assert t in [0,1]
			except:
				print("Pogrešan unos!")
				i_test = False
			else:
				i_test = True
			finally:
				print(display_separator)

		if new_move == True:
			result = mb.evaluate_move(r,c,t)

			if result == 'lost':
				show_board()
				print("\nBOOM!")
				new_move = False
			elif result == 'win':
				show_board()
				print("\nYOU WON!")
				new_move = False

def main():
	print("MINSWEEPER")
	
	new_game = True
	while new_game:
		print("\nGLAVNI MENU")
		print(display_separator)
		print("[0] - izlaz")
		print("[1] - easy (9x9,B=10)")
		print("[2] - intermediate (16x16,B=40)")
		print("[3] - expert (30x60,B=99)")
		print("[4] - custom (#x#)")

		n_test = False
		while n_test == False:
			try:
				new_game = int(input("Odabir [0,1,2,3,4] "))
				assert new_game in [0,1,2,3,4]
			except:
				print("Pogrešan unos!")
				n_test = False
			else:
				n_test = True
			finally:
				print(display_separator)

		if new_game == 0:
			print("Hvala i doviđenja.")
			break
		elif new_game == 1:
			play('b')
		elif new_game == 2:
			play('i')
		elif new_game == 3:
			play('e')
		elif new_game == 4:
			c_test = False
			while c_test == False:
				try:
					width = int(input(f"Sirina [{width_min}-{width_max}] "))
					assert width >= width_min and width <= width_max

					height = int(input(f"Visina [{height_min}-{height_max}] "))
					assert height >= height_min and height <= height_max
					
					bombs = int(input(f"Bombe [1-{width*height-1}] "))					
					assert bombs >= 1 and bombs <= width*height-1
				except:
					print("Pogrešan unos!")
					c_test = False
				else:
					c_test = True
				finally:
					print(display_separator)
			
			MBoard.difficulty['c']=(width,height,bombs)
		
			play('c')

main()