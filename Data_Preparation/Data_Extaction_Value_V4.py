import numpy as np
from netCDF4 import Dataset
import pandas as pd
import netCDF4 as nc
from osgeo import gdal
from datetime import datetime
import math
import csv
import re
import os
import time




def get_file_modis(root_path, all_files=[]):
    """
    递归函数，遍历该文档目录和子目录下的所有文件，获取其path
    """
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):  # not a dir
            all_files.append(root_path + '/' + file)
        else:  # is a dir
            get_file_modis((root_path + '/' + file), all_files)
    return all_files


def get_file_yun(root_path, all_files1=[]):
    """
    递归函数，遍历该文档目录和子目录下的所有文件，获取其path
    """
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):  # not a dir
            all_files1.append(root_path + '/' + file)
        else:  # is a dir
            get_file_yun((root_path + '/' + file), all_files1)
    return all_files1


def retime_utc_to_bj(path_yun):
    rules = re.compile(r'NC_H08_(.*?)00_L2CLP010_FLDK.02401_02401.nc')  # 文件名中无用部分
    time = re.findall(rules, str(os.path.split(path_yun)[-1]))[0]  # 提取Cloud文件时间
    if time[-2:] == '01':
        time_bj = time[:-3] + '09'
    elif time[-2:] == '02':
        time_bj = time[:-3] + '10'
    elif time[-2:] == '03':
        time_bj = time[:-3] + '11'
    elif time[-2:] == '04':
        time_bj = time[:-3] + '12'
    elif time[-2:] == '05':
        time_bj = time[:-3] + '13'
    elif time[-2:] == '06':
        time_bj = time[:-3] + '14'
    elif time[-2:] == '07':
        time_bj = time[:-3] + '15'
    elif time[-2:] == '08':
        time_bj = time[:-3] + '16'
    elif time[-2:] == '09':
        time_bj = time[:-3] + '17'
    
    return time_bj


