# %%
import scipy.io as sio
import torch
import numpy

# %%
# lib_py = sio.loadmat("lib_py.mat", squeeze_me=True)['lib_py']


# %%
def convert_object_to_tensor(x):
    return torch.tensor(x.item())

def convert_to_dict_of_tensors(x):
    ret = {}
    keys = x.dtype.names
    for key in keys:
        ret[key] = convert_object_to_tensor(x[key])
    return ret

# %%
def process_mat(x):
    # print(type(x))
    if type(x) != numpy.ndarray:
        return x
    keys = x.dtype.names
    if keys is None:
        return x
    # print(list(keys))
    if keys[0] == "cell1": # TODO
        ret = []
        for key in keys:
            # print(key)
            ret.append(process_mat(x[key].item()))
    else:
        ret = {}
        for key in keys:
            # print(key)
            ret[key] = process_mat(x[key].item())
    return ret

G_py = sio.loadmat("G/35G.mat", squeeze_me=True)['G']
G = process_mat(G_py)