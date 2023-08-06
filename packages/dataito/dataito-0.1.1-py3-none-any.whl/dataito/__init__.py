'''DataITO模块'''
'''Python数据输入(Input)、转换(transform)、输出(output)，一行代码读取/转换多种格式的数据文件'''

import os
import numpy as np
import pandas as pd
import json


'''输入(input):数据读取'''
def read(path):

    DataFormat = path.split(".")[1] #获取文件后缀

    if DataFormat == 'xlsx':
        data = pd.read_excel(path,engine='openpyxl')
        return np.array(data)
    elif DataFormat == 'json':
        data = json.loads(open(path).read())
        return data
    else:
        
        data = {
            # 'txt': open(path,"r").readlines(),    #保留换行符
            'txt': open(path, "r").read().splitlines(), #不保留换行符
            'csv': pd.read_csv(path,"r"),

             #这几个比较离谱，放在这里就会报错
            # 'json': pd.read_json(path,"r")
            # 'json': json.loads(open(path).read())
            # 'xlsx': pd.read_excel(path,engine='openpyxl')
        }.get(DataFormat,"error, unsupported format")

        return np.array(data)


'''转换(transform):格式转换'''
def transform(basic_data,target_data_type):
    
    try:
        df = pd.DataFrame(basic_data)   #先转化成dataframe

    except IOError:

        print("This function does not support JSON format or its converted format") #json格式转换成的数组大小是空的

    else:
        
        # 再转化成指定类型
        data = {

            'dataframe': df,                #转换为dataframe类型
            'pandas': df,                   #pandas支持的格式(虽然还是dataframe)

            'list': df.values.tolist(),     #列表

            'array': df.values,             #数组
            'numpy': np.array(df),          #numpy支持的格式(虽然还是数组)

        }.get(target_data_type,"error, unsupported format")
        return data


'''输出:数据保存'''
def save(data,savepath = " "):

    data = transform(data,'dataframe')      #统一转换为dataframe

    if isinstance(data,pd.DataFrame):
        if savepath == " ":                             #如果没有填写路径或文件名
            data.to_excel("data.xlsx")                  #默认文件名为data.xlsx
        elif savepath != " ":                           
            data.to_excel(savepath)                     
        else:
            print("save failed") 
    else:
        print("error, unsupported format")