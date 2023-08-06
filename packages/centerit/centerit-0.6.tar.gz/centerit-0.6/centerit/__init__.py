'''
A library for centering tkinter and pyqt windows both horizontally and vertically.
https://github.com/MrinmoyHaloi/centerit
'''

import sys

try:
	from PyQt5.QtWidgets import *
	from tkinter import *
except ImportError:
	print("One or none of the gui library not installed. But you can still use it for the other one")

if "PyQt5" in sys.modules:
	app = QApplication(sys.argv)
	screen = app.primaryScreen().size()

def centertk(win, width, height):
	'''
	Pass the root window name and the dimensions you want for your window. It uses tkinter winfo for getting screen width and height.
	'''
	try:
		xposi = win.winfo_screenwidth()/2 - width/2
		yposi = win.winfo_screenheight()/2 - height/2
		win.geometry(f'{width}x{height}+{int(xposi)}+{int(yposi)}')
	except ImportError:
		print("Tkinter not installed")

def centerqt(win, width, height):
	'''
	Pass the root window name and the dimensions you want for your window. It uses QApplicaton.primaryScreen for getting screen width and height.
	'''
	try:
		xposi = screen.width()/2 - width/2
		yposi = screen.height()/2 - height/2
		win.setGeometry(int(xposi),int(yposi),int(width),int(height))
	except ImportError:
		print("PyQt5 not installed")