from math import ceil
import matplotlib.pyplot as plt
import os

X, Y, Z = [], [], []
step = []
filepath = 'C:\\Users\\Dell\\Desktop\\第三次标注：202\\20200701-0101361822-16.txt'
with open(file=filepath, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    j = 0
    for line in lines:
        value = [float(s) for s in line.split()]
        X.append(value[0] / 10 - 12.8)
        Z.append(value[2] * 2)
        if 3 > (value[1] - 1799) > -3:
            Y.append(0)
            step.append(j)
        else:
            Y.append((value[1] - 1799) / 10)
            step.append(j)
            j = j + 1
label = []
T, t_temp = [], []
filepath = 'C:\\Users\\Dell\\Desktop\\第三次标注：202\\double_trigger_0-4679.txt'
with open(file=filepath, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        value = [str(s) for s in line.split('\t')]
        # label.append(float(value[0]))
        t_temp = value[0].split('--')
        t = []
        for time in t_temp:
            t.append(float(time))
        T.append(t)
f.close()

X_temp, Y_temp, Z_temp = [], [], []
for time in T:
    x_t, y_t, z_t = [], [], []
    for i in range(ceil(time[0] * 62), ceil(time[0] * 62) + 200):
        x_t.append(X[i])
        y_t.append(Y[i])
        z_t.append(Z[i])
    X_temp.append(x_t)
    Y_temp.append(y_t)
    Z_temp.append(z_t)

output = open('data3.xls', 'w', encoding='gbk')
for i in range(len(Z_temp)):
    for j in range(len(Z_temp[i])):
        output.write(str(Z_temp[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
        output.write('\t')  # 相当于Tab一下，换一个单元格
    output.write('\n')  # 写完一行立马换行
output.close()
# f = plt.figure(figsize=(7, 5.2), dpi=150)
# a = f.add_subplot(311)
# b = f.add_subplot(312)
# c = f.add_subplot(313)
# T = []
# for i in range(len(X_temp[0])):
#     T.append(i/62.5)
# for i in range(len(X_temp)):
#     a.plot(T, X_temp[i], color='black')
#     b.plot(T, Y_temp[i], color='black')
#     c.plot(T, Z_temp[i], color='black')
# font1 = {'family': 'Arial', 'weight': 'bold', 'size': 20}
# a.set_ylabel("Pressure", font1)
# b.set_ylabel("Flow", font1)
# c.set_ylabel("Volume", font1)
# c.set_xlabel("Time(s)", font1)
# a.tick_params(labelsize=13)
# b.tick_params(labelsize=13)
# c.tick_params(labelsize=13)
# labels = a.get_xticklabels() + a.get_yticklabels()
# [label.set_fontname('Arial') for label in labels]
# labels = b.get_xticklabels() + b.get_yticklabels()
# [label.set_fontname('Arial') for label in labels]
# labels = c.get_xticklabels() + c.get_yticklabels()
# [label.set_fontname('Arial') for label in labels]
# plt.show()

# filepath = 'C:\\Users\\chencheng\\Desktop\\新建文件夹\\20200707-0101360573-22.rpx_label.txt'
# (dir_path, tempfilename) = os.path.split(filepath)
# (origin_name, extension) = os.path.splitext(tempfilename)
# filename = dir_path + '/' + origin_name + "_label_modify.txt"
# filename = 'doubletrigger.txt'
# file = open(filename, 'a')
# for k in range(len(X_temp)):
#
#     s1 = str(X_temp[k]).replace('[', '').replace(']', '')
#     s2 = str(Y_temp[k]).replace('[', '').replace(']', '')
#     s3 = str(Z_temp[k]).replace('[', '').replace(']', '')
#     s = str(2) + '\t' + str(round(T[k][0], 2)) + '--' + str(
#         round(T[k][1], 2)) + '\t' + s2 + '\t' + s1 + '\t' + s3 + '\n'
#     file.write(s)
