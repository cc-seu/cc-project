import matplotlib.pyplot as plt
from scipy import signal
from numpy import *

X, Y, Z = [], [], []

filepath = 'C:\\Users\\Dell\\Desktop\\MP_WAVE.txt'
with open(file=filepath, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    j = 0
    for line in lines:
        value = [float(s) for s in line.split()]
        X.append(value[0] / 10 - 10)
        Z.append(value[2])
        if 3 > (value[1] - 1799) > -3:
            Y.append(0)

        else:
            Y.append((value[1] - 1799) / 10)
            j = j + 1

peaks_PIP, _ = signal.find_peaks(X, height=20)
PIP = X[peaks_PIP[0]]  # PIP
RR = ceil(60 / (len(X) / 62.5))  # RR
peaks_Vt, _ = signal.find_peaks(Z, height=300)
Vt = Z[peaks_Vt[0]]  # Vt
PEEP = 10  # PEEP

start = peaks_Vt[0]
end = 0
for k in range(start, len(Y)):
    if (Y[k + 1] + Y[k + 2] + Y[k + 3] - 3 * Y[k]) / 6 < -1:
        end = k
        break
P_temp = 0
for k in range(start, end):
    P_temp = P_temp + X[k]
P_plateau = P_temp / (end - start)  # P_plateau

MP = 0.098 * Vt * RR * (PIP - (P_plateau - PEEP) * 0.5)  # MP
print(MP)
print(PIP)
print(RR)
print(Vt)
print(PEEP)
print(P_plateau)

plt.subplot(3, 1, 1)
plt.plot(X)
plt.plot(peaks_PIP[0], X[peaks_PIP[0]], '.', markersize=10)
plt.plot(start, X[start], '.', markersize=10)
plt.plot(end, X[end], '.', markersize=10)
plt.subplot(3, 1, 2)
plt.plot(Y)
plt.subplot(3, 1, 3)
plt.plot(Z)
plt.plot(peaks_Vt[0], Z[peaks_Vt[0]], '.', markersize=10)
plt.show()
