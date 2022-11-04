def w_to_txt(filename,data):
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s+ ','  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.write('\n')
    file.close()
