from sys import path as sys_path			# working folder
from datetime import datetime as dt			# get date time now
from enum import Enum						# const enumeration
from PIL import Image,ImageTk				# img adjustments
from sense_emu import SenseHat				# RPi sense hat
import paramiko								# SSH to RPIs
import tkinter as tk						# interface
from tkinter import 	ttk,		\
						messagebox

# <EXCEPTIONS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class DependenciesError(Exception):
	def __str__(self):
		return 	"External dependencies:"								+ \
				"\n> sqlalchemy (pip install sqlalchemy)"				+ \
				"\n> sqlalchemy_utils (pip install sqlalchemy_utils)"

class DBConnectError(Exception):
	def __str__(self):
		return	"Pogreška pri spajanju na bazu!"

class DBReadError(Exception):
	def __str__(self):
		return	"Pogreška pri čitanju iz baze!"

class DBWriteError(Exception):
	def __str__(self):
		return	"Pogreška pri upisu u bazu!"

class IFOpenError(Exception):
	def __str__(self):
		return	"Pogreška pri otvaranju sučelja!"

class SensorConnectError(Exception):
	def __str__(self):
		return "Pogreška pri spajanju na senzor!"

# </EXCEPTIONS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <SENSORS>

class SensorSSH():
	# "real" RPi
	def __init__(self,name,ip,user,pkf):
		self.name = name
		self.ip = ip
		self.user = user
		self.pkf = pkf

		# attempt to start GUI (probe connection)
		process_name = 'sense_emu_gui'
		try:
			self.start_process(process_name)
		except:
			raise SensorConnectError

	def ssh_connect(self):
		private_key = paramiko.Ed25519Key.from_private_key(self.pkf)

		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(self.ip,username=self.user,pkey=private_key)

		return client	
	
	def start_process(self, process_name):
		client:'paramiko.SSHClient' = self.ssh_connect()
		
		# get all running ps:
		command = f"ps aux | grep {process_name}"
		# execute command on server
		_stdin, stdout, _stderr = client.exec_command(command)
		# read output
		lines = stdout.read().decode()
		# check if exists among running ps:
		if not lines:
			# if not running, spawn process:
			client.exec_command(process_name)
		# close conn
		client.close()

class SensorDummy():
	# dummy RPi for testing if no SSH
	def __init__(self,name):
		self.name = name

		# attempt to start GUI (probe connection)
		process_name = 'sense_emu_gui'
		try:
			self.start_process(process_name)
		except:
			raise SensorConnectError
	
	def start_process(self,process_name):
		from subprocess import Popen, PIPE, STDOUT
		# get all running ps:
		command = f"ps aux | grep {process_name}"
		# execute command on server
		p = Popen(
			command,
			shell=True,
			stdin=PIPE,
			stdout=PIPE,
			stderr=STDOUT,
			close_fds=True
			)
		# read output
		lines = p.stdout.read().decode()

		# check if exists among running ps:
		if not lines:
			# if not running, spawn process:
			Popen(
				process_name,
				shell=True,
				stdin=PIPE,
				stdout=PIPE,
				stderr=STDOUT,
				close_fds=True
				)

class SensorTest():
	# default values for testing
	def __init__(self,name):
		self.name = name

class SensorManager():

	# ASSUME RPIs CONFIGURED IN PARENT APP!
	
	class RPiUnutra(Enum):
		NAME = 'unutra'
		# equal to Izvan ... only 1 emu can be spawned =(
		IP = "192.168.0.15"
		USER = "marin"
		PKF = "C:\\Users\\Marin\\.ssh\\id_ed25519.key"
	
	class RPiIzvan(Enum):
		NAME = 'izvan'
		# equal to SensorUnutra ... only 1 emu can be spawned =(
		IP = "192.168.0.15"
		USER = "marin"
		PKF = "C:\\Users\\Marin\\.ssh\\id_ed25519.key"

	def __init__(self):

		self.RPis = []

		for RPi in [self.RPiUnutra,self.RPiIzvan]:
			# test RPi connection:
			try:
				# attempt to create ssh clients:
				# IF SSH DON'T NEED TO RUN HOST PROCESS ON PI
				self.RPis.append(SensorSSH(RPi.NAME.value,RPi.IP.value,RPi.USER.value,RPi.PKF.value))
			except:
				# attempt to create dummy clients:
				# IF NO SSH MUST RUN ON PI TO START DUMMIES
				try:
					self.RPis.append(SensorDummy(RPi.NAME.value))
				except:
					# create test clients (return defaults)
					self.RPis.append(SensorTest(RPi.NAME.value))

