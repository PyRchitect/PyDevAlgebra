import os
import random as rn
import itertools as it

class MBoard():
	values ={
		"hidden": 'X',
		"empty": ' ',
		"zero": 0,
		"bomb": 'B',
		"mark": 'M',
		"space": ' ',
		"sep": '|',
		"cross": '+'}

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

		self.bombs_pos_all = []
		self.bombs_pos_found = []

		self.marks_pos_all = []

		self.active = self.init_board(MBoard.values['hidden'])
		self.board = self.create_board(bombs)

	def display(self,board):
		board_display='|   |'
		# column titles
		for i in range(self.width):
			board_display+=f" {i:02d}|"

		for r in range(self.height):
			# row titles
			board_display+=f'\n| {r:02d}| '
			for c in range(self.width):
				value = board[r][c]
				color = Interface.palette[value]
				board_display+=color + f'{value}' + Interface.palette["ENDC"] +' | '

		print(board_display)
	
	def init_board(self,symbol):
		return [[symbol for _ in range(self.width)] for _ in range(self.height)]

	def create_board(self,bombs):
		# initialize board with zeroes
		board = self.init_board(MBoard.values['zero'])
	
		# populate board with bombs on random positions
		distribution = [*it.product(range(self.height),range(self.width))]		
		self.bombs_pos_all = rn.sample(distribution,k=bombs)
		for (r,c) in self.bombs_pos_all:
			board[r][c] = MBoard.values['bomb']

		# create perimeter around bombs
		for (r,c) in self.bombs_pos_all:
			for (rp,cp) in self.perimeter(r,c,type=8):
				if board[r+rp][c+cp] != MBoard.values['bomb']:
					board[r+rp][c+cp] += 1

		return board

	def perimeter(self,r,c,type=8):
		# reduce coordinates to cases (corner,side,inside):		
		def get_position(coordinate,dimension):
			if coordinate == 0:
				return 0
			elif coordinate < dimension-1:
				return 1
			else:
				return 2
			
		# point = [row,col]
		r = get_position(r,self.height)
		c = get_position(c,self.width)

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

		if t == 0 and a == MBoard.values['hidden']:			# if dig (left click)
			if v == MBoard.values['bomb']:					# dig bomb
				self.active[r][c] = v
				return 'lost'
			elif v > 0:										# dig num
				self.active[r][c] = v
				return 'dig'
			elif v == 0:									# dig empty
				self.flood_fill(r,c)
				return 'flood'

		elif t == 1:										# if mark (right click)
			if a == MBoard.values['hidden']:				# mark hidden
				self.active[r][c] = MBoard.values['mark']	# set mark
				if v == MBoard.values['bomb']:				# mark bomb
					self.bombs_pos_found.append([r,c])
					if self.get_bombs_remaining() == 0:
						return 'win'
					else:
						return 'bomb'
				else:										# mark not bomb
					return 'mark'
			
			elif a == MBoard.values['mark']:				# mark marked
				self.active[r][c] = MBoard.values['hidden']	# clear mark
				if v == MBoard.values['bomb']:				# unmark bomb
					self.bombs_pos_found.remove([r,c])
					return 'unmark'
				else:										# unmark not bomb
					return 'clear'
	
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

		if v == MBoard.values['bomb']:					# bomb: do nothing
			return										# do not reveal
		elif v > 0:										# on boundary: reveal
			self.active[r][c] = v						# reveal num
		elif v == 0:									# empty: dig, recurse
			self.active[r][c] = MBoard.values['empty']	# reveal empty
			# check perimeter around empty cells
			for (rp,cp) in self.perimeter(r,c,type=8):
				if self.active[r+rp][c+cp] == MBoard.values['hidden']:
					self.flood_fill(r+rp,c+cp)

