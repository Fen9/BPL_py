# %% 
import pyro
import pyro.distributions as dist
import torch

# enable validation (e.g. validate parameters of distributions)
pyro.enable_validation(True)

from motor_program.motor_program import motor_program
from stroke.stroke import stroke
from mat_utils import lib_py, convert_object_to_tensor, convert_to_dict_of_tensors

# %% 

def generate_exemplars(template: motor_program, lib):
    m: motor_program = motor_program()

    for i in range(m._num_strokes):
        s: stroke = m.get_strokes(i)
        # if s.get_R

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