def get_Value_to_csv(path_PM, path_Cloud, path_Satellite, path_ERA5, path_AUX, path_NDVI, path_result):
    # 读取result文件
    f = open(path_result, 'a+', encoding='utf-8', newline='')
    writer = csv.writer(f)
    # 读取ERA5数据
    data_ERA5 = Dataset(path_ERA5)
    Dataset.set_auto_mask(data_ERA5, False)
    # 读取ERA5变量
    time_ERA5 = nc.num2date(data_ERA5.variables['time'], data_ERA5.variables['time'].units)  # 变为标准时间
    V10_arr = data_ERA5.variables['v10'][:]
    U10_arr = data_ERA5.variables['u10'][:]
    BLH_arr = data_ERA5.variables['blh'][:]
    ET_arr = data_ERA5.variables['e'][:]
    SP_arr = data_ERA5.variables['sp'][:]
    PRE_arr = data_ERA5.variables['tp'][:]
    TEM_arr = data_ERA5.variables['t2m'][:]
    Td_arr = data_ERA5.variables['d2m'][:]
    # 读取辅助数据
    data_AUX = Dataset(path_AUX)  
    # 读取辅助数据变量
    DEM_arr = data_AUX.variables['Height'][:]
    LUCC_arr = data_AUX.variables['LandCoverType'][:]
    # 获取NDVI文件夹下，所有文件的路径
    path_NDVI_list = get_file_modis(path_NDVI)
    for path_modis in path_NDVI_list:
        # 读取NDVI数据
        dataset_NDVI = gdal.Open(path_modis)
        data_NDVI = dataset_NDVI.GetRasterBand(1).ReadAsArray()
        # 依据NDVI数据的时间，读取相应时间的Cloud数据
        rules = re.compile(r'MOD13A3.A(.*?).only_NDVI.tif')  # 文件名中无用部分
        time_month = re.findall(rules, str(os.path.split(path_modis)[-1]))[0]  # 提取Cloud文件时间
        # 获取所有Cloud文件路径
        path_yun_month_list = get_file_yun(f'{path_Cloud}/{time_month}/')
        for path_yun in path_yun_month_list:
            data_Cloud = Dataset(path_yun)  # 读取Cloud数据
            Dataset.set_auto_mask(data_Cloud, False)  # 解除mask
            # 读取Cloud数据变量
            CLTYPE_arr = data_Cloud['CLTYPE'][:]
            # 依据Cloud数据的时间，读取相应时间的卫星数据
            rule_Cloud = re.compile(r'NC_H08_(.*?)00_L2CLP010_FLDK.02401_02401.nc')  # 文件名中无用部分
            time = re.findall(rule_Cloud, str(os.path.split(path_yun)[-1]))[0]  # 提取Cloud文件时间
            path_Satellite_time_same_Cloud = f'{path_Satellite}/{time_month}/NC_H08_{time}00_R21_FLDK.06001_06001.nc'
            if os.path.exists(path_Satellite_time_same_Cloud):
                # 读取卫星数据
                data_Satellite = Dataset(path_Satellite_time_same_Cloud)
                Dataset.set_auto_mask(data_Satellite, False)
                # 将读取的PM2.5时间格式，转换为与ERA5格式相同(标准时间)，获取ERA5时间索引
                time_utc = time.replace('_', '')
                time_Cloud_to_ERA5 = datetime.strptime(str(time_utc), "%Y%m%d%H")
                time_ERA5_index = int(np.argwhere(time_ERA5 == time_Cloud_to_ERA5))  # 获取与PM2.5时间相同的ERA5的索引
                # 加载卫星数据属性
                SAA_arr = data_Satellite.variables['SAA'][:]
                SAZ_arr = data_Satellite.variables['SAZ'][:]
                SOA_arr = data_Satellite.variables['SOA'][:]
                SOZ_arr = data_Satellite.variables['SOZ'][:]
                TOAb1_arr = data_Satellite.variables['albedo_01'][:]
                TOAb2_arr = data_Satellite.variables['albedo_02'][:]
                TOAb3_arr = data_Satellite.variables['albedo_03'][:]
                TOAb4_arr = data_Satellite.variables['albedo_04'][:]
                TOAb5_arr = data_Satellite.variables['albedo_05'][:]
                TOAb6_arr = data_Satellite.variables['albedo_06'][:]
                # 读取PM数据
                time_bj = retime_utc_to_bj(path_yun)
                time_day = time_bj[:-2]
                data_PM = pd.read_csv(f'{path_PM}/{time_month}/china_sites_PM_{time_day}.csv')
                # 提取属性值
                index_pm = data_PM[data_PM.time == int(time_bj)].index.tolist()
                for i in index_pm:
                    # 获取时间相同的PM2.5经纬度
                    site_id = data_PM['site_id'][i]
                    # 获取这个站点的相应索引
                    Cloud_lat_index = data_PM['Cloud_lat_index'][i]
                    Cloud_lon_index = data_PM['Cloud_lon_index'][i]
                    AUX_H8_lat_index = data_PM['AUX_H8_lat_index'][i]
                    AUX_H8_lon_index = data_PM['AUX_H8_lon_index'][i]
                    ERA5_lat_index = data_PM['ERA5_lat_index'][i]
                    ERA5_lon_index = data_PM['ERA5_lon_index'][i]
                    NDVI_lat_index = data_PM['NDVI_lat_index'][i]
                    NDVI_lon_index = data_PM['NDVI_lon_index'][i]
                    # 获取CLTYPE值
                    CLTYPE = int(CLTYPE_arr[Cloud_lat_index, Cloud_lon_index])
                    if CLTYPE == 0:
                        # 提取经纬度坐标
                        lat = data_PM['latitude'][i]
                        lon = data_PM['longitude'][i]
                        # 提取pm2.5值
                        PM = data_PM['PM2.5'][i]
                        # 提取卫星数据
                        SAA = SAA_arr[AUX_H8_lat_index, AUX_H8_lon_index]
                        SAZ = SAZ_arr[AUX_H8_lat_index, AUX_H8_lon_index]
                        SOA = SOA_arr[AUX_H8_lat_index, AUX_H8_lon_index]
                        SOZ = SOZ_arr[AUX_H8_lat_index, AUX_H8_lon_index]
                        TOAb1 = TOAb1_arr[AUX_H8_lat_index, AUX_H8_lon_index]/np.cos(SOZ * math.pi / 180)
                        TOAb2 = TOAb2_arr[AUX_H8_lat_index, AUX_H8_lon_index]/np.cos(SOZ * math.pi / 180)
                        TOAb3 = TOAb3_arr[AUX_H8_lat_index, AUX_H8_lon_index]/np.cos(SOZ * math.pi / 180)
                        TOAb4 = TOAb4_arr[AUX_H8_lat_index, AUX_H8_lon_index]/np.cos(SOZ * math.pi / 180)
                        TOAb5 = TOAb5_arr[AUX_H8_lat_index, AUX_H8_lon_index]/np.cos(SOZ * math.pi / 180)
                        TOAb6 = TOAb6_arr[AUX_H8_lat_index, AUX_H8_lon_index]/np.cos(SOZ * math.pi / 180)
                        # 提取气象数据
                        V10 = 6.472245439708095E-4*V10_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]-2.1879227944008917
                        U10 = 7.22451843277552E-4*U10_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]-1.11798360140992
                        # WS = (V10 ** 2 + U10 ** 2) ** 0.5
                        BLH = 0.07730352840551938*BLH_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]+2541.3242861630433
                        ET = 1.5196842219541672E-8*ET_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]-4.563776624785195E-4
                        SP = 0.8459931446752018*SP_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]+76209.39340967766
                        PRE = 2.0922246268250585E-7*PRE_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]+0.006855383212254987
                        TEM = TEM_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]-273.15
                        Td = Td_arr[time_ERA5_index, ERA5_lat_index, ERA5_lon_index]-273.15
                        e = 6.112 * math.exp((17.67 * Td) / (Td + 243.5))
                        es = 6.112 * math.exp((17.67 * TEM) / (TEM + 243.5))
                        RH = 100.0 * (e / es)
                        # 提取辅助数据
                        NDVI = data_NDVI[NDVI_lat_index, NDVI_lon_index]/10000
                        DEM = DEM_arr[AUX_H8_lat_index, AUX_H8_lon_index]
                        LUCC = LUCC_arr[AUX_H8_lat_index, AUX_H8_lon_index]
                        # 写入数据到csv文件
                        writer.writerow(
                            [time_utc, lat, lon,
                            TOAb1, TOAb2, TOAb3, TOAb4, TOAb5, TOAb6, SAA, SAZ, SOA, SOZ,
                            V10, U10, BLH, ET, SP, PRE, TEM, RH,
                            DEM, LUCC, NDVI,
                            PM])  # 写入提取数据值
                data_Satellite.close()
            data_Cloud.close()
    data_ERA5.close()
    data_AUX.close()
    f.close()


