from choose_n_from_m import get_random_list_without_repetition
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from tslearn.clustering import silhouette_score
import tslearn.metrics as metrics
from read_label_file import read_label_file
import matplotlib.pyplot as plt


def pre_classification(X, Y, Z):
    learn_pressure, learn_flow, learn_volume = [], [], []
    # learn_index = get_random_list_without_repetition(3000, 1000)
    for i in range(len(X)):
        learn_pressure.append(X[i])
        learn_flow.append(Y[i])
        learn_volume.append(Z[i])
    p = metrics.cdist_dtw(learn_flow)
    with open("pairwise_word_distances.npy", "wb") as f:
        np.save(f, p)
    dtw_clustering = AgglomerativeClustering(linkage='average', n_clusters=5, affinity='precomputed')
    label = dtw_clustering.fit_predict(p)
    np.fill_diagonal(p, 0)
    score = silhouette_score(p, label, metric="precomputed")
    print("silhouette_score: " + str(score))

    count_num = [0, 0, 0, 0, 0]  # 寻找需要第二次无监督聚类的类别 key
    key = -1
    for i in range(len(label)):
        count_num[label[i]] += 1
    for i in range(len(count_num)):
        if count_num[i] >= len(label) * 0.5:
            key = i

    # label_num_threshold = [0, 0, 0, 0, 0]
    # filename = '5.txt'
    # file = open(filename, 'a')
    # for k in range(len(learn_flow)):
    #     if label[k] != key and label_num_threshold[label[k]] <= len(label) * 0.2:
    #         label_num_threshold[label[k]] += 1
    #         s = str(learn_pressure[k]).replace('[', '').replace(']', '') + '\t' + str(learn_flow[k]).replace('[',
    #                                                                                                          '').replace(
    #             ']', '') + '\t' + str(learn_volume[k]).replace('[', '').replace(']', '')
    #         s = str(label[k]) + '\t' + s + '\n'
    #         file.write(s)
    # file.write(str(score))
    # file.close()
    time = []
    for i in range(len(X[0])):
        time.append(i / 62.5)
    font1 = {'family': 'Arial', 'weight': 'bold', 'size': 30}
    fig, ax = plt.subplots(1, 5, sharex=True, sharey=True, figsize=(30, 6))
    # fig.delaxes(ax[1, 2])  # 删除最后一个子图
    # 设置所有子图x、y轴标签
    fig.text(0.01, 0.5, 'Flow(L/min)', va='center', rotation='vertical', font=font1)
    fig.text(0.5, 0.04, 'Time(s)', va='center', ha='center', font=font1)
    for yi in range(5):
        a = plt.subplot(1, 5, yi + 1)
        a.tick_params(labelsize=20)
        plt.ylim((-70, 70))
        a.set_yticks([-60, -30, 0, 30, 60])
        labels = a.get_xticklabels() + a.get_yticklabels()
        [l.set_fontname('Arial') for l in labels]
        for j in range(len(label)):
            if label[j] == yi:
                a.plot(time, learn_flow[j], "k-", alpha=0.8)
            # a.text(0.42, 0.85, 'Cluster %d' % (yi + 1), font1, transform=plt.gca().transAxes)

    plt.tight_layout()
    plt.show()

    iteration_pressure = []
    iteration_flow = []
    iteration_volume = []
    for i in range(len(label)):
        if label[i] == key:
            iteration_pressure.append(learn_pressure[i])
            iteration_flow.append(learn_flow[i])
            iteration_volume.append(learn_volume[i])
    p2 = metrics.cdist_dtw(iteration_flow)
    with open("pairwise_word_distances2.npy", "wb") as f:
        np.save(f, p2)
    dtw_clustering = AgglomerativeClustering(linkage='average', n_clusters=5, affinity='precomputed')
    label2 = dtw_clustering.fit_predict(p2)
    np.fill_diagonal(p2, 0)
    score = silhouette_score(p2, label2, metric="precomputed")
    print("silhouette_score: " + str(score))

    # label_num_threshold2 = [0, 0, 0, 0, 0]
    # file = open(filename, 'a')
    # for k in range(len(iteration_flow)):
    #     if label_num_threshold2[label2[k]] <= len(label2) * 0.2:
    #         label_num_threshold2[label2[k]] += 1
    #         s = str(iteration_pressure[k]).replace('[', '').replace(']', '') + '\t' + str(iteration_flow[k]).replace(
    #             '[', '').replace(']', '') + '\t' + str(iteration_volume[k]).replace('[', '').replace(']', '')
    #         s = str(label2[k]) + '\t' + s + '\n'
    #         file.write(s)
    # file.close()

    fig, ax = plt.subplots(1, 5, sharex=True, sharey=True, figsize=(30, 6))
    # fig.delaxes(ax[1, 2])  # 删除最后一个子图
    # 设置所有子图x、y轴标签
    fig.text(0.01, 0.5, 'Flow(L/min)', va='center', rotation='vertical', font=font1)
    fig.text(0.5, 0.04, 'Time(s)', va='center', ha='center', font=font1)
    for yi in range(5):
        a = plt.subplot(1, 5, yi + 1)
        a.tick_params(labelsize=20)
        plt.ylim((-70, 70))
        a.set_yticks([-60, -30, 0, 30, 60])
        labels = a.get_xticklabels() + a.get_yticklabels()
        [l.set_fontname('Arial') for l in labels]
        for j in range(len(label2)):
            if label2[j] == yi:
                plt.plot(time, iteration_flow[j], "k-", alpha=0.8)
            # plt.text(0.42, 0.85, 'Cluster %d' % (yi + 1), font1, transform=plt.gca().transAxes)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    A, X, Y, Z = [], [], [], []
    label, time = [], []
    filepath = 'C:\\Users\\Dell\\Desktop\\1_10_14_16_xu.txt'
    read_label_file(label, time, X, Y, Z, filepath)
    pre_classification(X, Y, Z)
    print(len(X))
