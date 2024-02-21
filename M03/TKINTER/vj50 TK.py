import tkinter as tk

def tkinter_practice_01():

	def otvori_me():
		lbl_poruka.pack(padx=5,pady=5)

	def zatvori_me():
		lbl_poruka.pack_forget()
		print("Zatvorio si me")

	root = tk.Tk()
	root.title('Otvori me')
	root.geometry('600x600')

	btn_otvori = tk.Button(root,text = "Otvori me",command=otvori_me)
	btn_otvori.pack(padx=5,pady=5)

	btn_zatvori = tk.Button(root,text = "Zatvori me",command=zatvori_me)
	btn_zatvori.pack(padx=5,pady=5)

	lbl_poruka = tk.Label(root,text="Otvorio si me",font=("Segoe UI",20))

	root.mainloop()

# tkinter_practice_01()

def tkinter_practice_02():

	pin_admin = '0000'

	def udji():
		nonlocal pin_admin
		pin_received = unos_pin.get()
		if pin_admin == pin_received:
			lbl_tekst = "Dobar dan, Admin"
		else:
			lbl_tekst = "Krivi pin"
		lbl_poruka.configure(text=lbl_tekst)
		lbl_poruka.grid(column=1,row=3,padx=5,pady=5)	
	
	root = tk.Tk()
	root.title('Otvori me')
	root.geometry('600x600')

	lbl_pin_oznaka = tk.Label(root,text="Pin:")
	lbl_pin_oznaka.grid(column=0,row=0,padx=5,pady=5)
	unos_pin = tk.Entry(bd=3)
	unos_pin.grid(column=1,row=0)

	btn_udji = tk.Button(root,text='UDJI',command=udji)
	btn_udji.grid(column=1,row=1)

	lbl_poruka = tk.Label(root,text="")

	root.mainloop()

# tkinter_practice_02()

def tkinter_practice_03():
	root = tk.Tk()

	lbl1 = tk.Label(root,text="Tekst prvi")
	lbl2 = tk.Label(root,text="Tekst drugi")
	lbl3 = tk.Label(root,text="Tekst treci")

	lbl1.grid(column=0,row=0,padx=5,pady=5)
	lbl2.grid(column=1,row=0,padx=5,pady=5)
	lbl3.grid(column=0,columnspan=2,padx=5,pady=5)

	root.mainloop()

tkinter_practice_03()