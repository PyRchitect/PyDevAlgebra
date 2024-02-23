import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

def _style_code():
    style = ttk.Style()
    style.theme_use('xpnative')    
    style.configure('.', font = "TkDefaultFont")

class Toplevel1:
    def __init__(self, top=None):

        # top.geometry("510x764+797+181")
        # top.minsize(120, 1)
        # top.maxsize(3844, 1061)
        # top.resizable(0,  0)
        # top.title("Toplevel 0")
        # top.configure(highlightcolor="SystemWindowText")

        self.top = top
        self.tch79 = tk.IntVar()

        # _style_code()
        self.frm_PIN = ttk.Labelframe(self.top)
        # self.frm_PIN.place(x=15, y=125, height=360, width=480)
        
        # self.frm_PIN.configure(relief='')
        # self.frm_PIN.configure(text='''PIN panel''')
        # self.frm_PIN.configure(style='frm.TLabelframe')

        # self.btn_PIN_01 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_01.place(x=20, y=95, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_01.configure(text='''1''')
        # self.btn_PIN_01.configure(compound='left')
        # self.btn_PIN_01.configure(style='btn_PIN.TButton')

        # self.btn_PIN_02 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_02.place(x=85, y=95, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_02.configure(text='''2''')
        # self.btn_PIN_02.configure(compound='left')
        # self.btn_PIN_02.configure(style='btn_PIN.TButton')

        # self.btn_PIN_03 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_03.place(x=150, y=95, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_03.configure(text='''3''')
        # self.btn_PIN_03.configure(compound='left')
        # self.btn_PIN_03.configure(style='btn_PIN.TButton')

        # self.btn_PIN_04 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_04.place(x=20, y=160, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_04.configure(text='''4''')
        # self.btn_PIN_04.configure(compound='left')
        # self.btn_PIN_04.configure(style='btn_PIN.TButton')

        # self.btn_PIN_05 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_05.place(x=85, y=160, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_05.configure(text='''5''')
        # self.btn_PIN_05.configure(compound='left')
        # self.btn_PIN_05.configure(style='btn_PIN.TButton')

        # self.btn_PIN_06 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_06.place(x=150, y=160, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_06.configure(text='''6''')
        # self.btn_PIN_06.configure(compound='left')
        # self.btn_PIN_06.configure(style='btn_PIN.TButton')

        # self.btn_PIN_07 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_07.place(x=20, y=225, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_07.configure(text='''7''')
        # self.btn_PIN_07.configure(compound='left')
        # self.btn_PIN_07.configure(style='btn_PIN.TButton')

        # self.btn_PIN_C = ttk.Button(self.frm_PIN)
        # self.btn_PIN_C.place(x=20, y=290, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_C.configure(text='''C''')
        # self.btn_PIN_C.configure(compound='left')
        # self.btn_PIN_C.configure(style='btn_PIN.TButton')

        # self.lbl_PIN_04 = ttk.Label(self.frm_PIN)
        # self.lbl_PIN_04.place(x=160, y=30, height=39, width=39
        #         , bordermode='ignore')
        # self.lbl_PIN_04.configure(background="SystemButtonFace")
        # self.lbl_PIN_04.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_PIN_04.configure(relief="solid")
        # self.lbl_PIN_04.configure(anchor='w')
        # self.lbl_PIN_04.configure(justify='left')
        # self.lbl_PIN_04.configure(compound='left')
        # self.lbl_PIN_04.configure(style='lbl_PIN.TLabel')

        # self.lbl_PIN_03 = ttk.Label(self.frm_PIN)
        # self.lbl_PIN_03.place(x=114, y=30, height=39, width=39
        #         , bordermode='ignore')
        # self.lbl_PIN_03.configure(background="SystemButtonFace")
        # self.lbl_PIN_03.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_PIN_03.configure(relief="solid")
        # self.lbl_PIN_03.configure(anchor='w')
        # self.lbl_PIN_03.configure(justify='left')
        # self.lbl_PIN_03.configure(compound='left')
        # self.lbl_PIN_03.configure(style='lbl_PIN.TLabel')

        # self.lbl_PIN_02 = ttk.Label(self.frm_PIN)
        # self.lbl_PIN_02.place(x=67, y=30, height=39, width=39
        #         , bordermode='ignore')
        # self.lbl_PIN_02.configure(background="SystemButtonFace")
        # self.lbl_PIN_02.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_PIN_02.configure(relief="solid")
        # self.lbl_PIN_02.configure(anchor='w')
        # self.lbl_PIN_02.configure(justify='left')
        # self.lbl_PIN_02.configure(compound='left')
        # self.lbl_PIN_02.configure(style='lbl_PIN.TLabel')

        # self.lbl_PIN_01 = ttk.Label(self.frm_PIN)
        # self.lbl_PIN_01.place(x=20, y=30, height=39, width=39
        #         , bordermode='ignore')
        # self.lbl_PIN_01.configure(background="SystemButtonFace")
        # self.lbl_PIN_01.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_PIN_01.configure(relief="solid")
        # self.lbl_PIN_01.configure(anchor='w')
        # self.lbl_PIN_01.configure(justify='left')
        # self.lbl_PIN_01.configure(compound='left')
        # self.lbl_PIN_01.configure(style='lbl_PIN.TLabel')

        # self.btn_PIN_CE = ttk.Button(self.frm_PIN)
        # self.btn_PIN_CE.place(x=150, y=290, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_CE.configure(text='''CE''')
        # self.btn_PIN_CE.configure(compound='left')
        # self.btn_PIN_CE.configure(style='btn_PIN.TButton')

        # self.lbl_PIN_poruke = ttk.Label(self.frm_PIN)
        # self.lbl_PIN_poruke.place(x=220, y=30, height=310, width=240
        #         , bordermode='ignore')
        # self.lbl_PIN_poruke.configure(background="SystemButtonFace")
        # self.lbl_PIN_poruke.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_PIN_poruke.configure(relief="solid")
        # self.lbl_PIN_poruke.configure(anchor='n')
        # self.lbl_PIN_poruke.configure(justify='left')
        # self.lbl_PIN_poruke.configure(text='''Status i poruke''')
        # self.lbl_PIN_poruke.configure(compound='left')
        # self.lbl_PIN_poruke.configure(style='lbl_PIN_oznake.TLabel')

        # self.btn_PIN_08 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_08.place(x=85, y=225, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_08.configure(text='''8''')
        # self.btn_PIN_08.configure(compound='left')
        # self.btn_PIN_08.configure(style='btn_PIN.TButton')

        # self.btn_PIN_09 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_09.place(x=150, y=225, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_09.configure(text='''9''')
        # self.btn_PIN_09.configure(compound='left')
        # self.btn_PIN_09.configure(style='btn_PIN.TButton')

        # self.btn_PIN_00 = ttk.Button(self.frm_PIN)
        # self.btn_PIN_00.place(x=85, y=290, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_PIN_00.configure(text='''0''')
        # self.btn_PIN_00.configure(compound='left')
        # self.btn_PIN_00.configure(style='btn_PIN.TButton')
        



        self.frm_gumbi = ttk.Labelframe(self.top)
        # self.frm_gumbi.place(x=15, y=10, height=100, width=480)
        # self.frm_gumbi.configure(relief='')
        # self.frm_gumbi.configure(text='''Panel s gumbima''')
        # self.frm_gumbi.configure(style='frm.TLabelframe')

        # self.btn_pozvoni = ttk.Button(self.frm_gumbi)
        # self.btn_pozvoni.place(x=20, y=30, height=50, width=50
        #         , bordermode='ignore')
        # self.btn_pozvoni.configure(text='''Z''')
        # self.btn_pozvoni.configure(compound='left')
        # self.btn_pozvoni.configure(style='btn_gumbi.TButton')

        # self.otkljucaj = ttk.Button(self.frm_gumbi)
        # self.otkljucaj.place(x=410, y=30, height=50, width=50
        #         , bordermode='ignore')
        # self.otkljucaj.configure(text='''O''')
        # self.otkljucaj.configure(compound='left')




        self.frm_DB = ttk.Labelframe(self.top)
        # self.frm_DB.place(x=15, y=500, height=246, width=480)
        # self.frm_DB.configure(relief='')
        # self.frm_DB.configure(text='''Upravljanje dodijeljenim kljucevima''')
        # self.frm_DB.configure(style='frm.TLabelframe')

        # self.lbl_ime = ttk.Label(self.frm_DB)
        # self.lbl_ime.place(x=220, y=30, height=27, width=60, bordermode='ignore')

        # self.lbl_ime.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_ime.configure(relief="flat")
        # self.lbl_ime.configure(anchor='w')
        # self.lbl_ime.configure(justify='left')
        # self.lbl_ime.configure(text='''Ime:''')
        # self.lbl_ime.configure(compound='left')
        # self.lbl_ime.configure(style='lbl_unos.TLabel')

        # self.lbl_prezime = ttk.Label(self.frm_DB)
        # self.lbl_prezime.place(x=220, y=60, height=27, width=60
        #         , bordermode='ignore')
        # self.lbl_prezime.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_prezime.configure(relief="flat")
        # self.lbl_prezime.configure(anchor='w')
        # self.lbl_prezime.configure(justify='left')
        # self.lbl_prezime.configure(text='''Prezime:''')
        # self.lbl_prezime.configure(compound='left')
        # self.lbl_prezime.configure(style='lbl_unos.TLabel')

        # self.lbl_PIN = ttk.Label(self.frm_DB)
        # self.lbl_PIN.place(x=220, y=90, height=27, width=60, bordermode='ignore')

        # self.lbl_PIN.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_PIN.configure(relief="flat")
        # self.lbl_PIN.configure(anchor='w')
        # self.lbl_PIN.configure(justify='left')
        # self.lbl_PIN.configure(text='''PIN:''')
        # self.lbl_PIN.configure(compound='left')
        # self.lbl_PIN.configure(style='lbl_unos.TLabel')

        # self.lbl_aktivan = ttk.Label(self.frm_DB)
        # self.lbl_aktivan.place(x=220, y=120, height=27, width=60
        #         , bordermode='ignore')
        # self.lbl_aktivan.configure(font="-family {Segoe UI} -size 9")
        # self.lbl_aktivan.configure(relief="flat")
        # self.lbl_aktivan.configure(anchor='w')
        # self.lbl_aktivan.configure(justify='left')
        # self.lbl_aktivan.configure(text='''Aktivan:''')
        # self.lbl_aktivan.configure(compound='left')
        # self.lbl_aktivan.configure(style='lbl_unos.TLabel')

        # self.btn_spremi = ttk.Button(self.frm_DB)
        # self.btn_spremi.place(x=220, y=200, height=30, width=70
        #         , bordermode='ignore')
        # self.btn_spremi.configure(text='''Spremi''')
        # self.btn_spremi.configure(compound='left')
        # self.btn_spremi.configure(style='btn_unos.TButton')

        # self.btn_odustani = ttk.Button(self.frm_DB)
        # self.btn_odustani.place(x=305, y=200, height=30, width=70
        #         , bordermode='ignore')
        # self.btn_odustani.configure(text='''Odustani''')
        # self.btn_odustani.configure(compound='left')
        # self.btn_odustani.configure(style='btn_unos.TButton')

        # self.btn_izbrisi = ttk.Button(self.frm_DB)
        # self.btn_izbrisi.place(x=390, y=200, height=30, width=70
        #         , bordermode='ignore')
        # self.btn_izbrisi.configure(text='''Izbrisi''')
        # self.btn_izbrisi.configure(compound='left')
        # self.btn_izbrisi.configure(style='btn_unos.TButton')

        # self.box_korisnici = ScrolledListBox(self.frm_DB)
        # self.box_korisnici.place(x=20, y=30, height=200, width=180
        #         , bordermode='ignore')
        # self.box_korisnici.configure(background="SystemButtonFace")
        # self.box_korisnici.configure(cursor="xterm")
        # self.box_korisnici.configure(disabledforeground="#b4b4b4")
        # self.box_korisnici.configure(font="-family {Segoe UI} -size 10")
        # self.box_korisnici.configure(foreground="SystemWindowText")
        # self.box_korisnici.configure(highlightcolor="#d9d9d9")
        # self.box_korisnici.configure(relief="solid")
        # self.box_korisnici.configure(selectbackground="#d9d9d9")
        # self.box_korisnici.configure(selectforeground="black")

        # self.ent_ime = ttk.Entry(self.frm_DB)
        # self.ent_ime.place(x=300, y=30, height=25, width=160
        #         , bordermode='ignore')
        # self.ent_ime.configure(font="-family {Segoe UI} -size 9")
        # self.ent_ime.configure(cursor="ibeam")
        # self.ent_ime.configure(style='ent_unos.TEntry')

        # self.ent_prezime = ttk.Entry(self.frm_DB)
        # self.ent_prezime.place(x=300, y=60, height=25, width=160
        #         , bordermode='ignore')
        # self.ent_prezime.configure(font="-family {Segoe UI} -size 9")
        # self.ent_prezime.configure(cursor="ibeam")
        # self.ent_prezime.configure(style='ent_unos.TEntry')

        # self.ent_PIN = ttk.Entry(self.frm_DB)
        # self.ent_PIN.place(x=300, y=90, height=25, width=160
        #         , bordermode='ignore')
        # self.ent_PIN.configure(font="-family {Segoe UI} -size 9")
        # self.ent_PIN.configure(cursor="ibeam")
        # self.ent_PIN.configure(style='ent_unos.TEntry')

        # self.chk_aktivan = ttk.Checkbutton(self.frm_DB)
        # self.chk_aktivan.place(x=300, y=120, width=65, height=29
        #         , bordermode='ignore')
        # self.chk_aktivan.configure(variable=self.tch79)
        # self.chk_aktivan.configure(compound='left')
        # self.chk_aktivan.configure(style='aktivan.TCheckbutton')




# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
            