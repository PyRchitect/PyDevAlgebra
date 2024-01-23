import os
import random as rn
import itertools as it

class Board():
	config = {
		'w_min':5,
		'w_max':30,
		'h_min':5,
		'h_max':30}

	values ={
		"zero": 0,
		"hidden": 'X',
		"empty": ' ',
		"bomb": 'B',
		"mark": 'M'}

	# [width,height,bombs] ; custom appends with key 'c'
	difficulty = {
		'b':(9,9,10),
		'i':(16,16,40),
		'e':(30,16,99)}

	def __init__(self,d_key):
		(self.width,self.height,bombs) = Board.difficulty[d_key]

		self.bombs_pos_all = []
		self.bombs_pos_found = []

		self.marks_pos_all = []

		self.active = self.init_board(Board.values['hidden'])
		self.real = self.create_board(bombs)
	
	def init_board(self,symbol):
		return [[symbol for _ in range(self.width)] for _ in range(self.height)]

	def create_board(self,bombs):
		# initialize board with zeroes
		board = self.init_board(Board.values['zero'])
	
		# populate board with bombs on random positions
		distribution = [*it.product(range(self.height),range(self.width))]		
		self.bombs_pos_all = rn.sample(distribution,k=bombs)
		for (r,c) in self.bombs_pos_all:
			board[r][c] = Board.values['bomb']

		# create perimeter around bombs
		for (r,c) in self.bombs_pos_all:
			for (rp,cp) in self.perimeter(r,c,type=8):
				if board[r+rp][c+cp] != Board.values['bomb']:
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

		v = self.real[r][c]
		a = self.active[r][c]

		if t == 0 and a == Board.values['hidden']:			# if dig (left click)
			if v == Board.values['bomb']:					# dig bomb
				self.active[r][c] = v
				return 'lost'
			elif v > 0:										# dig num
				self.active[r][c] = v
				return 'dig'
			elif v == 0:									# dig empty
				self.flood_fill(r,c)
				return 'flood'

		elif t == 1:										# if mark (right click)
			if a == Board.values['hidden']:				# mark hidden
				self.active[r][c] = Board.values['mark']	# set mark
				if v == Board.values['bomb']:				# mark bomb
					self.bombs_pos_found.append([r,c])
					if self.get_bombs_remaining() == 0:
						return 'win'
					else:
						return 'bomb'
				else:										# mark not bomb
					return 'mark'
			
			elif a == Board.values['mark']:				# mark marked
				self.active[r][c] = Board.values['hidden']	# clear mark
				if v == Board.values['bomb']:				# unmark bomb
					self.bombs_pos_found.remove([r,c])
					return 'unmark'
				else:										# unmark not bomb
					return 'clear'
	
	def flood_fill(self,r,c):
	
		v = self.real[r][c]
		# a = self.active[r][c]

		if v == Board.values['bomb']:					# bomb: do nothing
			return										# do not reveal
		elif v > 0:										# on boundary: reveal
			self.active[r][c] = v						# reveal num
		elif v == 0:									# empty: dig, recurse
			self.active[r][c] = Board.values['empty']	# reveal empty
			# check perimeter around empty cells
			for (rp,cp) in self.perimeter(r,c,type=8):
				if self.active[r+rp][c+cp] == Board.values['hidden']:
					self.flood_fill(r+rp,c+cp)

class Interface():
	config = {
		"d_sep": '- ',
		"m_sep": 20}

	separator = config['d_sep'] * config['m_sep']
	
	class SimpleMessage():
		def __init__(self,
			   text='',
			   sep=' ',
			   end='\n'):

			self.text = text
			self.sep = sep
			self.end = end			

		def show(self):
			print(self.text,sep=self.sep,end=self.end)

	class MultiMessage():
		def __init__(self,
			   lines='',
			   seps=' ',
			   ends='\n',
			   length=0):
			
			length = length or len(lines)
						
			def init_list(L,length,default):
				return [default]*length if L==default else L
			
			lines = init_list(lines,length,'')
			seps = init_list(seps,length,' ')
			ends = init_list(ends,length,'\n')

			self.messages = []
			for (l,s,e) in zip(lines,seps,ends):
				self.messages.append(Interface.SimpleMessage(l,s,e))
		
		def show(self):
			for m in self.messages:
				m.show()

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
					Interface.SimpleMessage(self.choice_label,end=' ').show()
					choice = input().split(self.choice_sep)

					if not self.choice_test:
						self.choice_test = [lambda x:x for _ in len(choice)]

					for i,c in enumerate(choice):
						c = self.choice_type[i](c)
						assert self.choice_test[i](c)						
						choice[i] = c
				except:
					Interface.SimpleMessage(self.choice_error).show()
					i_test == False
				else:
					i_test = True
				finally:
					Interface.SimpleMessage(Interface.separator)
			return choice

	class MultiGetter():
		def __init__(self,
			   choice_labels='',
			   choice_seps=' ',
			   choice_types=None,
			   choice_tests=None,
			   choice_errors=None,
			   length=0):
			
			length = length or len(choice_labels)
			
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
			Interface.SimpleMessage('\n'+self.title).show()
			Interface.SimpleMessage(Interface.separator).show()

			for option in self.options:
				Interface.SimpleMessage(option).show()

			Interface.SimpleMessage(Interface.separator).show()

			return Interface.SimpleGetter.get_input(self.getter)

