import os
import random as rn
import itertools as it

class MBoard():
	hidden = 'X'
	empty = ' '
	zero = 0
	bomb = 'B'
	mark = 'M'

	config = {
		'w_min':5,
		'w_max':30,
		'h_min':5,
		'h_max':30}

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

		self.active = self.init_board(MBoard.hidden)
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
				color = Interface.palette[value]
				board_display+=color + f'{value}' + Interface.palette["ENDC"] +' | '

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
			for p in self.perimeter(*b,type=8):
				if board[b[0]+p[0]][b[1]+p[1]] != MBoard.bomb:
					board[b[0]+p[0]][b[1]+p[1]] += 1

		return board

	def perimeter(self,pr,pc,type=8):
		# reduce coordinates to cases:		
		def get_position(coordinate,dimension):
			if coordinate == 0:
				return 0
			elif coordinate < dimension-1:
				return 1
			else:
				return 2
			
		# point = [row,col]
		r = get_position(pr,self.height)
		c = get_position(pc,self.width)

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
								[[1,2],		[1,2,3],	[2,3]],		# [r,d],	[r,d,l],	[d,l]
								[[0,1,2],	[0,1,2,3],	[0,2,3]],	# [u,r,d],	[all],		[u,d,l]
								[[0,1],		[0,1,3],	[0,3]]		# [u,r],	[u,r,l],	[u,l]
							]										# walk_direction[d]

		test_diagonals = 	[										# test dir. per cell
								[[1],		[1,2],		[2]],		# [dr],		[dr,dl],	[dl]
								[[0,1],		[0,1,2,3],	[2,3]],		# [ur,dr],	[all],		[ul,dl]
								[[0],		[0,3],		[3]]		# [ur],		[ur,ul],	[ul]
							]										# walk_direction[d]

		available = []
		for d in test_direction[r][c]:
			available.append(walk_direction[d])
		if type == 8:
			for d in test_diagonals[r][c]:
				available.append(walk_diagonals[d])
		
		return available

	def get_bombs_remaining(self):
		return len(self.bombs_pos_all) - len(self.bombs_pos_found)

	def evaluate_move(self,r,c,t):

		v = self.board[r][c]
		a = self.active[r][c]

		if t == 0 and a == MBoard.hidden:	# if dig
			if v == MBoard.bomb:
				self.active[r][c] = v
				return 'lost'
			if v > 0:
				self.active[r][c] = v
				return 'dig'
			else:
				self.flood_fill(r,c)
				return 'flood'

		elif t == 1 and a == MBoard.hidden:	# if mark
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
			self.active[r][c] = MBoard.hidden
			if v == MBoard.bomb:
				self.bombs_pos_found.remove([r,c])
			return 'unmark'
	
	def flood_fill(self,r,c):
		# # # # TEST
		# os.system('cls')
		# print()
		# self.display(self.board)
		# print()
		# self.display(self.active)
		# print()
		# # # # TEST
	
		v = self.board[r][c]
		# a = self.active[r][c]

		if v == MBoard.bomb:	# bomb: do nothing
			return
		elif v>0:				# on boundary: reveal
			self.active[r][c] = v
		else:					# empty: dig, recurse
			self.active[r][c] = MBoard.empty
			# check perimeter around empty cells
			for p in self.perimeter(r,c,type=8):
				# vektori kretanja mogu biti i negativnog smjera,
				# znači npr. 0 + (-1) = -1, a L[-1] je zapravo
				# zadnji element liste pa bi algoritam nastavio
				# flood fill na drugu stranu polja > OVERFLOW!
				# trebalo bi provjeriti r i c ostaju unutar ploče
				# > OVO JE SPRIJEČENO ODABIROM TOČNOG PERIMETRA
				if self.active[r+p[0]][c+p[1]] == MBoard.hidden:
					self.flood_fill(r+p[0],c+p[1])

class Interface(MBoard):
	config = {
		"d_sep" : '- '*20}

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
		MBoard.bomb: '\x1b[0;37;41m',
		MBoard.mark: '\x1b[38;5;52m',
		MBoard.empty: '\x1b[38;5;245m',
		MBoard.hidden: '\x1b[38;5;245m',
		"ENDC": '\x1b[0m'}

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

		print("\nMINESWEEPER")
		print(Interface.config['d_sep'])
		print("> UPUTA: r = ## red, c = ## stupac, t = tip poteza")
		print("> UPUTA: tip poteza: 0 = iskopaj, 1 = (od)markiraj")
		print("> UPUTA: za izlaz iz igre umjesto poteza unesi [x]")

	new_move = True
	while new_move == True:
		show_board()

		i_test=False
		while i_test == False:
			try:
				move = input("\n> unesi koordinate i tip poteza: [r c t] ili [x]: ")
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
				print(Interface.config['d_sep'])

		if new_move == True:
			result = mb.evaluate_move(r,c,t)

			if result == 'lost':
				show_board()
				print("\nBOOM!")
				new_move = False
			elif result == 'win':
				show_board()
				print("\nPOBJEDA!")
				new_move = False

def main():
	print("MINSWEEPER")
	
	new_game = True
	while new_game:
		print("\nGLAVNI MENU")
		print(Interface.config['d_sep'])
		print("[0] - izlaz")
		print("[1] - beginner\t(09x09, B = 10)")
		print("[2] - medium\t(16x16, B = 40)")
		print("[3] - expert\t(30x60, B = 99)")
		c_dims = f"[{MBoard.config['w_min']}-{MBoard.config['w_max']}]x[{MBoard.config['h_min']}-{MBoard.config['h_max']}]"
		c_bombs = f"[{MBoard.config['w_min']*MBoard.config['h_min']}-{MBoard.config['w_max']*MBoard.config['h_max']}]"
		print(f"[4] - custom\t({c_dims}, B = {c_bombs})")

		n_test = False
		while n_test == False:
			try:
				new_game = int(input("\n> Odabir [0,1,2,3,4] "))
				assert new_game in [0,1,2,3,4]
			except:
				print("Pogrešan unos!")
				n_test = False
			else:
				n_test = True
			finally:
				print(Interface.config['d_sep'])

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
					width = int(input(f"Sirina [{MBoard.config['w_min']}-{MBoard.config['w_max']}] "))
					assert width >= MBoard.config['w_min'] and width <= MBoard.config['w_max']

					height = int(input(f"Visina [{MBoard.config['h_min']}-{MBoard.config['h_max']}] "))
					assert height >= MBoard.config['h_min'] and height <= MBoard.config['h_max']
					
					bombs = int(input(f"Bombe [1-{width*height-1}] "))
					assert bombs >= 1 and bombs <= width*height-1
				except:
					print("Pogrešan unos!")
					c_test = False
				else:
					c_test = True
				finally:
					print(Interface.config['d_sep'])
			
			MBoard.difficulty['c']=(width,height,bombs)
		
			play('c')

main()