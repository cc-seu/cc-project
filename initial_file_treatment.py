# -*- coding: utf-8 -*-
# 初始呼吸波形文件后缀改变、文件内前缀删除、时间标识删除
import os

# # 列出当前目录下所有的文件
# filedir = 'C:\\Users\\WT\\Desktop\\test'
# files = os.listdir(filedir)   # 如果path为None，则使用 path = '.'
#
# for filename in files:
#     portion = os.path.splitext(filename)  # 分离文件名与扩展名
#     # 如果后缀是jpg
#     if portion[1] == '.jpg':
#         # 重新组合文件名与后缀名
#         newname = portion[0] + '.gif'
#         filename = filedir + '\\' + filename
#         newname = filedir + '\\' + newname
#         os.rename(filename, newname)


def modify_suffix(filedir, suffix):#（目标文件夹，替换后的文件类型）
    files = os.listdir(filedir)
    num = 0
    for filename in files:
        portion = os.path.splitext(filename)
        if portion[1] != suffix:
            newname = portion[0] + suffix
            filename = filedir + '\\' + filename
            newname = filedir + '\\' + newname
            os.rename(filename, newname)
            print("替换文件后缀", filename)
            num = num + 1
            print(num)


def modify_file_format(filedir):
    files = os.listdir(filedir)
    for file_path in files:
        file_path = filedir + '\\' + file_path
        with open(file_path, 'r') as h:
            lines = h.readlines()
        with open(file_path, 'w') as l:
            for line in lines:
                if line.startswith(" "):
                    l.write(line)


if __name__ == '__main__':

    modify_suffix('C:\\Users\\Dell\\Desktop\\新加数据', '.txt')
    modify_file_format('C:\\Users\\Dell\\Desktop\\新加数据')

