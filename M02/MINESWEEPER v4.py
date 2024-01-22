import os
import random as rn
import itertools as it
import TreeNode as tn
import urwid as uw

# boje:
# 1 blue
# 2 green
# 3 red
# 4 dark blue
# 5 brown
# 6 Cyan
# 7 Black
# 8 Grey

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
			
	class SimpleMenu():
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
		
		def show_text(self):
			Interface.SimpleMessage('\n'+self.title).show()
			Interface.SimpleMessage(Interface.separator).show()

			for option in self.options:
				Interface.SimpleMessage(option).show()

			Interface.SimpleMessage(Interface.separator).show()
		
		def show_input(self):
			return Interface.SimpleGetter.get_input(self.getter)
		
		def show(self):
			os.system('cls')
			self.show_text()
			return self.show_input()

	class CascadingMenu(tn.TreeNode):
		def __init__(self,data=None):
			# set basic menu options (palette,etc.)
			tn.TreeNode.__init__(self,data)
		
		def show_parents(self):
			for parent in self.parents():
				parent.data.show_text()
		
		def show_text(self):
			self.data.show_text()
		
		def show_input(self):
			return self.data.show_input()
		
		def show(self):
			os.system('cls')
			self.show_parents()
			self.show_text()
			return self.show_input()	

