import numpy as np
import scipy
from scipy import signal
import matplotlib.pyplot as plt
import math
from w_to_excel import write_excel_xls
from w_to_excel import write_excel_xls_append

X, Y, Z = [], [], []
div_point = []
div_point_index = []
file_path = 'C:\\Users\\Dell\\Desktop\\第七次标注：204\\20200704-0101360573-8.rpx_abnormal.txt'
with open(file=file_path, mode='r+', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        value = [str(s) for s in line.split('\t')]
        X_temp = value[2].split(',')
        Y_temp = value[3].split(',')
        Z_temp = value[4].split(',')
        x, y, z = [], [], []
        for num in X_temp:
            x.append(float(num))
        Y.append(x)
        for num in Y_temp:
            y.append(float(num))
        X.append(y)
        for num in Z_temp:
            z.append(float(num))
        Z.append(z)
f.close()

# n = len(X)
# book_name_xls = 'C:\\Users\\Dell\\Desktop\\20200502-0101352583-10.xls'
# sheet_name_xls = '20200502-0101352583-10'
# value_title = [['流量']]
# write_excel_xls(book_name_xls, sheet_name_xls, value_title)
#
# temp_w=[]
# for i in range(0, n - 1):
#     temp_w.append(X[i])
#
# write_excel_xls_append(book_name_xls, temp_w)

output = open('data1.xls', 'w', encoding='gbk')
output.write('name\tgender\tstatus\tage\n')
for i in range(len(Y)):
    for j in range(len(Y[i])):
        output.write(str(Y[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
        output.write('\t')  # 相当于Tab一下，换一个单元格
    output.write('\n')  # 写完一行立马换行
output.close()
