from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.widgets import Slider
import numpy as np


def readData(f):
    resultData = {
    }
    loadTimes = []
    # данные по итерации
    currentStep = {
        "loadTime": None,
        "relForce": [],
        "absForce": [],
        "relVar": [],
        "absVar": [],
        "absMax": [],
        "lineSearch": [],
        "count": 0
    }
    # countCal - кол-во значений
    countCal = 0

    lines = f.readlines()
    # с 4 индекса начинаются сами данные
    for line in lines[4:]:
        # проверка на переход к следующей итерации
        if line[:3] == "||-":
            # было ли что-то в итерации
            if currentStep["loadTime"] is not None:
                resultData[currentStep["loadTime"]] = currentStep
                loadTimes.append(currentStep["loadTime"])
            currentStep = {
                "loadTime": None,
                "relForce": [],
                "absForce": [],
                "relVar": [],
                "absVar": [],
                "absMax": [],
                "lineSearch": [],
                "count": 0
            }
        # проверка на criteria:
        elif line[3] == "C" or line[3] == "I":
            continue
        # итерация
        else:
            data = line.split("||")[1:-1]
            loadTime = float(data[0].strip())
            # обработка случая, если расчет закончен
            # Maximum number of iterations has been reached
            try:
                relForce = float(data[1].strip())
            except ValueError:
                continue
            absForce = float(data[2].strip())
            relVar = float(data[3].strip())
            absVar = float(data[4].strip())
            absMax = float(data[5].strip())
            countCal += 1
            # если первая запись итерации
            if currentStep["loadTime"] is None:
                currentStep["loadTime"] = loadTime
            # добавляем записи
            currentStep["relForce"].append(relForce)
            currentStep["absForce"].append(absForce)
            currentStep["relVar"].append(relVar)
            currentStep["absVar"].append(absVar)
            currentStep["absMax"].append(absMax)
    # добавление записей последней итерации
    if currentStep["loadTime"] is not None:
        resultData[currentStep["loadTime"]] = currentStep
        loadTimes.append(currentStep["loadTime"])

    return resultData, loadTimes, countCal


def preprocData(data, loadTimes):
    resultData = {
        "loadTime": [],
        "relForce": [],
        "absForce": [],
        "relVar": [],
        "absVar": [],
        "absMax": [],
        "steps": []
    }
    criteria_lines = []
    for time in loadTimes:
        relForce = data[time]["relForce"]
        absForce = data[time]["absForce"]
        relVar = data[time]["relVar"]
        absVar = data[time]["absVar"]
        absMax = data[time]["absMax"]
        for i in range(len(relForce)):
            resultData["loadTime"].append(time)
            resultData["relForce"].append(relForce[i])
            resultData["absForce"].append(absForce[i])
            resultData["relVar"].append(relVar[i])
            resultData["absVar"].append(absVar[i])
            resultData["absMax"].append(absMax[i])
        try:
            resultData["steps"].append(len(relForce) + resultData["steps"][-1])
        except IndexError:
            resultData["steps"].append(len(relForce))

    # удаление последней линии итераций
    resultData["steps"].pop()
    return resultData


def getDataPlots():
    try:
        with open(PATH_CON, 'r', encoding='utf-8') as f:
            data, loadTimes, countCal = readData(f)
            return preprocData(data, loadTimes)
    except OSError:
        print(f"Could not open file: {F_NAME}")


def add_slider(fig, step=1000):
    fig.subplots_adjust(left=0.25, bottom=0.25)
    ax_slider = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    slider = Slider(
        ax=ax_slider,
        label='Steps',
        valmin=0,
        valmax=step,
        valinit=0,
    )
    return slider


def graph_settings(PLOTS):
    plotRelForce = PLOTS["plotRelForce"]
    plotTime = PLOTS["plotTime"]
    plotAbsForce = PLOTS["plotAbsForce"]
    plotRelVar = PLOTS["plotRelVar"]
    plotAbsVar = PLOTS["plotAbsVar"]
    plotAbsMax = PLOTS["plotAbsMax"]
    # чистим все графики
    plotRelForce.clear()
    plotTime.clear()
    plotAbsForce.clear()
    plotRelVar.clear()
    plotAbsVar.clear()
    plotAbsMax.clear()

    # настройка REL FORCE
    plotRelForce.grid(True)  # устанавливаем сетку
    plotRelForce.set_yscale("log")  # Log-шкала по оси Y
    plotRelForce.set_ylabel("REL Force")  # Навзание оси Y

    # настройка TIME
    plotTime.grid(True)  # устанавливаем сетку
    plotTime.set_xlabel("Cumulative Iteration")  # Название оси X
    plotTime.set_ylabel("Time(s)")  # Название оси Y

    # настройка ABS FORCE
    plotAbsForce.grid(True)  # устанавливаем сетку
    plotAbsForce.set_xlabel("Cumulative Iteration")  # Название оси X
    plotAbsForce.set_ylabel("ABS Force")  # Название оси Y

    # настройка REL VAR
    plotRelVar.grid(True)  # устанавливаем сетку
    plotRelVar.set_xlabel("Cumulative Iteration")  # Название оси X
    plotRelVar.set_ylabel("REL Variable")  # Название оси Y

    # настройка ABS VAR
    plotAbsVar.grid(True)  # устанавливаем сетку
    plotAbsVar.set_xlabel("Cumulative Iteration")  # Название оси X
    plotAbsVar.set_ylabel("ABS Variable")  # Название оси Y

    # настройка ABS MAX
    plotAbsMax.grid(True)  # устанавливаем сетку
    plotAbsMax.set_xlabel("Cumulative Iteration")  # Название оси X
    plotAbsMax.set_ylabel("ABS Max")  # Название оси Y


