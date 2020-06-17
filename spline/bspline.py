import numpy as np
import numpy.matlib as matlib

def get_stk_from_bspline(P, neval):
    nland = P.shape

def bspline_gen_s(nland, neval):
    lb = 2
    ub = nland + 1 
    # interval = (ub - lb)/(neval - 1)
    # return list(range(lb, ub, interval)), lb, ub
    return lb, ub

# output C [n x 1]: the coefficients
def vectorized_bspline_coeff(vi, vs):
    c = np.zeros(vi.shape)
    sel1 = np.logical_and(vs >= vi, vs < vi+1)
    c[sel1] = (1/6)*np.power(vs[sel1]-vi[sel1], 3)

    sel2 = np.logical_and(vs >= vi+1, vs < vi+2)
    c[sel2] = (1/6)*(-3*np.power(vs[sel2]-vi[sel2]-1, 3) + 3*np.power(vs[sel2]-vi[sel2]-1, 2) + 3*(vs[sel2]-vi[sel2]-1)+1)
    
    sel3 =  np.logical_and(vs >= vi+2, vs < vi+3)
    c[sel3] = (1/6)*(3*np.power(vs[sel3]-vi[sel3]-2, 3) - 6*np.power(vs[sel3]-vi[sel3]-2, 2) + 4)
    
    sel4 = np.logical_and(vs >= vi+3, vs < vi+4)
    c[sel4] = (1/6)*np.power(1-(vs[sel4]-vi[sel4]-3), 3)

    return c

# sval: vector [k x 1] where 0 <= sval(i) <= n
# cpts: [n x 2] array of control points
def bspline_eval(sval, cpts):
    l = cpts.shape[0]
    ns = sval.shape[0]
    y = np.zeros((ns, 2))

    s = matlib.repmat(sval, 1, l)
    i = matlib.repmat([i for i in range(0, l)], ns, 1)
    cof = vectorized_bspline_coeff(i, s)
    sum_c = np.sum(cof)

    # cof = cof / matlib.repmat(sum_c, 1, l)
    cof = cof / sum_c

    y[:,0] = np.dot(cof, cpts[:, 0])
    y[:,1] = np.dot(cof, cpts[:, 1])

    return y, cof