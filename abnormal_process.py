from numpy import *
from scipy import stats
import matplotlib.pyplot as plt
from read_pre_classification_file import read_pre_classification_file
from pre_classification import pre_classification
from read_label_file import read_label_file

if __name__ == '__main__':
    X, Y, Z = [], [], []
    label, time = [], []
    X_250, Y_250, Z_250 = [], [], []
    filepath = 'C:\\Users\\Dell\\Desktop\\预处理文章选取样本\\16\\4号3-7---2床_label.txt'
    # read_pre_classification_file(X, Y, Z, filepath)
    read_label_file(label, time, X, Y, Z, filepath)
    # for i in range(0, 100):
    #     temp_x, temp_y, temp_z = [], [], []
    #     if len(X[i]) > 250:
    #         for j in range(250):`
    #             temp_x.append(X[i][j])
    #             temp_y.append(Y[i][j])
    #             temp_z.append(Z[i][j])
    #     else:
    #         for j in range(len(X[i])):
    #             temp_x.append(X[i][j])
    #             temp_y.append(Y[i][j])
    #             temp_z.append(Z[i][j])
    #         for j in range(len(X[i]), 250):
    #             temp_x.append(X[i][len(X[i])-1])
    #             temp_y.append(0)
    #             temp_z.append(0)
    #     X_250.append(temp_x)
    #     Y_250.append(temp_y)
    #     Z_250.append(temp_z)
    # pre_classification(X_250, Y_250, Z_250)


    print(len(label))