# </SENSORS>
# <INTERFACE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <SCROLLBOX> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _create_container(func):
	# factory function which equips element with a frame container
	# and binds the mouse wheel movement to the frame on hover

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

class ScrolledListBox(AutoScroll, tk.Listbox):

	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

# </SCROLLBOX> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <WIDGETS>  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class frmPostaja(ttk.LabelFrame):
	
	def __init__(self,master):

		self.root = master
		super().__init__(master)

		self.unos_ugoda_bracket = [0,12,22]
		# ugoda depends on postaja value bracket
		self.unos_ugoda = None
		# data from postaja
		self.unos_postaja = tk.DoubleVar()
		self.unos_postaja.set("")
		self.unos_ugoda = -1

		self.configure_basic()

		# initialize label images:
		self.lbl_ugoda_v = []
		self.img_active = []
		self.img_grey = []
		self.img_get = []
		self.init_images()
		
		self.attach_widgets()

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Meteo podaci [C]")

	def init_images(self):

		path_get = sys_path[0]+'\\'+f"IKONE_get.png"
		self.img_get = ImageTk.PhotoImage(
					Image.open(path_get).resize((25,25))
					)

		for x in range(4):
			path_active = sys_path[0]+'\\'+f"IKONE_{x}_active.jpg"
			path_grey = sys_path[0]+'\\'+f"IKONE_{x}_grey.jpg"
		
			self.img_active.append(
				ImageTk.PhotoImage(
					Image.open(path_active).resize((37,37))
					)
				)
			self.img_grey.append(
				ImageTk.PhotoImage(
					Image.open(path_grey).resize((37,37))
					)
				)
		
	def set_label_image(self,x):
		if x == self.unos_ugoda:
			self.lbl_ugoda_v[x].configure(image=self.img_active[x])
		else:
			self.lbl_ugoda_v[x].configure(image=self.img_grey[x])
	
	def get_data_postaja(self):

		from requests import get as rget
		import xml.etree.ElementTree as ET

		# url_base = https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici
		url = 'https://vrijeme.hr/hrvatska_n.xml'

		root = ET.fromstring(rget(url).text)
		for grad in root.findall("Grad"):
			if grad.find("GradIme").text == "Zagreb-Maksimir":
				podaci = grad.find("Podatci")
				t = float(podaci.find("Temp").text)
				# h = float(podaci.find("Vlaga").text)
				# p = float(podaci.find("Tlak").text)
		
		# tk var for lbl value
		self.unos_postaja.set(round(t,1))

		# img signal (0-3)
		self.unos_ugoda = 0
		for x in self.unos_ugoda_bracket:
			if t > x:
				self.unos_ugoda += 1
		
		# adjust label images
		for i in range(4):	
			self.set_label_image(i)

	def attach_widgets(self):

		lbl_postaja = ttk.Label(self,text='Ref. postaja:',style='lbl_naslov.TLabel')
		lbl_postaja.place(x=240, y=20, height=22, width=100, bordermode='ignore')

		lbl_postaja_v = ttk.Label(self,textvariable=self.unos_postaja,style='lbl_vrijednost.TLabel')
		lbl_postaja_v.place(x=240, y=40, height=40, width=100, bordermode='ignore')

		for i in range(4):	
			self.lbl_ugoda_v.append(
				ttk.Label(self,style='lbl_ugoda.TLabel')
			)
			self.lbl_ugoda_v[i].place(x=15+i*(39+8), y=30, height=39, width=39, bordermode='ignore')
			self.set_label_image(i)

		btn_get = ttk.Button(self)
		btn_get.place(x=346, y=30, height=39, width=39, bordermode='ignore')
		btn_get.configure(
			style='btn_get.TButton',
			image=self.img_get,
			command=self.get_data_postaja)