if __name__ == '__main__':
    # 读取数据所在路径
    # start_time=time.time() # 开始时间
    
    path_ERA5 = 'C:/Users/Tiger/Desktop/ceshi/ERA5/2020_01.nc'
    path_AUX = 'C:/Users/Tiger/Desktop/ceshi/FUZHU/H8nc_AHI.NAV2kmv2.more.xxxxyanglk.hdf'
    path_Cloud = 'C:/Users/Tiger/Desktop/ceshi/Cloud'
    path_PM = 'C:/Users/Tiger/Desktop/ceshi/PM'
    path_Satellite = 'E:/data'
    path_NDVI = 'C:/Users/Tiger/Desktop/ceshi/NDVI'
    path_result = 'C:/Users/Tiger/Desktop/result_2020_01.csv'
    
    get_Value_to_csv(path_PM, path_Cloud, path_Satellite, path_ERA5, path_AUX, path_NDVI, path_result)

    # end_time=time.time()

    # print(end_time-start_time)

    # profile = line_profiler.LineProfiler(get_Value_to_csv)  # 把函数传递到性能分析器
    # profile.enable()  # 开始分析
    # get_Value_to_csv(path_index, path_PM, path_Cloud, path_Satellite, path_ERA5, path_AUX, path_NDVI, path_result)
    # profile.disable()  # 停止分析
    # profile.print_stats(sys.stdout)  # 打印出性能分析结果