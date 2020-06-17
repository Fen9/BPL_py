# %%
import scipy.io as sio
import torch

lib_py = sio.loadmat("lib_py.mat", squeeze_me=True)['lib_py']

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
# [n x 1] probability of each number of strokes (starts at 1)
pkappa = convert_object_to_tensor(lib_py['pkappa'])

# number of control points
ncpt = convert_object_to_tensor(lib_py['ncpt'])

# relations
rel = convert_to_dict_of_tensors(lib_py['rel'].item())

# P(n_i | \kappa)
pmat_nsub = convert_object_to_tensor(lib_py['pmat_nsub'])

# .sigma_shape,sigma_invscale
tokenvar = convert_to_dict_of_tensors(lib_py['tokenvar'].item())

# [N x 1] log-prob of beginning in each state
logStart = convert_object_to_tensor(lib_py['logStart'])

# %% the cell arrays in matlab can be accessed "cell" + index
test_cell = lib_py['Spatial'].item()['list_SH'].item()['cell1'].item()['logpYX'].item()