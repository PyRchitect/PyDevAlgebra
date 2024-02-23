import tkinter as tk
import tkinter.ttk as ttk

# < SCROLLBOX - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _bound_to_mousewheel(event, widget):
	child = widget.winfo_children()[0]
	child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))

def _unbound_to_mousewheel(event, widget):
	widget.unbind_all('<MouseWheel>')

def _on_mousewheel(event, widget):
	widget.yview_scroll(-1*int(event.delta/120),'units')

def _create_container(func):
	# create ttk Frame with given master and use
	# this new frame to place the scrollbars and the widget
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

		# apply methods from master as own (except config and internal)
		methods = 	tk.Pack.__dict__.keys() | \
					tk.Grid.__dict__.keys() | \
					tk.Place.__dict__.keys()
		
		for m in methods:
			if m[0] != '_' and m not in ('config', 'configure'):
				setattr(self, m, getattr(master, m))

	@staticmethod
	def _autoscroll(sbar):
		# hide / show scrollbar
		def wrapped(first, last):
			first = float(first)
			last = float(first)

			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

	def __str__(self):
		return str(self.master)

class ScrolledListBox(AutoScroll, tk.Listbox):

	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

	def size_(self):
		sz = tk.Listbox.size(self)
		return sz

# SCROLLBOX > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class frmGumbi(ttk.LabelFrame):
	
	def __init__(self,master):
		super().__init__(master)

		self.configure_basic()
		self.attach_widgets()

	def configure_basic(self):
		self.configure(style='frm.TLabelframe',text='Panel s gumbima')

	def attach_widgets(self):
		self.btn_pozvoni = ttk.Button(self)
		self.btn_pozvoni.place(x=20, y=30, height=50, width=50, bordermode='ignore')
		self.btn_pozvoni.configure(style='btn_gumbi.TButton',text = 'Z')

		self.btn_otkljucaj = ttk.Button(self)
		self.btn_otkljucaj.place(x=410, y=30, height=50, width=50, bordermode='ignore')
		self.btn_otkljucaj.configure(style='btn_gumbi.TButton',text = 'O')

class frmPIN(ttk.LabelFrame):
	
	def __init__(self,master):
		super().__init__(master)
		self.configure_basic()
		self.attach_widgets()

	def configure_basic(self):
		self.configure(style='frm.TLabelframe',text='PIN panel')

	def attach_widgets(self):
		
		for i in range(4):
			lbl_PIN = ttk.Label(self,text="",style='lbl_PIN.TLabel')
			lbl_PIN.place(x=20+i*47,y=30,height=39,width=39,bordermode='ignore')
	
		t = [["1","2","3"],["4","5","6"],["7","8","9"],["C","0","CE"]]
		for i in range(4):
			for j in range(3):
				button = ttk.Button(self,text=t[i][j],style='btn_PIN.TButton')
				button.place(x=(20+j*65),y=(95+i*65), height=50, width=50, bordermode='ignore')

		lbl_PIN_poruke = ttk.Label(self,text="Status i poruke",style='lbl_PIN_poruke.TLabel')
		lbl_PIN_poruke.place(x=220, y=30, height=310, width=240,bordermode='ignore')

