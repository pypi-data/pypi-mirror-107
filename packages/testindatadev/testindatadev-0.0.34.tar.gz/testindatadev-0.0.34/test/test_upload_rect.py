import os
import json

from testindatadev.TDA import TDA

#初始化TDA
#测试
T_key = "9e819cc1596ab3a3789443f15b60135d"
ip = "10.10.32.54"

#本地
# T_key = "0fbe149adf07e5f4afa01a7a4e787fde"
# ip = "10.32.144.73"

tda = TDA(T_key)
tda.SetDataset("ds_r2pi8jxrvhiwjl-l13pp", ip)

#单纯上传数据, 仅上传pcd文件，不填表示上传任何文件
# print(tda.UploadFilesToDataset("/Users/hejinlong/Desktop/毫末", ext=".pcd"))

#上传单个文件
# print(tda.UploadFileToDataset("/Users/hejinlong/Desktop/毫末/pcds/1614562848500000.pcd", basePath="/Users/hejinlong/Desktop/毫末/pcds/"))


#传可视化数据
local_file_path = "/Users/hejinlong/Desktop/数据集测试数据/拉框"
for root, dirs, files in os.walk(local_file_path):
    for filename in files:
        if filename.endswith(".jpg"):

            #文件路径
            pic_file_path = os.path.join(root, filename)

            file = tda.AddFile(pic_file_path, "/Users/hejinlong/Desktop/数据集测试数据/拉框")
            # file = tda.AddFile(pic_file_path)
            file.AddReferId(filename)
            #添加matadata
            file.AddmetaData({
                "myfid":filename,
                "mykey":"myvalue"
            })


            #添加标注结果
            json_path = "/".join([item for item in pic_file_path.split("/")[:-2]]) + "/json/" + filename.replace(".jpg", ".json")
            with open(json_path, "r", encoding="utf-8") as jf:
                jsonData = json.load(jf)
                for mark in jsonData["marks"]:
                    bbox = mark["bbox"]
                    box = {
                        "x": bbox["xmin"],
                        "y": bbox["ymin"],
                        "width": bbox["xmax"] - bbox["xmin"],
                        "height": bbox["ymax"] - bbox["ymin"],
                    }

                    file.AddBox2D(box, label=mark["name"], attrs={"post":mark["post"], "angle":mark["post"]})

# commit 到某个版本
commit = tda.Commit()
print(tda.Upload(commit))

# print(tda.Upload())

