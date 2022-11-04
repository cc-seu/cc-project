import numpy as np
import scipy
from scipy import signal
import matplotlib.pyplot as plt
import math


def DTWDistance(s1, s2):
    DTW = {}

    for i in range(len(s1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist = (s1[i] - s2[j]) ** 2
            DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])

    return math.sqrt(DTW[len(s1) - 1, len(s2) - 1])


A, B, C, D, E, F, G, H = [], [], [], [], [], [], [], []
file_path = 'C:\\Users\\陈哥\\Desktop\\周期呼吸波形\\standard1.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        A.append(float(line))

file_path = 'C:\\Users\\陈哥\\Desktop\\周期呼吸波形\\standard2.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        B.append(float(line))

file_path = 'C:\\Users\\陈哥\\Desktop\\周期呼吸波形\\standard3.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        C.append(float(line))

file_path = 'C:\\Users\\陈哥\\Desktop\\周期呼吸波形\\standard4.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        D.append(float(line))

file_path = 'C:\\Users\\陈哥\\Desktop\\周期呼吸波形\\standard5.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        E.append(float(line))

file_path = 'C:\\Users\\陈哥\\Desktop\\周期呼吸波形\\standard6.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        F.append(float(line))

# file_path = 'C:\\Users\\陈哥\\Desktop\\周期呼吸波形\\6.txt'
# with open(file=file_path, mode='r+', encoding='utf-8') as f:
#     for line in f.readlines():
#         line = line.strip('\n')  # 去掉列表中每一个元素的换行符
#         G.append(float(line))

G.append(A)
G.append(B)
G.append(C)
G.append(D)
G.append(E)
G.append(F)

# for i in range (0,7):
#     H.append(DTWDistance(H[0],H[i]))
# print(H)
for i in range(0, 6):
    for j in range(0, 6):
        H.append(DTWDistance(G[i], G[j]))
print(H)

I = []

temp_sum = 0
for i in range(0, 6):
    temp_sum += H[i]
I.append(temp_sum)

temp_sum = 0
for i in range(6, 12):
    temp_sum += H[i]
I.append(temp_sum)

temp_sum = 0
for i in range(12, 18):
    temp_sum += H[i]
I.append(temp_sum)

temp_sum = 0
for i in range(18, 24):
    temp_sum += H[i]
I.append(temp_sum)

temp_sum = 0
for i in range(24, 30):
    temp_sum += H[i]
I.append(temp_sum)

temp_sum = 0
for i in range(30, 36):
    temp_sum += H[i]
I.append(temp_sum)
print(I)
# A = X_smooth[signal.argrelextrema(X_smooth, np.less)]
# D = signal.argrelextrema(X_smooth, np.less)[0]
# X = np.array(X)
# B = X[signal.argrelextrema(X, np.less)]
# k=len(A)
# for i in range(0,k-1):
#     if(A[i]<-20):
#         C.append(A[i])
#         E.append(D[i])
#         print(A[i])


# for i in range(0,k-1):
#     if(B[i]<-20):
#         print(B[i])
# print(X_smooth[signal.argrelextrema(X_smooth, np.less)])
# print(signal.argrelextrema(X_smooth, np.less))
# plt.subplot(3,1,3)
# plt.plot(Z)

# a=DTWDistance(X,Y)
# b=DTWDistance(X,Z)
# print(a)
# print(b)
# plt.subplot(2,1,1)
# plt.plot(X)
# plt.plot(signal.argrelextrema(X, np.less)[0],X[signal.argrelextrema(X, np.less)],'+', markersize=10)
# plt.subplot(2,1,2)
# plt.plot(X_smooth)
# plt.plot(E,C,'+', markersize=10)
# plt.show()
