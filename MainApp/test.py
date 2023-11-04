# from MainApp.src.plot import getDataPlots

# data, loadTimes = getDataPlots()
#
# for time in loadTimes:
#     print(f"Time: {time}")
#     print("REL FORCES:")
#     for relForce in data[time]["relForce"]:
#         print(relForce)
#     print("ABS FORCES:")
#     for absForce in data[time]["absForce"]:
#         print(absForce)
#     print("REL VARIABLE:")
#     for relVar in data[time]["relVar"]:
#         print(relVar)
#     print("ABS VARIABLE:")
#     for absVar in data[time]["absVar"]:
#         print(absVar)
#     print("ABS MAX:")
#     for absMax in data[time]["absMax"]:
#         print(absMax)
#     print()
#     print()

from matplotlib.widgets import Slider
import math

import matplotlib.pyplot as plt


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

t = [i / 100. for i in range(0, int(math.pi) * 100, 1)]

s = [math.sin(i * 20) for i in t]
l, = plt.plot(t, s, lw=2, color='red')
plt.axis([0, 1, -10, 10])

axcolor = 'gray'
ax_x_pos = plt.axes([0.25, 0.1, 0.65, 0.03])

wsize = 10

x_pos = Slider(ax_x_pos, 'Position', 0, len(t) - wsize - 1, valfmt='%d', valinit=0)

ax.set_xlim(t[0], t[wsize])
ax.set_ylim(-1.1, 1.1)


def update(val):
    print(x_pos.val)
    pos = int(x_pos.val)
    ax.set_xlim(t[pos], t[pos + wsize])
    fig.canvas.draw_idle()

x_pos.on_changed(update)

plt.show()