class frmBasic(ttk.LabelFrame):

	def __init__(self,master):

		self.root = master
		super().__init__(master)

		# attach on config
		self.unos_unutar = tk.StringVar()
		self.unos_izvan = tk.StringVar()
		self.unos_ocitanja = tk.Variable()

		# ref listbox for easier refresh control
		self.box_ocitanja = None
		self.data_column = self.get_data_column()

		self.configure_basic()

		self.attach_widgets()

		self.init_sensors()
		# needs to set unutar, izvan values
		self.get_sensor_data()

		self.refresh_list(self.data_column)

	def init_sensors(self):
		...

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# functions different for each mode
	# to be implemented in child classes
	# primitive abstractmethod style coding

	def configure_basic(self):
		raise NotImplementedError("Configure labelframe style, text, ...")

	def get_data_column(self):
		raise NotImplementedError("Define data column (return 't','h','p')")

	def get_sensor_data(self):
		raise NotImplementedError("Set: self.unos_unutar, self.unos_izvan")

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -

	def refresh_list(self,data_type):
		try:
			# catch all db exceptions as DBReadError
			try:
				res = self.root.DB_link.select_data(data_type)
			except Exception as e:
				raise DBWriteError()
		except DBReadError:
			messagebox.showerror("Greška pri otvaranju",DBReadError())
			return

		self.unos_ocitanja.set(res)

	def attach_widgets(self):

		# LABELS

		lbl_unutar = ttk.Label(self,text='Unutar kuće:',style='lbl_naslov.TLabel')
		lbl_unutar.place(x=240, y=20, height=22, width=100, bordermode='ignore')

		lbl_unutar_v = ttk.Label(self,textvariable=self.unos_unutar,style='lbl_vrijednost.TLabel')
		lbl_unutar_v.place(x=240, y=40, height=40, width=100, bordermode='ignore')

		lbl_izvan = ttk.Label(self,text='Izvan kuće:',style='lbl_naslov.TLabel')
		lbl_izvan.place(x=240, y=100, height=22, width=100, bordermode='ignore')

		lbl_izvan_v = ttk.Label(self,textvariable=self.unos_izvan,style='lbl_vrijednost.TLabel')
		lbl_izvan_v.place(x=240, y=120, height=40, width=100, bordermode='ignore')

		# SCROLLBOX

		self.box_ocitanja = ScrolledListBox(self)
		self.box_ocitanja.place(x=15, y=25, height=130, width=180, bordermode='ignore')
		# custom element containing scroll and list, Listbox NOT ttk
		# easier to configure the widget here (only one element in frm)
		# than to define for it a custom ttk class with style specs
		self.box_ocitanja.configure(
			listvariable=self.unos_ocitanja,
			selectmode=tk.BROWSE,
			background="white",
			disabledforeground="#b4b4b4",
			font=('Segoe UI',9),
			foreground="black",
			highlightcolor="#d9d9d9",
			selectbackground="#d9d9d9",
			selectforeground="black",
			relief="solid",
			cursor="xterm",
		)
		self.box_ocitanja.bind("<<ListboxSelect>>",self.box_select)

	def box_select(self,event:'tk.Event'):
		# nothing to do, template method
		pass

class frmTemp(frmBasic):
	
	def __init__(self,master):
		# nothing to do, template method
		# initialize master
		super().__init__(master)
	
	def get_data_column(self):
		return 'temp'
	
	def get_sensor_data(self):
		self.unos_unutar.set("00")
		self.unos_izvan.set("00")

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Temperatura [C]")

