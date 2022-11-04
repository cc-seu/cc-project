import tkinter
from tkinter import filedialog, dialog
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import tkinter.messagebox
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy import signal

root = tkinter.Tk()  # 创建tkinter的主窗口
root.title("呼吸波形标注")
X, Y, Z, step, X_smooth, Y_smooth, Z_smooth = [], [], [], [], [], [], []
array1, array2, array3, array4, array5, array6 = [], [], [], [], [], []
div_point = []
file_path = ''
pic_count = 0
show_time = 0
which_line = 0
auto_label_time = 0
manual_label_time = 0
rect = None
start_x = None
start_y = None
x = 0
y = 0
label = None  # 异步标签
time_min = 0  # 异步起始
time_max = 0  # 异步终止
time_min_temp = 0  # 过渡
time_max_temp = 0  # 过渡
f = plt.Figure(figsize=(10, 5), dpi=100)
a = f.add_subplot(311)  # 添加子图:1行1列第1个
b = f.add_subplot(312)
c = f.add_subplot(313)
a.set_ylabel("Pressure")
b.set_ylabel("Flow")
c.set_ylabel("Volume")
c.set_xlabel("Time/s")
# 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                            fill=tkinter.BOTH,  # 填充方式
                            expand=tkinter.YES)  # 随窗口大小调整而调整
# matplotlib的导航工具栏显示上来(默认是不会显示它的)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tkinter.TOP,  # get_tk_widget()得到的就是_tkcanvas
                      fill=tkinter.BOTH,
                      expand=tkinter.YES)


def right_key1(event):
    menubar.post(event.x_root, event.y_root)


def red_line():
    global which_line
    which_line = 1


def yellow_line():
    global which_line
    which_line = 3


def blue_line():
    global which_line
    which_line = 2


def green_line():
    global which_line
    which_line = 4


def stop_con_line():
    global which_line
    which_line = 0


def get_show_time(*args):
    """获取展示时间"""
    global show_time
    show_time = numberChosen.get()


# 右键弹出控制标注线菜单
menubar = tkinter.Menu(root, tearoff=False)
menubar.add_command(label='控制红线', command=red_line)
menubar.add_command(label='控制黄线', command=yellow_line)
menubar.add_command(label='控制蓝线', command=blue_line)
menubar.add_command(label='控制绿线', command=green_line)
menubar.add_command(label='停止控制', command=stop_con_line)

# 显示时间下拉框
number = tkinter.IntVar()
numberChosen = ttk.Combobox(textvariable=number, state='readonly')
numberChosen['values'] = (10, 20, 30, 40, 50, 60)  # 设置下拉列表的值
numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
numberChosen.bind("<<ComboboxSelected>>", get_show_time)
numberChosen.pack()  # 设置其在界面中出现的位置  column代表列   row 代表行


def right_key2(event):
    menubar2.post(event.x_root, event.y_root)


def print_invalid():
    global label
    label = "无效触发"
    print("标签类型：" + label)


def print_delay():
    global label
    label = "延迟触发"
    print("标签类型：" + label)


def print_double():
    global label
    label = "双触发"
    print("标签类型：" + label)


def print_false():
    global label
    label = "误触发"
    print("标签类型：" + label)


def print_insufficient():
    global label
    label = "流速不足"
    print("标签类型：" + label)


def print_over():
    global label
    label = "流速过大"
    print("标签类型：" + label)


def print_desynchrony():
    global label
    label = "流呼气不同步"
    print("标签类型：" + label)


# 异步标签右键菜单
menubar2 = tkinter.Menu(root, tearoff=False)
menubar2.add_command(label='无效触发', command=print_invalid)
menubar2.add_command(label='延迟触发', command=print_delay)
menubar2.add_command(label='双触发', command=print_double)
menubar2.add_command(label='误触发', command=print_false)
menubar2.add_command(label='流速不足', command=print_insufficient)
menubar2.add_command(label='流速过大', command=print_over)
menubar2.add_command(label='呼气不同步', command=print_desynchrony)


def motion_min(event):
    global time_min
    global time_min_temp
    time_min_temp = event.xdata


