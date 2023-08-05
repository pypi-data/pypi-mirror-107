import os
import sys
from testindatadev.TDA import TDA
import json

T_key = "1f25eddfeefc374a49e7c125341a6b3f"
ip = "http://10.10.32.54/"

tda = TDA(T_key, debug=True)

tda.Debug()

dataset = tda.SetDataset("ds_we2r3pqtdhz4nciurso3", ip)


dataDir = "/Users/hejinlong/Desktop/数据集测试数据/点云非融合数据/pcd"

for root, dirs, files in os.walk(dataDir):
    for filename in files:
        if filename.endswith(".pcd"):
            frame = filename.replace(".pcd", "")

            metaData = {
                "myfid": frame,
                "from": "DJ",
                "mykey": "test_" + frame
            }

            #标注结果
            jsonPath = os.path.join("/Users/hejinlong/Desktop/数据集测试数据/点云非融合数据/label", frame + ".json")
            with open(jsonPath) as rjf:
                markData = json.load(rjf)


            #添加点云文件
            pcdPath = os.path.join(root, filename)
            pcdFile = tda.AddFile(pcdPath, referId=frame + ".pcd", metaData=metaData)

            #点云添加标注结果
            for mark in markData["marks"]:
                box3d = {
                    "position": {
                        "x": mark["position"]["x"],
                        "y": mark["position"]["y"],
                        "z": mark["position"]["z"],
                    },
                    "scale": {
                        "x": mark["scale"]["x"],
                        "y": mark["scale"]["y"],
                        "z": mark["scale"]["z"],
                    },
                    "rotation": {
                        "x": mark["rotation"]["x"],
                        "y": mark["rotation"]["y"],
                        "z": mark["rotation"]["z"],
                    }
                }

                label = mark["property"][0][0]["ptitle"]
                instance = mark["objectId"]

                attr = {
                    "type":mark["property"][0][0]["ptitle"],
                    "carried":mark["property"][1][1]["ptitle"],
                    "lied":mark["property"][1][3]["ptitle"],
                    "crowd":mark["property"][1][5]["ptitle"],
                }


                pcdFile.AddBox3D(box3d, label=label, instance=instance, attrs=attr)


print(tda.Upload())