class Menus():
	class MainMenu():
		def __init__(self):
			mc = Board.config
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
			mc = Board.config

			labels = (
				f"> Sirina [{mc['w_min']}-{mc['w_max']}] ",
				f"> Visina [{mc['h_min']}-{mc['h_max']}] ")

			seps = (' ',' ')

			types = ((int,),(int,))

			tests = (
				(lambda x: (x>=mc['w_min'] and x<=mc['w_max']),),
				(lambda x: (x>=mc['h_min'] and x<=mc['h_max']),))

			errors = ('Pogresan unos!','Pogresan unos!')

			self.gwh = Interface.MultiGetter(labels,seps,types,tests,errors)
		
		def show(self):
			return self.gwh.get_inputs()

	class CustomBombs():
		def __init__(self,width,height):
			self.gb = Interface.SimpleGetter()
			self.gb.choice_label = f"> Bombe [1-{width*height-1}] "
			self.gb.choice_sep = ' '
			self.gb.choice_type = (int,)
			self.gb.choice_test = (lambda x: (x>=1 and x<=width*height-1),)
			self.gb.choice_error = 'Pogresan unos!'

		def show(self):
			return self.gb.get_input()			

	class GetMove():
		def __init__(self,width,height):
			self.move = Interface.SimpleGetter()
			self.move.choice_label = "\n> unesi koordinate i tip poteza: [r c t] ili [x]: "
			self.move.choice_sep = ' '
			self.move.choice_type = (str,int,int,)
			self.move.choice_test = (
				lambda r: r=='x' or (int(r)>=0 and int(r)<=height),
				lambda c: (c>=0 and c<=width),
				lambda t: t in [0,1],)
			self.move.choice_error = 'Pogresan unos!'
		
		def show(self):
			result = self.move.get_input()
			r = result[0]
			if r != 'x':
				(r,c,t) = result
				return (int(r),c,t)
			else:
				return (r,'','')

class Graphics():
	config = {
		'h_separate': False,
		'h_spacing': 1,
		'v_separate': True,
		'v_spacing': 0,
		'value_width': 1,
		'axis_name_width':2}

	values ={
		"h_space": ' ',
		"v_space": ' ',
		"h_sep": '|',
		"v_sep": '-',
		"cross": '+',
		"corner": 'X'}

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
		Board.values['hidden']: '\x1b[0;37;40m',
		Board.values['empty']: '\x1b[0;37;40m',
		Board.values['bomb']: '\x1b[0;37;41m',
		Board.values['mark']: '\x1b[38;5;52m',
		values['h_space']: '\x1b[0;37;40m',
		values['v_space']: '\x1b[0;37;40m',
		values['h_sep']: '\x1b[0;37;40m',
		values['v_sep']: '\x1b[0;37;40m',
		values['cross']: '\x1b[0;37;40m',
		values['corner']: '\x1b[0;37;40m',
		"ENDC": '\x1b[0m'}

	def __init__(self):
		...
	
	def render(self,board:'Board',board_type):
		if board_type not in ['real','active']:
			raise ValueError("board: real or active")
		elif board_type == 'real':
			board_chosen = board.real
		elif board_type == 'active':
			board_chosen = board.active

		# short names for containters
		gc = Graphics.config
		gv = Graphics.values

		# if separate false override separator to none
		sep = gv['h_sep'] if gc['v_separate'] == True else ' '

		# short names for common values
		# value cells
		vhs = gc['h_spacing']*gv['h_space']
		vhst = vhs+gc['value_width']*gv['h_space']+vhs
		# separator cells
		shs = gc['h_spacing']+gc['value_width']+gc['h_spacing']
		shst = shs*gv['v_sep']
		# title cells
		ths = (gc['h_spacing']+(gc['value_width']-gc['axis_name_width']))*gv['h_space']
		thst = vhs+"{value:0{width}}"+ths

		def add_separator_row():
			board_separator = ""

			# blank rows
			if gc['v_spacing']:
				for _ in range(gc['v_spacing']):
					board_separator+='\n'+sep
					for _ in range(board.width+2):
						board_separator+=vhst+sep
			
			# separator row:
			if gc['h_separate']:
				board_separator+='\n'+gv['cross']
				for _ in range(board.width+2):
					board_separator+=shst+gv['cross']

			# blank rows
			if gc['v_spacing']:
				for _ in range(gc['v_spacing']):
					board_separator+='\n'+sep
					for _ in range(board.width+2):
						board_separator+=vhst+sep
			
			return board_separator

		def add_corner_cell():
			return vhs+gc['value_width']*gv['corner']+vhs+sep

		def add_column_titles():
			board_titles = ""
			for i in range(board.width):
				board_titles+=thst.format(value=i,width=gc['axis_name_width'])+sep
			return board_titles

		def add_title_row():
			board_title = ""
			# corner cell
			board_title+=add_corner_cell()
			# column titles
			board_title+=add_column_titles()
			# corner cell
			board_title+=add_corner_cell()
			return board_title

		def add_row_titles(r):
			return thst.format(value=r,width=gc['axis_name_width'])+sep

		def add_value_cells(r):
			cell_display = ""
			for c in range(board.width):
				value = board_chosen[r][c]
				color_start = Graphics.palette[value]
				color_end = Graphics.palette["ENDC"]

				cell_display+=vhs+color_start+str(value)+color_end+vhs+sep
			return cell_display

		# start empty
		board_display = ''

		board_display+=sep
		# title row
		board_display+=add_title_row()
		# separate from values
		board_display+=add_separator_row()

		for r in range(board.height):
			board_display+='\n'+sep
			# row titles
			board_display+=add_row_titles(r)
			# value cells
			board_display+=add_value_cells(r)
			# row titles
			board_display+=add_row_titles(r)
			# separate from next row
			board_display+=add_separator_row()

		board_display+='\n'+sep
		# title row
		board_display+=add_title_row()

		print(board_display)

