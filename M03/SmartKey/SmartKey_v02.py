import os, sys
from enum import Enum
import pandas as pd
from time import sleep

import tkinter as tk
from tkinter import 	ttk,		\
						messagebox
# <INTERFACE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <SCROLLBOX> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _create_container(func):
	# factory function which equips element with a frame container
	# and the mouse wheel movement bound to the frame on hover

	speed_reduction = 100

	def _on_mousewheel(event, widget):
		widget.yview_scroll(-1*int(event.delta/speed_reduction),'units')

	def _bound_to_mousewheel(event, widget):
		child = widget.winfo_children()[0]
		child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))

	def _unbound_to_mousewheel(event, widget):
		widget.unbind_all('<MouseWheel>')

	def wrapped(cls, master, **kw):
		container = ttk.Frame(master)
		container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)

	return wrapped

class AutoScroll():

	def __init__(self, master):
		vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
		hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

		self.configure(
			yscrollcommand=self._autoscroll(vsb),
			xscrollcommand=self._autoscroll(hsb)
		)

		self.grid(column=0, row=0, sticky='nsew')
		vsb.grid(column=1, row=0, sticky='ns')
		hsb.grid(column=0, row=1, sticky='ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		# take packing methods (except config and internal)
		methods = 	tk.Pack.__dict__.keys() | \
					tk.Grid.__dict__.keys() | \
					tk.Place.__dict__.keys()

		for m in methods:
			if m[0] != '_' and m not in ('config', 'configure'):
				setattr(self, m, getattr(master, m))

	@staticmethod
	def _autoscroll(sbar):
		# factory function which hides / shows scrollbar
		def wrapped(first, last):
			first = float(first)
			last = float(first)

			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):

	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

# </SCROLLBOX> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <WIDGETS>  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class frmGumbi(ttk.LabelFrame):

	def __init__(self,master):
		self.root = master
		super().__init__(master)

		self.configure_basic()
		self.attach_widgets()

	def configure_basic(self):
		self.configure(style='frm.TLabelframe',text='Panel s gumbima')

	def use_bell(self):
		messagebox.showinfo("Zvono aktivirano","Netko će uskoro doći i otvoriti vrata")

	def use_key(self):
		self.master.attach_PIN_frame()

	def attach_widgets(self):

		from PIL import Image,ImageTk

		# bell_path = os.path.join(sys.path[0],"bell.png")
		bell_path = sys.path[0]+'\\'+"bell.png"
		self.img_bell = ImageTk.PhotoImage(Image.open(bell_path).resize((25,25)))

		self.btn_pozvoni = ttk.Button(self)
		self.btn_pozvoni.place(x=20, y=30, height=50, width=50, bordermode='ignore')
		self.btn_pozvoni.configure(
			style='btn_gumbi.TButton',
			image=self.img_bell,
			command=self.use_bell)

		# key_path = os.path.join(sys.path[0],"key.png")
		key_path = sys.path[0]+'\\'+"key.png"
		self.img_key = ImageTk.PhotoImage(Image.open(key_path).resize((25,25)))

		self.btn_otkljucaj = ttk.Button(self)
		self.btn_otkljucaj.place(x=410, y=30, height=50, width=50, bordermode='ignore')
		self.btn_otkljucaj.configure(
			style='btn_gumbi.TButton',
			image=self.img_key,
			command=self.use_key)

