import os
import json

from testindatadev.TDA import TDA

#获取数据测试代码

#初始化TDA
T_key = "0fbe149adf07e5f4afa01a7a4e787fde"
tda = TDA(T_key)
tda.SetDataset("ds__tq1wnhun2oged8tbsjy", "10.32.141.220")

#获取数据
# print(tda.GetData())
print(tda.GetData(offset=8, limit=9))#分页查询

#获取数据及标注结果
# print(tda.GetFileAndLabel(fid="fs_uZI662vd-f7UwA-8VK_1"))#根据fid
# print(tda.GetFileAndLabel(fid="fs_N7T02AgYJGF6yxAbk75R"))#根据fid
# print(tda.GetFileAndLabel(ref_id="104.jpg"))#根据ref_id







