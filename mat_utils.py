# %%
import scipy.io as sio
import torch
import numpy as np
from motor_program.motor_program import motor_program
import copy

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
    if type(x) != np.ndarray:
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


def load_mat_G(path):
    G = sio.loadmat(path, squeeze_me=True)['G']
    G = process_mat(G)
    out_G = {}
    
    for k in G:
        out_G[k] = None
    
    out_G['scores'] = np.array(G['scores'])
    out_G['img'] = G['img']
    out_G['PM'] = G['PM']

    out_G['models'] = []
    for i in range(len(G['models'])):
        out_G['models'].append(motor_program(0))
        out_G['models'][i]._I = copy.deepcopy(G['models'][i]['I'])
        out_G['models'][i]._fixed_parameter= copy.deepcopy(G['models'][i]['parameters'])
        out_G['models'][i]._epsilon= copy.deepcopy(G['models'][i]['epsilon'])
        out_G['models'][i]._blur_sigma = copy.deepcopy(G['models'][i]['blur_sigma'])
        out_G['models'][i]._affine_transformation = np.array(copy.deepcopy(G['models'][i]['A']))
        out_G['models'][i]._num_strokes = copy.deepcopy(G['models'][i]['ns'])
        out_G['models'][i]._prob_img = copy.deepcopy(G['models'][i]['pimg'])
        out_G['models'][i]._ink_off_page = copy.deepcopy(G['models'][i]['ink_off_page'])

        out_G['models'][i]._motor = []
        for j in range(len(G['models'][i]['motor'])):
            out_G['models'][i]._motor.append([G['models'][0]['motor'][j][0]['val']])

        out_G['models'][i]._motor = []
        for j in range(len(G['models'][i]['motor_warped'])):
            out_G['models'][i]._motor_warped.append([G['models'][0]['motor_warped'][j][0]['val']])

        out_G['models'][i]._cache_grant_curent = copy.deepcopy(G['models'][i]['ink_off_page'])
    
        out_G['models'][i]._stroke = # todo
        
    return out_G

if __name__ == "__main__":
    G_py = sio.loadmat("./model/G/35G.mat", squeeze_me=True)['G']
    G = process_mat(G_py)
    load_mat_G("./model/G/35G.mat")
    print((G['models'][0]['motor'][0][0]['val']))
    print(len(G['models'][0]['motor']))