class frmPIN(ttk.LabelFrame):

	class Poruke(Enum):
		START =			"UNESI ID U (####) OBLIKU"

		EXIT =			"\n"							+ \
						"\n"							+ \
						"\nZA IZLAZ UNESITE X"

		ID_SUCCESS =	"ID USPJESNO UNESEN."			+ \
						"\n"							+ \
						"\n"							+ \
						"\nUNESI PIN U (####) OBLIKU"

		ID_UNKNOWN =	"NEPOZNAT ID"					+ \
						"\n"							+ \
						"\n"							+ \
						"\nMOLIMO POKUŠAJTE PONOVO"

		ID_ADMIN =		"\n"							+ \
						"\n"							+ \
						"\nADMINISTRATORSKI ID"			+ \
						"\nMOLIMO UNESITE PIN ZA OPERACIJU"

		PIN_SUCCESS =	"PIN USPJESNO UNESEN."			+ \
						"\n"							+ \
						"\n"							+ \
						"\nDOBRODOŠLI, "

		PIN_UNKNOWN =	"POGREŠNO UNESEN PIN."			+ \
						"\n"							+ \
						"\n"							+ \
						"\nMOLIMO POKUŠAJTE PONOVO"

		PIN_ADMIN =		"\n"							+ \
						"\n"							+ \
						"\nOPERACIJA USPJEŠNA"			+ \
						"\nZA NOVU OPERACIJU"			+ \
						"\nPONOVITE POSTUPAK"

		ACTIVE_YES =	"\n"							+ \
						"\n"							+ \
						"\nKORISNIK JE AKTIVAN"

		ACTIVE_NO =		"\n"							+ \
						"\n"							+ \
						"\nULAZ NIJE DOPUŠTEN."			+ \
						"\nKORISNIK NIJE AKTIVAN."		+ \
						"\nZA AKTIVACIJU KORISNIKA"		+ \
						"\nKONTAKTIRAJTE ADMINISTRATORA"

	def __init__(self,master):
		self.root = master
		super().__init__(master)
		self.configure_basic()
		self.attach_widgets()

		self.step = 0
		self.ID = None
		self.PIN = None

	def configure_basic(self):
		self.configure(style='frm.TLabelframe',text='PIN panel')

	def enter_PIN(self,event:'tk.Event'):
		signal = event.widget['text']
		try:
			if signal != '0':
				# if signal is a number
				# 0 doesn't pass assertion
				assert int(signal)
			# check how many digits entered
			value = frmPIN.join_SVL(self.lbl_PIN_numbers)
			pos = len(value)
			# add signal to row
			self.lbl_PIN_numbers[pos].set(signal)
			if pos == 3:
				# if row full perform check
				# sleep a bit so user can see last num entered
				self.root.tksleep(0.5)

				if self.ID == None:
					# if id not entered perform first step
					self.first_step()
				elif self.PIN == None:
					# if id correct perform second step
					self.second_step()

		except:
			if signal == 'X':
				self.root.detach_PIN_frame()
			elif signal == 'C':
				# check how many digits entered
				value = frmPIN.join_SVL(self.lbl_PIN_numbers)
				pos = len(value)
				# clear last label
				if pos == 0:
					# if empty nothing to do
					return
				else:
					self.lbl_PIN_numbers[pos-1].set("")

	@staticmethod
	def join_SVL(StringVarList):
		return "".join([x.get() for x in StringVarList])

	def verify_step(self,key):
		check_var = "".join([x.get() for x in self.lbl_PIN_numbers])

		# reset label row to empty
		[x.set("") for x in self.lbl_PIN_numbers]

		# retrieve data from DB
		DB = self.root.DB_link
		# PANDAS FOR TESTING
		if key == "ID":
			check_var = int(check_var)
			check_DB = DB.users.loc[DB.users.index==check_var]
		elif key == "PIN":
			check_DB = DB.users.loc[(DB.users.index==self.ID) & (DB.users["PIN"]==check_var)]

		# SQLITE FOR APPLICATION


		if len(check_DB.index)>0:
			# set ID / PIN to correctly entered value
			self.__dict__[key] = check_var
			return self.verify_successful(check_DB,key)
		else:
			return self.verify_error(key)

	def verify_successful(self,data,key):

		if key == "ID":
			name_insert = ""
		elif key == "PIN":
			name_insert = "\n" + data["IME"].values[0] + " " + data["PREZIME"].values[0]

		active = int(data["AKTIVAN"].iloc[0])
		admin = int(data["ADMIN"].iloc[0])

		# messages enum short name
		d = frmPIN.Poruke.__dict__

		active_insert = d["ACTIVE_YES"].value if active else d["ACTIVE_NO"].value
		if admin:
			message = 	d[key+"_SUCCESS"].value	+ \
						name_insert				+ \
						d[key+"_ADMIN"].value	+ \
						active_insert			+ \
						d["EXIT"].value
			self.lbl_PIN_text.set(message)
			return ("admin",data)
		else:
			message =	d[key+"_SUCCESS"].value	+ \
						name_insert				+ \
						active_insert			+ \
						d["EXIT"].value
			self.lbl_PIN_text.set(message)
			return ("user",data)

	def verify_error(self,key):

		# messages enum short name
		d = frmPIN.Poruke.__dict__

		message = 	d[key+"_UNKNOWN"].value		+ \
					d["EXIT"].value
		self.lbl_PIN_text.set(message)
		return ("unknown",None)

	def first_step(self):
		self.verify_step("ID")

	def second_step(self):
		(result,data) = self.verify_step("PIN")

		if result != 'unknown' and messagebox.askyesno(
			"Administracija sustava",
			"Želite li pokrenuti upravljanje podacima?"
			):
			if result == 'admin':
				mode = frmDB.Modes.MODE_ADMIN.value
			elif result == 'user':
				mode = frmDB.Modes.MODE_USER.value

			self.root.attach_DB_frame(mode,data)

	def attach_widgets(self):

		self.lbl_PIN_numbers = []
		for i in range(4):
			self.lbl_PIN_numbers.append(tk.StringVar())
			lbl_PIN = ttk.Label(self)
			lbl_PIN.place(x=20+i*47,y=30,height=39,width=39,bordermode='ignore')
			lbl_PIN.configure(
				style='lbl_PIN.TLabel',
				textvariable=self.lbl_PIN_numbers[i]
			)

		t = [
			["1","2","3"],
			["4","5","6"],
			["7","8","9"],
			["X","0","C"]
			]
		for i in range(4):
			for j in range(3):
				button = ttk.Button(self)
				button.place(x=(20+j*65),y=(95+i*65), height=50, width=50, bordermode='ignore')
				button.configure(
					style='btn_PIN.TButton',
					text=t[i][j]
				)
				button.bind('<Button>',self.enter_PIN)

		self.lbl_PIN_text = tk.StringVar(value=frmPIN.Poruke.START.value)
		lbl_PIN_poruke = ttk.Label(self)
		lbl_PIN_poruke.place(x=220, y=30, height=310, width=240,bordermode='ignore')
		lbl_PIN_poruke.configure(
			style='lbl_PIN_poruke.TLabel',
			textvariable=self.lbl_PIN_text
		)

