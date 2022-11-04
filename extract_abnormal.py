import math
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from tslearn.clustering import silhouette_score
import tslearn.metrics as metrics

X, Y, Z = [], [], []
filepath = 'C:\\Users\\Dell\\Desktop\\第三次标注：202\\20200701-0101361822-16.rpx_label.txt'
with open(file=filepath, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        value = [str(s) for s in line.split('\t')]
        X.append(float(value[0]))
        if float(value[0]) == 2:
            Z_temp = value[2].split(',')
            z = []
            for num in Z_temp:
                z.append(float(num))
            Z.append(z)
            Y.append(value[1])
f.close()
K = []  # K存储异常波形变量
T = []  # T存储异常波形对应的时间段
print(len(Z))  # 4679
for i in range(1500, 2000):
    K.append(Z[i])
    T.append(Y[i])

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

filename = 'double_trigger3.txt'
file = open(filename, 'a')
for k in range(len(K)):
    if label[k] == 3:
        s = str(K[k]).replace('[', '').replace(']', '')
        s = T[k] + '\t' + s + '\n'
        file.write(s)
file.close()


