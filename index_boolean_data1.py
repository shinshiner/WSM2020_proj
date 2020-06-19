#!/usr/bin/env python
# coding: utf-8

# ### 1.Rename the file

import shutil
import os
def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "/" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == False:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            shutil.rmtree(file_data)



def rename_data(path,suffix):
    files = os.listdir(path)
    for i, file in enumerate(files):
        if i % 10000 == 0:
            print(i)
        NewFileName = os.path.join(path, str(i)+suffix)
        OldFileName = os.path.join(path, file)
        os.rename(OldFileName, NewFileName)
       
path = './zxgk'
rename_data(path, '.json')

