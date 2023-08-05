from testindatadev.TDA import TDA
import sys
import os
import json

accessKey = "cbf567048e4685fe5ad445d16fc534a2"
host = "127.0.0.1"
ds = "ds_vixwaog54ckpmov_t4vm"

tda = TDA(accessKey, host=host)
tda.Debug()
tda.SetDataset(ds)

files = tda.GetData()

i = 0
for file in files["files"]:
    i += 1
    file.referId = i
    print(file.Update())

