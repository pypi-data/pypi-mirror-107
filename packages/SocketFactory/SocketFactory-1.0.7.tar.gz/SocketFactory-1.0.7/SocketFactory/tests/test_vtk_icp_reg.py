
import unittest
import vtk
import numpy as np
from SocketFactory.utilities import utility, gui_utilities
from SocketFactory.registration import registration_methods as registration
from SocketFactory.tests import common

static_color = (0.67, 0.71, 0.8)
moving_color = (0.94, 0.7, 0.48)

class TestVtkIcpRegistration(unittest.TestCase):

        def setUp(self):

            path_static = "s.stl"
            self.static = utility.read(path_static)
            self.translation = [10, 10, 10]
            self.rotationX = 0
            self.rotationY = 5
            self.rotationZ = 0
            self.scale = [1.3, 1.3, 1.3]
            self.precision = 0.01

        def test_1_vtk_icp_rigid(self):
           
            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            moving = registration.apply_transformation(self.static, transform)
            color1 = static_color
            color2 = moving_color
            #gui_utilities.visualize_meshes([self.static, moving], [color1, color2])
            
            icp = registration.run_icp_vtk(self.static, moving, "RMS", "RigidBody", 200, 1, 0.000001, 600)
            outputMatrix = vtk.vtkMatrix4x4()
            icp.GetMatrix(outputMatrix)
            
            icp.Inverse() # Need to invert output matrix to compare initial transformation matrix
            transformMatrix = vtk.vtkMatrix4x4()
            icp.GetMatrix(transformMatrix)
    
            moving_transformed = registration.apply_transformation(moving, transformMatrix)
            #gui_utilities.visualize_meshes([self.static, moving_transformed], [color1, color2])

            original_transform = utility.vtkmatrix_to_numpy(transform.GetMatrix())
            icp_transform = utility.vtkmatrix_to_numpy(outputMatrix)

            self.assertTrue(common.matrices_comparison(original_transform, icp_transform, self.precision))
            self.assertTrue(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))
            
        def test_2_vtk_icp_similarity(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            transform.Scale(self.scale)
            moving = registration.apply_transformation(self.static, transform)

            color1 = static_color
            color2 = moving_color
           # gui_utilities.visualize_meshes([self.static, moving], [color1, color2])

            icp = registration.run_icp_vtk(self.static, moving, "RMS", "Similarity", 200, 1, 0.000001, 600)
            outputMatrix = vtk.vtkMatrix4x4()
            icp.GetMatrix(outputMatrix)

            icp.Inverse()
            transformMatrix = vtk.vtkMatrix4x4()
            icp.GetMatrix(transformMatrix)
            moving_transformed =  registration.apply_transformation(moving, transformMatrix)
           # gui_utilities.visualize_meshes([self.static, moving_transformed], [color1, color2])

            original_transform = utility.vtkmatrix_to_numpy(transform.GetMatrix())
            icp_transform = utility.vtkmatrix_to_numpy(outputMatrix)
            self.assertTrue(common.matrices_comparison(original_transform, icp_transform, self.precision))
            self.assertTrue(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))


        def test_3_vtk_icp_affine(self):

            matrix = vtk.vtkMatrix4x4()
            arr = np.array([[1, -0.03, -0.18, 0.44],
                            [0.18, 0.91, -0.41, 0.3],
                            [0, 0, 1, -0.09],
                            [0, 0, 0, 1]])
            for i in range(0, 4):
                    for j in range(0, 4):
                        matrix.SetElement(i, j, arr[i, j])
        
            transform = vtk.vtkTransform()
            transform.SetMatrix(matrix)
            moving = registration.apply_transformation(self.static, transform)

            color1 = static_color
            color2 = moving_color
           # gui_utilities.visualize_meshes([self.static, moving], [color1, color2])

            # NB: Need to change parameters to get the desired precision
            icp = registration.run_icp_vtk(self.static, moving, "RMS", "Affine", 400, 1, 0.000001, 800)
            outputMatrix = vtk.vtkMatrix4x4()
            icp.GetMatrix(outputMatrix)

            icp.Inverse()
            transformMatrix = vtk.vtkMatrix4x4()
            icp.GetMatrix(transformMatrix)
            moving_transformed = registration.apply_transformation(moving, transformMatrix)
           # gui_utilities.visualize_meshes([self.static, moving_transformed], [color1, color2])

            original_transform = utility.vtkmatrix_to_numpy(transform.GetMatrix())
            icp_transform = utility.vtkmatrix_to_numpy(outputMatrix)
            self.assertTrue(common.matrices_comparison(original_transform, icp_transform, self.precision))

if __name__ == '__main__':
    unittest.main()