from testindatadev.TDA import TDA
import sys
import os
import json

accessKey = "10872f411df14100045a24964d15d815"
host = "10.10.32.54"
ds = "ds_nqtpzio8p7qloyjvjl7g"

tda = TDA(accessKey, host=host)
tda.Debug()
tda.SetDataset(ds)

file = tda.AddUrlFile(url="https://desk-fd.zol-img.com.cn/t_s208x130c5/g6/M00/07/07/ChMkKWCcnHmIYdYhACzayVLYQEUAAOv8AOO2d0ALNrh047.jpg", referId="1", metaData={"key":"v"}, md5="234234", filesize=10, filename="aaa.jpg")

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

tda.Upload()