class Menus():
	class MainMenu():
		def __init__(self):
			mc = Board.config
			self.menu = Interface.SimpleMenu()
			self.menu.title = "GLAVNI MENU"

			opt = []
			opt.append('[0] - izlaz')
			opt.append('[1] - beginner\t(09x09, B = 10)')
			opt.append('[2] - medium\t(16x16, B = 40)')
			opt.append('[3] - expert\t(30x60, B = 99)')
			c_dims = f"[{mc['w_min']}-{mc['w_max']}]x[{mc['h_min']}-{mc['h_max']}]"
			c_bombs = f"[{mc['w_min']*mc['h_min']}-{mc['w_max']*mc['h_max']}]"
			opt.append(f"[4] - custom\t({c_dims}, B = {c_bombs})")
			opt.append(f"[5] - settings")
			self.menu.options = opt

			g = Interface.SimpleGetter()
			g.choice_label = 'Odabir [0|...|5]: '
			g.choice_sep = ' '
			g.choice_type = (int,)
			g.choice_test = (lambda x: x in list(range(5+1)),)
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

	class ModifyHSeparate():
		def __init__(self,current_value):
			self.hs = Interface.SimpleGetter()
			self.hs.choice_label = f"> Horizontalni separator [0 = NE, 1 = DA] ({int(current_value)}) "
			self.hs.choice_sep = ' '
			self.hs.choice_type = (int,)
			self.hs.choice_test = (lambda x: x in [0,1],)
			self.hs.choice_error = 'Pogresan unos!'

		def show(self):
			return self.hs.get_input()

	class ModifyHSpacing():
		def __init__(self,current_value):
			self.hs = Interface.SimpleGetter()
			self.hs.choice_label = f"> Horizontalni razmak [1|2|3] ({current_value}) "
			self.hs.choice_sep = ' '
			self.hs.choice_type = (int,)
			self.hs.choice_test = (lambda x: x in [1,2,3],)
			self.hs.choice_error = 'Pogresan unos!'

		def show(self):
			return self.hs.get_input()

	class ModifyVSeparate():
		def __init__(self,current_value):
			self.vs = Interface.SimpleGetter()
			self.vs.choice_label = f"> Vertikalni separator [0 = NE, 1 = DA] ({int(current_value)}) "
			self.vs.choice_sep = ' '
			self.vs.choice_type = (int,)
			self.vs.choice_test = (lambda x: x in [0,1],)
			self.vs.choice_error = 'Pogresan unos!'

		def show(self):
			return self.vs.get_input()

	class ModifyVSpacing():
		def __init__(self,current_value):
			self.vs = Interface.SimpleGetter()
			self.vs.choice_label = f"> Vertikalni razmak [0|1|2] ({current_value}) "
			self.vs.choice_sep = ' '
			self.vs.choice_type = (int,)
			self.vs.choice_test = (lambda x: x in [0,1,2],)
			self.vs.choice_error = 'Pogresan unos!'

		def show(self):
			return self.vs.get_input()

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
			if r != 'x' and len((r,c,t))==3:
				(r,c,t) = result
				return (int(r),c,t)
			else:
				return (r,'','')

	class ConfigMenu():
		def __init__(self):
			self.menu = Interface.CascadingMenu(self.ConfigRoot())
			self.menu.addChild(Interface.CascadingMenu(self.ConfigInput()))
			self.menu.addChild(Interface.CascadingMenu(self.ConfigDisplay()))

		@staticmethod
		def ConfigRoot():
			menu = Interface.SimpleMenu()
			menu.title = "SETTINGS"

			opt = []
			opt.append('[0] - izlaz')
			opt.append('[1] - input settings')
			opt.append('[2] - display settings')
			menu.options = opt

			c = Interface.SimpleGetter()
			c.choice_label = 'Odabir [0|1|2]: '
			c.choice_sep = ' '
			c.choice_type = (int,)
			c.choice_test = (lambda x: x in [0,1,2],)
			c.choice_error = 'Pogresan unos!'
			menu.getter = c

			return menu
		
		@staticmethod
		def ConfigInput():
			menu = Interface.SimpleMenu()
			menu.title = "INPUT SETTINGS"

			opt = []
			opt.append('[0] - izlaz')
			opt.append('[1] - keyboard')
			opt.append('[2] - mouse')
			menu.options = opt

			c = Interface.SimpleGetter()
			c.choice_label = 'Odabir [0|1|2]: '
			c.choice_sep = ' '
			c.choice_type = (int,)
			c.choice_test = (lambda x: x in [0,1,2],)
			c.choice_error = 'Pogresan unos!'
			menu.getter = c

			return menu
		
		@staticmethod
		def ConfigDisplay():
			menu = Interface.SimpleMenu()
			menu.title = "DISPLAY SETTINGS"

			opt = []
			opt.append('[0] - izlaz')
			opt.append('[1] - horizontalni separator')
			opt.append('[2] - horizontalni razmak')
			opt.append('[3] - vertikalni separator')
			opt.append('[4] - vertikalni razmak')
			menu.options = opt

			c = Interface.SimpleGetter()
			c.choice_label = 'Odabir [0|...|4]: '
			c.choice_sep = ' '
			c.choice_type = (int,)
			c.choice_test = (lambda x: x in [0,1,2,3,4],)
			c.choice_error = 'Pogresan unos!'
			menu.getter = c

			return menu

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

	def __init__(self,input_mode = 0):
		r = range(len(self.renderers))
		if input_mode not in r:
			raise ValueError(f"Graphics input: {'|'.join(r)}")
		self.set_renderer(input_mode)

	class KeyboardMode():	

		def __init__(self,config,values):
			self.config = config
			self.values = values
			self.palette = {
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
				self.values['h_space']: '\x1b[0;37;40m',
				self.values['v_space']: '\x1b[0;37;40m',
				self.values['h_sep']: '\x1b[0;37;40m',
				self.values['v_sep']: '\x1b[0;37;40m',
				self.values['cross']: '\x1b[0;37;40m',
				self.values['corner']: '\x1b[0;37;40m',
				"ENDC": '\x1b[0m'}

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

			return board_display

		def display(self,board:'Board',board_type):
			print(self.render(board,board_type))

		@staticmethod
		def translate_move(x,y,active_board):
			test = True
			if test:
				return (True,x,y)
			else:
				return (False,x,y)

		def get_move(self,active_board):
			...

	class MouseMode():

		def __init__(self,config,values):
			self.config = config
			self.values = values
			self.palette = {
				0: '',
				1: '',
				2: '',
				3: '',
				4: '',
				5: '',
				6: '',
				7: '\x1b[1;36;40m',
				8: '\x1b[1;30;40m',
				Board.values['hidden']: '',
				Board.values['empty']: '',
				Board.values['bomb']: '',
				Board.values['mark']: '',
				self.values['v_space']: '',
				self.values['h_sep']: '',
				self.values['v_sep']: '',
				self.values['cross']: '',
				self.values['corner']: '',
				"ENDC": '\x1b[0m'}

		def render(self,board:'Board',board_type):
			...

		def display(self,board:'Board',board_type):
			...		

		@staticmethod
		def translate_move(x,y,active_board):
			test = True
			if test:
				return (True,x,y)
			else:
				return (False,x,y)

		def get_move(self,active_board):
			...

	def set_renderer(self,input_mode):
		self.renderer = self.renderers[input_mode](self.config,self.values)
	
	renderers = {0: KeyboardMode, 1: MouseMode}

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
		# cleaning, DB operatons, ...
		Interface.SimpleMessage("Hvala i doviđenja").show()
		# exit()
	