class frmDB(ttk.LabelFrame):

	class Modes(Enum):
		MODE_USER = 'user'
		MODE_ADMIN = 'admin'

	def __init__(self,master):

		self.root = master
		super().__init__(master)

		# attach on config
		self.unos_ime = tk.StringVar()
		self.unos_prezime = tk.StringVar()
		self.unos_PIN = tk.StringVar()
		self.attach_widgets()

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# functions different for each mode
	# to be implemented in child classes
	# primitive abstractmethod style coding

	def configure_basic(self):
		raise NotImplemented("Must define basic configuration!")

	def save(self):
		raise NotImplemented("Must define save button function!")

	def abort(self):
		raise NotImplemented("Must define abort button function!")

	def delete(self):
		raise NotImplemented("Must define delete button function!")

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -

	def attach_widgets(self):

		# LABELS

		lbl_ime = ttk.Label(self,text='Ime:',style='lbl_unos.TLabel')
		lbl_ime.place(x=220, y=30, height=27, width=60, bordermode='ignore')

		lbl_prezime = ttk.Label(self,text='Prezime:',style='lbl_unos.TLabel')
		lbl_prezime.place(x=220, y=60, height=27, width=60, bordermode='ignore')

		lbl_PIN = ttk.Label(self,text='PIN:',style='lbl_unos.TLabel')
		lbl_PIN.place(x=220, y=90, height=27, width=60, bordermode='ignore')

		# ENTRIES

		ent_ime = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_ime)
		ent_ime.place(x=300, y=30, height=25, width=160, bordermode='ignore')

		ent_prezime = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_prezime)
		ent_prezime.place(x=300, y=60, height=25, width=160, bordermode='ignore')

		ent_PIN = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_PIN)
		ent_PIN.place(x=300, y=90, height=25, width=160, bordermode='ignore')

		# BUTTONS

		btn_spremi = ttk.Button(self)
		btn_spremi.place(x=220, y=200, height=30, width=70, bordermode='ignore')
		btn_spremi.configure(
			text='Spremi',style='btn_unos.TButton',command=self.save
		)

		btn_odustani = ttk.Button(self)
		btn_odustani.place(x=305, y=200, height=30, width=70, bordermode='ignore')
		btn_odustani.configure(
			text='Odustani',style='btn_unos.TButton',command=self.abort
		)

		btn_izbrisi = ttk.Button(self)
		btn_izbrisi.place(x=390, y=200, height=30, width=70, bordermode='ignore')
		btn_izbrisi.configure(
			text='Izbrisi',style='btn_unos.TButton',command=self.delete
		)

