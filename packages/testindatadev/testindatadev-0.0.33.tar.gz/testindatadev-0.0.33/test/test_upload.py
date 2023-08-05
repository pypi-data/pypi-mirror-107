from testindatadev.TDA import TDA

T_key = "bb76998774f7c1347fe347369a4ed470"
host = "https://dataset.testin.cn/"
ds = "ds_i-dvsho2htj4bav4obsp"


# T_key = "cbf567048e4685fe5ad445d16fc534a2"
# ip = "127.0.0.1"
# ds = "ds_0cyeyhrqkqumaq9h_hkq"


tda = TDA(T_key, host, debug=True)
tda.Debug()

dataset = tda.SetDataset(ds)

metaData = {
    "metaKey1":"metaVal1",
    "metaKey2":"metaVal2",
    "metaKey3":"metaVal3",
}

file = tda.AddFile("/Users/hejinlong/Desktop/test_pic/11.jpg", referId="myTestRefId", metaData=metaData)

# box = {
#     "x": 10,
#     "y": 10,
#     "width": 100,
#     "height": 100,
# }
#
# label = "myTestLabelName"
#
# attr = {
#     "attrKey1":"attrVal1",
#     "attrKey2":"attrVal2",
#     "attrKey3":"attrVal3",
# }
#
# file.AddBox2D(box, label=label, attrs=attr)

print(tda.Upload())
