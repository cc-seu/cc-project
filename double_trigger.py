# 判断某一个时间序列是不是双重触发的先验模型

import matplotlib.pyplot as plt
from scipy import signal
from numpy import *


def is_double_trigger(data):
    peak, _ = signal.find_peaks(data, height=30, distance=50)
    if len(peak) == 2:
        return True
    else:
        return False


if __name__ == '__main__':
    A, X, Z = [], [], []
    filepath = 'C:\\Users\\Dell\\Desktop\\标注结果\\第三次标注：202\\double_trigger_0-4679.txt'
    with open(file=filepath, mode='r+', encoding='utf-8') as f:
        lines = f.readlines()
        point = 0
        for line in lines:
            value = [str(s) for s in line.split('\t')]
            X.append(value[0])
            Z_temp = value[1].split(',')
            z = []
            for num in Z_temp:
                z.append(float(num))
            Z.append(z)
    f.close()
    num = 0
    for i in range(len(Z)):
        if is_double_trigger(Z[i]):
            num += 1
    print(num)
    print(len(Z))

# l = len(X)
# for j in range(l):
#     plt.plot(Z[j], "k-", alpha=.3)
# plt.tight_layout()
# plt.show()
#
    y = Z[1]
    peaks, _ = signal.find_peaks(y, height=30, distance=50)
    plt.figure(figsize=(10, 5))
    plt.plot(y)
    for i in range(len(peaks)):
        plt.plot(peaks[i], y[peaks[i]], '.', markersize=10)
    plt.show()
