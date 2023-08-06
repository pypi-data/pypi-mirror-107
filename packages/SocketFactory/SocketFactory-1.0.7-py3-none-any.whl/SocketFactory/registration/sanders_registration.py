import numpy as np
import math
from scipy import spatial
from scipy.optimize import minimize
from MeshAnalysis.utilities import utility
from MeshAnalysis.registration import common
import pyvista as pv

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

def sanders_errors(X, mv, sv, nm, ns, weights):
    [angx, angy, angz] = X[:3]
    Rx = np.array([[1, 0, 0],
                    [0, np.cos(angx), -np.sin(angx)],
                    [0, np.sin(angx), np.cos(angx)]])
    Ry = np.array([[np.cos(angy), 0, np.sin(angy)],
                    [0, 1, 0],
                    [-np.sin(angy), 0, np.cos(angy)]])
    Rz = np.array([[np.cos(angz), -np.sin(angz), 0],
                    [np.sin(angz), np.cos(angz), 0],
                    [0, 0, 1]])
    R = np.dot(np.dot(Rz, Ry), Rx)
    moved = np.dot(mv, R.T)
    moved += X[3:]
    movedNorms = np.dot(nm, R.T)
    err = calcF(moved, sv, movedNorms, ns, weights)
        
    return err
    
def sanders(mv, sv, nm, ns, weights, opt='L-BFGS-B'):
        print(weights)
        X = np.zeros(6)
        lim = [-np.pi/4, np.pi/4] * 3 + [-40, 40] * 3 # da verificare!
        lim = np.reshape(lim, [6, 2])
        try:
            X = minimize(sanders_errors, X,
                         args=(mv, sv, nm, ns, weights),
                         bounds=lim, method=opt)
        except:
            X = minimize(sanders_errors, X,
                         args=(mv, sv, nm, ns, weights),
                         method=opt)
        [angx, angy, angz] = X.x[:3]
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(angx), -np.sin(angx)],
                       [0, np.sin(angx), np.cos(angx)]])
        Ry = np.array([[np.cos(angy), 0, np.sin(angy)],
                       [0, 1, 0],
                       [-np.sin(angy), 0, np.cos(angy)]])
        Rz = np.array([[np.cos(angz), -np.sin(angz), 0],
                       [np.sin(angz), np.cos(angz), 0],
                       [0, 0, 1]])
        R = np.dot(np.dot(Rz, Ry), Rx)
        T = X.x[3:]
        return (R, T)
 
def runICP(static, moving, maxiter=20, weights = [(1, 0), (0.8, 0.2)], *args, **kwargs):
      
        static = pv.PolyData(static)
        moving = pv.PolyData(moving)
        static_vert = utility.get_vertices(static)
        moving_vert = utility.get_vertices(moving)

        static.compute_normals()
        static_norms = static.point_normals
        print(static_norms)
        moving.compute_normals()
        moving_norms = moving.point_normals

        # Define the rotation, translation, error and quaterion arrays
        Rs = np.zeros([3, 3, maxiter + 1])
        Ts = np.zeros([3, maxiter + 1])
        err = np.zeros([maxiter + 1])
        
        initTransform = np.eye(4)
        Rs[:, :, 0] = initTransform[:3, :3]
        Ts[:, 0] = initTransform[3, :3]
        
        kdTree = spatial.cKDTree(static_vert)

        [dist, idx] = kdTree.query(moving_vert, 1)
        
        err[0] = math.sqrt(dist.mean())

        for i in range(maxiter):
   
            if (i < maxiter/2) :
                [R, T] = sanders(moving_vert,
                                static_vert[idx, :], moving_norms, 
                                static_norms[idx, :], weights[0],
                                *args, **kwargs)
            else :
                [R, T] = sanders(moving_vert,
                                static_vert[idx, :], moving_norms, 
                                static_norms[idx, :], weights[1],
                                *args, **kwargs)
           
            Rs[:, :, i + 1] = np.dot(R, Rs[:, :, i])
            Ts[:, i + 1] = np.dot(R, Ts[:, i]) + T

            R = Rs[:, :, -1]
            T = Ts[:, -1]
            print(R)
            print(T)
            rotation_matrix = np.r_[np.c_[R, np.zeros(3)], np.append(T, 1)[:, None].T]
            print(rotation_matrix)
            matrix = utility.npmatrix_to_vtk(rotation_matrix)

            moving = common.apply_transformation(moving, matrix)
            moving_vert = utility.get_vertices(moving)
            moving = pv.PolyData(moving)
            moving.compute_normals()
            moving_norms = moving.point_normals
            [dist, idx] = kdTree.query(moving_vert, 1)
            err[i+1] = math.sqrt(dist.mean())

        R = Rs[:, :, -1]
        #Simpl
        [U, s, V] = np.linalg.svd(R)
        R = np.dot(U, V)
        tForm = np.r_[np.c_[R, np.zeros(3)], np.append(Ts[:, -1], 1)[:, None].T]
        R = R
        T = Ts[:, -1]
        rmse = err[-1]  
       
        return tForm, moving
 