def motion_max(event):
    global time_max
    global time_min
    global time_min_temp
    global time_max_temp
    time_max_temp = event.xdata
    if time_min_temp != None and time_max_temp != None:
        if (time_max_temp - time_min_temp) > 0.3:
            time_min = round(time_min_temp, 2)
            time_max = round(time_max_temp, 2)
            print("起始时间：" + str(time_min))
            print("终止时间：" + str(time_max))
    else:
        result = tkinter.messagebox.showwarning(title='出错了！', message='标注越界！')
        print(result)


def nop(event):
    """空操作"""
    pass


def wave_label():
    """矩形辅助标注"""
    if len(X) == 0:
        result = tkinter.messagebox.showwarning(title='出错了！', message='请打开文件！')
        print(result)
    else:
        root.bind("<Button-3>", right_key2)

        def on_button_press(event):
            """绘制矩形左键按下"""
            global rect
            global start_x
            global start_y
            global x, y
            start_x = event.x
            start_y = event.y
            if not rect:
                rect = canvas._tkcanvas.create_rectangle(x, y, 1, 1, outline="black")

        def on_move_press(event):
            """绘制矩形左键移动"""
            global curX, curY, rect
            curX, curY = (event.x, event.y)
            canvas._tkcanvas.coords(rect, start_x, start_y, curX, curY)

        def on_button_release(event):
            """绘制矩形左键释放"""
            pass

        root.bind("<ButtonPress-1>", on_button_press)
        root.bind("<B1-Motion>", on_move_press)
        root.bind("<ButtonRelease-1>", on_button_release)
        canvas.mpl_connect('button_press_event', motion_min)
        canvas.mpl_connect('button_release_event', motion_max)


def stop_label():
    """停止矩形辅助标注"""
    if len(X) == 0:
        result = tkinter.messagebox.showwarning(title='出错了！', message='请打开文件！')
        print(result)
    else:
        root.bind("<Button-3>", nop)
        global rect
        canvas._tkcanvas.delete(rect)
        rect = None
        temp1 = canvas.mpl_connect('button_press_event', motion_min)
        temp2 = canvas.mpl_connect('button_release_event', motion_max)
        f.canvas.mpl_disconnect(temp1)
        f.canvas.mpl_disconnect(temp2)
        root.bind("<ButtonPress-1>", nop)
        root.bind("<B1-Motion>", nop)
        root.bind("<ButtonRelease-1>", nop)


def comfirm_label():
    """写入异步时间，标签"""
    global label  # 异步标签
    global time_min  # 异步起始
    global time_max  # 异步终止
    global file_path
    if len(X) == 0:
        result = tkinter.messagebox.showwarning(title='出错了！', message='请打开文件！')
        print(result)
    else:
        if label == None:
            result = tkinter.messagebox.showwarning(title='出错了！', message='请选择异步标签！')
            print(result)
        elif time_min == 0 and time_max == 0:
            result = tkinter.messagebox.showwarning(title='出错了！', message='请选择异步波段！')
            print(result)
        else:
            (dir_path, tempfilename) = os.path.split(file_path)
            (origin_name, extension) = os.path.splitext(tempfilename)
            filename = dir_path + '/' + origin_name + "_label.txt"
            if os.path.exists(filename) is False:
                hint = "起始时间：" + str(time_min) + "\n" + "结束时间：" + str(time_max) + "\n" + "异步类型：" + label
                ask = tkinter.messagebox.askyesnocancel('是否写入？', hint)
                if ask is True:
                    with open(filename, 'a') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                        f.write("start_time\tend_time \tasynchronies_type\n")
                        f.write(str(time_min) + "\t\t" + str(time_max) + "\t\t" + label + "\n")
                    label = None
                    time_max = 0
                    time_min = 0
            elif os.path.exists(filename) is True:
                hint = "起始时间：" + str(time_min) + "\n" + "结束时间：" + str(time_max) + "\n" + "异步类型：" + label
                ask = tkinter.messagebox.askyesnocancel('是否写入？', hint)
                if ask is True:
                    with open(filename, 'a') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                        f.write(str(time_min) + "\t\t" + str(time_max) + "\t\t" + label + "\n")
                    label = None
                    time_max = 0
                    time_min = 0