class frmVlaga(frmBasic):
	
	def __init__(self,master):
		# nothing to do, template method
		# initialize master
		super().__init__(master)
	
	def get_data_column(self):
		return 'vlaga'
	
	def get_sensor_data(self):
		self.unos_unutar.set("00")
		self.unos_izvan.set("00")

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Vlažnost [%]")

class frmTlak(frmBasic):
	
	def __init__(self,master):
		# nothing to do, template method
		# initialize master
		super().__init__(master)
	
	def get_data_column(self):
		return 'tlak'
	
	def get_sensor_data(self):
		self.unos_unutar.set("0000")
		self.unos_izvan.set("0000")

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Vlažnost [%]")

class tkRoot(tk.Tk):

	def __init__(self,DB_link,SH_link):
		# database link
		self.DB_link = DB_link
		# sense hat link
		self.SH_link = SH_link

		super().__init__()

		self.configure_basic()
		self.style = self.style_config()

		self.attach_frames()
		self.attach_widgets()

	def configure_basic(self):
		self.title("PROGNOZA")
		self.resizable(0,0)

		self.configure(
			highlightcolor="SystemWindowText"
		)

	def save(self):
		...
	
	def delete(self):
		...
	
	def start(self):
		...
	
	def stop(self):
		...

	def attach_frames(self):
		self.geometry("430x680")
		
		self.frm_postaja = frmPostaja(self)
		self.frm_postaja.place(x=15, y=10, height=85, width=400)
		self.frm_temp = frmTemp(self)
		self.frm_temp.place(x=15, y=100, height=170, width=400)
		self.frm_vlaga = frmVlaga(self)
		self.frm_vlaga.place(x=15, y=275, height=170, width=400)
		self.frm_tlak = frmTlak(self)
		self.frm_tlak.place(x=15, y=450, height=170, width=400)
	
	def attach_widgets(self):

		self.btn_spremi = ttk.Button(self)
		self.btn_spremi.place(x=15, y=635, height=30, width=75, bordermode='ignore')
		self.btn_spremi.configure(
			text='Spremi',
			style='btn_general.TButton',
			command=self.save)

		self.btn_izbrisi = ttk.Button(self)
		self.btn_izbrisi.place(x=100, y=635, height=30, width=75, bordermode='ignore')
		self.btn_izbrisi.configure(
			text='Izbrisi',
			style='btn_general.TButton',
			command=self.delete)

		self.btn_pokreni = ttk.Button(self)
		self.btn_pokreni.place(x=255, y=635, height=30, width=75, bordermode='ignore')
		self.btn_pokreni.configure(
			text='Pokreni',
			style='btn_general.TButton',
			command=self.start)

		self.btn_zaustavi = ttk.Button(self)
		self.btn_zaustavi.place(x=340, y=635, height=30, width=75, bordermode='ignore')
		self.btn_zaustavi.configure(
			text='Zaustavi',
			style='btn_general.TButton',
			command=self.stop)

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
			'lbl_ugoda.TLabel',
			background='white',
			borderwidth=1,
			relief="solid",
			font=('Segoe UI',12),
			anchor='center',
			justify='center',
			compound='image'
		)
		self.style.configure(
			'btn_general.TButton',
			relief='groove',
			compound='center',
			font=('Segoe UI',9),
		)
		self.style.configure(
			'btn_get.TButton',
			relief='groove',
			compound='center',
			font=('Segoe UI',9),
		)
		self.style.configure(
			'lbl_naslov.TLabel',
			font=('Segoe UI',9),
			relief="flat",
			anchor='w',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'lbl_vrijednost.TLabel',
			font=('Segoe UI',18),
			relief="flat",
			anchor='w',
			justify='left',
			compound='left'
		)

	def tksleep(self,t):
		# emulate time.sleep(seconds)
		var = tk.IntVar(self)
		self.after(int(t*1000), var.set, 1)
		self.wait_variable(var)

# </WIDGETS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# </INTERFACE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <DATABASE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <DB IMPORTS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

try:
	import sqlalchemy as sa
	from sqlalchemy import	create_engine,	\
							MetaData,		\
							select,			\
							insert,			\
							update,			\
							delete,			\
							Table,			\
							Column,			\
							String,			\
							Integer,		\
							Boolean

	from sqlalchemy_utils import	database_exists,	\
									create_database