def plotSteps(PLOTS, steps):
    plotRelForce = PLOTS["plotRelForce"]
    plotAbsForce = PLOTS["plotAbsForce"]
    plotRelVar = PLOTS["plotRelVar"]
    plotAbsVar = PLOTS["plotAbsVar"]
    plotAbsMax = PLOTS["plotAbsMax"]

    plots = [plotRelForce, plotAbsForce, plotRelVar, plotAbsVar, plotAbsMax]

    for plot in plots:
        flagFirst = True
        for step in steps:
            if flagFirst:
                plot.axvline(step, color='g', linestyle='dashed',
                        label="Substep Converged")
                flagFirst = False
            else:
                plot.axvline(step, color='g', linestyle='dashed')


def plot(fig, PLOTS, canvas):
    global CURRENT_LOAD_TIME
    global CURRENT_REL_FORCE
    global CURRENT_ABS_FORCE
    global CURRENT_REL_VAR
    global CURRENT_ABS_VAR
    global CURRENT_ABS_MAX
    plotRelForce = PLOTS["plotRelForce"]
    plotTime = PLOTS["plotTime"]
    plotAbsForce = PLOTS["plotAbsForce"]
    plotRelVar = PLOTS["plotRelVar"]
    plotAbsVar = PLOTS["plotAbsVar"]
    plotAbsMax = PLOTS["plotAbsMax"]

    data = getDataPlots()
    loadTime = np.array(data["loadTime"])
    relForce = np.array(data["relForce"])
    absForce = np.array(data["absForce"])
    relVar = np.array(data["relVar"])
    absVar = np.array(data["absVar"])
    absMax = np.array(data["absMax"])
    steps = data["steps"]

    # держим в памяти предыдущее считывание
    CURRENT_LOAD_TIME = loadTime
    CURRENT_REL_FORCE = relForce
    CURRENT_ABS_FORCE = absForce
    CURRENT_REL_VAR = relVar
    CURRENT_ABS_VAR = absVar
    CURRENT_ABS_MAX = absMax

    graph_settings(PLOTS)

    # отрисовка графиков
    plotRelForce.plot(relForce, marker='.', color='#4B0082',
                 linewidth=1, label="REL Force Convergence")
    plotAbsForce.plot(absForce, marker='.', color='#4B0082',
                 linewidth=1, label="ABS Force Convergence")
    plotRelVar.plot(relVar, marker='.', color='#4B0082',
                 linewidth=1, label="REL Variable Convergence")
    plotAbsVar.plot(absVar, marker='.', color='#4B0082',
                 linewidth=1, label="ABS Variable Convergence")
    plotAbsMax.plot(absMax, marker='.', color='#4B0082',
                 linewidth=1, label="ABS Max Convergence")
    plotTime.plot(loadTime, 'r.')
    plotSteps(PLOTS, steps)
    canvas.draw()


def draw_slider(fig, plotRelForce, plotTime):
    pass


CURRENT_LOAD_TIME = None
CURRENT_REL_FORCE = None
CURRENT_ABS_FORCE = None
CURRENT_REL_VAR = None
CURRENT_ABS_VAR = None
CURRENT_ABS_MAX = None

PATH_CON = 'C:/Users/skyri/Documents/CAE-Fidesys-6.0/PLOTS/fidesys01/Convergence.log'
F_NAME = PATH_CON.split('/')[-1]

window = Tk()
window.geometry("1500x1000")
window.title("Convergence Plots")

plot_button = Button(master=window,
                     command=lambda: plot(fig, PLOTS, canvas),
                     height=2,
                     width=10,
                     text="Draw")
plot_button.pack(side=LEFT)

slide_button = Button(master=window, command=lambda: draw_slider(fig, PLOTS), height=2, width=10,
                      text="Slide")
slide_button.pack(side=LEFT)

# создание фигуры с графиками
fig = Figure(figsize=(15, 10), dpi=100)
# создание графиков
plotRelForce = fig.add_subplot(611)
plotAbsForce = fig.add_subplot(612)
plotRelVar = fig.add_subplot(613)
plotAbsVar = fig.add_subplot(614)
plotAbsMax = fig.add_subplot(615)
plotTime = fig.add_subplot(616)

PLOTS = {
    "plotRelForce": plotRelForce,
    "plotAbsForce": plotAbsForce,
    "plotRelVar": plotRelVar,
    "plotAbsVar": plotAbsVar,
    "plotAbsMax": plotAbsMax,
    "plotTime": plotTime
}

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
canvas.get_tk_widget().pack()

window.mainloop()
