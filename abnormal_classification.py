import tkinter
from tkinter import filedialog, dialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter.messagebox
from pearson import correlation
from tkinter import *
from numpy.fft import fft
from numpy import linspace, sin, pi, power, ceil, log2, arange, random
from scipy.signal import butter, lfilter, freqz
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np
import tslearn.metrics as metrics
# 自定义数据处理
from tslearn.clustering import silhouette_score
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.generators import random_walks
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from tslearn.clustering import KShape
import tkinter.font as tf
from numpy import *
from scipy import stats
import math
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from tslearn.clustering import silhouette_score
import tslearn.metrics as metrics

X, Y, Z, step, S_temp = [], [], [], [], []
S1, S2, S3, S4, S5, S6 = [], [], [], [], [], []
S1_temp, S2_temp, S3_temp, S4_temp, S5_temp, S6_temp = [], [], [], [], [], []
X_norm, Y_norm, Z_norm, T_norm = [], [], [], []
X_abnorm, Y_abnorm, Z_abnorm, T_abnorm = [], [], [], []
div_point = []
div_point_index = []
div_point_flag = []
label_state = []
X_norm_learn, Y_norm_learn, Z_norm_learn = [], [], []
flag_norm, flag_abnorm = [], []
step = []

filepath = 'C:\\Users\\Dell\\Desktop\\第三次标注：202\\20200701-0101361822-16.rpx.txt'
with open(file=filepath, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    j = 0
    for line in lines:
        value = [float(s) for s in line.split()]
        X.append(value[0] / 10)
        Z.append(value[2] * 2)
        if 3 > (value[1] - 1799) > -3:
            Y.append(0)
            step.append(j)
        else:
            Y.append((value[1] - 1799) / 10)
            step.append(j)
            j = j + 1

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard1.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f1:
    for line in f1.readlines():
        line = line.strip('\n')
        S1.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard2.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f2:
    for line in f2.readlines():
        line = line.strip('\n')
        S2.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard3.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f3:
    for line in f3.readlines():
        line = line.strip('\n')
        S3.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard4.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f4:
    for line in f4.readlines():
        line = line.strip('\n')
        S4.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard5.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f5:
    for line in f5.readlines():
        line = line.strip('\n')
        S5.append(float(line))

file_path = 'C:\\Users\\Dell\\Desktop\\周期呼吸波形\\standard6.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f6:
    for line in f6.readlines():
        line = line.strip('\n')
        S6.append(float(line))

for i in range(0, 200):  # 将所有序列长度设为200
    S1_temp.append(S1[i])
    S2_temp.append(S2[i])
    S3_temp.append(S3[i])
    S4_temp.append(S4[i])
    S5_temp.append(S5[i])
    S6_temp.append(S6[i])

n = len(Y)
if n != 0:
    for i in range(0, n - 2):  # 自动分割
        if (Y[i - 1] == 0 and Y[i + 1] > 0 and Y[i] == 0 and Z[i] < 100) or (
                -1 < Y[i] < 0 and Y[i] < Y[i + 1] < Y[i + 2] < Y[i + 3] < Y[i + 4] and Z[i] < 100):
            div_point.append(1)
            div_point_flag.append(1)
        else:
            div_point.append(0)
            div_point_flag.append(0)

for i in range(len(div_point) - 80):  # 消除同一个周期中多次划分
    if div_point[i] == 1:
        for j in range(i + 1, i + 80):
            if div_point[j] == 1:
                div_point[i] = 0
                div_point_flag[i] = 0

for i in range(0, n - 2):
    if div_point[i] == 1:
        div_point_index.append(i)

m = len(div_point_index)

for i in range(0, m - 1):
    X_temp, Y_temp, Z_temp, temp1, tempx, tempz, T_temp = [], [], [], [], [], [], []
    point = 0
    for j in range(div_point_index[i], div_point_index[i + 1] + 1):
        X_temp.append(X[j])
        Y_temp.append(Y[j])
        Z_temp.append(Z[j])
        T_temp.append(j / 62)

    if 150 <= (div_point_index[i + 1] - div_point_index[i] + 1) < 300:  # 将所有序列长度设为200，不够就补0
        if len(Y_temp) >= 200:
            for k in range(0, 200):
                temp1.append(Y_temp[k])
                tempx.append(X_temp[k])
                tempz.append(Z_temp[k])
        elif len(Y_temp) < 200:
            for k in range(0, len(Y_temp)):
                temp1.append(Y_temp[k])
                tempx.append(X_temp[k])
                tempz.append(Z_temp[k])
            for k in range(len(Y_temp), 200):
                temp1.append(0)
                tempx.append(0)
                tempz.append(0)

        cor1 = correlation(temp1, S1_temp)  # 与多个标准波形进行比较，算出其相似度
        if cor1 >= 0.6:
            point += 1
        cor2 = correlation(temp1, S2_temp)
        if cor2 >= 0.6:
            point += 1
        cor3 = correlation(temp1, S3_temp)
        if cor3 >= 0.6:
            point += 1
        cor4 = correlation(temp1, S4_temp)
        if cor4 >= 0.6:
            point += 1
        cor5 = correlation(temp1, S5_temp)
        if cor5 >= 0.6:
            point += 1
        cor6 = correlation(temp1, S6_temp)
        if cor6 >= 0.6:
            point += 1
        if point >= 5 and -1 < mean(temp1) < 1:
            X_norm.append(X_temp)
            X_norm_learn.append(tempx)
            Y_norm.append(Y_temp)
            Y_norm_learn.append(temp1)
            Z_norm.append(Z_temp)
            Z_norm_learn.append(tempz)
            T_norm.append(T_temp)
            flag_norm.append(i)
        else:
            X_abnorm.append(X_temp)
            Y_abnorm.append(Y_temp)
            Z_abnorm.append(Z_temp)
            T_abnorm.append(T_temp)
            flag_abnorm.append(i)
    elif (div_point_index[i + 1] - div_point_index[i] + 1) < 150 or (
            div_point_index[i + 1] - div_point_index[i] + 1) >= 300:
        T_temp2 = []
        for k in range(div_point_index[i], div_point_index[i + 1] + 1):
            T_temp2.append(k / 62)

        X_abnorm.append(X_temp)
        Y_abnorm.append(Y_temp)
        Z_abnorm.append(Z_temp)
        T_abnorm.append(T_temp2)
        flag_abnorm.append(i)

xab, yab, zab = [], [], []
for wave in Y_abnorm:
    abx, aby, abz = [], [], []
    if len(wave) >= 300:
        for k in range(0, 300):
            aby.append(wave[k])
    elif 150 < len(wave) < 300:
        for k in range(0, len(wave)):
            aby.append(wave[k])
        for k in range(len(wave), 300):
            aby.append(0)
    if (len(aby) != 0):
        yab.append(aby)
# print(len(yab))
# print(len(Y_abnorm))
# for i in range(len(yab)):
#     plt.plot(yab[i], "k-", alpha=.3)
# plt.show()

K = []
for i in range(1000, 2000):
    K.append(yab[i])

p = metrics.cdist_dtw(K)
with open("pairwise_word_distances.npy", "wb") as f:
    np.save(f, p)
dtw_clustering = AgglomerativeClustering(linkage='average', n_clusters=5, affinity='precomputed')
label = dtw_clustering.fit_predict(p)
print(label)
np.fill_diagonal(p, 0)

for yi in range(5):
    plt.subplot(2, 3, yi + 1)
    l = len(label)
    for j in range(l):
        if label[j] == yi:
            plt.plot(K[j], "k-", alpha=.3)
        plt.text(0.55, 0.85, 'Cluster %d' % (yi + 1), transform=plt.gca().transAxes)
plt.tight_layout()
plt.show()

K_2 = []
for i in range(len(K)):
    if label[i] == 2:
        K_2.append(K[i])

p = metrics.cdist_dtw(K_2)
with open("pairwise_word_distances2.npy", "wb") as f:
    np.save(f, p)
dtw_clustering = AgglomerativeClustering(linkage='average', n_clusters=5, affinity='precomputed')
label = dtw_clustering.fit_predict(p)
print(label)
np.fill_diagonal(p, 0)

for yi in range(5):
    plt.subplot(2, 3, yi + 1)
    l = len(label)
    for j in range(l):
        if label[j] == yi:
            plt.plot(K[j], "k-", alpha=.3)
        plt.text(0.55, 0.85, 'Cluster %d' % (yi + 1), transform=plt.gca().transAxes)
plt.tight_layout()
plt.show()
