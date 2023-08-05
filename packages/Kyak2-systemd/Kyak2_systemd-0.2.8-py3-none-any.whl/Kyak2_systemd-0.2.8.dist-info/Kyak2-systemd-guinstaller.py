#!/usr/bin/env python3
# -*- coding: utf-8 -*
from tkinter import *
import os
veri = Tk()
veri.title('Kyak2-systemd-installer')
veri.geometry('400x200')
veri.configure(bg='#252726')
veri.maxsize(400,200)
veri.minsize(400,200)

Label(text="Welcome to my app it needs Xterm terminal software\nand sudo permission to copy files needed locations\nTwo times password is asked for each button\nEnter password wait 5 sec and close.",fg='#00FA9A',bg='#252726').place(x=0,y=0)


def deger1():
    os.system("xterm -hold -e sudo cp Kyak2-systemd.py /usr/share/applications")
    os.system("xterm -hold -e sudo cp Kyak2-systemd.desktop /usr/share/applications")
def deger2():
    os.system("xterm -hold -e sudo cp Kyak2-systemd.py /usr/bin")
    os.system("xterm -hold -e sudo cp Kyak2-systemd.desktop /usr/bin")
	
buton = Button(veri,text='Menu Launcher',fg='crimson',bg='#252726',command=deger1)
buton.place(x=135, y=100)
buton2 = Button(veri,text='Terminal Shortcut',fg='crimson',bg='#252726',command=deger2)
buton2.place(x=135, y=160)




veri.mainloop()