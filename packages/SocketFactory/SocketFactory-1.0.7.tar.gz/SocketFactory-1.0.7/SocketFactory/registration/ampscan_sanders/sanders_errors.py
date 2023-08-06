
import numpy as np

def compute_re(static_vert, moving_vert, static_norm):
    """
    Signed distance between vertex and closest point
    Resulting distance is projected on the reference normal
    """
    dist = moving_vert - static_vert
    proj_dist = np.abs(np.sum(dist * static_norm, axis = 1)) # Need to use absolute value in order to have a correct function minimization
    return proj_dist

def compute_snae(static_norm, moving_norm):
    '''
    J.E. Sanders Parameters
    Mean Surface Normal Angle Error
    Mean hyperbolic arctangent of the dot product of the normals
    '''

    result = np.sum(static_norm * moving_norm, axis = 1) - 10e-7
    atanh = np.arctanh(result)
    return atanh

def calcF(moving_vert, static_vert, moving_norm, static_norm, weights):

    radial_weight, normal_weight = weights
    re_values = compute_re(static_vert, moving_vert, static_norm)
    snae_values = compute_snae(static_norm, moving_norm)
    f = radial_weight * re_values.mean() - normal_weight * snae_values.mean()
    return f
