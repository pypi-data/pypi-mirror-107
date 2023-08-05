import os
import sys
from testindatadev.TDA import TDA
import json

T_key = "1f25eddfeefc374a49e7c125341a6b3f"
ip = "http://10.10.32.54/"

tda = TDA(T_key, debug=True)

tda.Debug()

dataset = tda.SetDataset("ds_yrm_rtwsoih1j45d5dqh", ip)


dataDir = "/Users/hejinlong/Desktop/数据集测试数据/点云"

camTrans = {
    "image_0":"camera_0",
    "image_11":"camera_1",
    "image_13":"camera_2",
    "image_2":"camera_3",
    "image_4":"camera_4",
    "image_7":"camera_5",
    "image_9":"camera_6",
}

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
            jsonPath = os.path.join("/Users/hejinlong/Desktop/数据集测试数据/点云/label", frame + ".json")
            with open(jsonPath) as rjf:
                markData = json.load(rjf)


            #添加点云文件
            pcdPath = os.path.join(root, filename)
            pcdFile = tda.AddFile(pcdPath, referId=frame + ".pcd", metaData=metaData, frameId=frame, sensor="pointcloud")

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

            # 添加图片image_0
            for img, cam in camTrans.items():
                imgPath = os.path.join("/Users/hejinlong/Desktop/数据集测试数据/点云/" + img, frame + ".jpg")
                imgFile = tda.AddFile(imgPath, referId=img + "/" + frame + ".jpg", metaData=metaData, frameId=frame, sensor=cam)

                for mark in markData["cameraMarks"][img]:
                    box = {
                        "x": mark["point"]["left"],
                        "y": mark["point"]["top"],
                        "width": mark["point"]["right"] - mark["point"]["left"],
                        "height": mark["point"]["bottom"] - mark["point"]["top"],
                    }

                    label = mark["property"][0][0]["ptitle"]
                    instance = mark["objectId"]

                    attr = {
                        "type": mark["property"][0][0]["ptitle"],
                        "carried": mark["property"][1][1]["ptitle"],
                        "lied": mark["property"][1][3]["ptitle"],
                        "crowd": mark["property"][1][5]["ptitle"],
                    }

                    imgFile.AddBox2D(box, label=label, instance=instance, attrs=attr)
print(tda.Upload())