class frmDB_user(frmDB):

	def __init__(self,master):
		# vars controlled only by user:
		#

		super().__init__(master)

		self.configure_basic()

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Upravljanje podacima korisnika")
		# retrieve data from self id
		self.unos_ime.set("")
		self.unos_prezime.set("")
		self.unos_PIN.set("")

class frmDB_admin(frmDB):

	def __init__(self,master):
		# vars controlled only by admin:
		self.aktivan = tk.IntVar()

		super().__init__(master)

		self.configure_basic()

		self.attach_admin_widgets()

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Upravljanje podacima")
		# set entries to zero
		self.unos_ime.set("")
		self.unos_prezime.set("")
		self.unos_PIN.set("")
		self.aktivan.set(0)

	def save(self):
		...

	def abort(self):
		self.unos_ime.set("")
		self.unos_prezime.set("")
		self.unos_PIN.set("")

	def delete(self):
		...

	def attach_admin_widgets(self):

		# CHECKBOX (ONLY ADMIN MODE)

		lbl_aktivan = ttk.Label(self,text='Aktivan:',style='lbl_unos.TLabel')
		lbl_aktivan.place(x=220, y=120, height=27, width=60, bordermode='ignore')

		chk_aktivan = ttk.Checkbutton(self,style='aktivan.TCheckbutton',variable=self.aktivan)
		chk_aktivan.place(x=300, y=120, width=65, height=29, bordermode='ignore')

		# SCROLLBOX (ONLY ADMIN MODE)

		box_korisnici = ScrolledListBox(self)
		box_korisnici.place(x=20, y=30, height=200, width=180, bordermode='ignore')
		# custom element > easier to config here than to define custom style
		box_korisnici.configure(
			background="white",
			disabledforeground="#b4b4b4",
			font=('Segoe UI',9),
			foreground="white",
			highlightcolor="#d9d9d9",
			selectbackground="#d9d9d9",
			selectforeground="black",
			relief="solid",
			cursor="xterm",
		)