def Show(p, t, y):
    """重新定义绘图函数"""
    len_y = len(y)
    x = t
    _y = [y[-1]] * len_y
    p.plot(x, y, color='skyblue')
    line_x = p.axvline(x=t[len_y - 1], color='blue')
    line_y = p.axvline(x=t[len_y - 1], color='red')
    line_z = p.axvline(x=t[len_y - 1], color='yellow')
    line_p = p.axvline(x=t[len_y - 1], color='green')

    def motion(event):
        global which_line
        try:
            if int(which_line) == 1:
                if event.xdata is not None:
                    line_y.set_xdata(event.xdata)
                    f.canvas.draw_idle()
            elif int(which_line) == 2:
                if event.xdata is not None:
                    line_x.set_xdata(event.xdata)
                    f.canvas.draw_idle()
            elif int(which_line) == 3:
                if event.xdata is not None:
                    line_z.set_xdata(event.xdata)
                    f.canvas.draw_idle()
            elif int(which_line) == 4:
                if event.xdata is not None:
                    line_p.set_xdata(event.xdata)
                    f.canvas.draw_idle()

        except:
            pass

    f.canvas.mpl_connect('motion_notify_event', motion)


def open_file():
    """打开文件"""
    global file_path
    global pic_count
    global show_time
    pic_count = 0
    show_time = numberChosen.get()
    file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('C:/')))
    print('打开文件：', file_path)
    step.clear()
    X.clear()
    Y.clear()
    Z.clear()
    if file_path is not None:
        j = 0
        with open(file=file_path, mode='r+', encoding='utf-8') as g:
            lines = g.readlines()
            for line in lines:
                value = [float(s) for s in line.split()]
                X.append(value[0] / 10)
                if 3 > (value[1] - 1799) > -3:
                    Y.append(0)
                else:
                    Y.append((value[1] - 1799) / 10)
                Z.append(value[2])
                step.append(j / 62)
                j = j + 1
        result = tkinter.messagebox.showinfo(title='信息提示！', message='文件读取完毕！')
        print(result)


def draw_wave():
    """绘制波形"""
    global pic_count
    global show_time
    global auto_label_time
    global manual_label_time
    stop_label()
    pic_count = 0
    n = int(show_time) * 62  # 每秒采样62点
    auto_label_time = 0
    manual_label_time = 0
    if len(X) == 0:
        result = tkinter.messagebox.showwarning(title='出错了！', message='请打开文件！')
        print(result)
    else:
        array1.clear()
        array2.clear()
        array3.clear()
        array4.clear()
        array5.clear()
        array6.clear()
        for i in range(0, n - 1):
            array1.append(X[i])
            array2.append(step[i])
            array3.append(Y[i])
            array4.append(step[i])
            array5.append(Z[i])
            array6.append(step[i])
        a.cla()
        b.cla()
        c.cla()
        a.set_ylabel("Pressure")
        b.set_ylabel("Flow")
        c.set_ylabel("Volume")
        c.set_xlabel("Time/s")
        Show(a, array2, array1)
        Show(b, array4, array3)
        Show(c, array6, array5)
        canvas.draw()


def Modify_The_File():
    """去除文件中的表头以及时间标识"""
    file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('C:/')))
    print('打开文件：', file_path)
    if file_path is not None:
        with open(file=file_path, mode='r') as h:
            lines = h.readlines()
            with open(file=file_path, mode='w') as l:
                for line in lines:
                    if line.startswith(" "):
                        l.write(line)


def _quit():
    """点击退出按钮时调用这个函数"""
    root.quit()  # 结束主循环
    root.destroy()  # 销毁窗口


