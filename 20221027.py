# import tkinter
# from tkinter import *
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
#
# root = tkinter.Tk()
#
# x = []
# t = []
# for i in range(10000):
#     x.append(i)
#     t.append(i)
# fig, ax = plt.subplots()
# ax.plot(t, x)
#
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
# scrollbar = tkinter.Scrollbar(master=root, orient=HORIZONTAL)
# scrollbar.pack(side=tkinter.BOTTOM, fill=X)
# # scrollbar["command"] = canvas.get_tk_widget().xview
# # canvas.get_tk_widget()["xscrollcommand"] = scrollbar.set
# tkinter.mainloop()

# import matplotlib
# import numpy as np
# import tkinter as tk
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from matplotlib.widgets import Slider
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
# # load data
# nDt = 1000
# nDx = 400
# grd = np.zeros((nDt, nDx))
# val = np.zeros((nDt, nDx))
# for t in np.arange(nDt):
#     for x in np.arange(nDx):
#         grd[t, x] = x / nDx
#         val[t, x] = (x / nDx) * (t / nDt) * np.sin(10 * 2 * np.pi * (t - x) / nDt)
#
# matplotlib.use('TkAgg')
#
# root = tk.Tk()
# root.wm_title("Embedding in TK")
#
# fig = plt.Figure(figsize=(8, 6))
# canvas = FigureCanvasTkAgg(fig, root)
# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#
# ax = fig.add_subplot(111)
# fig.subplots_adjust(bottom=0.25)
# ax.set(xlim=(-0.05, 1.05), ylim=(-1.05, 1.05))
# ax.grid()
#
# ax_time = fig.add_axes([0.12, 0.1, 0.78, 0.03])
# s_time = Slider(ax_time, 'Time', 0, nDt, valinit=0, valstep=1)
# i_anim = 0
# i_relative = 0
# i_current = 0
#
#
# def updateGraph(i):
#     y_i = val[i, :]
#     ax.cla()
#     ax.plot(grd[i, :], y_i)
#
#
# def updateFromAnim(i):
#     global i_anim
#     global i_current
#     global i_relative
#     i_anim = i
#     i_current = i + i_relative
#     s_time.set_val(i_current)
#     updateGraph(i_current)
#
#
# def updateFromScroll(val):
#     global i_anim
#     global i_current
#     global i_relative
#     i_relative = int(s_time.val) - i_anim
#     i_current = int(s_time.val)
#     updateGraph(i_current)
#
#
# def onClick():
#     global anim_running
#     if anim_running:
#         anim.event_source.stop()
#         anim_running = False
#     else:
#         anim.event_source.start()
#         anim_running = True
#
#
# start_button = tk.Button(root, text="START/STOP", command=onClick)
# start_button.pack()
#
# anim_running = True
# anim = FuncAnimation(fig, updateFromAnim, interval=100, frames=np.linspace(0, nDt - 1, nDt))
#
# s_time.on_changed(updateFromScroll)
#
# tk.mainloop()

# import tkinter
#
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# # Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
#
# import numpy as np
#
#
# root = tkinter.Tk()
# root.wm_title("Embedding in Tk")
#
# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
#
# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
#
# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)
#
#
# canvas.mpl_connect("key_press_event", on_key_press)
#
#
# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
#
#
# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)
#
# tkinter.mainloop()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()  # 创建figure对象
ax = fig.add_subplot(projection='polar')  # 极坐标系
ax.set_axis_off()  # 取消坐标轴的显示
ln, = ax.plot([], [])

# 图像初始化
def init():
    ax.set_xlim(0, 2*np.pi)       # 设定x值范围
    ax.set_ylim(-1, 1)            # 设定y值范围
    xdata = [1,2,3,4]
    ydata = [0, 0, 0, 0]
    ln.set_data(xdata, ydata)
    return ln,

# 图像更新
def update(frame):
    xdata = [1*frame, 2*frame, 3*frame, 4*frame]
    ydata = [0,0,0,0]
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True, interval=1)
plt.show()