class tkRoot(tk.Tk):

	def __init__(self,DB_link):
		self.DB_link = DB_link

		# receives DB row on registration
		self.current_user = None

		super().__init__()
		self.configure_basic()
		self.style = self.style_config()

		self.attach_default_frame()
		self.frm_PIN = None
		self.frm_DB = None

	def configure_basic(self):
		self.title("SmartKey")
		self.resizable(0,0)

		self.configure(
			highlightcolor="SystemWindowText"
		)

	def attach_default_frame(self):
		self.geometry("510x120")
		self.frm_gumbi = frmGumbi(self)
		self.frm_gumbi.place(x=15, y=10, height=100, width=480)

	def attach_PIN_frame(self):
		self.geometry("510x500")
		self.frm_PIN = frmPIN(self)
		self.frm_PIN.place(x=15, y=125, height=360, width=480)

	def detach_PIN_frame(self):
		if self.frm_DB and self.frm_DB.winfo_exists():
			self.detach_DB_frame()
		self.frm_PIN.destroy()
		self.geometry("510x120")

	def attach_DB_frame(self,mode,data):
		if mode not in [x.value for x in frmDB.Modes]:
			raise ValueError("Nepoznat mod korištenja!")

		# activate current user DB link:
		self.current_user = data

		# expand form, insert frame:
		self.geometry("510x760")
		if mode == frmDB.Modes.MODE_USER.value:
			self.frm_DB = frmDB_user(self)
		elif mode == frmDB.Modes.MODE_ADMIN.value:
			self.frm_DB = frmDB_admin(self)

		self.frm_DB.place(x=15, y=500, height=245, width=480)

	def detach_DB_frame(self):
		self.frm_DB.destroy()
		self.geometry("510x500")

	def style_config(self):
		self.style = ttk.Style(self)
		# self.style.theme_use('xpnative')
		self.style.configure(
			'.', font = 'TkDefaultFont'
		)
		self.style.configure(
			"frm.TLabelframe",
			relief='flat'
		)
		self.style.configure(
			"btn_gumbi.TButton",
			relief='groove',
			compound='center',
			font=('Segoe UI',12),
		)
		self.style.configure(
			'lbl_PIN.TLabel',
			background='white',
			relief="solid",
			font=('Segoe UI',12),
			anchor='center',
			justify='center',
			compound='center'
		)
		self.style.configure(
			'btn_PIN.TButton',
			relief='groove',
			compound='center',
			font=('Segoe UI',12),
		)
		self.style.configure(
			'lbl_PIN_poruke.TLabel',
			background='white',
			relief="solid",
			font=('Segoe UI',9),
			padding=(2,2,2,2),
			anchor='nw',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'lbl_unos.TLabel',
			font=('Segoe UI',9),
			relief="flat",
			anchor='w',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'ent_unos.TEntry',
			font=('Segoe UI',9),
			compound='left'
		)
		self.style.configure(
			'aktivan.TCheckbutton',
			compound='left'
		)
		self.style.configure(
			'btn_unos.TButton',
			relief='groove',
			font=('Segoe UI',9),
			compound='center'
		)

	def tksleep(self,t):
		# emulate time.sleep(seconds)
		var = tk.IntVar(self)
		self.after(int(t*1000), var.set, 1)
		self.wait_variable(var)

# </WIDGETS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# </INTERFACE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <DATABASE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <DB_TEST>  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class DB_TEST():

	def __init__(self):
		c = ["IME","PREZIME","PIN","AKTIVAN","ADMIN"]
		r = [1,2,3,4,5]
		d = [
			["Mate","Matic",'0001','1','1'],			# admin obicni
			["Ivan","Ivic", '0002','0','1'],			# admin generiraj test bazu
			["Ana","Anic", '0003','1','0'],				# admin obrisi test bazu
			["Josip","Josipovic", '0004','1','0'],		# user aktivan
			["Marko","Markovic", '0005','0','0']		# user neaktivan
		]
		self.users = pd.DataFrame.from_records(data=d,index=r,columns=c)

# </DB_TEST> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <DB_APP> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from sys import path as sys_path
from os import getcwd as os_cwd

import sqlalchemy as sa

from sqlalchemy import	create_engine,				\
						MetaData,					\
						select,						\
						insert,						\
						update,						\
						delete,						\
						Table,						\
						Column,						\
						String,						\
						Integer,					\
						Boolean,					\
						and_,						\
						or_


from sqlalchemy.engine.url import URL

from sqlalchemy_utils import	database_exists,	\
								create_database

# from sqlalchemy-utils import

# <BASIC DB MGMT> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# allow only one instance of core classes (engine,meta,session,...)
class singleton_class:
	def __init__(self,aClass):
		self.aClass = aClass
		self.instance = None
	def __call__(self,*args,**kwargs):
		if self.instance == None:
			self.instance = self.aClass(*args,**kwargs)
		return self.instance
	def __getattr__(self,attrname):
		return getattr(self.aClass,attrname)


