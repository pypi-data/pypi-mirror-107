from testindatadev.TDA import TDA
import sys
import os
import json

accessKey = "bb76998774f7c1347fe347369a4ed470"
host = ""
ds = "ds_34j5zqkn9xqfotjoda-7"

tda = TDA(accessKey, host=host)
tda.Debug()
tda.SetDataset(ds)

path = "/Users/hejinlong/Desktop/数据集测试数据/图像/多边形/pic"

i = 0
for root, dirs, files in os.walk(path):
    for filename in files:
        if filename.endswith(".jpg"):
            filepath = os.path.join(root, filename)
            jsonPath = os.path.join("/Users/hejinlong/Desktop/数据集测试数据/图像/多边形/json", filename + ".json")

            file = tda.AddFile(filepath)

            with open(jsonPath) as jf:
                jsonData = json.load(jf)

                polygonArr = []
                for mark in jsonData["marks"]:
                    polygonArr.append(mark)
                polygonArr.reverse()

                index = 0
                for mark in polygonArr:
                    if mark["type"] == "polygon":
                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }
                        index += 1
                        file.AddPolygon(mark["point"], label=mark["property"][0][0]["ptitle"], attrs=attr, index=index)


print(tda.Upload())
