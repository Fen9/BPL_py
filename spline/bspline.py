def get_stk_from_bspline(P, neval):
    nland = P.shape

def bspline_gen_s(nland,neval):
    lb = 2
    ub = nland + 1 
    interval = (ub - lb)/(neval - 1)
    return list(range(lb, ub, interval)), lb, ub

# TODO:
def bspline_eval(sval,cpts):
    pass