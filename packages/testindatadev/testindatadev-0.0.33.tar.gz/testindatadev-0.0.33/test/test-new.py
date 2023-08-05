from testindatadev.TDA import TDA
T_key = "cbf567048e4685fe5ad445d16fc534a2"
host = "127.0.0.1"
ds = "ds_0cyeyhrqkqumaq9h_hkq"

tda = TDA(T_key, host=host)
tda.Debug()
dataset = tda.SetDataset(ds)

objectName = "test1/test122/test3/a.jpg"

tda.A(objectName=objectName, filePath="/Users/hejinlong/Desktop/1.png")

