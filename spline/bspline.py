import numpy as np

def get_stk_from_bspline(P, neval):
    nland = P.shape

def bspline_gen_s(nland, neval):
    lb = 2
    ub = nland + 1 
    # interval = (ub - lb)/(neval - 1)
    # return list(range(lb, ub, interval)), lb, ub
    return lb, ub

def vectorized_bspline_coeff(vi, vs):
    c = np.zeros(vi.shape)


def bspline_eval(sval, cpts):
    l = cpts.shape[0]
    ns = sval.shape[0]
    y = np.array((ns, 2))

    s = np.matlib.repmat(sval, 1, l)
    i = np.matlib.repmat([i for i in range(0, l)], ns, 1)
    cof = vectorized_bspline_coeff(i, s)
    sum_c = np.sum(cof,2)
    cof = cof / np.matlib(sum_c, 1, l)
    y[:,0] = cof * cpts[:, 0]
    y[:,1] = cof * cpts[:, 1]

    return y, cof