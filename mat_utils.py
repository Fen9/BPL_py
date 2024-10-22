# %%
import scipy.io as sio
import torch
import numpy as np
from motor_program.motor_program import motor_program
from stroke.stroke import stroke
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
    
    out_G['scores'] = copy.deepcopy(np.array(G['scores']))
    out_G['img'] = copy.deepcopy(G['img'])
    out_G['PM'] = copy.deepcopy(G['PM'])

    out_G['models'] = []
    for i in range(len(G['models'])):
        out_G['models'].append(motor_program(0))
        out_G['models'][i]._I = copy.deepcopy(G['models'][i]['I'])
        out_G['models'][i]._fixed_parameters= copy.deepcopy(G['models'][i]['parameters'])
        out_G['models'][i]._epsilon= copy.deepcopy(G['models'][i]['epsilon'])
        out_G['models'][i]._blur_sigma = copy.deepcopy(G['models'][i]['blur_sigma'])
        out_G['models'][i]._affine_transformation = np.array(copy.deepcopy(G['models'][i]['A']))
        out_G['models'][i]._num_strokes = copy.deepcopy(G['models'][i]['ns'])
        out_G['models'][i]._prob_img = copy.deepcopy(G['models'][i]['pimg'])
        out_G['models'][i]._ink_off_page = copy.deepcopy(G['models'][i]['ink_off_page'])

        out_G['models'][i]._motor = []
        for j in range(len(G['models'][i]['motor'])):
            out_G['models'][i]._motor.append([])
            for k in range(len(G['models'][i]['motor'][j])):
                out_G['models'][i]._motor[j].append(copy.deepcopy(G['models'][i]['motor'][j][k]['val']))

        out_G['models'][i]._motor_warped = []
        for j in range(len(G['models'][i]['motor_warped'])):
            out_G['models'][i]._motor_warped.append([])
            for k in range(len(G['models'][i]['motor_warped'][j])):
                out_G['models'][i]._motor_warped[j].append(copy.deepcopy(G['models'][i]['motor_warped'][j][k]['val']))

        out_G['models'][i]._cache_grant_curent = copy.deepcopy(G['models'][i]['ink_off_page'])
    
        out_G['models'][i]._strokes = []
        for j in range(0, len(G['models'][i]['S'])):
            s = stroke()
            # print(G['models'][i]['S'][j].keys())
            s._my_type = copy.deepcopy(G['models'][i]['S'][j]['myType'])
            # s._lh = copy.deepcopy(G['models'][i]['S'][j]['lh'])
            s._R = copy.deepcopy(G['models'][i]['S'][j]['R'])
            s._ids = copy.deepcopy(G['models'][i]['S'][j]['ids'])
            s._invscales_type = copy.deepcopy(G['models'][i]['S'][j]['invscales_type'])
            s._shapes_type = copy.deepcopy(G['models'][i]['S'][j]['shapes_type'])
            s._pos_token = copy.deepcopy(G['models'][i]['S'][j]['pos_token'])
            s._invscale_token = copy.deepcopy(G['models'][i]['S'][j]['invscales_token'])
            s._shapes_token = copy.deepcopy(G['models'][i]['S'][j]['shapes_token'])
            s._nsub = copy.deepcopy(G['models'][i]['S'][j]['nsub'])

            s._motor = []
            for k in range(len(G['models'][i]['S'][j]['motor'])):
                s._motor.append(copy.deepcopy(G['models'][i]['S'][j]['motor'][k]['val']))
            s._motor_spline = copy.deepcopy(G['models'][i]['S'][j]['motor_spline'])
            out_G['models'][i]._strokes.append(s)

    out_G['samples_type'] = []
    for m in range(0, len(G['samples_type'])):
        out_G['samples_type'].append([])
        for i in range(0, len(G['samples_type'][m])):
            # print("m = ", m, "i = ", i)
            out_G['samples_type'][m].append(motor_program(0))
            out_G['samples_type'][m][i]._I = copy.deepcopy(G['samples_type'][m][i]['I'])
            out_G['samples_type'][m][i]._fixed_parameters = copy.deepcopy(G['samples_type'][m][i]['parameters'])
            out_G['samples_type'][m][i]._epsilon= copy.deepcopy(G['samples_type'][m][i]['epsilon'])
            out_G['samples_type'][m][i]._blur_sigma = copy.deepcopy(G['samples_type'][m][i]['blur_sigma'])
            out_G['samples_type'][m][i]._affine_transformation = np.array(copy.deepcopy(G['samples_type'][m][i]['A']))
            out_G['samples_type'][m][i]._num_strokes = copy.deepcopy(G['samples_type'][m][i]['ns'])
            out_G['samples_type'][m][i]._prob_img = copy.deepcopy(G['samples_type'][m][i]['pimg'])
            out_G['samples_type'][m][i]._ink_off_page = copy.deepcopy(G['samples_type'][m][i]['ink_off_page'])

            out_G['samples_type'][m][i]._motor = []
            for j in range(len(G['samples_type'][m][i]['motor'])):
                out_G['samples_type'][m][i]._motor.append([])
                for k in range(len(G['samples_type'][m][i]['motor'][j])):
                    out_G['samples_type'][m][i]._motor[j].append(copy.deepcopy(G['samples_type'][m][i]['motor'][j][k]['val']))

            out_G['samples_type'][m][i]._motor_warped = []
            for j in range(len(G['samples_type'][m][i]['motor_warped'])):
                out_G['samples_type'][m][i]._motor_warped.append([])
                for k in range(len(G['samples_type'][m][i]['motor_warped'][j])):
                    out_G['samples_type'][m][i]._motor_warped[j].append(copy.deepcopy(G['samples_type'][m][i]['motor_warped'][j][k]['val']))

            out_G['samples_type'][m][i]._cache_grant_curent = copy.deepcopy(G['samples_type'][m][i]['ink_off_page'])
        
            out_G['samples_type'][m][i]._strokes = []
            for j in range(0, len(G['samples_type'][m][i]['S'])):
                s = stroke()
                s._my_type = copy.deepcopy(G['samples_type'][m][i]['S'][j]['myType'])
                # s._lh = copy.deepcopy(G['samples_type'][m][i]['S'][j]['lh'])
                s._R = copy.deepcopy(G['samples_type'][m][i]['S'][j]['R'])
                s._ids = copy.deepcopy(G['samples_type'][m][i]['S'][j]['ids'])
                s._invscales_type = copy.deepcopy(G['samples_type'][m][i]['S'][j]['invscales_type'])
                s._shapes_type = copy.deepcopy(G['samples_type'][m][i]['S'][j]['shapes_type'])
                s._pos_token = copy.deepcopy(G['samples_type'][m][i]['S'][j]['pos_token'])
                s._invscale_token = copy.deepcopy(G['samples_type'][m][i]['S'][j]['invscales_token'])
                s._shapes_token = copy.deepcopy(G['samples_type'][m][i]['S'][j]['shapes_token'])
                s._nsub = copy.deepcopy(G['samples_type'][m][i]['S'][j]['nsub'])

                s._motor = []
                for k in range(len(G['samples_type'][m][i]['S'][j]['motor'])):
                    s._motor.append(copy.deepcopy(G['samples_type'][m][i]['S'][j]['motor'][k]['val']))
                s._motor_spline = copy.deepcopy(G['samples_type'][m][i]['S'][j]['motor_spline'])
                out_G['samples_type'][m][i]._strokes.append(s)
    return out_G

if __name__ == "__main__":
    G_py = sio.loadmat("./model/G/35G.mat", squeeze_me=True)['G']
    G = process_mat(G_py)
    load_mat_G("./model/G/35G.mat")
    # print((G['models'][0]['motor'][0][0]['val']))
    # print(G['models'][0]['S'][0]['motor'])

