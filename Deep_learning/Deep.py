# 导入所需库
import tensorflow as tf
import numpy as np
import pandas as pd

# 导入数据集
# 列标签
LABEL_COLUMN = 'PM'

def get_dataset(file_path):
    dataset = tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size=12,
        label_name=LABEL_COLUMN,
        na_value='?',
        num_epochs=1,
        ignore_errors=True
    )
    return dataset

raw_train_data = get_dataset(train_file_path)
df_train = pd.read_csv('C:/Users/Tiger/Desktop/result_2020_01.csv')
features_cols = ['TOAb1', 'TOAb2', 'TOAb3', 'TOAb4', 'TOAb5', 'TOAb6', 'SAA', 'SAZ', 'SOA', 'SOZ', 'V10', 'U10', 'BLH',
                 'ET', 'SP', 'PRE', 'TEM', 'RH', 'DEM', 'LUCC', 'NDVI']
x_tranin = df_train.loc[:, features_cols]
y_train = df_train.PM

# 定义模型
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=()),
    tf.keras.layers.Dense(1, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

# 训练模型

# 参数提取、acc/loss可视化、前向推理实现应用
