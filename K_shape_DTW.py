import numpy as np
import tslearn.metrics as metrics
# 自定义数据处理
from LTTB import LTTB
from tslearn.clustering import silhouette_score
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.generators import random_walks
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from read_txt_line import read_txt_line
from tslearn.clustering import KShape
from sklearn.metrics.cluster import homogeneity_score,completeness_score
# X = read_txt_line('C:\\Users\\chencheng\\Desktop\\波形测试\\test.txt')
# X = np.array(X)
seed = 0
X, Y, Z = [], [], []
filepath = 'C:\\Users\\Dell\\Desktop\\20200502-0101352583-10_label.txt'
with open(file=filepath, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        value = [str(s) for s in line.split('\t')]
        X.append(float(value[0]))
        Y.append(value[1])
        if float(value[0]) == 1:
            Z_temp = value[2].split(',')
            z = []
            for num in Z_temp:
                z.append(float(num))
            Z.append(z)
f.close()
print(len(Z))
K = []
for i in range(0, 1000):
    K.append(Z[i])


# elbow法则找最佳聚类数，结果：elbow = 5
def test_elbow():
    global Z, seed
    distortions = []
    X = TimeSeriesScalerMeanVariance(mu=0.0, std=1.0).fit_transform(Z)
    # 1 to 10 clusters
    for i in range(2, 7):
        ks = KShape(n_clusters=i, n_init=10, verbose=True, random_state=seed)
        # Perform clustering calculation
        ks.fit(X)
        # ks.fit will give you ks.inertia_ You can
        # inertia_
        distortions.append(ks.inertia_)
    plt.plot(range(2, 7), distortions, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()


def test_k_shape():
    global Z, seed
    np.random.seed(seed)
    num_cluster = 5
    # 标准化数据
    X = TimeSeriesScalerMeanVariance(mu=0.0, std=1.0).fit_transform(K)
    ks = KShape(n_clusters=num_cluster, max_iter=100, n_init=10, verbose=True, random_state=seed)
    y_pred = ks.fit_predict(X)
    dists = metrics.cdist_dtw(X)
    np.fill_diagonal(dists, 0)  # 将矩阵dists对角元素设置为0
    score = silhouette_score(dists, y_pred, metric="precomputed")
    print("silhouette_score: " + str(score))
    for yi in range(num_cluster):
        plt.subplot(2, 3, yi + 1)
        for xx in X[y_pred == yi]:
            plt.plot(xx.ravel(), "k-", alpha=.3)
        plt.plot(ks.cluster_centers_[yi].ravel(), "r-")
        plt.text(0.55, 0.85, 'Cluster %d' % (yi + 1),
                 transform=plt.gca().transAxes)
        if yi == 1:
            plt.title("SBD" + "  $k$-shape")
    plt.tight_layout()
    plt.show()


test_elbow()
# test_k_shape()
