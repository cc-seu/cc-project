#  读取从label_software生成的文件,只读2
def read_label_file(label, time, X, Y, Z, file_path):
    with open(file=file_path, mode='r+', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            value = [str(s) for s in line.split('\t')]
            if float(value[0]) == 2:
                label.append(float(value[0]))
                time.append(value[1])
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


import matplotlib.pyplot as plt

if __name__ == '__main__':
    label, time, X, Y, Z = [], [], [], [], []
    file = 'C:\\Users\\Dell\\Desktop\\新建文件夹\\20200716-0101364104-17_label_10.txt'
    read_label_file(label, time, X, Y, Z, file)
    print(len(X))
    # f = plt.figure(figsize=(7, 5.2), dpi=150)
    # a = f.add_subplot(311)
    # b = f.add_subplot(312)
    # c = f.add_subplot(313)
    # T = []
    # for i in range(len(X[0])):
    #     T.append(i / 62.5)
    # for i in range(200):
    #     a.plot(T, X[i], color='black')
    #     b.plot(T, Y[i], color='black')
    #     c.plot(T, Z[i], color='black')
    # font1 = {'family': 'Arial', 'weight': 'bold', 'size': 20}
    # a.set_ylabel("Pressure", font1)
    # b.set_ylabel("Flow", font1)
    # c.set_ylabel("Volume", font1)
    # c.set_xlabel("Time(s)", font1)
    # a.tick_params(labelsize=13)
    # b.tick_params(labelsize=13)
    # c.tick_params(labelsize=13)
    # labels = a.get_xticklabels() + a.get_yticklabels()
    # [label.set_fontname('Arial') for label in labels]
    # labels = b.get_xticklabels() + b.get_yticklabels()
    # [label.set_fontname('Arial') for label in labels]
    # labels = c.get_xticklabels() + c.get_yticklabels()
    # [label.set_fontname('Arial') for label in labels]
    # plt.show()
