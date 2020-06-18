# %% 
import pyro
import pyro.distributions as dist
import torch

# enable validation (e.g. validate parameters of distributions)
pyro.enable_validation(True)

from motor_program.motor_program import motor_program
from stroke.stroke import stroke
from classes_relations.relations import relation
import generate_exemplars.CPD as CPD
import matplotlib.pylab as plt
# %% 

def generate_exemplar(template, lib):
    m: motor_program = motor_program(template)

    for i in range(m._num_strokes):
        s: stroke = m._strokes[i]
        r: relations = s.get_R()
        if r['type'] == 'mid':
            r['eval_spot_token'] = CPD.sample_relation_token(lib, r['eval_spot_type'])
        s._pos_token = CPD.sample_position(lib, r, m._strokes[:i])
        s._shapes_token = CPD.sample_shape_token(lib, s._shapes_type)
        s._invscale_token = CPD.sample_invscale_token(lib, s._invscales_type)
        
    m._affine_transformation = CPD.sample_affine(lib)
    m._blur_sigma = template._fixed_parameters['min_blur_sigma']
    m._epsilon = template._fixed_parameters['min_epsilon']
    # sample image
    print(m.get_prob_img())
    plt.imshow(m._prob_img)
    plt.colorbar()
    plt.show()
    return CPD.sample_image(m.get_prob_img())


# %%
# def generate_exemplars():
#     num_parts = pyro.sample('num_parts', dist.Categorical(pkappa))
#     num_parts += 1     # sample number of parts, start from 1
#     objectTemplate = Concept(num_parts.item())

#     for i in range(num_parts):
#         # sample relations, CPD.m line 293
#         if i == 0:
#             edge_type_idx = 0 # TODO: does it need to be named in pyro?
#         else:
#             edge_type_idx = pyro.sample('edge_type_idx', dist.Categorical(rel['mixprob']))
#         edge_type = EdgeType(edge_type_idx)

#         # TODO: sample_relation_token
#         # pyro.sample('', dist.Normal(0, 1))

#         # sample subparts
#         nsub_mat_idx = num_parts-1 # index from 0
#         num_subparts = pyro.sample('nsub', dist.Categorical(pmat_nsub[nsub_mat_idx]))
#         num_subparts = num_subparts + 1 # sample number of subparts, start from 1

#         pStart = torch.exp(logStart)
#         sq[0] = 
#         for j in range(num_subparts):