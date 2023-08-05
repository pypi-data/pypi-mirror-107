from testindatadev.TDA import TDA
import sys
import os
import json
#
# T_key = "0fbe149adf07e5f4afa01a7a4e787fde"
# ip = "10.32.141.220"
# ds = "ds_ihtxzc_uhocslt4fjhrc"

T_key = "492535c229015dcd8de80e2ad64c299b"
ip = "10.10.32.54"
ds = "ds_iilbqah_e38vou0mdd4o"


tda = TDA(T_key)
tda.Debug()
dataset = tda.SetDataset(ds, ip)

# #分页更新
# page = 0
# limit = 100
# i = 0
# while True:
#     offset = page * limit
#     page += 1
#     fileData = tda.GetData(offset, limit)
#     if len(fileData["files"]) <= 0:
#         break
#
#     print(fileData.keys())
#     exit()

    #
    # for file in fileData["files"]:
    #     print(file)
    #     exit()
#         i += 1
#         box = {
#             "x": 10,
#             "y": 10,
#             "width": 100,
#             "height": 100,
#         }
#         file.AddBox2D()
#         print(file.Update())
#         print(i)
#         print(file.fid)
#

#根据fid或者referid更新
file = tda.GetFileAndLabel(fid="fs_y0V4FFBTpvt-y5t2mz_H")

# print(file.ToList())

# print(file.anotations.labels)
# print(file.fid)
# print(file.referId)
# print(file.meta)
# print(file.md5)
# print(file.path)


# file.Update()
# exit()

#新增标注结果

file.referId = "test_refer_id"
file.metaData = {
    "key1":"test_val"
}

file.name = "23333.jpg"

file.sensor = "camera_1"
file.frameId = "test_frame_id"

box = {
    "x": 10,
    "y": 10,
    "width": 100,
    "height": 100,
}

label = "myTestLabelName"

attr = {
    "attrKey1":"attrVal1",
    "attrKey2":"attrVal2",
    "attrKey3":"attrVal3",
}

file.AddBox2D(box, label=label, attrs=attr)

print(file.Update())