class Game():
	title = "MINESWEEPER"

	BEGINNER = 'b'
	INTERMEDIATE = 'i'
	EXPERT = 'e'
	CUSTOM = 'c'	

	def __init__(self):
		self.board = None
		self.menus = Menus()
		self.graphics = Graphics()
	
	def init_game(self,difficulty,settings):
		if difficulty == Game.CUSTOM:
			# appends/modifies 'custom' key in Board
			Board.difficulty[Game.CUSTOM] = settings
		self.board = Board(difficulty)
	
	def quit_game(self):
		Interface.SimpleMessage("Hvala i doviđenja").show()
		exit()

def play(ms:'Game'):
	
	def show_board():
		nonlocal ms

		os.system('cls')
		# # # TEST
		Interface.SimpleMessage("\nINICIJALIZIRANA PLOCA").show()
		ms.graphics.render(ms.board,'real')
		Interface.SimpleMessage("> OTVORENA ZA TESTIRANJE").show()
		# # # TEST

		Interface.SimpleMessage("\nAKTIVNA PLOCA").show()
		ms.graphics.render(ms.board,'active')
		Interface.SimpleMessage(f"> PREOSTALO BOMBI: {ms.board.get_bombs_remaining()}").show()

		lines = []
		lines.append('\n'+ms.title)
		lines.append(Interface.separator)
		lines.append("> UPUTA: r = ## red, c = ## stupac, t = tip poteza")
		lines.append("> UPUTA: tip poteza: 0 = iskopaj, 1 = (od)markiraj")
		lines.append("> UPUTA: za izlaz iz igre umjesto poteza unesi [x]")
		Interface.MultiMessage(lines).show()

	new_move = True	
	while new_move == True:
		show_board()

		(r,c,t) = ms.menus.GetMove(ms.board.width,ms.board.height).show()

		if str(r).upper() == 'X':
			new_move=False
			break

		if new_move == True:
			result = ms.board.evaluate_move(r,c,t)

			if result == 'lost':
				show_board()
				Interface.SimpleMessage("\nBOOM!").show()
				new_move = False
			elif result == 'win':
				show_board()
				Interface.SimpleMessage("\nPOBJEDA!").show()
				new_move = False

def main():
	ms = Game()

	os.system('cls')
	Interface.SimpleMessage(ms.title).show()
	
	new_game = True
	while new_game:
		(new_game,) = ms.menus.MainMenu().show()

		settings = ()
		if new_game == 0:
			ms.quit_game()
		elif new_game == 1:
			difficulty = Game.BEGINNER
		elif new_game == 2:
			difficulty = Game.INTERMEDIATE
		elif new_game == 3:
			difficulty = Game.EXPERT
		elif new_game == 4:
			difficulty = Game.CUSTOM

			((width,),(height,)) = ms.menus.CustomSize().show()
			(bombs,) = ms.menus.CustomBombs(width,height).show()
			settings = (width,height,bombs)

		ms.init_game(difficulty,settings)

		play(ms)

main()