except Exception as e:
	raise DependenciesError()

# </DB IMPORTS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <DB MGMT> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
		DATABASE = "meteo.db"

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

		self.table_name = 'thp_data'

		tbl = self.tables.get(self.table_name)
		if tbl is None:
			self.create_table()
			self.populate_data()

	def create_table(self):
		Table(
			self.table_name,
			self.meta,
			Column('id',Integer,primary_key=True),
			Column('temp',Integer),
			Column('vlaga',Integer),
			Column('tlak',Integer),
			Column('date',String),
			Column('time',String)
		)
		self.meta.create_all(bind=self.engine)

	def delete_data_all(self,table_name):
		tbl = self.tables[table_name]
		stmt = delete(tbl)
		with self.engine.begin() as conn:
			conn.execute(stmt)

	def populate_data(self):

		with self.engine.begin() as conn:
			conn.execute(insert(self.tables[self.table_name]),
				[
					{"temp":20,"vlaga":50,"tlak":1020,"date":"2024-03-20","time":"10:00:00"},
					{"temp":21,"vlaga":51,"tlak":1021,"date":"2024-03-21","time":"11:00:00"},
					{"temp":22,"vlaga":52,"tlak":1022,"date":"2024-03-22","time":"12:00:00"},
					{"temp":23,"vlaga":53,"tlak":1023,"date":"2024-03-23","time":"13:00:00"},
					{"temp":24,"vlaga":54,"tlak":1024,"date":"2024-03-24","time":"14:00:00"},
				]
			)

	def display_data(self):
		for table_name,table_object in self.tables.items():
			print(f"\n> table: {table_name}")
			with self.engine.connect() as conn:
				for row in conn.execute(select(table_object)):
					print(row)

	def check_id(self,id):
		tbl = self.tables[self.table_name]

		condition_id = (tbl.c.id == id)
		stmt = select(tbl).where(condition_id)

		with self.engine.connect() as conn:
			result = conn.execute(stmt)

		result = [row._asdict() for row in result]
		return result[0] if result else None

	def select_data(self,data_type):
		tbl = self.tables[self.table_name]

		# # # !
		if data_type not in ['temp','vlaga','tlak']:
			raise ValueError("Unknown data type!")
		
		stmt = select(
			(tbl.columns[data_type]).label(data_type),
			(tbl.c.date).label("date"),
			(tbl.c.time).label("time"),
			)
		with self.engine.connect() as conn:
			result = conn.execute(stmt)

		# # # !
		rl = [f"{x[0]:>4} : {x[1]} {x[2]}" for x in result]
		return rl

	def insert_data(self,data):
		tbl = self.tables[self.table_name]
		stmt = insert(tbl)
		with self.engine.begin() as conn:
			conn.execute(stmt,data)

	def delete_data_by_id(self,id):
		tbl = self.tables[self.table_name]
		stmt = delete(tbl).where(tbl.c.id == id)
		with self.engine.begin() as conn:
			conn.execute(stmt)

# </DB MGMT>  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# </DATABASE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <APPLICATION> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class App():

	def __init__(self):

		try:
			# generate/connect to DB, break on error
			self.database = DB()
		except Exception as e:
			raise DBConnectError()

		try:
			# generate/connect to sensors, break on error
			self.sensors = SensorManager()
		except Exception as e:
			raise SensorConnectError()

		try:
			# generate tk interface, break on error
			self.interface_root = tkRoot(self.database,self.sensors)
		except Exception as e:
			raise IFOpenError()

	def run(self):
		self.interface_root.mainloop()

def main():
	try:
		App().run()
	except DBConnectError as dbe:
		print(dbe)
	except IFOpenError as ioe:
		print(ioe)
	except SensorConnectError as sce:
		print(sce)
	except Exception as e:
		print(f"Error! {e}")

if __name__ == '__main__':
		main()

# </APPLICATION> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -