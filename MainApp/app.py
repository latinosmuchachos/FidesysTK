from tkinter import *
from tkinter import ttk

import styles
from src import *

# Setting up the Main Application Window
window = Tk()
window.title("Convergence Plots")

# styles
styles.setMainframeStyle()
styles.setLabelStyle()

# Creating a Main Frame
mainframe = ttk.Frame(window, width=1000, height=700, style='TFrame')
# mainframe.pack()
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# путь до файла
pathToFile = StringVar()
pathToFile_entry = ttk.Entry(mainframe, textvariable=pathToFile, width=40)
pathToFile_entry.grid(column=1, row=1, sticky=(W, E))
ttk.Label(mainframe, text="Путь до файла расчета").grid(column=2, row=1,
                                                        sticky=(W, E))

# Frame для флагов отображения типов расчетов
choiceTypeDecision = ttk.Frame(mainframe, width=400, height=350,
                               style="TFrame")
choiceTypeDecision.grid(column=1, row=2, sticky=(W, E))
ttk.Label(choiceTypeDecision, text="Выберите типы отображаемых решений").grid(
    column=1, row=1, sticky=(W, E))

# ToDo: сделать флаги расчета

# кнопка запуска расчета
buttonStart = ttk.Button(mainframe, text="Запустить", command=startPlots)
buttonStart.grid(column=2, row=3, sticky=(W, E))


# паддинги для всех widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
