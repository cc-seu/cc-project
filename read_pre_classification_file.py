#  读取从pre_classification生成的文件
def read_pre_classification_file(X, Y, Z, file_path):
    with open(file=file_path, mode='r+', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            value = [str(s) for s in line.split('\t')]
            X_temp = value[1].split(',')
            Y_temp = value[2].split(',')
            Z_temp = value[3].split(',')
            x, y, z = [], [], []
            for num in X_temp:
                x.append(float(num))
            X.append(x)
            for num in Y_temp:
                y.append(float(num))
            Y.append(y)
            for num in Z_temp:
                z.append(float(num))
            Z.append(z)
    f.close()
