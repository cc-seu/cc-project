import numpy as np
import scipy
from scipy import signal
import matplotlib.pyplot as plt
import math
import os
from w_to_excel import write_excel_xls
from w_to_excel import write_excel_xls_append

X, step = [], []
div_point = []
div_point_index = []
div_point_flag = []
file_path = 'C:\\Users\\chencheng\\Desktop\\rand.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as g:
    lines = g.readlines()
    j = 0
    for line in lines:
        value = [float(s) for s in line.split()]
        if (value[1] - 1799) < 3 and (value[1] - 1799) / 10 > -3:
            X.append(0)
            step.append(j)
        else:
            X.append((value[1] - 1799) / 10)
            step.append(j)
            j = j + 1
# X_smooth = scipy.signal.savgol_filter(X, 21, 5)
n = len(X)

if len(X) != 0:
    for i in range(0, n - 2):  # 自动标注
        if (X[i - 1] == 0 and X[i + 1] > 0 and X[i] == 0):
            div_point.append(1)
            div_point_flag.append(1)
        else:
            div_point.append(0)
            div_point_flag.append(0)

for i in range(0, n - 2):
    if div_point[i] == 1:
        plt.subplot(3, 1, 1)
        plt.axvline(i, color='r')

for i in range(0, n - 2):
    if div_point[i] == 1:
        div_point_index.append(i)

book_name_xls = 'C:\\Users\\chencheng\\Desktop\\可能正常波形.xls'
book_name_xls2 = 'C:\\Users\\chencheng\\Desktop\\异常波形.xls'

sheet_name_xls = '可能正常波形'
sheet_name_xls2 = '异常波形'

value_title = [['流量']]
m = len(div_point_index)
write_excel_xls(book_name_xls, sheet_name_xls, value_title)
write_excel_xls(book_name_xls2, sheet_name_xls2, value_title)
temp1 = []
temp2 = []
for i in range(0, m - 1):
    if (div_point_index[i + 1] - div_point_index[i] >= 350) or (div_point_index[i + 1] - div_point_index[i] < 100):
        temp_b_w = []
        if i + 2 > m - 1:
            for j in range(div_point_index[i - 2], n - 1):
                temp_b_w.append(X[j])
                temp1.append(X[j])
            div_point_flag[div_point_index[i]] = -1
            div_point_flag[div_point_index[i - 1]] = -1
            div_point_flag[div_point_index[i - 2]] = -1
            div_point_flag[div_point_index[i + 1]] = -1
            temp_b_w.append(100)
            temp1.append(100)
        elif i - 2 < 0:
            for j in range(0, div_point_index[i + 2]):
                temp_b_w.append(X[j])
                temp1.append(X[j])
            div_point_flag[div_point_index[i]] = -1
            div_point_flag[div_point_index[i - 1]] = -1
            div_point_flag[div_point_index[i + 2]] = -1
            div_point_flag[div_point_index[i + 1]] = -1
            temp_b_w.append(100)
            temp1.append(100)
        else:
            for j in range(div_point_index[i - 2], div_point_index[i + 2]):
                temp_b_w.append(X[j])
                temp1.append(X[j])
            div_point_flag[div_point_index[i]] = -1
            div_point_flag[div_point_index[i - 1]] = -1
            div_point_flag[div_point_index[i - 2]] = -1
            div_point_flag[div_point_index[i + 1]] = -1
            div_point_flag[div_point_index[i + 2]] = -1
            temp_b_w.append(100)
            temp1.append(100)
        write_excel_xls_append(book_name_xls2, temp_b_w)
for i in range(0, m - 1):
    if (div_point_index[i + 1] - div_point_index[i] < 350) and (div_point_index[i + 1] - div_point_index[i] >= 100)and div_point_flag[div_point_index[i + 1]] !=-1:
        temp_w = []
        for j in range(div_point_index[i], div_point_index[i + 1]):
            temp_w.append(X[j])
            temp2.append(X[j])
        temp_w.append(100)
        temp2.append(100)
        write_excel_xls_append(book_name_xls, temp_w)

print(div_point_index)
plt.subplot(3, 1, 1)
plt.plot(X)
plt.subplot(3, 1, 2)
plt.plot(temp1)
plt.subplot(3, 1, 3)
plt.plot(temp2)
plt.show()