def next_picture():
    """绘制下一张图"""
    global pic_count
    global show_time
    global auto_label_time
    global manual_label_time
    global array1
    global array2
    global array3
    global array4
    global array5
    global array6
    stop_label()
    pic_count += 1
    n = int(show_time) * 62
    auto_label_time = 0
    manual_label_time = 0
    if len(X) == 0:
        result = tkinter.messagebox.showwarning(title='出错了！', message='请打开文件！')
        print(result)
    else:
        array1.clear()
        array2.clear()
        array3.clear()
        array4.clear()
        array5.clear()
        array6.clear()
        if pic_count * n <= (len(X) - 1):
            if ((pic_count + 1) * n - 1) <= (len(X) - 1):
                for i in range(pic_count * n, (pic_count + 1) * n - 1):
                    array1.append(X[i])
                    array2.append(step[i])
                    array3.append(Y[i])
                    array4.append(step[i])
                    array5.append(Z[i])
                    array6.append(step[i])
                a.cla()
                b.cla()
                c.cla()
                Show(a, array2, array1)
                Show(b, array4, array3)
                Show(c, array6, array5)
                a.set_ylabel("Pressure")
                b.set_ylabel("Flow")
                c.set_ylabel("Volume")
                c.set_xlabel("Time/s")
                canvas.draw()
            elif ((pic_count + 1) * n - 1) > (len(X) - 1):
                array1.clear()
                array2.clear()
                array3.clear()
                array4.clear()
                array5.clear()
                array6.clear()
                for i in range(pic_count * n, len(X) - 1):
                    array1.append(X[i])
                    array2.append(step[i])
                    array3.append(Y[i])
                    array4.append(step[i])
                    array5.append(Z[i])
                    array6.append(step[i])
                a.cla()
                b.cla()
                c.cla()
                Show(a, array2, array1)
                Show(b, array4, array3)
                Show(c, array6, array5)
                a.set_ylabel("Pressure")
                b.set_ylabel("Flow")
                c.set_ylabel("Volume")
                c.set_xlabel("Time/s")
                canvas.draw()
        else:
            pic_count -= 1
            result = tkinter.messagebox.showwarning(title='出错了！', message='当前已是最后一张图')
            print(result)


def last_picture():
    """绘制上一张图"""
    global pic_count
    global show_time
    global auto_label_time
    global manual_label_time
    global array1
    global array2
    global array3
    global array4
    global array5
    global array6
    stop_label()
    pic_count -= 1
    n = int(show_time) * 62
    auto_label_time = 0
    manual_label_time = 0
    if len(X) == 0:
        result = tkinter.messagebox.showwarning(title='出错了！', message='请打开文件！')
        print(result)
    else:
        if pic_count >= 0:
            array1.clear()
            array2.clear()
            array3.clear()
            array4.clear()
            array5.clear()
            array6.clear()
            for i in range(pic_count * n, (pic_count + 1) * n - 1):
                array1.append(X[i])
                array2.append(step[i])
                array3.append(Y[i])
                array4.append(step[i])
                array5.append(Z[i])
                array6.append(step[i])
            a.cla()
            b.cla()
            c.cla()

            Show(a, array2, array1)
            Show(b, array4, array3)
            Show(c, array6, array5)
            a.set_ylabel("Pressure")
            b.set_ylabel("Flow")
            c.set_ylabel("Volume")
            c.set_xlabel("Time/s")
            canvas.draw()
        else:
            pic_count += 1
            result = tkinter.messagebox.showwarning(title='出错了！', message='当前已是第一张图')
            print(result)


