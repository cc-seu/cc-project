# coding=utf-8
import tkinter as tk
from tkinter import filedialog, dialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter.messagebox
from pearson import correlation
from tkinter import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.naive_bayes import GaussianNB
import numpy as np
# import tslearn.metrics as metrics
# from tslearn.clustering import silhouette_score
# from tslearn.preprocessing import TimeSeriesScalerMeanVariance
# from tslearn.generators import random_walks
# from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from tslearn.clustering import KShape
import tkinter.font as tf
from numpy import *
from scipy import stats
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
# from sequentia.classifiers import KNNClassifier


class RootWindow(tk.Frame):
    def __init__(self, master=None):
        # 呼吸波形序列采样率统一为62.5
        self.X, self.Y, self.Z, self.step, self.S_temp = [], [], [], [], []
        self.S1, self.S2, self.S3, self.S4, self.S5, self.S6 = [], [], [], [], [], []
        self.S1_temp, self.S2_temp, self.S3_temp, self.S4_temp, self.S5_temp, self.S6_temp = [], [], [], [], [], []
        self.X_norm, self.Y_norm, self.Z_norm, self.T_norm = [], [], [], []
        self.X_norm_learn, self.Y_norm_learn, self.Z_norm_learn = [], [], []
        self.X_abnorm, self.Y_abnorm, self.Z_abnorm, self.T_abnorm = [], [], [], []
        self.cur_X, self.cur_Y, self.cur_Z, self.cur_T = [], [], [], []              # 用于自动选择标注周期
        self.choose_X, self.choose_Y, self.choose_Z, self.choose_T = [], [], [], []  # 用于手动选择标注周期
        self.scroll_x, self.scroll_y, self.scroll_z, self.scroll_t = [], [], [], []
        self.man_X, self.man_Y, self.man_Z, self.man_label = [], [], [], []
        self.s_time = None
        self.ax_time = None
        self.anim = None
        self.exist = False
        self.scroll_num = 0
        self.anim_num = 0
        self.scroll_rela_anim = 0
        self.anim_running = True
        self.div_point = []
        self.div_point_index = []
        self.div_point_flag = []
        self.label_state = []
        self.flag_norm, self.flag_abnorm = [], []
        self.filepath = ''
        self.pic_count = -1
        self.label_mod = 0
        # self.peep = 15  # 呼气末期正压
        tk.Frame.__init__(self, master)
        self.f = plt.Figure(figsize=(10, 6), dpi=200)
        self.a = self.f.add_subplot(311)  # 添加子图:1行1列第1个
        self.b = self.f.add_subplot(312)
        self.c = self.f.add_subplot(313)
        self.f.subplots_adjust(left=None, bottom=0.2, right=None, top=0.9, wspace=None, hspace=0.5)
        self.font1 = {'family': 'Arial', 'weight': 'bold', 'size': 20}
        self.a.set_ylabel("Pressure", self.font1)
        self.b.set_ylabel("Flow", self.font1)
        self.c.set_ylabel("Volume", self.font1)
        self.c.set_xlabel("Time(s)", self.font1)
        self.a.tick_params(labelsize=13)
        self.b.tick_params(labelsize=13)
        self.c.tick_params(labelsize=13)
        self.labels = self.a.get_xticklabels() + self.a.get_yticklabels()
        [label.set_fontname('Arial') for label in self.labels]
        self.labels = self.b.get_xticklabels() + self.b.get_yticklabels()
        [label.set_fontname('Arial') for label in self.labels]
        self.labels = self.c.get_xticklabels() + self.c.get_yticklabels()
        [label.set_fontname('Arial') for label in self.labels]
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.callbacks.connect('button_press_event', self.left_key)  # 获取鼠标点击的坐标位置
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)
        self.createWigets()
        self.pack()

    def createWigets(self):
        ftEntry = tf.Font(family='黑体', size=13, weight=tf.BOLD, slant=tf.ROMAN, underline=False, overstrike=False)
        ft1 = tf.Font(family='黑体', size=15, weight=tf.BOLD, slant=tf.ROMAN, underline=False, overstrike=False)
        ft2 = tf.Font(family='黑体', size=25, weight=tf.BOLD, slant=tf.ROMAN, underline=False, overstrike=False)
        self.contentVar = tkinter.StringVar(self, '')
        self.contentEntry = tkinter.Entry(self, font=ftEntry, textvariable=self.contentVar)
        self.contentEntry['state'] = 'readonly'
        self.contentEntry.place(x=50, y=10, width=300, height=70)
        self.contentVar1 = tkinter.StringVar(self, '')
        self.contentEntry1 = tkinter.Entry(self, font=ftEntry, textvariable=self.contentVar1)
        self.contentEntry1['state'] = 'readonly'
        self.contentEntry1.place(x=365, y=10, width=300, height=70)

        tkinter.Button(master=self, text="加载数据", font=ft1, width=9, height=2, command=self.open_file).\
            place(relx=0.35, rely=0.012, width=150, height=50)
        tkinter.Button(master=self, text="正常/异常检测", font=ft1, width=9, height=2, command=self.pre_learn).\
            place(relx=0.44, rely=0.012, width=150, height=50)
        tkinter.Button(master=self, text="←", font=ft1, width=7, height=2, command=self.last_picture).\
            place(relx=0.92, rely=0.43, width=130, height=60)
        tkinter.Button(master=self, text="→", font=ft1, width=7, height=2, command=self.next_picture).\
            place(relx=0.92, rely=0.34, width=130, height=60)
        tkinter.Button(master=self, text="√", font=ft2, fg='green', width=7, height=2, command=self.true).\
            place(relx=0.92, rely=0.61, width=130, height=60)
        tkinter.Button(master=self, text="×", font=ft2, fg='red', width=7, height=2, command=self.false).\
            place(relx=0.92, rely=0.52, width=130, height=60)
        tkinter.Button(master=self, text="播放/暂停", font=ft1, width=7, height=2, command=self.wave_Player).\
            place(relx=0.92, rely=0.7, width=130, height=60)

    def update_Graph(self):
        """根据滚动条值更新显示波形"""
        self.a.cla()
        self.b.cla()
        self.c.cla()
        self.a.plot(self.scroll_t[self.scroll_num], self.scroll_x[self.scroll_num], 'black')
        self.b.plot(self.scroll_t[self.scroll_num], self.scroll_y[self.scroll_num], 'black')
        self.c.plot(self.scroll_t[self.scroll_num], self.scroll_z[self.scroll_num], 'black')
        self.a.set_ylabel("Pressure")
        self.b.set_ylabel("Flow")
        self.c.set_ylabel("Volume")
        self.c.set_xlabel("Time/s")
        self.canvas.draw()

    def update_From_Scroll(self, val):
        """利用滚动条播放原始波形"""
        self.scroll_num = int(self.s_time.val)
        self.scroll_rela_anim = int(self.s_time.val) - self.anim_num
        self.update_Graph()

    def update_From_Anim(self, val):
        """自动播放原始波形"""
        self.anim_num = val
        self.scroll_num = val + self.scroll_rela_anim
        self.s_time.set_val(self.scroll_num)
        if self.scroll_num < len(self.scroll_x):
            self.update_Graph()

    def wave_Player(self):
        """控制自动播放开始/暂停"""
        if self.anim_running:
            self.anim.event_source.stop()
            self.anim_running = False
        else:
            self.anim.event_source.start()
            self.anim_running = True

    def left_key(self, event):
        """描红左键点击的波形区域"""
        if event.inaxes is not None and event.y > 200:
            if self.label_mod == 1:
                tk.messagebox.showinfo(title='信息提示！', message='当前选中周期尚未标注！')
            else:
                x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
                right_seg = 0
                for right_seg in range(len(self.div_point_index)):   # 这边可以使用二分法进行查找
                    if self.div_point_index[right_seg] >= x * 62.5:
                        break
                left_seg = right_seg - 1                           # 将选中的周期波形高亮显示
                self.choose_X = []
                self.choose_Y = []
                self.choose_Z = []
                self.choose_T = []
                for i in range(self.div_point_index[left_seg], self.div_point_index[right_seg] + 1):
                    self.choose_X.append(self.X[i])
                    self.choose_Y.append(self.Y[i])
                    self.choose_Z.append(self.Z[i])
                    self.choose_T.append(i / 62.5)
                self.a.plot(self.choose_T, self.choose_X, 'r')
                self.b.plot(self.choose_T, self.choose_Y, 'r')
                self.c.plot(self.choose_T, self.choose_Z, 'r')
                self.canvas.draw()
                self.label_mod = 1
                self.man_X.append(self.choose_X)
                self.man_Y.append(self.choose_Y)
                self.man_Z.append(self.choose_Z)

    def open_file(self):
        """打开并读取原始文件"""
        self.pic_count = -1
        self.X.clear()
        self.Y.clear()
        self.Z.clear()
        self.step.clear()
        self.S1.clear()
        self.S2.clear()
        self.S3.clear()
        self.S4.clear()
        self.S5.clear()
        self.S6.clear()
        self.S_temp.clear()
        self.S1_temp.clear()
        self.S2_temp.clear()
        self.S3_temp.clear()
        self.S4_temp.clear()
        self.S5_temp.clear()
        self.S6_temp.clear()
        self.X_norm.clear()
        self.Y_norm.clear()
        self.Z_norm.clear()
        self.T_norm.clear()
        self.X_norm_learn.clear()
        self.Y_norm_learn.clear()
        self.Z_norm_learn.clear()
        self.X_abnorm.clear()
        self.Y_abnorm.clear()
        self.Z_abnorm.clear()
        self.T_abnorm.clear()
        self.div_point.clear()
        self.div_point_index.clear()
        self.div_point_flag.clear()
        self.label_state.clear()
        self.flag_norm.clear()
        self.flag_abnorm.clear()
        self.filepath = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('C:/')))
        with open(file=self.filepath, mode='r+', encoding='utf-8') as f:
            lines = f.readlines()
            j = 0
            for line in lines:
                value = [float(s) for s in line.split()]
                self.X.append(round((value[0] / 10) - 12.8, 1))
                self.Z.append(value[2])
                if 3 > (value[1] - 1799) > -3:
                    self.Y.append(0)
                    self.step.append(j)
                else:
                    self.Y.append((value[1] - 1799) / 10)
                    self.step.append(j)
                    j = j + 1
        self.scroll_x.clear()
        self.scroll_y.clear()
        self.scroll_z.clear()
        self.scroll_t.clear()
        count = 0
        tmp_x = []
        tmp_y = []
        tmp_z = []
        tmp_t = []
        for i in range(len(self.X)):
            if count == 1500 or i == len(self.X) - 1:
                self.scroll_x.append(tmp_x)
                self.scroll_y.append(tmp_y)
                self.scroll_z.append(tmp_z)
                self.scroll_t.append(tmp_t)
                count = 1
                tmp_x = []
                tmp_y = []
                tmp_z = []
                tmp_t = []
                tmp_x.append(self.X[i])
                tmp_y.append(self.Y[i])
                tmp_z.append(self.Z[i])
                tmp_t.append(i / 62.5)
            elif count != 1500:
                tmp_x.append(self.X[i])
                tmp_y.append(self.Y[i])
                tmp_z.append(self.Z[i])
                tmp_t.append(i / 62.5)
                count += 1
        if self.exist:
            del self.ax_time
        self.ax_time = self.f.add_axes([0.12, 0.05, 0.78, 0.03], frameon=True)
        self.s_time = Slider(self.ax_time, '', 0, len(self.scroll_x) - 1, valinit=0, valstep=1)
        self.exist = True
        self.s_time.on_changed(self.update_From_Scroll)
        self.anim = FuncAnimation(self.f, self.update_From_Anim, interval=500, frames=len(self.scroll_x) - 1)
        self.wave_pretreatment()
        tk.messagebox.showinfo(title='信息提示！', message='文件预处理完毕！')
        self.next_picture()

    # def read_standard(self, file_path, data):
    #     with open(file=file_path, mode='r+', encoding='utf-8') as f:
    #         for line in f.readlines():
    #             line = line.strip('\n')
    #             data.append(float(line))

    def wave_pretreatment(self):  # 呼吸波形序列预处理
        # 加载标准波形（6个）
        # file_path = 'standard1.txt'
        # self.read_standard(file_path, self.S1)
        # file_path = 'standard2.txt'
        # self.read_standard(file_path, self.S2)
        # file_path = 'standard3.txt'
        # self.read_standard(file_path, self.S3)
        # file_path = 'standard4.txt'
        # self.read_standard(file_path, self.S4)
        # file_path = 'standard5.txt'
        # self.read_standard(file_path, self.S5)
        # file_path = 'standard6.txt'
        # self.read_standard(file_path, self.S6)
        self.S1 = [0.0, 1.1, 4.2, 7.4, 11.2, 15.8, 20.7, 25.5, 29.8, 33.4, 35.1, 35.3, 35.0, 34.3, 34.1, 33.8, 33.5,
                   33.0, 32.6, 31.7, 31.0, 30.3, 29.6, 28.9, 28.2, 27.8, 27.0, 26.1, 25.4, 24.9, 24.2, 23.6, 23.0, 22.5,
                   22.2, 21.7, 21.3, 20.8, 20.3, 20.2, 19.7, 19.0, 18.8, 18.5, 17.9, 17.8, 17.7, 17.3, 16.7, 16.6, 15.8,
                   15.5, 15.1, 14.3, 14.0, 13.5, 13.1, 12.7, 11.9, 11.6, 11.2, 10.7, 10.2, 6.6, -3.9, -16.4, -25.3,
                   -30.4, -32.6, -32.7, -33.0, -32.8, -32.0, -30.6, -30.6, -30.5, -29.3, -28.7, -27.0, -26.2, -26.0,
                   -25.4, -24.9, -24.5, -23.7, -23.1, -22.2, -22.5, -21.9, -21.9, -21.2, -21.0, -20.5, -20.2, -20.3,
                   -19.4, -19.7, -18.8, -18.5, -18.0, -17.2, -16.8, -16.1, -15.3, -14.6, -14.6, -13.8, -14.2, -13.4,
                   -12.9, -12.2, -11.4, -11.6, -11.4, -11.0, -10.2, -9.9, -9.7, -8.9, -8.8, -8.7, -9.0, -8.8, -8.5,
                   -8.1, -7.9, -7.5, -7.1, -6.8, -6.2, -6.4, -5.9, -5.5, -5.3, -5.4, -5.3, -5.3, -5.4, -5.4, -5.3, -5.0,
                   -4.4, -4.0, -3.7, -3.7, -3.7, -3.8, -3.6, -3.6, -3.4, -3.3, -3.4, -3.5, -3.4, -3.6, -3.8, -3.8, -4.0,
                   -4.0, -4.0, -3.9, -3.7, -3.4, -3.2, -3.1, -3.2, -3.3, -3.2, -3.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.S2 = [0.0, 1.1, 5.3, 9.5, 13.6, 18.4, 23.5, 28.3, 32.6, 35.3, 36.4, 36.2, 35.4, 34.7, 34.3, 34.0, 34.0,
                   33.5, 33.0, 32.1, 31.2, 30.5, 29.5, 29.0, 28.3, 27.7, 27.2, 26.1, 25.5, 24.9, 24.2, 23.6, 22.9, 22.3,
                   21.8, 21.2, 20.6, 20.4, 19.6, 18.9, 18.5, 17.9, 17.5, 17.2, 16.7, 16.2, 15.8, 15.5, 14.9, 14.5, 14.0,
                   13.5, 12.9, 12.5, 11.9, 11.5, 10.9, 10.4, 10.0, 9.3, 8.8, 8.4, 8.2, 3.2, -11.2, -24.3, -28.9, -32.3,
                   -33.3, -33.3, -33.2, -32.3, -31.5, -31.0, -30.6, -29.8, -28.7, -28.2, -27.4, -26.2, -25.4, -25.1,
                   -24.8, -23.7, -23.0, -23.3, -22.3, -21.3, -21.3, -21.5, -20.1, -20.4, -20.1, -20.1, -19.8, -19.4,
                   -19.2, -18.9, -17.7, -16.8, -16.7, -16.3, -15.2, -14.6, -14.3, -14.2, -13.8, -13.2, -12.4, -11.3,
                   -11.9, -11.1, -11.1, -10.5, -10.3, -9.6, -9.3, -9.5, -9.6, -8.8, -8.3, -7.7, -7.5, -7.4, -7.0, -6.8,
                   -6.5, -6.2, -5.9, -5.9, -5.8, -5.5, -5.3, -5.1, -4.9, -4.5, -4.4, -4.5, -4.2, -4.4, -4.5, -4.6, -4.6,
                   -4.3, -3.8, -3.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.S3 = [0.0, 1.3, 4.4, 7.8, 10.5, 14.9, 20.2, 24.6, 29.3, 33.4, 35.7, 37.0, 37.3, 36.7, 36.2, 35.5, 35.0,
                   34.5, 33.7, 33.1, 32.2, 31.5, 31.1, 30.5, 29.9, 29.5, 28.9, 28.2, 27.4, 26.6, 25.8, 25.1, 24.4, 23.9,
                   22.9, 22.2, 21.6, 20.8, 20.0, 19.7, 19.1, 18.4, 17.9, 17.5, 17.3, 16.7, 16.2, 15.8, 15.2, 14.9, 14.3,
                   13.9, 13.8, 13.3, 13.0, 12.8, 12.3, 12.2, 11.7, 11.1, 10.8, 10.5, 9.9, 6.4, -4.1, -17.2, -26.1,
                   -30.7, -33.0, -32.6, -32.6, -32.0, -31.7, -31.2, -30.2, -30.0, -29.0, -29.0, -27.8, -26.7, -26.2,
                   -25.9, -24.9, -24.6, -24.2, -23.9, -22.8, -21.8, -21.5, -20.6, -20.7, -19.8, -19.6, -20.4, -19.7,
                   -19.2, -19.0, -18.8, -18.0, -17.3, -16.8, -16.9, -15.8, -15.5, -15.0, -15.2, -14.7, -14.3, -13.4,
                   -13.1, -12.2, -12.4, -11.7, -11.3, -11.0, -10.8, -10.2, -10.0, -10.1, -9.3, -9.2, -9.0, -8.2, -7.8,
                   -7.5, -7.4, -7.3, -6.9, -6.8, -6.4, -6.3, -5.9, -5.7, -5.5, -5.0, -4.7, -4.3, -4.0, -3.9, -3.8, -3.7,
                   -3.5, -3.2, -3.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3.1, -3.2, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.S4 = [0.0, 3.4, 5.2, 8.4, 13.4, 17.6, 22.6, 27.7, 31.7, 35.0, 36.5, 36.9, 36.5, 35.8, 35.1, 34.5, 34.0,
                   33.6, 33.4, 32.5, 31.9, 31.3, 30.3, 29.6, 28.7, 27.9, 27.2, 26.2, 25.7, 25.4, 24.6, 24.3, 24.2, 23.4,
                   22.8, 22.2, 21.5, 20.8, 19.8, 19.1, 18.2, 17.8, 17.0, 16.1, 15.6, 14.7, 14.1, 13.4, 12.8, 12.2, 11.9,
                   11.6, 11.2, 11.0, 10.4, 10.0, 9.9, 9.5, 9.2, 9.2, 8.9, 8.9, 9.1, 3.6, -10.4, -22.8, -27.5, -30.3,
                   -31.5, -31.9, -31.6, -31.3, -30.1, -29.9, -29.8, -28.9, -28.1, -26.5, -26.0, -25.4, -24.9, -24.0,
                   -23.6, -23.1, -23.3, -22.2, -22.2, -21.6, -20.7, -20.6, -20.8, -19.9, -19.7, -19.4, -18.9, -18.3,
                   -17.2, -16.8, -16.2, -15.6, -16.1, -15.6, -15.0, -13.8, -13.4, -12.6, -12.8, -12.7, -12.9, -12.2,
                   -11.5, -11.3, -11.2, -11.0, -10.5, -9.7, -9.8, -8.6, -9.4, -8.7, -8.3, -8.2, -7.6, -7.3, -6.9, -6.5,
                   -6.7, -5.8, -5.3, -5.1, -4.9, -4.4, -4.1, -3.9, -3.9, -3.7, -3.3, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.S5 = [0.0, 3.8, 7.3, 10.6, 15.9, 21.3, 26.1, 31.0, 35.0, 36.7, 37.6, 37.3, 36.8, 36.1, 35.5, 35.4, 34.9,
                   34.2, 33.5, 33.0, 32.2, 31.5, 30.8, 29.9, 29.5, 28.8, 28.0, 27.2, 26.6, 25.8, 25.1, 24.2, 23.6, 22.6,
                   22.0, 21.6, 21.0, 20.6, 20.1, 19.6, 19.2, 18.6, 17.7, 17.2, 16.7, 15.9, 15.2, 14.3, 13.6, 12.9, 12.1,
                   11.5, 10.8, 10.5, 10.0, 9.5, 9.1, 8.9, 8.8, 8.4, 8.1, 8.0, 5.1, -4.7, -17.9, -26.4, -30.5, -32.4,
                   -32.4, -32.4, -32.2, -31.2, -30.9, -30.5, -29.9, -29.0, -27.9, -27.3, -26.8, -26.0, -25.7, -24.6,
                   -24.6, -23.7, -23.4, -22.5, -22.2, -21.2, -20.9, -20.7, -20.2, -19.3, -19.3, -18.9, -19.0, -18.1,
                   -17.2, -17.2, -17.0, -16.7, -16.7, -16.5, -14.8, -14.2, -13.0, -13.0, -13.3, -13.6, -12.9, -12.6,
                   -12.2, -11.5, -10.8, -10.7, -11.0, -10.7, -9.8, -9.9, -9.5, -9.5, -9.3, -8.9, -8.4, -8.0, -7.3, -7.0,
                   -6.7, -6.8, -6.7, -6.4, -6.4, -6.0, -5.6, -4.8, -4.8, -4.3, -3.9, -3.5, -3.3, -3.3, -3.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.S6 = [0.0, 1.1, 0.7, 1.4, 2.0, 4.1, 6.8, 9.4, 13.4, 17.9, 22.5, 27.0, 31.4, 35.0, 37.9, 39.1, 39.1, 38.4,
                   37.6, 37.2, 36.8, 36.7, 36.7, 36.1, 35.5, 34.6, 33.9, 33.2, 32.5, 32.1, 31.4, 30.7, 30.3, 29.5, 29.0,
                   28.2, 27.6, 27.2, 26.8, 26.4, 25.8, 25.8, 25.6, 25.1, 24.5, 24.4, 24.0, 23.7, 23.6, 23.1, 23.0, 22.7,
                   22.4, 22.3, 22.0, 21.5, 20.8, 20.4, 20.1, 19.3, 19.0, 18.9, 18.0, 17.6, 17.5, 17.0, 16.2, 16.5, 6.6,
                   -7.8, -19.9, -24.4, -28.6, -30.4, -30.9, -29.7, -30.0, -28.3, -27.6, -27.8, -27.3, -26.4, -26.3,
                   -26.7, -26.3, -25.5, -25.0, -24.3, -24.2, -24.1, -24.5, -24.0, -24.1, -23.9, -23.7, -23.6, -23.9,
                   -23.5, -22.9, -23.2, -23.4, -23.0, -22.7, -22.1, -21.3, -21.0, -21.3, -20.8, -20.3, -19.6, -19.3,
                   -19.0, -18.6, -18.5, -17.1, -17.1, -16.6, -16.0, -16.0, -16.0, -14.9, -13.7, -13.1, -12.8, -13.0,
                   -12.1, -11.9, -12.3, -12.0, -10.9, -10.5, -10.3, -9.9, -9.4, -9.0, -8.8, -8.7, -8.3, -8.1, -7.8,
                   -7.7, -7.3, -7.2, -7.0, -6.7, -6.6, -6.1, -5.9, -5.6, -5.7, -5.9, -6.0, -5.9, -6.0, -5.6, -5.4, -4.9,
                   -4.7, -4.7, -4.7, -4.4, -4.4, -4.7, -4.7, -4.7, -4.7, -4.7, -4.8, -4.8, -4.9, -4.9, -4.9, -4.7, -4.5,
                   -4.5, -4.2, -3.8, -3.7, -3.6, -3.2, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        for i in range(0, 200):  # 将所有标准序列长度设为200
            self.S1_temp.append(self.S1[i])
            self.S2_temp.append(self.S2[i])
            self.S3_temp.append(self.S3[i])
            self.S4_temp.append(self.S4[i])
            self.S5_temp.append(self.S5[i])
            self.S6_temp.append(self.S6[i])

        n = len(self.Y)
        if len(self.Y) != 0:
            for i in range(0, n - 10):  # 自动分割 结合流速波形以及容量阈值
                if -5 < self.Y[i] < 5 and (
                        (self.Y[i + 10] - self.Y[i]) / 0.16 + (self.Y[i + 8] - self.Y[i]) / 0.128 + (
                        self.Y[i + 6] - self.Y[i]) / 0.096 + (
                                self.Y[i + 4] - self.Y[i]) / 0.064 + (self.Y[i + 2] - self.Y[i]) / 0.032) > 600 and \
                        self.Z[i] < 50 and self.div_point[len(self.div_point) - 1] != 1:  # 利用斜率变化和容量进行综合判断
                    self.div_point.append(1)
                    self.div_point_flag.append(1)
                else:
                    self.div_point.append(0)
                    self.div_point_flag.append(0)

        for i in range(len(self.div_point) - 80):  # 消除同一个周期中多次划分
            if self.div_point[i] == 1:
                for j in range(i + 1, i + 80):
                    if self.div_point[j] == 1:
                        self.div_point[i] = 0
                        self.div_point_flag[i] = 0

        for i in range(0, n - 10):
            if self.div_point[i] == 1:
                self.div_point_index.append(i)  # div_point_index用来记录在哪些索引下面进行了周期的划分

        # 统计序列长度信息
        # Len = []
        # for i in range(0, m - 1):
        #     if 150 <= (div_point_index[i + 1] - div_point_index[i] + 1) < 300:
        #         len_temp = div_point_index[i + 1] - div_point_index[i] + 1  # 保留每个小序列的长度
        #         Len.append(len_temp)
        # print(mean(Len))
        # print(median(Len))
        # print(max(Len))
        # print(min(Len))
        # print(stats.mode(Len)[0][0])

        m = len(self.div_point_index)
        for i in range(0, m - 1):
            X_temp, Y_temp, Z_temp, tempx, tempy, tempz, T_temp = [], [], [], [], [], [], []
            point = 0  # point用来记录对当前周期波形的评分，大于等于5正常，否则算异常
            for j in range(self.div_point_index[i], self.div_point_index[i + 1] + 1):  # 将每个周期的波形分割保存
                X_temp.append(self.X[j])
                Y_temp.append(self.Y[j])
                Z_temp.append(self.Z[j])
                T_temp.append(j / 62.5)

            if 150 <= (self.div_point_index[i + 1] - self.div_point_index[i] + 1) < 300:  # 将所有序列长度设为200，不够就补0或peep
                if len(Y_temp) >= 200:
                    for k in range(0, 200):
                        tempx.append(X_temp[k])
                        tempy.append(Y_temp[k])
                        tempz.append(Z_temp[k])
                elif len(Y_temp) < 200:
                    for k in range(0, len(Y_temp)):
                        tempx.append(X_temp[k])
                        tempy.append(Y_temp[k])
                        tempz.append(Z_temp[k])
                    for k in range(len(Y_temp), 200):
                        tempx.append(X_temp[len(Y_temp) - 1])
                        tempy.append(0)
                        tempz.append(0)

                cor1 = correlation(tempy, self.S1_temp)  # 与多个标准波形进行比较，算出其相似度 0.4中等相关以上
                if cor1 >= 0.4:
                    point += 1
                cor2 = correlation(tempy, self.S2_temp)
                if cor2 >= 0.4:
                    point += 1
                cor3 = correlation(tempy, self.S3_temp)
                if cor3 >= 0.4:
                    point += 1
                cor4 = correlation(tempy, self.S4_temp)
                if cor4 >= 0.4:
                    point += 1
                cor5 = correlation(tempy, self.S5_temp)
                if cor5 >= 0.4:
                    point += 1
                cor6 = correlation(tempy, self.S6_temp)
                if cor6 >= 0.4:
                    point += 1
                if point >= 5 and -1 < mean(tempy) < 1:  # 此处加入均值判断
                    self.X_norm.append(X_temp)
                    self.X_norm_learn.append(tempx)
                    self.Y_norm.append(Y_temp)
                    self.Y_norm_learn.append(tempy)
                    self.Z_norm.append(Z_temp)
                    self.Z_norm_learn.append(tempz)
                    self.T_norm.append(T_temp)
                    self.flag_norm.append(i)  # flag_norm用来记录正常波形在dix_point_index中的起始索引
                else:
                    self.X_abnorm.append(X_temp)
                    self.Y_abnorm.append(Y_temp)
                    self.Z_abnorm.append(Z_temp)
                    self.T_abnorm.append(T_temp)
                    self.flag_abnorm.append(i)  # flag_abnorm用来记录异常波形在dix_point_index中的起始索引
            elif self.div_point_index[i + 1] - self.div_point_index[i] + 1 >= 300:  # 周期划分过长可能是异常
                T_temp2 = []
                for k in range(self.div_point_index[i], self.div_point_index[i + 1] + 1):
                    T_temp2.append(k / 62.5)

                self.X_abnorm.append(X_temp)
                self.Y_abnorm.append(Y_temp)
                self.Z_abnorm.append(Z_temp)
                self.T_abnorm.append(T_temp2)
                self.flag_abnorm.append(i)

        (dir_path, tempfilename) = os.path.split(self.filepath)
        (origin_name, extension) = os.path.splitext(tempfilename)
        filename = dir_path + '/' + origin_name + "_abnormal.txt"
        file = open(filename, 'a')
        for k in range(len(self.X_abnorm)):
            # l = len(T_abnorm[k])
            s1 = str(self.X_abnorm[k]).replace('[', '').replace(']', '')
            s2 = str(self.Y_abnorm[k]).replace('[', '').replace(']', '')
            s3 = str(self.Z_abnorm[k]).replace('[', '').replace(']', '')
            # s = str(2) + '\t' + str(round(T_abnorm[k][0], 2)) + '--' + str(
            #     round(T_abnorm[k][l - 1], 2)) + '\t' + s2 + '\t' + s1 + '\t' + s3 + '\n'
            s = str(2) + '\t' + str(0) + '--' + str(0) + '\t' + s2 + '\t' + s1 + '\t' + s3 + '\n'
            # s = str(2) + '\t' + s1 + '\t' + s2 + '\t' + s3 + '\n'
            file.write(s)
        file.close()

        self.contentVar.set('疑似正常：' + str(len(self.Y_norm)) + '  ' + '疑似异常：' + str(len(self.Y_abnorm)))
        for i in range(0, len(self.X_norm)):
            self.label_state.append(0)

    # def Show(self, p, t, y):
    #     """重新定义绘图函数"""
    #     p.plot(t, y, color='black')

    def show_wave_in_all(self, pic_count: int):
        self.cur_X.clear()
        self.cur_Y.clear()
        self.cur_Z.clear()
        self.cur_T.clear()
        x2, y2, z2, t2 = [], [], [], []
        m = len(self.X)
        if 500 <= self.div_point_index[self.flag_norm[pic_count]] < m - 600:
            for i in range(self.div_point_index[self.flag_norm[pic_count]] - 500,
                           self.div_point_index[self.flag_norm[pic_count]] + 600):
                self.cur_X.append(self.X[i])
                self.cur_Y.append(self.Y[i])
                self.cur_Z.append(self.Z[i])
                self.cur_T.append(i / 62.5)
            for i in range(self.div_point_index[self.flag_norm[pic_count]],
                           self.div_point_index[self.flag_norm[pic_count] + 1]):
                x2.append(self.X[i])
                y2.append(self.Y[i])
                z2.append(self.Z[i])
                t2.append(i / 62.5)

        elif self.flag_norm[pic_count] < 500:
            for i in range(0, self.div_point_index[self.flag_norm[pic_count]] + 600):
                self.cur_X.append(self.X[i])
                self.cur_Y.append(self.Y[i])
                self.cur_Z.append(self.Z[i])
                self.cur_T.append(i / 62.5)
            for i in range(self.div_point_index[self.flag_norm[pic_count]],
                           self.div_point_index[self.flag_norm[pic_count] + 1]):
                x2.append(self.X[i])
                y2.append(self.Y[i])
                z2.append(self.Z[i])
                t2.append(i / 62.5)

        elif self.flag_norm[pic_count] >= m - 600:
            for i in range(self.div_point_index[self.flag_norm[pic_count]] - 500, m - 1):
                self.cur_X.append(self.X[i])
                self.cur_Y.append(self.Y[i])
                self.cur_Z.append(self.Z[i])
                self.cur_T.append(i / 62.5)
            for i in range(self.div_point_index[self.flag_norm[pic_count]],
                           self.div_point_index[self.flag_norm[pic_count] + 1]):
                x2.append(self.X[i])
                y2.append(self.Y[i])
                z2.append(self.Z[i])
                t2.append(i / 62.5)
        self.a.cla()
        self.b.cla()
        self.c.cla()
        self.a.plot(self.cur_T, self.cur_X, 'black')
        self.b.plot(self.cur_T, self.cur_Y, 'black')
        self.c.plot(self.cur_T, self.cur_Z, 'black')
        self.a.plot(t2, x2, 'r')
        self.b.plot(t2, y2, 'r')
        self.c.plot(t2, z2, 'r')
        self.a.set_ylabel("Pressure")
        self.b.set_ylabel("Flow")
        self.c.set_ylabel("Volume")
        self.c.set_xlabel("Time/s")
        # self.f.align_labels()
        self.a.vlines(x=t2[0], ymin=0, ymax=20, color='red', linestyles="dotted")
        self.b.vlines(x=t2[0], ymin=-50, ymax=50, color='red', linestyles="dotted")
        self.c.vlines(x=t2[0], ymin=0, ymax=500, color='red', linestyles="dotted")
        self.a.vlines(x=t2[len(t2) - 1], ymin=0, ymax=20, color='red', linestyles="dotted")
        self.b.vlines(x=t2[len(t2) - 1], ymin=-50, ymax=50, color='red', linestyles="dotted")
        self.c.vlines(x=t2[len(t2) - 1], ymin=0, ymax=500, color='red', linestyles="dotted")
        self.a.set_ylim((0, 20))
        self.canvas.draw()

    def next_picture(self):
        """绘制下一张图"""
        if self.label_mod == 0:
            self.pic_count += 1
            if self.label_state[self.pic_count] == 0:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '未标注')
            elif self.label_state[self.pic_count] == 1:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '正常')
            elif self.label_state[self.pic_count] == 2:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '异常')
            self.show_wave_in_all(self.pic_count)
        elif self.label_mod == 1:
            tk.messagebox.showinfo(title='信息提示！', message='当前选中周期尚未标注！')

    def last_picture(self):
        """绘制上一张图"""
        if self.label_mod == 0:
            self.pic_count -= 1
            if self.label_state[self.pic_count] == 0:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '未标注')
            elif self.label_state[self.pic_count] == 1:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '正常')
            elif self.label_state[self.pic_count] == 2:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '异常')
            self.show_wave_in_all(self.pic_count)
        elif self.label_mod == 1:
            tk.messagebox.showinfo(title='信息提示！', message='当前选中周期尚未标注！')

    def true(self):
        if self.label_mod == 0:
            self.label_state[self.pic_count] = 1
            self.pic_count += 1
            if self.label_state[self.pic_count] == 0:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '未标注')
            elif self.label_state[self.pic_count] == 1:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '正常')
            elif self.label_state[self.pic_count] == 2:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '异常')
            self.show_wave_in_all(self.pic_count)
        elif self.label_mod == 1:
            self.man_label.append(1)
            # print(self.man_label[len(self.man_label) - 1])
            # print(self.man_Y[len(self.man_Y) - 1])
            self.label_mod = 0
            self.a.plot(self.choose_T, self.choose_X, 'blue')
            self.b.plot(self.choose_T, self.choose_Y, 'blue')
            self.c.plot(self.choose_T, self.choose_Z, 'blue')
            self.canvas.draw()

    def false(self):
        if self.label_mod == 0:
            self.label_state[self.pic_count] = 2
            self.pic_count += 1
            if self.label_state[self.pic_count] == 0:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '未标注')
            elif self.label_state[self.pic_count] == 1:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '正常')
            elif self.label_state[self.pic_count] == 2:
                self.contentVar1.set('当前标注：' + str(self.pic_count) + '  ' + '标注状态：' + '异常')
            self.show_wave_in_all(self.pic_count)
        elif self.label_mod == 1:
            self.man_label.append(0)
            # print(self.man_label[len(self.man_label) - 1])
            # print(self.man_Y[len(self.man_Y) - 1])
            self.label_mod = 0
            self.a.plot(self.choose_T, self.choose_X, 'blue')
            self.b.plot(self.choose_T, self.choose_Y, 'blue')
            self.c.plot(self.choose_T, self.choose_Z, 'blue')
            self.canvas.draw()

    def pre_learn(self):
        x, x_temp, y, y_temp, y_learn, y_learn_temp = [], [], [], [], [], []  # x:流速波形数据；y:标注信息
        for i in range(0, self.pic_count):
            x.append(np.array(self.Y_norm_learn[i]))
            y.append(self.label_state[i])
        x_temp = x
        y_temp = y
        # x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)
        # knn = KNNClassifier(k=5, classes=[1, 2])
        # knn.fit(x_train, y_train)
        # answer = knn.predict(x_test)
        # print(classification_report(y_test, answer))
        x = np.array(x).reshape(self.pic_count, 200)
        y = np.array(y).reshape(self.pic_count, 1)
        x_train1, x_test1, y_train1, y_test1 = train_test_split(x, y, train_size=0.8)
        knn = KNeighborsClassifier().fit(x_train1, y_train1)
        answer_knn = knn.predict(x_test1)
        print(classification_report(y_test1, answer_knn))
        n = len(self.Y_norm)
        for j in range(self.pic_count, n):
            y_learn.append(np.array(self.Y_norm_learn[j]))
        y_learn_temp = y_learn
        y_learn = np.array(y_learn).reshape(n - self.pic_count, 200)
        answer2 = knn.predict(y_learn)
        # 存储顺序流速Y，压力X，潮气量Z
        m = len(x_temp)
        (dir_path, tempfilename) = os.path.split(self.filepath)
        (origin_name, extension) = os.path.splitext(tempfilename)
        filename = dir_path + '/' + origin_name + "_label.txt"
        file = open(filename, 'a')
        for k in range(len(x)):
            l = len(self.T_norm[k])
            s1 = str(self.X_norm_learn[k]).replace('[', '').replace(']', '')
            s2 = str(self.Y_norm_learn[k]).replace('[', '').replace(']', '')
            s3 = str(self.Z_norm_learn[k]).replace('[', '').replace(']', '')
            s = str(y_temp[k]) + '\t' + str(round(self.T_norm[k][0], 2)) + '--' + str(
                round(self.T_norm[k][l - 1], 2)) + '\t' + s2 + '\t' + s1 + '\t' + s3 + '\n'
            file.write(s)
        for i in range(len(y_learn)):
            l = len(self.T_norm[m + i])
            s1 = str(self.X_norm_learn[m + i]).replace('[', '').replace(']', '')
            s2 = str(self.Y_norm_learn[m + i]).replace('[', '').replace(']', '')
            s3 = str(self.Z_norm_learn[m + i]).replace('[', '').replace(']', '')
            s = str(answer2[i]) + '\t' + str(round(self.T_norm[m + i][0], 2)) + '--' + str(
                round(self.T_norm[m + i][l - 1], 2)) + '\t' + s2 + '\t' + s1 + '\t' + s3 + '\n'
            file.write(s)
        file.write('标注次数：' + str(self.pic_count) + '\n')
        file.write(classification_report(y_test1, answer_knn))
        file.close()
        tk.messagebox.showinfo(title='信息提示！', message='检测完毕！')


if __name__ == '__main__':
    app = RootWindow(master=tk.Tk())
    app.master.title("波形预标注")
    app.mainloop()