def configure(ms:'Game',node=None):

	# if no node provided, initialize menu
	if not node:
		node = ms.menus.ConfigMenu().menu

	(choice,) = node.show()
	title = node.data.title

	if title=="SETTINGS":
		if choice == 0:
			return
			# return to previous menu
		elif choice == 1:
			configure(ms,node=node.children[0])
			# open input settings
		elif choice == 2:
			configure(ms,node=node.children[1])
			# open display settings

	elif title=="INPUT SETTINGS":
		if choice == 0:
			configure(ms,node=node.parent)
			# return to previous menu
		elif choice == 1:
			ms.graphics.set_renderer(0)
			# set input to keyboard
			configure(ms,node=node.parent)
		elif choice == 2:
			ms.graphics.set_renderer(1)
			# set input to mouse
			configure(ms,node=node.parent)
	
	elif title=="DISPLAY SETTINGS":
		with ms.graphics.renderer.config as rc:
			if choice == 0:
				configure(ms,node=node.parent)
				# return to previous menu
			elif choice == 1:
				(value,) = ms.menus.ModifyHSeparate(rc['h_separate']).show()
				rc['h_separate'] = value
				configure(ms,node)
				# set horizontal separate on/off
			elif choice == 2:
				(value,) = ms.menus.ModifyHSpacing(rc['h_spacing']).show()
				rc['h_spacing'] = value
				# set horizontal spacing on/off
				configure(ms,node)
			elif choice == 3:
				(value,) = ms.menus.ModifyVSeparate(rc['v_separate']).show()
				rc['v_separate'] = value
				# set vertical separate on/off
				configure(ms,node)
			elif choice == 4:
				(value,) = ms.menus.ModifyVSpacing(rc['v_spacing']).show()
				rc['v_spacing'] = value
				# set vertical spacing on/off
				configure(ms,node)

def play(ms:'Game'):
	
	def show_board_keyboard():
		nonlocal ms

		os.system('cls')
		# # # TEST
		Interface.SimpleMessage("\nINICIJALIZIRANA PLOCA").show()
		image = ms.graphics.renderer.render(ms.board,'real')
		Interface.SimpleMessage(image).show()
		Interface.SimpleMessage("> OTVORENA ZA TESTIRANJE").show()
		# # # TEST

		Interface.SimpleMessage("\nAKTIVNA PLOCA").show()
		image = ms.graphics.renderer.render(ms.board,'active')
		Interface.SimpleMessage(image).show()
		Interface.SimpleMessage(f"> PREOSTALO BOMBI: {ms.board.get_bombs_remaining()}").show()

		lines = []
		lines.append('\n'+ms.title)
		lines.append(Interface.separator)
		lines.append("> UPUTA: r = ## red, c = ## stupac, t = tip poteza")
		lines.append("> UPUTA: tip poteza: 0 = iskopaj, 1 = (od)markiraj")
		lines.append("> UPUTA: za izlaz iz igre umjesto poteza unesi [x]")
		Interface.MultiMessage(lines).show()

	def show_board_mouse():
		nonlocal ms

		def exit_on_x(key):
			nonlocal txt
			if key in ('x','X'):
				raise uw.ExitMainLoop()
			txt.set_text(repr(key))

		image = ''
		image += ("\nINICIJALIZIRANA PLOCA")
		image += "\n"+ms.graphics.renderer.render(ms.board,'real')
		image += ("\n> OTVORENA ZA TESTIRANJE")
		image += "\n"
		image += "\nAKTIVNA PLOCA"
		image += "\n"+ms.graphics.render(ms.board,'active')
		image += f"\n> PREOSTALO BOMBI: {ms.board.get_bombs_remaining()}"
		image += '\n'+ms.title
		image += '\n'+Interface.separator
		image += "\n> UPUTA: polja se otkrivaju/označavaju klikovima miša"
		image += "\n> UPUTA: tip poteza: LC = iskopaj, RC = (od)markiraj"
		image += "\n> UPUTA: za izlaz iz igre umjesto poteza unesi [x]"

		txt = uw.Text(image)
		fill = uw.Filler(txt,'top')
		loop = uw.MainLoop(fill,unhandled_input=exit_on_x)
		loop.run()

	new_move = True	
	while new_move == True:
		if ms.graphics.input_mode == "keyboard":
			ms.graphics.renderer.display()
			(r,c,t) = ms.menus.GetMove(ms.board.width,ms.board.height).show()

			if str(r).upper() == 'X':
				new_move=False
				break

			if new_move == True:
				result = ms.board.evaluate_move(r,c,t)

				if result == 'lost':
					show_board_keyboard()
					Interface.SimpleMessage("\nBOOM!").show()
					new_move = False
				elif result == 'win':
					show_board_keyboard()
					Interface.SimpleMessage("\nPOBJEDA!").show()
					new_move = False

		elif ms.graphics.input_mode == "mouse":
			ms.graphics.renderer.display()
			new_move=False
			# # # TEST
			# get mouse click through graphics
			# if move == True ... evaluate r,c,t
			# # # TEST

def main():
	ms = Game()

	os.system('cls')
	Interface.SimpleMessage(ms.title).show()
	
	new_game = True
	while new_game:
		(new_game,) = ms.menus.MainMenu().show()

		settings = ()
		if new_game == 0:
			new_game = False
			ms.quit_game()
			continue

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

		elif new_game == 5:
			configure(ms)
			continue

		ms.init_game(difficulty,settings)

		play(ms)

main()
