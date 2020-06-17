import numpy as np

# flatten a nested cell array, to create a cell array
# of [nx1] elements
def flatten_substrokes(nested):
    # ncell = 0
    # ns = len(nested)
    # for i in range(ns):
    #     ncell = ncell + len(nested[i])
    vcell = []

    for i in range(len(nested)):
        for j in range(len(nested[i])):
            vcell.append(nested[i][j])

    return vcell

def apply_each_substroke(nested, func, B):
    for sid in range(len(nested)):
        for bid in range(len(nested[sid])):
            nested[i][j] = func(nested[i][j], B)


# Affine warp defined by
# A(1) * [x y] + [A(2) A(3)]
# OR
# A(1:2) .* [x y] + [A(3) A(4)]
# 
# Input
# stk [n x 2] stroke
# A : [3x1 or 4x1] affine warp
def affine_warp(stk, affine):
    n = stk.shape[0]
    if affine.shape[0] == 3:
        stk = affine[0] * stk
        stk = stk + affine[1:3]
    else:
        stk = affine[0:1] * stk
        stk = stk + affine[2:4]