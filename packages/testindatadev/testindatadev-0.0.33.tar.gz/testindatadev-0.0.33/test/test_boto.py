from testindatadev.TDA import TDA

T_key = "cbf567048e4685fe5ad445d16fc534a2"
ip = "127.0.0.1"
ds = "ds_iz1e9nqnxxiqh75no2z2"


tda = TDA(T_key)
dataset = tda.SetDataset(ds, ip)


files = dataset.client.ListObjects("youshu", recursive=True)

for file in files:
    print(file)
