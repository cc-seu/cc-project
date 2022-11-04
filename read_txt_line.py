def read_txt_line(filename):
    with open(file=filename, mode='r+', encoding='utf-8') as g:
        lines = g.readlines()
        j = 0
        X = []
        for line in lines:
            value = [float(s) for s in line.split()]
            l = len(value)
            temp = []
            for i in range(0, l):
                temp.append(value[i])
            X.append(temp)

    return X
