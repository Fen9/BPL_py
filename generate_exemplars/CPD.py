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
    # print("sample_relation_token")
    # print(eval_spot_type)
    # sample an attachment, but within the bounds as defined by the model
    sigma_attach = torch.tensor(lib['tokenvar']['sigma_attach'])
    eval_spot_token = eval_spot_type + sigma_attach * torch.randn((1, ))
    # print(eval_spot_type)
    while not score_relation_token(lib, eval_spot_token, eval_spot_type):
        eval_spot_token = eval_spot_type + sigma_attach * torch.randn((1, ))
    # print(eval_spot_token)
    return eval_spot_token.numpy()

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
    return invscales_token.numpy()

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
    return ret.numpy()

def sample_affine(lib): # just one sample
    # affine transformation [x-scale,y-scale,x-translate,y-translate]
    # the translation is relative to the center of mass
    # (x-scale and y-scale cannot be 0 or negative)

    sample_A = np.zeros((1, 4))

    # sample the image scale
    mu_scale = lib['affine']['mu_scale']
    sigma_scale = lib['affine']['Sigma_scale']
    sample_scale = np.random.multivariate_normal(mu_scale, sigma_scale, 1)[0]
    sample_A[:, 0] = sample_scale[0]
    sample_A[:, 1] = sample_scale[1]

    # sample the translation
    m_x = lib['affine']['mu_xtranslate']
    m_y = lib['affine']['mu_ytranslate']
    s_x = lib['affine']['sigma_xtranslate']
    s_y = lib['affine']['sigma_ytranslate']
    sample_A[:, 2] = np.random.normal(m_x, s_x, 1)
    sample_A[:, 3] = np.random.normal(m_y, s_y, 1)

    if not sample_A[:,0] > 0 or not sample_A[:,1] > 0:
        print('Warning: sampled scale variable is less than zero')

    return sample_A

def sample_image(prob_img):
    return np.random.binomial(1, prob_img)