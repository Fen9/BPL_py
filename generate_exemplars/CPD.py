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
    