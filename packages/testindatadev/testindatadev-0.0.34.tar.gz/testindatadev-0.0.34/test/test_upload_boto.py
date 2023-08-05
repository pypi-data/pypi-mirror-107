import os
import json

from testindatadev.TDA import TDA

#aws测试

#初始化TDA
#测试
# T_key = "1f25eddfeefc374a49e7c125341a6b3f"
# ip = "10.10.32.54"

#本地
T_key = "0fbe149adf07e5f4afa01a7a4e787fde"
ip = "10.32.143.63"

tda = TDA(T_key, True)
tda.SetDataset("ds_7_hxflkjegen8hmucubk", ip)

# 传可视化数据
local_file_path = "/Users/hejinlong/Desktop/数据集测试数据/全工具"
for root, dirs, files in os.walk(local_file_path):
    for filename in files:
        if filename.endswith(".jpg"):

            #文件路径
            pic_file_path = os.path.join(root, filename)
            json_file_path = pic_file_path.replace("/pic/", "/json/") + ".json"
            toolType = json_file_path.split("/")[6]


            file = tda.AddFile(pic_file_path, "/Users/hejinlong/Desktop/数据集测试数据/全工具")
            # file = tda.AddFile(pic_file_path)
            file.AddReferId(filename)
#             #添加matadata
            file.AddmetaData({
                "myfid":filename,
                "toolType":toolType,
                "originPath":pic_file_path
            })

            index = 0
            with open(json_file_path, "r", encoding="utf-8") as jf:
                jsonData = json.load(jf)
                if "marks" not in jsonData.keys():
                    file.AddmetaData({
                        "myfid": filename,
                        "toolType": toolType,
                        "originPath": pic_file_path,
                        "markable":False
                    })
                    continue

                for mark in jsonData["marks"]:
                    if mark["type"] == "cuboid":
                        sideCuboid = {
                            "back":[
                                {
                                    "x":mark["finshPoints"][2]["x"],
                                    "y":mark["finshPoints"][2]["y"],
                                },
                                {
                                    "x":mark["finshPoints"][3]["x"],
                                    "y":mark["finshPoints"][3]["y"],
                                },
                            ],
                            "front":[
                                # mark["point"][0], mark["point"][1], mark["point"][2], mark["point"][3]
                                {
                                    "x":mark["finshPoints"][0]["x"],
                                    "y":mark["finshPoints"][0]["y"],
                                },
                                {
                                    "x":mark["finshPoints"][1]["x"],
                                    "y":mark["finshPoints"][0]["y"],
                                },
                                {
                                    "x":mark["finshPoints"][1]["x"],
                                    "y":mark["finshPoints"][1]["y"],
                                },
                                {
                                    "x":mark["finshPoints"][0]["x"],
                                    "y":mark["finshPoints"][1]["y"],
                                }
                            ]
                        }

                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }

                        file.AddSideCuboid(sideCuboid, label=mark["property"][0][0]["ptitle"], attrs=attr)
                    elif mark["type"] == "curve":
                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }

                        file.AddCurve(mark["point"], label=mark["property"][0][0]["ptitle"], attrs=attr)
                    elif mark["type"] == "point":
                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }

                        file.AddPoint(mark["point"], label=mark["property"][0][0]["ptitle"], attrs=attr)
                    elif mark["type"] == "polygon":
                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }
                        index += 1
                        file.AddPolygon(mark["point"], label=mark["property"][0][0]["ptitle"], attrs=attr, index=index)
                    elif mark["type"] == "rect":
                        box = {
                            "x": mark["point"]["left"],
                            "y": mark["point"]["top"],
                            "width": mark["point"]["right"] - mark["point"]["left"],
                            "height": mark["point"]["bottom"] - mark["point"]["top"],
                        }

                        attr = {
                            "type":mark["property"][0][0]["ptitle"],
                            "pname":mark["property"][0][0]["pname"],
                            "pselect":mark["pselect"],
                        }

                        file.AddBox2D(box, label=mark["property"][0][0]["ptitle"], attrs=attr)
                    elif mark["type"] == "ellipse":
                        box = {
                            "x": mark["point"]["left"],
                            "y": mark["point"]["top"],
                            "width": mark["point"]["right"] - mark["point"]["left"],
                            "height": mark["point"]["bottom"] - mark["point"]["top"],
                        }

                        attr = {
                            "type":mark["property"][0][0]["ptitle"],
                            "pname":mark["property"][0][0]["pname"],
                            "pselect":mark["pselect"],
                        }

                        file.AddEllipse(box, label=mark["property"][0][0]["ptitle"], attrs=attr)
                    elif mark["type"] == "line":
                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }
                        index += 1
                        file.AddLine(mark["point"], label=mark["property"][0][0]["ptitle"], attrs=attr)
                    elif mark["type"] == "3drect":
                        cuboid = {
                            "back":mark["back"],
                            "front":mark["front"]
                        }
                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }
                        index += 1
                        file.AddCuboid(cuboid, label=mark["property"][0][0]["ptitle"], attrs=attr)
                    elif mark["type"] == "parallel":
                        attr = {
                            "type": mark["property"][0][0]["ptitle"],
                            "pname": mark["property"][0][0]["pname"],
                            "pselect": mark["pselect"],
                        }
                        index += 1
                        file.AddParallel(mark["point"], label=mark["property"][0][0]["ptitle"], attrs=attr)
                    else:
                        print("未知工具：" + mark["type"])
                        exit()

commit = tda.Commit()
print(tda.Upload(commit))

# print(tda.Upload("6eqv8g0nxibth2c7y3sjfu1l95d4worp"))

