import tkinter as tk
import sys

def tkinter_basic_01():
	rootWindow = tk.Tk()
	tk.Button(rootWindow,text='Hello World!').pack()
	rootWindow.mainloop()

	# Window
	# Frame
	# Label
	# Button
	# Checkbutton
	# Radiobutton
	# Entry
	# Listbox
	# Text

# tkinter_basic_01()

def tkinter_basic_02():

	root = tk.Tk()

	root.title("Nas prvi TK program")
	root.geometry('600x400')

	root.mainloop()

# tkinter_basic_02()

def tkinter_basic_03():

	root = tk.Tk()

	root.title("Botunici")
	root.geometry('600x400')

	button = tk.Button(root,text='Botun')
	button.pack()

	def click():
		print("Kliknuli ste na botun")

	button_click = tk.Button(root,text='Klikni me!',command=click)
	button_click.pack(padx=10,pady=10)

	root.mainloop()

# tkinter_basic_03()
	
def tkinter_basic_04():

	root = tk.Tk()

	root.title('Botunici')
	root.geometry('600x400')

	button = tk.Button(root,text='Botun')
	button.pack()

	def click():
		print("Kliknuli ste na botun")

	button_click = tk.Button(root,text='Klikni me!',command=click)
	button_click.pack(padx=10,pady=10)

	subfolder = 'Resources'
	filename = 'python.gif'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + filename
	btn_image = tk.PhotoImage(file=filepath)
	button_image = tk.Button(
		root,
		text='Botun sa slikom',
		image=btn_image,
		compound = tk.LEFT,
		relief=tk.GROOVE,
		command=click,
		state=tk.ACTIVE
	)
	button_image.pack(padx=40,pady=10,expand=True,fill='x')

	root.mainloop()

tkinter_basic_04()

def tkinter_basic_05():

	def click():
		# nonlocal lbl
		lbl.config(
			text='Nova poruka',
			font=('Helvetica',18),
			fg='red'
		)

	root = tk.Tk()
	root.title("Botuni i Label")
	root.geometry('600x400')

	lbl = tk.Label(
		root,
		text = 'Poruka',
		font = ('Segoe UI', 16)
	)
	lbl.pack(padx=30,pady=40)

	btnClick = tk.Button(
		root,
		text = 'Klikni me!',
		command = click
	)
	btnClick.pack(padx=10,pady=10)

	subfolder = 'Resources'
	filename = 'python-logo.png'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + filename
	img_in_lbl = tk.PhotoImage(file=filepath).subsample(7)
	lbl_pict = tk.Label(
		root,
		text = 'Tekst u slici',
		font = ('Segoe UI',20),
		compound = tk.CENTER,		# LEFT,RIGHT,TOP,BOTTOM,CENTER,NONE
		image = img_in_lbl
	)
	lbl_pict.pack(padx=5,pady=10)

	root.mainloop()

# tkinter_basic_05()
	
def tkinter_basic_06():

	root = tk.Tk()

	root.title('Place')
	root.geometry('600x400')

	subfolder = 'Resources'
	filename = 'python.gif'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + filename
	btn_img = tk.PhotoImage(file=filepath)
	button = tk.Button(
		root,
		text='Botun sa slikom',
		image = btn_img,
		compound=tk.LEFT
	)
	button.place(x=150,y=75)

	label = tk.Label(root,text='Nekakvi tekst')
	label.place(x=200,y=90)

	root.mainloop()

# tkinter_basic_06()

def tkinter_basic_07():

	root = tk.Tk()
	root.title('Grid')

	for i in range(3):
		root.columnconfigure(i,weight=1,minsize=75)
		root.rowconfigure(i,weight=1,minsize=75)

		for j in range(3):
			frm = tk.Frame(root,relief=tk.RAISED,borderwidth=1)
			frm.grid(row=i,column=j,padx=1,pady=1)
			lbl = tk.Label(frm,text=f"Red {i}\nStupac {j}",font=('Segoe UI',16))
			lbl.pack(padx=10,pady=10)

			lbl2 = tk.Label(frm,text='Test')
			lbl2.pack(padx=10,pady=10)
	
	root.mainloop()

# tkinter_basic_07()