class DB():

	class ConnParams(Enum):
		ECHO = False
		DIALECT = "sqlite"
		DBAPI = "pysqlite"
		DATABASE = "SmartKeyUsers.db"

	@staticmethod
	def create_conn_string():
		return	f"{DB.ConnParams.DIALECT.value}"	+ \
				f"+{DB.ConnParams.DBAPI.value}:"	+ \
				f"///{sys_path[0]}"+"\\"			+ \
				f"{DB.ConnParams.DATABASE.value}"
	
	def __init__(self):
		self.engine = create_engine(
			DB.create_conn_string(),
			echo=DB.ConnParams.ECHO.value)
		self.meta = MetaData()

		if not database_exists(self.engine.url):
			create_database(self.engine.url)
		self.meta.reflect(bind=self.engine)		
		self.tables = self.meta.tables

		if "user_account" not in self.tables.keys():
			self.create_user_table()
			self.populate_user_data()
			# self.display_data()

	def create_user_table(self):
		Table(
			"user_account",
			self.meta,
			Column('id',Integer,primary_key=True),
			Column('firstname',String),
			Column('surname',String),
			Column('PIN',String),
			Column('active',Boolean),
			Column('admin',Boolean)
		)
		self.meta.create_all(bind=self.engine)
	
	def populate_user_data(self):
		
		with self.engine.begin() as conn:
			check_db = database_exists(self.engine.url)
			check_table = "user_account" in self.meta.tables
			conn.execute(insert(self.tables["user_account"]),
				[
					{"firstname":"Mate","surname":"Matic","PIN":"0001","active":1,"admin":1},
					{"firstname":"Ivan","surname":"Ivic","PIN":"0002","active":0,"admin":1},
					{"firstname":"Ana","surname":"Anic","PIN":"0003","active":1,"admin":0},
					{"firstname":"Josip","surname":"Josipovic","PIN":"0004","active":1,"admin":0},
					{"firstname":"Marko","surname":"Markovic","PIN":"0005","active":0,"admin":0},
				]
			)
	
	def display_data(self):
		for table_name,table_object in self.tables.items():
			print(f"\n> table: {table_name}")
			with self.engine.connect() as conn:
				for row in conn.execute(select(table_object)):
					print(row)
	
	def check_id(self,id):
		users = self.tables["user_account"]
		stmt = select(
			(users.c.id).label(id)
		).where("id" == id)
		with self.engine.connect() as conn:
			result = conn.execute(stmt).all()
		return result[0] if result else None

	def check_pin(self,id,PIN):
		users = self.tables["user_account"]
		stmt = select(
			(users.c.id).label("id"),			
			(users.c.PIN).label("PIN")
		).where(
			and_("id"==id,"PIN"==PIN)
		)
		with self.engine.connect() as conn:
			result = conn.execute(stmt).all()
		return result[0] if result else None
	
	def select_user_names(self):
		users = self.tables["user_account"]
		stmt = select(
			(users.c.firstname).label("fn"),
			(users.c.surname).label("sn")
			)
		with self.engine.connect() as conn:
			result = conn.execute(stmt).all()
		rl = [" ".join(x.fn,x.sn) for x in result]
		return rl
	
	def update_user(self,id,data:"dict"):
		users = self.tables["user_account"]
		stmt = update(users).where(users.c.id == id).values(data)
		with self.engine.begin() as conn:
			conn.execute(stmt)
	
	def insert_user(self,data):
		users = self.tables["user_account"]
		stmt = insert(users)
		with self.engine.begin() as conn:
			conn.execute(stmt,data)
	
	def delete_user(self,data):
		users = self.tables["user_account"]
		stmt = delete(users).where(
			users.c.id == id
		)



	


# </DB_APP> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# </DATABASE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <APPLICATION> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class App():

	class DBConnectError(Exception):
		def __str__(self):
			return "Pogreška pri spajanju na bazu!"

	class IFOpenError(Exception):
		def __str__(self):
			return "Pogreška pri otvaranju sučelja!"

	def __init__(self):
		# self.database = DB_TEST()

		try:
			# connect to DB, break if unsucessfull
			self.database = DB()
		except Exception as e:
			raise App.DBConnectError()

		try:
			# generate interface, break if unsucessfull
			self.interface_root = tkRoot(self.database)
		except Exception as e:
			raise App.IFOpenError()

	def run(self):
		self.interface_root.mainloop()

def main():
	try:
		App().run()
	except App.DBConnectError as dbe:
		print(dbe)
	except App.IFOpenError as ioe:
		print(ioe)
	except Exception as e:
		print(f"Error! {e}")


if __name__ == '__main__':
	while True:
		launch = int(input("launch?"))
		if launch == 0:
			break
		else:
			main()

# </APPLICATION> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -