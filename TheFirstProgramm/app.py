from tkinter import *
from tkinter import ttk


def calculate(*args):
    try:
        # variavles feet and meters automatically update the global variables
        # it is magic textVariable in TK
        value = float(feet.get())
        meters.set(int(0.308 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


# Setting up the Main Application Window
root = Tk()
root.title("Feet to Meters")

# Creating a Content Frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# frame should expand to fill any extra space if the window is resized
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# Creating the Entry Widget
feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))


# Creating the Remaining Widgets
meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3,
                                                                row=3,
                                                                sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)


# Adding Some Polish
# walk through all the widgets contained within our content frame
for child in mainframe.winfo_children():
    # add a bit of paddin around each
    child.grid_configure(padx=5, pady=5)
# focus our entry widget
# users don't have to click on it before starting to type
feet_entry.focus()
# if user presses the Enter, it should call our calculate routine
root.bind("<Return>", calculate)


# Start the Event Loop
root.mainloop()
