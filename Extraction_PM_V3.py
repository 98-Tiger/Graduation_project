import pandas as pd
import numpy as np
from netCDF4 import Dataset
import re
import os

def get_file(root_path, all_files=[]):
    """
    递归函数，遍历该文档目录和子目录下的所有文件，获取其path
    """
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):  # not a dir
            all_files.append(root_path + '/' + file)
        else:  # is a dir
            get_file((root_path + '/' + file), all_files)
    return all_files


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False


def Extaction_site_PM(path_environment, path_site_index, path_out):
    """
    path_environment: PM2.5数据路径
    path_site: 站点列表路径
    path_out：输出数据路径
    """
    path_environment_list = get_file(path_environment)
    for path_environment in path_environment_list:
        # 读取所有监测站环境检测数据
        df_environment = pd.read_csv(path_environment)
        # 提取pm2.5所在行
        df_environment = df_environment.set_index('type', drop=False)  # 将type设为索引
        df_environment = df_environment.loc[['PM2.5'], :]
        # 将id_vars中指定列保留原格式，其余转换成列，字符串列名设为site_id，数值列名设为PM2.5
        df_environment = pd.melt(df_environment, id_vars=['date', 'hour', 'type'],
                    var_name='site_id', value_name='PM2.5')
        # 剔除PM2.5列中空值
        df_environment = df_environment.dropna(subset=['PM2.5'])
        # 去除不需要时间数据
        df_environment = df_environment[~df_environment['hour'].isin(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 18, 19, 20, 21, 22, 23])]
        # 将df_environment与站点列表数据合并，提取所需经纬度范围内数据
        df_site = pd.read_csv(path_site_index)  # 读取站点列表数据
        # 按照site_id合并数据
        df_result = pd.merge(df_environment, df_site, on='site_id')  
        df_result = df_result.sort_values(
            by=['hour', 'latitude', 'longitude'])  # 按照hour，latitude，longitude排列
        # 将date和hour合并成新列time
        df_result['hour'] = df_result['hour'].map(str)
        df_result['time'] = df_result['date'].map(str) + df_result['hour'].replace('9', '09')
        # 重新排列列
        df_result = df_result.loc[:, ['time', 'site_id', 'latitude', 'longitude', 
        'Cloud_lat_index', 'Cloud_lon_index', 'AUX_H8_lat_index', 'AUX_H8_lon_index', 
        'ERA5_lat_index', 'ERA5_lon_index', 'NDVI_lat_index', 'NDVI_lon_index', 'PM2.5']]  
        # 依据时间，创建数据存储文件夹
        rules = re.compile(r'china_sites_(.*?).csv')  # 文件名中无用部分
        time_PM_month = re.findall(rules, str(os.path.split(path_environment)[-1]))[0][:-2]  # 提取environment文件时间到月
        mkdir(f'{path_out}/{time_PM_month}')  # 创建文件夹
        # 输出数据
        rules = re.compile(r'china_sites_(.*?).csv')  # 文件名中无用部分
        time_PM = re.findall(rules, str(os.path.split(path_environment)[-1]))[0]  # 提取environment文件时间
        out_put = f'{path_out}/{time_PM_month}/china_sites_PM_{time_PM}.csv'  # 输出路径
        df_result.to_csv(out_put, index=False)  # 输出为csv文件


if __name__ == '__main__':
    path_environment = 'C:/Users/Tiger/Desktop/BiShe/Data/PM2.5/Original/china_sites_20200101-20201231'
    path_site_index = 'C:/Users/Tiger/Desktop/ceshi/site_index.csv'
    path_out = 'C:/Users/Tiger/Desktop/PM2.5'
    Extaction_site_PM(path_environment, path_site_index, path_out)
