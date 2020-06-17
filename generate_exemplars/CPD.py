# %% 
import pyro
import pyro.distributions as dist
import torch
import numpy as np

# enable validation (e.g. validate parameters of distributions)
pyro.enable_validation(True)

from motor_program.motor_program import motor_program
from stroke.stroke import stroke
import spline.bspline as bspline
import classes_relations.relations as relations

# %%
def sample_relation_token(lib, eval_spot_type):
    # print(eval_spot_type)
    # sample an attachment, but within the bounds as defined by the model
    sigma_attach = torch.tensor(lib['tokenvar']['sigma_attach'])
    eval_spot_token = eval_spot_type + sigma_attach * torch.randn((1, ))
    # print(eval_spot_type)
    while not score_relation_token(lib, eval_spot_token, eval_spot_type):
        eval_spot_token = eval_spot_type + sigma_attach * torch.randn((1, ))
    # print(eval_spot_token)
    return eval_spot_token

# simplified from matlab code, not actually scoring, just checking if within bound....
def score_relation_token(lib, eval_spot_token, eval_spot_type):
    # _, lb, ub = bspline.bspline_gen_s(lib['ncpt'], 1)
    lb, ub = bspline.bspline_gen_s(lib['ncpt'], 1)
    if eval_spot_token < lb or eval_spot_token > ub: # out of bound
        return False
    return True

def sample_invscale_token(lib, invscales_type):
    # Gaussian noise, but don't allow negative scales.
    # Sampling is done by rejection sampling
    # sz = invscales_type.shape
    sz = 1
    invscales_type = torch.tensor(invscales_type)
    sigma_invscale = torch.tensor(lib['tokenvar']['sigma_invscale'])
    invscales_token = invscales_type + sigma_invscale * torch.randn(sz)
    while not score_invscale_token(lib, invscales_token, invscales_type):
        invscales_token = invscales_type + sigma_invscale * torch.randn(sz)
    return invscales_token

# simplified from matlab code, not actually scoring, just checking if within bound....
# invscales_token: [n x 1] vector
# invscales_type: [n x 1] vector
def score_invscale_token(lib, invscales_token, invscales_type):
    # log of multivariate normal density <= 0
    # don't allow invscales that are negative
    # TODO: not too sure about this one
    return torch.all(dist.Normal(invscales_type, lib['tokenvar']['sigma_invscale']).log_prob(invscales_token) > 0).item()
    # return dist.MultivariateNormal(invscales_type, torch.eye(1) * lib['tokenvar']['sigma_invscale']).log_prob(invscales_token) > 0

# # ns: number of strokes in the character
# def sample_substroke_number(lib, ns): 
#     pass

# def sample_substroke_sequence(lib, ns, nsub=None):
#     if nsub is None:
#         nsub = sample_substroke_number(lib, ns)
#     pass

# def sample_shape_type(lib, subid):
#     pass


# Given a relation R and the previous strokes,
#  sample where the position of this stroke should be
def sample_position(lib, r, previous_strokes):
    base = relations.getAttachPoint(r, previous_strokes)
    sigma_x = lib['rel']['sigma_x']
    sigma_y = lib['rel']['sigma_y']
    return dist.Normal(torch.tensor(base), torch.tensor([sigma_x, sigma_y])).sample()

# bspline_stack: (ncpt x 2 x k) shapes of bsplines
def sample_shape_token(lib, bspline_stack):
    sigma_shape = lib['tokenvar']['sigma_shape']
    ret = torch.from_numpy(bspline_stack) + torch.tensor(sigma_shape) * torch.randn(bspline_stack.shape)
    return ret

def sample_affine(lib): # just one sample
    # affine transformation [x-scale,y-scale,x-translate,y-translate]
    # the translation is relative to the center of mass
    # (x-scale and y-scale cannot be 0 or negative)
    A = torch.zeros((4,))
    mu_scale = torch.tensor(lib['affine']['mu_scale'])
    sigma_scale = torch.tensor(lib['affine']['Sigma_scale'])
    A[:2] = dist.MultivariateNormal(mu_scale, sigma_scale).sample((2,))
    if (A[:2] > 0).sum() != 2:
        print('Warning: sampled scale variable is less than zero')

    A[2] = dist.Normal(lib['affine']['mu_xtranslate'], lib['affine']['sigma_xtranslate']).sample()
    A[3] = dist.Normal(lib['affine']['mu_ytranslate'], lib['affine']['sigma_ytranslate']).sample()
    return A

def sample_image(prob_img):
    return torch.distributions.Binomial(probs=prob_img).sample()