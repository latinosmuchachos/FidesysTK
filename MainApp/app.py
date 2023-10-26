from tkinter import *
from tkinter import ttk


# Setting up the Main Application Window
root = Tk()
# ToDO придумать название
root.title("")


# Creating a Content Frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# frame should expand to fill any extra space if the window is resized
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)