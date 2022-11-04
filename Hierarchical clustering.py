import numpy as np
from sklearn_extra.cluster import KMedoids
import tslearn.metrics as metrics
# 自定义数据处理
from LTTB import LTTB
from tslearn.clustering import silhouette_score
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.generators import random_walks
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from read_txt_line import read_txt_line
from sklearn.cluster import AgglomerativeClustering

X = read_txt_line('C:\\Users\\chencheng\\Desktop\\波形测试\\test.txt')
X = np.array(X)
seed = 0


def test_heirarchical():
    # 声明precomputed自定义相似度计算方法
    dtw_clustering = AgglomerativeClustering(linkage='average', n_clusters=5, affinity='precomputed')
    # 采用tslearn中的DTW系列及变种算法计算相似度，生成距离矩阵dists
    dists = metrics.cdist_dtw(X)
    y_pred = dtw_clustering.fit_predict(dists)
    np.fill_diagonal(dists, 0)
    score = silhouette_score(dists, y_pred, metric="precomputed")
    for i in range(len(y_pred)):
        plt.subplot(3, 2, y_pred[i] + 1)
        plt.plot(X[i].ravel(), "k-", alpha=.3)
    # print(X.shape)
    print(y_pred)
    print("silhouette_score: " + str(score))
    plt.show()
test_heirarchical()
