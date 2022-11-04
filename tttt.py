# 取txt文件 的若干行到另一个txt
f1 = open('C:\\Users\\Dell\\Desktop\\待处理文件\\20200728-0101366027-10.txt', 'rb')
f2 = open('C:\\Users\\Dell\\Desktop\\verify_cut\\20200728-0101366027-10#.txt', 'ab')

i = 0
while True:
    line = f1.readline()
    i += 1
    if 0 < i <= 18750:
        f2.write(line)
    if i > 18750:
        break
