import numpy as np
from scipy import spatial

def matrices_comparison(m1, m2, precision = 0.01):
    """
    Compares to matrices.
    """

    print()
    print(m1)
    print(m2)
    return np.allclose(m1, m2, precision, precision)

def rmse(static_vert, moving_vert):
    n = len(static_vert)
    kdTree = spatial.cKDTree(static_vert)
    [d, idx] = kdTree.query(moving_vert, 1)
    rmse = np.sqrt(np.sum(d ** 2) / n)
    return rmse

def check_rmse(static_vert, moving_vert, precision = 0.00001):
    rmse_value = rmse(static_vert, moving_vert)
    print(rmse_value)
    return rmse_value < precision


