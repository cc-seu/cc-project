from tkinter import filedialog
import matplotlib.pyplot as plt
import tkinter as tk  # 导入tkinter模块
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from read_label_file import read_label_file
from read_pre_classification_file import read_pre_classification_file
import os
import tkinter.font as tf
from PIL import Image, ImageTk


class PopupDialog(tk.Toplevel):
    def __init__(self, parent, path):
        super().__init__()
        self.title('特征图片对照')
        self.parent = parent  # 显式地保留父窗口
        image = Image.open(path)
        self.photo = ImageTk.PhotoImage(image)
        Lab = tk.Label(self, image=self.photo)
        Lab.pack()  # 设置主界面

    def ok(self):
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.destroy()


class RootWindow(tk.Frame):
    def __init__(self, master=None):
        self.pic_count = -1
        self.X, self.Y, self.Z = [], [], []
        self.label, self.time = [], []
        self.label_write = []
        self.filepath = ''
        self.flag1 = True
        self.flag2 = True
        self.flag3 = True
        self.flag4 = True
        self.flag5 = True
        self.flag6 = True
        self.flag7 = True
        self.pw1 = None
        self.pw2 = None
        self.pw3 = None
        self.pw4 = None
        self.pw5 = None
        self.pw6 = None
        self.pw7 = None
        tk.Frame.__init__(self, master)
        self.F = plt.Figure(figsize=(5, 5), dpi=150)
        self.a = self.F.add_subplot(311)
        self.b = self.F.add_subplot(312)
        self.c = self.F.add_subplot(313)
        self.F.subplots_adjust(left=0.15, right=0.75, top=0.9, bottom=0.1)
        self.canvas = FigureCanvasTkAgg(self.F, master=self)
        self.font1 = {'family': 'Arial', 'weight': 'bold', 'size': 18}
        self.font2 = tf.Font(family='黑体', size=15, weight=tf.BOLD, slant=tf.ROMAN, underline=False, overstrike=False)
        self.font3 = tf.Font(family='Arial', size=10, weight=tf.BOLD, slant=tf.ROMAN, underline=False, overstrike=False)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.contentVar = tk.StringVar(self, '')
        self.contentEntry = tk.Entry(self, textvariable=self.contentVar, font=("Arial", 15, "bold"))
        self.pack()
        self.createWigets()

    def createWigets(self):
        self.a.set_ylabel("Pressure", self.font1)
        self.b.set_ylabel("Flow", self.font1)
        self.c.set_ylabel("Volume", self.font1)
        self.c.set_xlabel("Time/s", self.font1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.contentEntry['state'] = 'readonly'
        self.contentEntry.place(x=110, y=10, width=300, height=50)
        tk.Button(master=self, text="加载数据", font=self.font2, command=self.open_file). \
            place(relx=0.58, rely=0.01, width=120, height=50)
        tk.Button(master=self, text="保存数据", font=self.font2, command=self.save). \
            place(relx=0.76, rely=0.01, width=120, height=50)
        tk.Button(master=self, text="←", font=self.font2, command=self.last_picture). \
            place(relx=0.8, rely=0.19, width=120, height=50)
        tk.Button(master=self, text="→", font=self.font2, command=self.next_picture). \
            place(relx=0.8, rely=0.1, width=120, height=50)
        tk.Button(master=self, text="延迟触发", font=self.font2, command=self.first). \
            place(relx=0.8, rely=0.28, width=120, height=50)
        tk.Button(master=self, text="无效触发", font=self.font2, command=self.second). \
            place(relx=0.8, rely=0.37, width=120, height=50)
        tk.Button(master=self, text="自动触发", font=self.font2, command=self.third). \
            place(relx=0.8, rely=0.46, width=120, height=50)
        tk.Button(master=self, text="流量异步", font=self.font2, command=self.fourth). \
            place(relx=0.8, rely=0.55, width=120, height=50)
        tk.Button(master=self, text="双重触发", font=self.font2, command=self.fifth). \
            place(relx=0.8, rely=0.64, width=120, height=50)
        tk.Button(master=self, text="提前循环", font=self.font2, command=self.sixth). \
            place(relx=0.8, rely=0.73, width=120, height=50)
        tk.Button(master=self, text="延迟循环", font=self.font2, command=self.seventh). \
            place(relx=0.8, rely=0.82, width=120, height=50)
        tk.Button(master=self, command=self.setup_config1).place(relx=0.96, rely=0.28, width=15, height=50)
        tk.Button(master=self, command=self.setup_config2).place(relx=0.96, rely=0.37, width=15, height=50)
        tk.Button(master=self, command=self.setup_config3).place(relx=0.96, rely=0.46, width=15, height=50)
        tk.Button(master=self, command=self.setup_config4).place(relx=0.96, rely=0.55, width=15, height=50)
        tk.Button(master=self, command=self.setup_config5).place(relx=0.96, rely=0.64, width=15, height=50)
        tk.Button(master=self, command=self.setup_config6).place(relx=0.96, rely=0.73, width=15, height=50)
        tk.Button(master=self, command=self.setup_config7).place(relx=0.96, rely=0.82, width=15, height=50)

    def setup_config1(self):
        if self.flag1:
            self.pw1 = PopupDialog(self, '1.jpg')
            self.flag1 = False
            self.wait_window(self.pw1)
        elif not self.flag1:
            self.flag1 = True
            self.pw1.cancel()

    def setup_config2(self):
        if self.flag2:
            self.pw2 = PopupDialog(self, 'ineffective_effort_2.jpg')
            self.flag2 = False
            self.wait_window(self.pw2)
        elif not self.flag2:
            self.flag2 = True
            self.pw2.cancel()

    def setup_config3(self):
        if self.flag3:
            self.pw3 = PopupDialog(self, 'auto_triggering_3.png')
            self.flag3 = False
            self.wait_window(self.pw3)
        elif not self.flag3:
            self.flag3 = True
            self.pw3.cancel()

    def setup_config4(self):
        if self.flag4:
            self.pw4 = PopupDialog(self, '1.jpg')
            self.flag4 = False
            self.wait_window(self.pw4)
        elif not self.flag4:
            self.flag4 = True
            self.pw4.cancel()

    def setup_config5(self):
        if self.flag5:
            self.pw5 = PopupDialog(self, 'double_triggering_5.png')
            self.flag5 = False
            self.wait_window(self.pw5)
        elif not self.flag5:
            self.flag5 = True
            self.pw5.cancel()

    def setup_config6(self):
        if self.flag6:
            self.pw6 = PopupDialog(self, 'early_cycling_6.jpg')
            self.flag6 = False
            self.wait_window(self.pw6)
        elif not self.flag6:
            self.flag6 = True
            self.pw6.cancel()

    def setup_config7(self):
        if self.flag7:
            self.pw7 = PopupDialog(self, 'delay_cycling_7.jpg')
            self.flag7 = False
            self.wait_window(self.pw7)
        elif not self.flag7:
            self.flag7 = True
            self.pw7.cancel()

    def open_file(self):
        """
        打开需要标注的文件
        """
        self.X.clear()
        self.Y.clear()
        self.Z.clear()
        self.label.clear()
        self.time.clear()
        self.label_write.clear()
        self.pic_count = -1
        self.filepath = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('C:/')))
        # read_label_file(label, time, X, Y, Z, filepath)
        read_pre_classification_file(self.X, self.Y, self.Z, self.filepath)
        for i in range(len(self.X)):
            self.label_write.append(0)
        tk.messagebox.showinfo(title='信息提示！', message='文件读取完毕！')
        self.next_picture()

    def save(self):
        """
        保存标注好的数据至txt文件
        """
        (dir_path, tempfilename) = os.path.split(self.filepath)
        (origin_name, extension) = os.path.splitext(tempfilename)
        filename = os.path.join(dir_path, origin_name + "_label.txt")
        file = open(filename, 'a')
        for k in range(len(self.X)):
            s1 = str(self.X[k]).replace('[', '').replace(']', '')
            s2 = str(self.Y[k]).replace('[', '').replace(']', '')
            s3 = str(self.Z[k]).replace('[', '').replace(']', '')
            s = str(self.label_write[k]) + '\t' + s2 + '\t' + s1 + '\t' + s3 + '\n'
            file.write(s)
        tk.messagebox.showinfo(title='信息提示！', message='文件保存完毕！')

    def next_picture(self):
        """
        显示下一页
        """
        self.pic_count += 1
        if self.pic_count >= len(self.X):
            tk.messagebox.showwarning(title='提示', message='当前已是最后一张图')
        else:
            self.show_wave()

    def last_picture(self):
        """
        显示上一页
        """
        self.pic_count -= 1
        self.show_wave()

    def show_wave(self):
        """
        显示pic_count对应的三通道波形
        """
        time = []
        for i in range(len(self.X[self.pic_count])):
            time.append(i / 62.5)
        self.a.cla()
        self.a.plot(time, self.X[self.pic_count], color='black')
        self.b.cla()
        self.b.plot(time, self.Y[self.pic_count], color='black')
        self.c.cla()
        self.c.plot(time, self.Z[self.pic_count], color='black')
        self.a.set_ylabel("Pressure")
        self.b.set_ylabel("Flow")
        self.c.set_ylabel("Volume")
        self.c.set_xlabel("Time/s")
        self.contentVar.set('样本总数：' + str(len(self.X)) + '  已标注：' + str(self.pic_count))
        self.canvas.draw()

    def first(self):
        self.label_write[self.pic_count] = 1  # delay triggering
        self.next_picture()

    def second(self):
        self.label_write[self.pic_count] = 2  # ineffective effort
        self.next_picture()

    def third(self):
        self.label_write[self.pic_count] = 3  # auto triggering
        self.next_picture()

    def fourth(self):
        self.label_write[self.pic_count] = 4  # flow asynchrony
        self.next_picture()

    def fifth(self):
        self.label_write[self.pic_count] = 5  # double triggering
        self.next_picture()

    def sixth(self):
        self.label_write[self.pic_count] = 6  # early cycling
        self.next_picture()

    def seventh(self):
        self.label_write[self.pic_count] = 7  # delayed cycling
        self.next_picture()


if __name__ == '__main__':
    app = RootWindow(master=tk.Tk())
    app.master.title("人机不同步类型标注")
    app.mainloop()
