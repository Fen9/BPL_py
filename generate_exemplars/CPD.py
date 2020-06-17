# %% 
import pyro
import pyro.distributions as dist
import torch

# enable validation (e.g. validate parameters of distributions)
pyro.enable_validation(True)

from motor_program.motor_program import motor_program
from stroke.stroke import stroke

# %%
def sample_relation_token(lib, eval_spot_type):
    pass

def sample_stroke_number(lib):
    # Number of strokes model (Kappa)
    pass

# ns: number of strokes in the character
def sample_substroke_number(lib, ns): 
    pass

def sample_substroke_sequence(lib, ns, nsub=None):
    if nsub is None:
        nsub = sample_substroke_number(lib, ns)
    pass

def sample_shape_type(lib, subid):
    pass

def sample_invscale_token(lib, invscales_type):
    pass

# Given a relation R and the previous strokes,
#  sample where the position of this stroke should be
def sample_position():
    pass

# bspline_stack: (ncpt x 2 x k) shapes of bsplines
def sample_shape_token(lib, bspline_stack):
    sigma_shape = lib['tokenvar']['signam_shape']
    return bspline_stack + sigma_shape * torch.randn(bspline_stack.shape)