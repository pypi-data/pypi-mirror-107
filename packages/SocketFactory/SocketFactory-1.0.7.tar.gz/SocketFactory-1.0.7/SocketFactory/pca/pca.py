
import numpy as np 
from sklearn.decomposition import PCA
import vtk
import pyvista as pv
import numpy as np
from vtk.util import numpy_support
from SocketFactory.utilities import utility

class PCAWrapper(object):

    def __init__(self, meshes, differential = False):
        self.meshes = meshes
        self.f = len(meshes)
        if (not differential):
            self.faces = meshes[0].faces
            self.n_vertices = meshes[0].GetNumberOfPoints()
        self.run_pca(self.meshes)

    def run_pca(self, meshes):
        """
        Computes PCA, eigenvalues, eigenvectors and mean shape given a set of meshes.
        """

        vertices = list(map(lambda mesh : utility.get_vertices(mesh).flatten(), meshes))

        X = np.matrix(vertices) # f * 3N
        pca = PCA()
        pca.fit(X) # Also centers points

        self.mean_shape = pca.mean_

        #cov = pca.get_covariance() # 3N * 3N (too big!!)
        self.V_pca = pca.components_.T # 3N * f, eigenvectors
        self.lambda_ = pca.explained_variance_ # 3N * 1, eigenvalues
        self.lamda_ratios = pca.explained_variance_ratio_ # 3N * 1
        #T = np.dot(X - pca.mean_, V_pca) # f * f -> same as transform
        T_pca = pca.transform(X)

    def select_components(self, starting_index, ending_index):

        # eigenvalues to be considered
        self.lambda_r = self.lambda_[starting_index : ending_index]
        self.V_r = self.V_pca[:, starting_index : ending_index]
        self.lamda_ratios_r = self.lamda_ratios[starting_index : ending_index]
        self.v = np.sqrt(self.lambda_r)

    def generate_shape(self, weights):
        """
        Generates a new shape, given eignevalues to be considered and relative weights.
        """
        
        self.b_r = weights * self.v # r * 1
        Y = self.mean_shape + self.V_r @ self.b_r  # 3N * 1 + 3N * r @ r * 1 # b comlumn vector (r * 1), mesh new values

        shape = np.array(Y).reshape((self.n_vertices, 3))
        new_shape = pv.PolyData(shape, self.faces)
        return new_shape

    def get_mean_shape(self):
        """
        Return mean shape mesh.
        """
        
        mean_shape_vertices = np.array(self.mean_shape).reshape((self.n_vertices, 3))
        mean_mesh = pv.PolyData(mean_shape_vertices, self.faces)
        return mean_mesh

    def get_shape_from_differential_pca(self, weights, base_mesh):

        self.b_r = weights * self.v # r * 1
        Y = self.mean_shape + self.V_r @ self.b_r 

        vertices = utility.get_vertices(base_mesh)
        faces = base_mesh.faces
        shape = np.array(Y).reshape((len(vertices), 3))
        new_shape = pv.PolyData(vertices + shape, faces)
        return new_shape