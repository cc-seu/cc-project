from w_to_txt import w_to_txt
from LTTB import LTTB
from pearson import correlation
import matplotlib.pyplot as plt

X, Z, step = [], [], []
S1, S2, S3, S4, S5, S6 = [], [], [], [], [], []
S_temp1, S_temp2, S_temp3, S_temp4, S_temp5, S_temp6 = [], [], [], [], [], []
normal, abnormal = [], []
div_point = []
div_point_index = []
div_point_flag = []
file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard1.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        S1.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard2.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        S2.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard3.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        S3.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard4.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        S4.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard5.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        S5.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard6.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        S6.append(float(line))

for i in range(0, 150):
    S_temp1.append(S1[i])
for i in range(0, 150):
    S_temp2.append(S2[i])
for i in range(0, 150):
    S_temp3.append(S3[i])
for i in range(0, 150):
    S_temp4.append(S4[i])
for i in range(0, 150):
    S_temp5.append(S5[i])
for i in range(0, 150):
    S_temp6.append(S6[i])

file_path = 'C:\\Users\\Dell\\Desktop\\波形测试\\20200502-0101352583-10.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    j = 0
    for line in lines:
        value = [float(s) for s in line.split()]
        if 3 > (value[1] - 1799) > -3:
            X.append(0)
            step.append(j)
        else:
            X.append((value[1] - 1799) / 10)
            step.append(j)
            j = j + 1
        Z.append(value[2] * 2)
n = len(X)
if len(X) != 0:
    for i in range(0, n - 2):  # 自动标注
        if X[i - 1] == 0 and X[i + 1] > 0 and X[i] == 0 and Z[i] < 100:
            div_point.append(1)
            div_point_flag.append(1)
        else:
            div_point.append(0)
            div_point_flag.append(0)

for i in range(0, n - 2):
    if div_point[i] == 1:
        div_point_index.append(i)

m = len(div_point_index)
for i in range(0, m - 1):
    temp, temp1 = [], []
    point = 0
    for j in range(div_point_index[i], div_point_index[i + 1] + 1):
        temp.append(X[j])
    if 150 <= (div_point_index[i + 1] - div_point_index[i] + 1) < 350:
        for k in range(0, 150):
            temp1.append(temp[k])
        cor1 = correlation(temp1, S_temp1)
        if cor1 >= 0.6:
            point = point + 1
        elif cor1 < 0.6:
            point = point

        cor2 = correlation(temp1, S_temp2)
        if cor2 >= 0.6:
            point = point + 1
        elif cor2 < 0.6:
            point = point

        cor3 = correlation(temp1, S_temp3)
        if cor3 >= 0.6:
            point = point + 1
        elif cor3 < 0.6:
            point = point

        cor4 = correlation(temp1, S_temp4)
        if cor4 >= 0.6:
            point = point + 1
        elif cor4 < 0.6:
            point = point

        cor5 = correlation(temp1, S_temp5)
        if cor5 >= 0.6:
            point = point + 1
        elif cor5 < 0.6:
            point = point

        cor6 = correlation(temp1, S_temp6)
        if cor6 >= 0.6:
            point = point + 1
        elif cor6 < 0.6:
            point = point

        if point == 6:
            normal.append(temp)
            # plt.plot(temp)
            # plt.show()
            # w_to_txt('C:\\Users\\Dell\\Desktop\\波形测试\\正常波形-pearson.txt', temp)
        elif point < 6:
            abnormal.append(temp)
            # plt.plot(temp)
            # plt.show()
            # w_to_txt('C:\\Users\\Dell\\Desktop\\波形测试\\异常波形-pearson.txt', temp)

    elif (div_point_index[i + 1] - div_point_index[i] + 1) < 150 or (
            div_point_index[i + 1] - div_point_index[i] + 1) >= 350:
        abnormal.append(temp)
    #     w_to_txt('C:\\Users\\Dell\\Desktop\\波形测试\\异常波形-pearson.txt', temp)
plt.plot(normal[1])
plt.show()