def auto_time_label():
    """自动标注波形的各时间点"""
    global show_time
    global auto_label_time
    if len(X) != 0:
        if auto_label_time == 0:
            n = len(array5)
            auto_label_time += 1
            for i in range(1, n - 10):  # 自动标注
                # if -1 < array3[i] < 0 and array3[i] < array3[i + 1] < array3[i + 2] < array3[i + 3] < array3[i + 4] < \
                #         array3[
                #             i + 5] and array5[i] < 50 or (
                #         array3[i - 1] == 0 and 0 < array3[i + 1] and array3[i] == 0 and (
                #         array5[i] < 50 or array5[i + 1] < 50)):
                if -3 < array3[i] < 3 and array5[i] < 50 and ((array3[i + 10] - array3[i]) / 0.16 + (array3[i + 8] - array3[i]) / 0.128 + (array3[i + 6] - array3[i]) / 0.096 + (array3[i + 4] - array3[i]) / 0.064 + (array3[i + 2] - array3[i]) / 0.032) > 600 :
                    a.axvline(x=array4[i], color='red')
                    b.axvline(x=array4[i], color='red')
                    c.axvline(x=array4[i], color='red')
                    canvas.draw()
            # for i in range(0, n - 2):
            #     if array5[i - 1] <= array5[i] and array5[i + 1] < array5[i] and array5[i] > 500 and array1[i] > 20:
            #         a.axvline(x=array4[i], color='yellow')
            #         b.axvline(x=array4[i], color='yellow')
            #         c.axvline(x=array4[i], color='yellow')
            #         canvas.draw()
        elif auto_label_time == 1:
            auto_label_time -= 1
            a.cla()
            b.cla()
            c.cla()
            Show(a, array2, array1)
            Show(b, array4, array3)
            Show(c, array6, array5)
            a.set_ylabel("Pressure")
            b.set_ylabel("Flow")
            c.set_ylabel("Volume")
            c.set_xlabel("Time/s")
            canvas.draw()
    elif len(X) == 0:
        result = tkinter.messagebox.showwarning(title='出错了！', message='请打开文件！')
        print(result)


def manual_time_label():
    """手动标注波形的各时间点"""
    global manual_label_time
    if manual_label_time == 0:
        manual_label_time += 1
        root.bind("<Button-3>", right_key1)
    elif manual_label_time == 1:
        global which_line
        which_line = 0
        manual_label_time -= 1
        root.bind("<Button-3>", nop)
        a.cla()
        b.cla()
        c.cla()
        Show(a, array2, array1)
        Show(b, array4, array3)
        Show(c, array6, array5)
        a.set_ylabel("Pressure")
        b.set_ylabel("Flow")
        c.set_ylabel("Volume")
        c.set_xlabel("Time/s")
        canvas.draw()


# 创建一个按钮,并把上面那个函数绑定过来
button_quit = tkinter.Button(master=root, text="退出", width=7, height=1, command=_quit)
button_open_file = tkinter.Button(text='打开文件', width=7, height=1, command=open_file)
button_draw_wave = tkinter.Button(text='绘制波形', width=7, height=1, command=draw_wave)
# button_Modify_The_File = tkinter.Button( text='修改文件', width=10, height=2, command=Modify_The_File)
button_next_picture = tkinter.Button(text='下一张', width=7, height=1, command=next_picture)
button_last_picture = tkinter.Button(text='上一张', width=7, height=1, command=last_picture)
button_auto_label_time = tkinter.Button(text="自动时间标注", width=10, height=1, command=auto_time_label)
button_manual_label_time = tkinter.Button(text="手动时间标注", width=10, height=1, command=manual_time_label)
button_wave_label = tkinter.Button(text="波形标注", width=7, height=1, command=wave_label)
button_stop_label = tkinter.Button(text="停止标注", width=7, height=1, command=stop_label)
button_comfirm_label = tkinter.Button(text="标注写入", width=7, height=1, command=comfirm_label)
button_quit.pack(side=tkinter.RIGHT, anchor=tkinter.NE)
button_comfirm_label.pack(side=tkinter.RIGHT, anchor=tkinter.NE)
button_open_file.pack(side=tkinter.LEFT, anchor=tkinter.NW)
button_draw_wave.pack(side=tkinter.LEFT, anchor=tkinter.NW)
# button_Modify_The_File.pack()
button_next_picture.pack(side=tkinter.LEFT, anchor=tkinter.NW)
button_last_picture.pack(side=tkinter.LEFT, anchor=tkinter.NW)
button_auto_label_time.pack(side=tkinter.LEFT, anchor=tkinter.NW)
button_manual_label_time.pack(side=tkinter.LEFT, anchor=tkinter.NW)
button_wave_label.pack(side=tkinter.LEFT, anchor=tkinter.NW)
button_stop_label.pack(side=tkinter.LEFT, anchor=tkinter.NW)

# 主循环
root.mainloop()
