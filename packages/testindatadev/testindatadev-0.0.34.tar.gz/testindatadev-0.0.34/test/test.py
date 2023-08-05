from testindatadev.TDA import TDA

# T_key = "bb76998774f7c1347fe347369a4ed470"
# ds = "ds_lvsq4xd2obicciiwf6nk"
#
#
# tda = TDA(T_key)
# tda.Debug()
# dataset = tda.SetDataset(ds)
#
# print(dataset)


T_key = "492535c229015dcd8de80e2ad64c299b"
host = "10.10.32.54"
ds = "ds_iilbqah_e38vou0mdd4o"


tda = TDA(T_key, host=host)
tda.Debug()
tda.SetDataset(ds)

file = tda.GetFileAndLabel(fid="fs_y0V4FFBTpvt-y5t2mz_H")

file.Update()
