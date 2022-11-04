# coding=utf-8
import tkinter as tk
from tkinter import filedialog, dialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
import matplotlib.pyplot as plt
import tkinter.font as tf
from numpy import *


class RootWindow(tk.Frame):
    def __init__(self, master=None):
        # 呼吸波形序列采样率统一为62.5
        self.X, self.Y, self.Z, self.step = [], [], [], []
        self.origin, self.right = [], []
        self.div_point = []
        self.filepath = ''
        self.pic_count = -1
        tk.Frame.__init__(self, master)
        self.f = plt.Figure(figsize=(10, 5.2), dpi=150)
        self.a = self.f.add_subplot(311)
        self.b = self.f.add_subplot(312)
        self.c = self.f.add_subplot(313)
        self.font1 = {'family': 'Arial', 'weight': 'bold', 'size': 20}
        self.font2 = tf.Font(family='黑体', size=15, weight=tf.BOLD, slant=tf.ROMAN, underline=0, overstrike=0)
        self.createWigets()
        self.pack()

    def createWigets(self):
        self.f.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
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
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.label = tk.Label(self, bg="white", text="分割数量：", font=("微软雅黑", 14, "bold"))
        self.label.place(x=425, y=10, width=150, height=50)
        self.contentVar = tk.StringVar(self, '')
        self.contentEntry = tk.Entry(self, font=("微软雅黑", 14, "bold"), textvariable=self.contentVar)
        self.contentEntry['state'] = 'readonly'
        self.contentEntry.place(x=550, y=10, width=150, height=50)

        self.label1 = tk.Label(self, bg="white", text="应有数量：", font=("微软雅黑", 14, "bold"))
        self.label1.place(x=700, y=10, width=150, height=50)
        self.contentEntry1 = tk.Entry(self, font=("微软雅黑", 14, "bold"))
        self.contentEntry1.place(x=825, y=10, width=150, height=50)

        self.button_open_file = tk.Button(master=self, text="打开文件", font=self.font2, width=9, height=2,
                                          command=self.open_file).place(x=100, y=10, width=150, height=50)
        self.button_save = tk.Button(master=self, text="保存文件", font=self.font2, width=7, height=2,
                                     command=self.save).place(x=260, y=10, width=150, height=50)
        self.button_last_pic = tk.Button(master=self, text="←", font=self.font2, width=7, height=2,
                                         command=self.last_picture).place(relx=0.92, rely=0.43, width=100, height=50)
        self.button_next_pic = tk.Button(master=self, text="→", font=self.font2, width=7, height=2,
                                         command=self.next_picture).place(relx=0.92, rely=0.34, width=100, height=50)

    def open_file(self):
        self.pic_count = -1
        self.X.clear()
        self.Y.clear()
        self.Z.clear()
        self.step.clear()
        self.origin.clear()
        self.right.clear()
        self.div_point.clear()
        self.filepath = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('C:/')))
        with open(file=self.filepath, mode='r+', encoding='utf-8') as f:
            lines = f.readlines()
            j = 0
            for line in lines:
                value = [float(s) for s in line.split()]
                self.X.append(value[0] / 10 - 12.8)
                self.Z.append(value[2])
                if 3 > (value[1] - 1799) > -3:
                    self.Y.append(0)
                    self.step.append(j)
                else:
                    self.Y.append((value[1] - 1799) / 10)
                    self.step.append(j)
                    j = j + 1
        tk.messagebox.showinfo(title='信息提示！', message='文件读取完毕！')
        self.wave_pretreatment()
        self.next_picture()

    def wave_pretreatment(self):  # 呼吸波形序列预处理
        n = len(self.Y)
        if n != 0:
            for i in range(0, n - 10):  # 自动分割 结合流速波形以及容量阈值
                if -5 < self.Y[i] < 5 and ((self.Y[i + 10] - self.Y[i]) / 0.16 + (self.Y[i + 8] - self.Y[i]) / 0.128 + (self.Y[i + 6] - self.Y[i]) / 0.096 + (self.Y[i + 4] - self.Y[i]) / 0.064 + (self.Y[i + 2] - self.Y[i]) / 0.032) > 600 and self.Z[i] < 50 and self.div_point[len(self.div_point) - 1] != 1:
                    self.div_point.append(1)
                else:
                    self.div_point.append(0)
            for i in range(10):
                self.div_point.append(0)

        for i in range(len(self.div_point) - 80):  # 消除同一个周期中多次划分
            if self.div_point[i] == 1:
                for j in range(i + 1, i + 80):
                    if self.div_point[j] == 1:
                        self.div_point[i] = 0

    def show_wave(self):
        x1, y1, z1, t1, t2 = [], [], [], [], []
        for i in range(self.pic_count * 1875, (self.pic_count + 1) * 1875):
            x1.append(self.X[i])
            y1.append(self.Y[i])
            z1.append(self.Z[i])
            t1.append(i)
            t2.append(i / 62.5)
        self.a.cla()
        self.b.cla()
        self.c.cla()
        self.a.plot(t2, x1, color='black')
        self.b.plot(t2, y1, color='black')
        self.c.plot(t2, z1, color='black')
        self.a.set_ylabel("Pressure")
        self.b.set_ylabel("Flow")
        self.c.set_ylabel("Volume")
        self.c.set_xlabel("Time/s")
        count = 0
        for i in range(len(t1)):
            if self.div_point[t1[i]] == 1:
                count += 1
                self.a.axvline(x=t2[i], color='red')
                self.b.axvline(x=t2[i], color='red')
                self.c.axvline(x=t2[i], color='red')
                self.canvas.draw()
        self.origin.append(count)
        self.contentVar.set(str(count))
        self.canvas.draw()

    def next_picture(self):
        """绘制下一张图"""
        self.pic_count += 1
        if self.pic_count != 0:
            if self.contentEntry1.get() != '':
                self.right.append(self.contentEntry1.get())
            else:
                self.right.append('0')
            self.contentEntry1.delete(0, END)
        if self.pic_count * 1875 >= len(self.X):
            tk.messagebox.showwarning(title='提示', message='当前已是最后一张图')
        else:
            self.show_wave()

    def last_picture(self):
        """绘制上一张图"""
        self.pic_count -= 1
        self.show_wave()

    def save(self):
        sum_of_right = 0
        sum_of_origin = 0
        wave_num_differ = 0
        for k in range(len(self.right)):
            sum_of_origin = sum_of_origin + int(self.origin[k])
            sum_of_right = sum_of_right + int(self.right[k])
            wave_num_differ = wave_num_differ + abs(int(self.origin[k]) - int(self.right[k]))
        (dir_path, tempfilename) = os.path.split(self.filepath)
        (origin_name, extension) = os.path.splitext(tempfilename)
        filename = dir_path + '/' + origin_name + "verify_cut.txt"
        file = open(filename, 'a')
        for k in range(len(self.right)):
            s = str(self.right[k]) + '\t' + str(self.origin[k]) + '\n'
            file.write(s)
        s = str(wave_num_differ / sum_of_right)
        file.write(s)
        tk.messagebox.showinfo(title='信息提示！', message='文件保存完毕！')


if __name__ == '__main__':
    app = RootWindow(master=tk.Tk())
    app.master.title("周期划分判断")
    app.mainloop()
