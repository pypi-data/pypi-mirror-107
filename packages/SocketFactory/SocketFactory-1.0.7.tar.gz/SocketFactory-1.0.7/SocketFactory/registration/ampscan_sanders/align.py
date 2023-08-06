# -*- coding: utf-8 -*-
"""
Package for dealing with alignment methods between two AmpObject meshes
Copyright: Joshua Steer 2020, Joshua.Steer@soton.ac.uk
"""

import numpy as np
import copy
import vtk
import math
from scipy import spatial
from scipy.optimize import minimize
from SocketFactory.registration.ampscan_sanders.core import AmpObject
from SocketFactory.registration.ampscan_sanders.sanders_errors import calcF

class align(object):
    r"""
    Automated alignment methods between two meshes
    
    Parameters
    ----------
    moving: AmpObject
        The moving AmpObject that is to be aligned to the static object
    static: AmpObject
        The static AmpObject that the moving AmpObject that the moving object 
        will be aligned to
    method: str, default 'linPoint2Plane'
        A string of the method used for alignment
    *args:
    	The arguments used for the alignment methods
    **kwargs:
    	The keyword arguments used for the alignment methods

    Returns
    -------
    m: AmpObject
        The aligned AmpObject, it same number of vertices and face array as 
        the moving AmpObject
        Access this using align.m

    Examples
    --------
    >>> static = AmpObject(staticfh)
    >>> moving = AmpObject(movingfh)
    >>> al = align(moving, static).m

    """    

    def __init__(self, moving, static, *args, **kwargs):
        mData = dict(zip(['vert', 'faces', 'values'], 
                         [moving.vert, moving.faces, moving.values]))
        alData = copy.deepcopy(mData)
        self.m = AmpObject(alData, stype='reg')
        self.s = static
        self.runICP(*args, **kwargs)

    
    def runICP(self, maxiter=20, inlier=1.0,
               initTransform=None, weights = [(1, 0), (0.8, 0.2)], *args, **kwargs):
        r"""
        The function to run the ICP algorithm, this function calls one of 
        multiple methods to calculate the affine transformation 
        
        Parameters
        ----------
        method: str, default 'linPoint2Plane'
            A string of the method used for alignment
        maxiter: int, default 20
            Maximum number of iterations to run the ICP algorithm
        inlier: float, default 1.0
            The proportion of closest points to use to calculate the 
            transformation, if < 1 then vertices with highest error are 
            discounted
        *args:
        	The arguments used for the alignment methods
        **kwargs:
        	The keyword arguments used for the alignment methods
        
        """
        # Define the rotation, translation, error and quaterion arrays
        Rs = np.zeros([3, 3, maxiter+1])
        Ts = np.zeros([3, maxiter+1])
        err = np.zeros([maxiter+1])
        if initTransform is None:
            initTransform = np.eye(4)
        Rs[:, :, 0] = initTransform[:3, :3]
        Ts[:, 0] = initTransform[3, :3]
        
        kdTree = spatial.cKDTree(self.s.vert)
        self.m.rigidTransform(Rs[:, :, 0], Ts[:, 0])
        inlier = math.ceil(self.m.vert.shape[0]*inlier)
        [dist, idx] = kdTree.query(self.m.vert, 1)
        # Sort by distance
        sort = np.argsort(dist)
        # Keep only those within the inlier fraction
        [dist, idx] = [dist[sort], idx[sort]]
        [dist, idx, sort] = dist[:inlier], idx[:inlier], sort[:inlier]
        err[0] = math.sqrt(dist.mean())

        self.s.calcVNorm()
        self.m.calcVNorm()

        s_norm = self.s.vNorm
        m_norm = self.m.vNorm

        for i in range(maxiter):
            
            if (i < maxiter/2) :
                [R, T] = getattr(self, 'sanders')(self.m.vert[sort, :],
                                                self.s.vert[idx, :], self.m.vNorm, 
                                                self.s.vNorm[idx], weights[0],
                                                *args, **kwargs)
            else :
                [R, T] = getattr(self, 'sanders')(self.m.vert[sort, :],
                                                self.s.vert[idx, :], self.m.vNorm, 
                                                self.s.vNorm[idx], weights[1],
                                                *args, **kwargs)
            Rs[:, :, i+1] = np.dot(R, Rs[:, :, i])
            Ts[:, i+1] = np.dot(R, Ts[:, i]) + T
            self.m.rigidTransform(R, T)
            self.m.calcVNorm()
            [dist, idx] = kdTree.query(self.m.vert, 1)
            sort = np.argsort(dist)
            [dist, idx] = [dist[sort], idx[sort]]
            [dist, idx, sort] = dist[:inlier], idx[:inlier], sort[:inlier]
            err[i+1] = math.sqrt(dist.mean())

        R = Rs[:, :, -1]
        
        [U, s, V] = np.linalg.svd(R)
        R = np.dot(U, V)
        self.tForm = np.r_[np.c_[R, np.zeros(3)], np.append(Ts[:, -1], 1)[:, None].T]
        self.R = R
        self.T = Ts[:, -1]
        self.rmse = err[-1]  
            
    @staticmethod
    def sanders(mv, sv, nm, ns, weights, opt='L-BFGS-B'):
        print(weights)
        X = np.zeros(6)
        lim = [-np.pi/4, np.pi/4] * 3 + [-40, 40] * 3
        lim = np.reshape(lim, [6, 2])
        try:
            X = minimize(align.sanders_errors, X,
                         args=(mv, sv, nm, ns, weights),
                         bounds=lim, method=opt)
        except:
            X = minimize(align.sanders_errors, X,
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

    @staticmethod
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