def tkinter_basic_08():

	unesena_slova = ''

	def handle_keypress(event):
		nonlocal unesena_slova
		nonlocal lbl_txt_var
		print(event.char)
		if len(unesena_slova)>15:
			unesena_slova=''
		unesena_slova += str(event.char)
		lbl_txt_var.set(unesena_slova)

	root = tk.Tk()
	root.title('Events')
	root.geometry('600x400')

	lbl_txt_var = tk.StringVar()
	lbl_txt_var.set('Mjesto za ispis slova')

	lbl_naslov = tk.Label(root,text='Key event',font=('Segoe UI',18))
	lbl_naslov.grid(column=0,row=0)

	lbl_ispis = tk.Label(root,textvariable=lbl_txt_var,font=("Segoe UI",24),fg='red')
	lbl_ispis.grid(column=0,row=1)

	root.bind("<Key>",handle_keypress)

	root.mainloop()

# tkinter_basic_08()

def tkinter_basic_09():

	def zbroji():
		nonlocal ispis_rezultat
		ispis_rezultat.delete(0,tk.END)
		prvi_broj = int(unos_prvi_broj.get())
		drugi_broj = int(unos_drugi_broj.get())
		rezultat = prvi_broj+drugi_broj
		print(f"Zbroj {rezultat}")
		ispis_rezultat.insert(tk.END,str(rezultat))
	
	def handle_btn_oduzmi(event):
		nonlocal ispis_rezultat
		ispis_rezultat.delete(0,tk.END)
		print(str(event))
		prvi_broj = int(unos_prvi_broj.get())
		drugi_broj = int(unos_drugi_broj.get())
		rezultat = prvi_broj-drugi_broj
		print(f"Razlika {rezultat}")
		ispis_rezultat.insert(tk.END,str(rezultat))
	
	def handle_btn_pomnozi(event):
		nonlocal ispis_rezultat
		ispis_rezultat.delete(0,tk.END)
		print(str(event))
		prvi_broj = int(unos_prvi_broj.get())
		drugi_broj = int(unos_drugi_broj.get())
		rezultat = prvi_broj*drugi_broj
		print(f"Razlika {rezultat}")
		ispis_rezultat.insert(tk.END,str(rezultat))
	
	def handle_btn_podijeli(event):
		nonlocal ispis_rezultat
		ispis_rezultat.delete(0,tk.END)
		print(str(event))
		prvi_broj = int(unos_prvi_broj.get())
		drugi_broj = int(unos_drugi_broj.get())
		if drugi_broj == 0:
			rezultat = "dijeljenje s nulom"
		else:
			rezultat = prvi_broj/drugi_broj
		print(f"Razlika {rezultat:.2f}")
		ispis_rezultat.insert(tk.END,str(rezultat))

	root = tk.Tk()
	root.title('Entry')
	root.geometry('600x400')

	lbl_prvi_broj = tk.Label(root,text='Prvi broj')
	lbl_prvi_broj.grid(column=0,row=0,padx=5,pady=5)

	unos_prvi_broj = tk.Entry(bd=3)
	unos_prvi_broj.grid(column=1,row=0,padx=5,pady=5)

	lbl_drugi_broj = tk.Label(root,text='Drugi broj')
	lbl_drugi_broj.grid(column=0,row=1,padx=5,pady=5)

	unos_drugi_broj = tk.Entry(bd=3)
	unos_drugi_broj.grid(column=1,row=1,padx=5,pady=5)

	btn_zbroji = tk.Button(root,text='zbroji +',command=zbroji)
	btn_zbroji.grid(column=0,row=2,padx=5,pady=5)

	btn_oduzmi = tk.Button(root,text='oduzmi -')
	btn_oduzmi.grid(column=1,row=2,padx=5,pady=5)
	btn_oduzmi.bind('<Button-1>',handle_btn_oduzmi)

	btn_pomnozi = tk.Button(root,text='pomnozi *')
	btn_pomnozi.grid(column=0,row=3,padx=5,pady=5)
	btn_pomnozi.bind('<Button-1>',handle_btn_pomnozi)

	btn_podijeli = tk.Button(root,text='podijeli /')
	btn_podijeli.grid(column=1,row=3,padx=5,pady=5)
	btn_podijeli.bind('<Button-1>',handle_btn_podijeli)

	lbl_rezultat = tk.Label(root,text='Rezultat')
	lbl_rezultat.grid(column=0,row=4,padx=5,pady=5)
	ispis_rezultat = tk.Entry(bd=3)
	ispis_rezultat.grid(column=1,row=4,padx=5,pady=5)




	root.mainloop()

# tkinter_basic_09()