class Interface():
	config = {
		"d_sep": '- ',
		"m_sep": 20,
		'h_sep': True,
		'h_space': 1,
		'v_sep': True,
		'v_space': 1}

	separator = config['d_sep'] * config['m_sep']

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
		MBoard.values['bomb']: '\x1b[0;37;41m',
		MBoard.values['mark']: '\x1b[0;37;40m',
		MBoard.values['empty']: '\x1b[0;37;40m',
		MBoard.values['hidden']: '\x1b[0;37;40m',
		MBoard.values['space']: '\x1b[0;37;40m',
		MBoard.values['sep']: '\x1b[0;37;40m',
		MBoard.values['cross']: '\x1b[0;37;40m',
		"ENDC": '\x1b[0m'}
	
	class Message():
		def __init__(self,text,sep=' ',end='\n'):
			self.text = text
			self.sep = sep
			self.end = end			
		
		def show(self):
			print(self.text,sep=self.sep,end=self.end)

	class SimpleGetter():
		def __init__(self,
			   choice_label='',
			   choice_sep=' ',
			   choice_type=None,
			   choice_test=None,
			   choice_error=None):
			
			self.choice_label = choice_label
			self.choice_sep = choice_sep
			self.choice_type = choice_type
			self.choice_test = choice_test
			self.choice_error = choice_error
		
		def get_input(self):
			i_test = False
			while i_test == False:
				try:
					Interface.Message(self.choice_label,end=' ').show()
					choice = input().split(self.choice_sep)

					if not self.choice_test:
						self.choice_test = [lambda x:x for _ in len(choice)]

					for i,c in enumerate(choice):
						c = self.choice_type[i](c)
						assert self.choice_test[i](c)						
						choice[i] = c
				except:
					Interface.Message(self.choice_error).show()
					i_test == False
				else:
					i_test = True
				finally:
					Interface.Message(Interface.separator)
			return choice

	class MultiGetter():
		def __init__(self,length,
			   choice_labels='',
			   choice_seps=' ',
			   choice_types=None,
			   choice_tests=None,
			   choice_errors=None):
			
			def init_list(L,length,default):
				return [default]*length if L==default else L

			choice_labels = init_list(choice_labels,length,'')
			choice_seps = init_list(choice_seps,length,'')
			choice_types = init_list(choice_types,length,None)
			choice_tests = init_list(choice_tests,length,None)
			choice_errors = init_list(choice_errors,length,None)

			self.getters = []
			for (cl,cs,ct,ctest,ce) in zip(
				choice_labels,
				choice_seps,
				choice_types,
				choice_tests,
				choice_errors):
				self.getters.append(Interface.SimpleGetter(cl,cs,ct,ctest,ce))
		
		def get_inputs(self):
			choices = []
			for g in self.getters:
				choices.append(g.get_input())
			return choices
			
	class Menu():
		def __init__(self,
			   title='',
			   options='',
			   choice_label='',
			   choice_sep=' ',
			   choice_type=None,
			   choice_test=None,
			   choice_error=None):

			self.title = title

			self.options = options

			self.getter = Interface.SimpleGetter(
				choice_label,
				choice_sep,
				choice_type,
				choice_test,
				choice_error)
		
		def show(self):
			Interface.Message('\n'+self.title).show()
			Interface.Message(Interface.separator).show()

			for option in self.options:
				Interface.Message(option).show()

			Interface.Message(Interface.separator).show()

			return Interface.SimpleGetter.get_input(self.getter)

class Menus():
	class MainMenu():
		def __init__(self):
			mc = MBoard.config
			self.menu = Interface.Menu()
			self.menu.title = "GLAVNI MENU"

			opt = []
			opt.append('[0] - izlaz')
			opt.append('[1] - beginner\t(09x09, B = 10)')
			opt.append('[2] - medium\t(16x16, B = 40)')
			opt.append('[3] - expert\t(30x60, B = 99)')
			c_dims = f"[{mc['w_min']}-{mc['w_max']}]x[{mc['h_min']}-{mc['h_max']}]"
			c_bombs = f"[{mc['w_min']*mc['h_min']}-{mc['w_max']*mc['h_max']}]"
			opt.append(f"[4] - custom\t({c_dims}, B = {c_bombs})")
			self.menu.options = opt

			g = Interface.SimpleGetter()
			g.choice_label = 'Odabir [0,1,2,3,4]: '
			g.choice_sep = ' '
			g.choice_type = (int,)
			g.choice_test = (lambda x: x in [0,1,2,3,4],)
			g.choice_error = 'Pogresan unos!'
			self.menu.getter = g
		
		def show(self):
			return self.menu.show()
	
	class CustomSize():
		def __init__(self):
			mc = MBoard.config

			labels = (
				f"Sirina [{mc['w_min']}-{mc['w_max']}] ",
				f"Visina [{mc['h_min']}-{mc['h_max']}] ")

			seps = (' ',' ')

			types = ((int,),(int,))

			tests = (
				(lambda x: (x>=mc['w_min'] and x<=mc['w_max']),),
				(lambda x: (x>=mc['h_min'] and x<=mc['h_max']),))

			errors = ('Pogresan unos!','Pogresan unos!')

			self.gwh = Interface.MultiGetter(2,labels,seps,types,tests,errors)
		
		def show(self):
			return self.gwh.get_inputs()

	class CustomBombs():
		def __init__(self,width,height):
			self.gb = Interface.SimpleGetter()
			self.gb.choice_label = f"Bombe [1-{width*height-1}] "
			self.gb.choice_sep = ' '
			self.gb.choice_type = (int,)
			self.gb.choice_test = (lambda x: (x>=1 and x<=width*height-1),)
			self.gb.choice_error = 'Pogresan unos!'

		def show(self):
			return self.gb.get_input()			

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

def quit_game():
	# all necessarry cleanup, db.op,etc.
	Interface.Message("Hvala i doviđenja.").show()
	exit()

def main():
	Interface.Message("MINESWEEPER").show()
	
	new_game = True
	while new_game:
		(new_game,) = Menus.MainMenu().show()

		if new_game == 0:
			quit_game()
		elif new_game == 1:
			play('b')
		elif new_game == 2:
			play('i')
		elif new_game == 3:
			play('e')
		elif new_game == 4:
			((width,),(height,)) = Menus.CustomSize().show()
			(bombs,) = Menus.CustomBombs(width,height).show()

			MBoard.difficulty['c']=(width,height,bombs)

			play('c')

main()