class frmDB(ttk.LabelFrame):
	
	def __init__(self,master):
		super().__init__(master)
		self.configure_basic()

		# attach on config
		self.unos_ime = None
		self.unos_prezime = None
		self.unos_PIN = None
		self.aktivan = None

		self.attach_widgets()

	def configure_basic(self):
		self.configure(style='frm.TLabelframe',text="Upravljanje dodijeljenim kljucevima")

	def attach_widgets(self):

		# LABELS
		
		lbl_ime = ttk.Label(self,text='Ime:',style='lbl_unos.TLabel')
		lbl_ime.place(x=220, y=30, height=27, width=60, bordermode='ignore')

		lbl_prezime = ttk.Label(self,text='Prezime:',style='lbl_unos.TLabel')
		lbl_prezime.place(x=220, y=60, height=27, width=60, bordermode='ignore')

		lbl_PIN = ttk.Label(self,text='PIN:',style='lbl_unos.TLabel')
		lbl_PIN.place(x=220, y=90, height=27, width=60, bordermode='ignore')

		lbl_aktivan = ttk.Label(self,text='Aktivan:',style='lbl_unos.TLabel')
		lbl_aktivan.place(x=220, y=120, height=27, width=60, bordermode='ignore')

		# ENTRIES

		ent_ime = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_ime)
		ent_ime.place(x=300, y=30, height=25, width=160, bordermode='ignore')

		ent_prezime = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_prezime)
		ent_prezime.place(x=300, y=60, height=25, width=160, bordermode='ignore')

		ent_PIN = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_PIN)
		ent_PIN.place(x=300, y=90, height=25, width=160, bordermode='ignore')

		# CHECKBOX

		chk_aktivan = ttk.Checkbutton(self,style='aktivan.TCheckbutton',variable=self.aktivan)
		chk_aktivan.place(x=300, y=120, width=65, height=29, bordermode='ignore')

		# BUTTONS

		btn_spremi = ttk.Button(self,text='Spremi',style='btn_unos.TButton')
		btn_spremi.place(x=220, y=200, height=30, width=70, bordermode='ignore')

		btn_odustani = ttk.Button(self,text='Odustani',style='btn_unos.TButton')
		btn_odustani.place(x=305, y=200, height=30, width=70, bordermode='ignore')

		btn_izbrisi = ttk.Button(self,text='Izbrisi',style='btn_unos.TButton')
		btn_izbrisi.place(x=390, y=200, height=30, width=70, bordermode='ignore')

		# SCROLLBOX

		box_korisnici = ScrolledListBox(self)
		box_korisnici.place(x=20, y=30, height=200, width=180, bordermode='ignore')
		box_korisnici.configure(
			background="SystemButtonFace",
			cursor="xterm",
			disabledforeground="#b4b4b4",
			font="-family {Segoe UI} -size 10",
			foreground="SystemWindowText",
			highlightcolor="#d9d9d9",
			relief="solid",
			selectbackground="#d9d9d9",
			selectforeground="black",
		)

class tkRoot(tk.Tk):
	
	def __init__(self):
		super().__init__()
		self.configure_basic()
		self.style = self.style_config()
		self.attach_frames()
	
	def configure_basic(self):
		self.title = "SmartKey"
		self.geometry("510x764+797+181")
		self.resizable(0,0)

		self.configure(
			highlightcolor="SystemWindowText"
		)
	
	def attach_frames(self):
		self.frm_gumbi = frmGumbi(self)
		self.frm_gumbi.place(x=15, y=10, height=100, width=480)

		self.frm_PIN = frmPIN(self)
		self.frm_PIN.place(x=15, y=125, height=360, width=480)

		self.frm_DB = frmDB(self)
		self.frm_DB.place(x=15, y=500, height=246, width=480)

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
			compound='center'
		)
		self.style.configure(
			'lbl_PIN.TLabel',
			background='SystemButtonFace',
			relief="solid",
			font="-family {Segoe UI} -size 9",
			anchor='w',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'btn_PIN.TButton',
			relief='groove',
			compound='center'
		)
		self.style.configure(
			'lbl_PIN_poruke.TLabel',
			background='SystemButtonFace',
			relief="solid",
			font="-family {Segoe UI} -size 9",
			anchor='n',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'lbl_unos.TLabel',
			font="-family {Segoe UI} -size 9",
			relief="flat",
			anchor='w',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'lbl_unos.TLabel',			
			font="-family {Segoe UI} -size 9",
			cursor='ibeam'
		)
		self.style.configure(
			'aktivan.TCheckbutton',
			compound='left'
		)
		self.style.configure(
			'btn_unos.TButton',
			relief='groove',
			compound='center'
		)

class App(tk.Tk):

	def __init__(self):
		self.root = tkRoot()

	def run(self):
		self.root.mainloop()

def main():
	App().run()

if __name__ == '__main__':
	main()