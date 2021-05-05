import pandas as pd
import numpy as np
from netCDF4 import Dataset
from osgeo import osr
from osgeo import gdal


def get_YUN_lat_index_from_Parallel_lonlat(x):
    # 经纬度边界值
    lat_up = 60
    # 单元格大小
    Unit_lat = 0.05
    if x['latitude'] != '-':
        # 行列号
        lat_PM = float(np.array(x['latitude']))
        YUN_lat_index = int((lat_up - lat_PM) / Unit_lat)
    # 返回行列号对应的像素值
        return YUN_lat_index


def get_YUN_lon_index_from_Parallel_lonlat(x):
    # 经纬度边界值
    lon_left = 80  
    # 单元格大小
    Unit_lon = 0.05
    # 行列号
    if x['longitude'] != '-':
        lon_PM = float(np.array(x['longitude']))
        YUN_lon_index = int((lon_PM - lon_left) / Unit_lon)  # 经度方向
        # 返回行列号对应的像素值
        return YUN_lon_index


def get_AUX_H8_lat_index_from_Parallel_lonlat(x):
    # 经纬度边界值
    lat_up = 60.0  # lat_arr.max()
    # 单元格大小
    Unit_lat = 0.02
    # 行列号
    if x['latitude'] != '-':
        lat_PM = float(np.array(x['latitude']))
        AUX_H8_lat_index = int((lat_up - lat_PM) / Unit_lat)
        return AUX_H8_lat_index


def get_AUX_H8_lon_index_from_Parallel_lonlat(x):
    # 经纬度边界值
    lon_left = 80.0  # lon_arr.min()
    # 单元格大小
    Unit_lon = 0.02
    # 行列号
    if x['longitude'] != '-':
        lon_PM = float(np.array(x['longitude']))
        AUX_H8_lon_index = int((lon_PM - lon_left) / Unit_lon)  # 经度方向
        return AUX_H8_lon_index


def get_ERA5_lat_index_from_Parallel_lonlat(x):
    # 经纬度边界值
    lat_up = 60  # lat_arr.max()
    # 单元格大小
    Unit_lat = 0.25
    # 行列号
    if x['latitude'] != '-':
        lat_PM = float(np.array(x['latitude']))
        ERA5_lat_index = int((lat_up - lat_PM) / Unit_lat)
        # 返回行列号对应的像素值
        return ERA5_lat_index


def get_ERA5_lon_index_from_Parallel_lonlat(x):
    # 经纬度边界值
    lon_left = 80  # lon_arr.min()
    # 单元格大小
    Unit_lon = 0.25
    if x['longitude'] != '-':
        # 行列号
        lon_PM = float(np.array(x['longitude']))
        ERA5_lon = int((lon_PM - lon_left) / Unit_lon)  # 经度方向
        return ERA5_lon

# 读取数据
file_path = 'C:/Users/Tiger/Desktop/ceshi/NDVI/MOD13A3.A202001.only_NDVI.tif'
dataset = gdal.Open(file_path)
pcs = osr.SpatialReference()
pcs.ImportFromWkt(dataset.GetProjection())
gcs = pcs.CloneGeogCS()
extend = dataset.GetGeoTransform()
shape = (dataset.RasterXSize, dataset.RasterYSize)
# 经纬度转投影坐标
ct = osr.CoordinateTransformation(gcs, pcs)
def get__lon_lat_index_from_WG84(x):
    # 读取数据
    file_path = ''
    dataset = gdal.Open(file_path)
    psc = osr.SpatialReference()
    gcs = data_srs.CloneGeogCS()
    extend = dataset.GetGeoTransform()
    shape = (dataset.RasterXSize, dataset.RasterYSize)
    # 经纬度转投影坐标
    ct = osr.CoordinateTransformation(gcs, psc)
    coordinates = ct.TransformPoint(lon, lat)
    x = coordinates[0]
    y = coordinates[1]
    # 投影坐标转行列号
    a = np.array([[extend[1], extend[2]], [extend[4], extend[5]]])
    b = np.array([x - extend[0], y - extend[3]])
    row_col = np.linalg.solve(a, b)
    row = int(np.floor(row_col[1]))
    col = int(np.floor(row_col[0]))


def get_lon_to_index_from_WGS84(x_):
    if x_['longitude'] != '-':
        x_ = float(np.array(x_['longitude']))
        lat = 30
        coordinates = ct.TransformPoint(x_, lat)
        x = coordinates[0]
        y = coordinates[1]
        # 投影坐标转行列号
        a = np.array([[extend[1], extend[2]], [extend[4], extend[5]]])
        b = np.array([x - extend[0], y - extend[3]])
        row_col = np.linalg.solve(a, b)
        col = int(np.floor(row_col[0]))
        return col


def get_lat_to_index_from_WGS84(x_):
    if x_['latitude'] != '-':
        x_ = float(np.array(x_['latitude']))
        lon = 100
        coordinates = ct.TransformPoint(lon, x_)
        x = coordinates[0]
        y = coordinates[1]
        # 投影坐标转行列号
        a = np.array([[extend[1], extend[2]], [extend[4], extend[5]]])
        b = np.array([x - extend[0], y - extend[3]])
        row_col = np.linalg.solve(a, b)
        row = int(np.floor(row_col[1]))
        return row


def Extaction_site_index(path_site, path_out):
    # 读取站点列表文件
    df = pd.read_excel(path_site)
    # 除去不需要的列
    df = df.drop(['监测点名称', '城市', '对照点'], axis=1)  
    # 去除含有 - 的行
    df = df[~df['latitude'].isin(['-'])]
    df = df[~df['latitude'].isin(['-'])]
    # 将经纬度列转为float
    df[['latitude']] = df[['latitude']].astype(float)
    df[['longitude']] = df[['longitude']].astype(float)
    # 选取经纬度范围
    df = df.loc[(80 < df["longitude"]) & (df["longitude"] < 180), :]
    df = df.loc[(0 < df["latitude"]) & (df["longitude"] < 160), :]
    # 计算各站点对应于各个数据的索引
    df.loc[:, 'Cloud_lat_index'] = df.apply(get_YUN_lat_index_from_Parallel_lonlat, axis=1)
    df.loc[:, 'Cloud_lon_index'] = df.apply(get_YUN_lon_index_from_Parallel_lonlat, axis=1)
    df.loc[:, 'AUX_H8_lat_index'] = df.apply(get_AUX_H8_lat_index_from_Parallel_lonlat, axis=1)
    df.loc[:, 'AUX_H8_lon_index'] = df.apply(get_AUX_H8_lon_index_from_Parallel_lonlat, axis=1)
    df.loc[:, 'ERA5_lat_index'] = df.apply(get_ERA5_lat_index_from_Parallel_lonlat, axis=1)
    df.loc[:, 'ERA5_lon_index'] = df.apply(get_ERA5_lon_index_from_Parallel_lonlat, axis=1)
    df.loc[:, 'NDVI_lat_index'] = df.apply(get_lat_to_index_from_WGS84, axis=1)
    df.loc[:, 'NDVI_lon_index'] = df.apply(get_lon_to_index_from_WGS84, axis=1)
    # 除去重复站点
    df = df.drop_duplicates(['site_id'])
    # 输出为csv文件
    df.to_csv(path_out, index=False)
    

if __name__ == '__main__':
    path_site = 'C:/Users/Tiger/Desktop/BiShe/Data/PM2.5/Original/site_list_2021.01.01.xlsx'
    path_out = 'C:/Users/Tiger/Desktop/site_index.csv'
    Extaction_site_index(path_site, path_out)
