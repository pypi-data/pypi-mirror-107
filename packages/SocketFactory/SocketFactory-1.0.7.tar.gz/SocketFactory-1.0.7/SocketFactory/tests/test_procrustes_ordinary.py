

import unittest
import vtk
import numpy as np
from SocketFactory.utilities import utility, gui_utilities, file_handler
from SocketFactory.registration import registration_methods as registration
from SocketFactory.tests import common

static_color = (0.6, 0.99, 1)
moving_color = (1, 0.73, 0.6)

class ProcrustesOrdinaryRegistration(unittest.TestCase):

        def setUp(self):

            path_static = "s.stl"
            self.static = utility.read(path_static)
           
            self.translation = [10, 10, 10]
            self.rotationX = 0
            self.rotationY = 5
            self.rotationZ = 0
            self.scale = [1.3, 1.3, 1.3]

        def test_1_rigid_reg(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            moving = registration.apply_transformation(self.static, transform)
            gui_utilities.visualize_meshes([self.static, moving], [static_color, moving_color])

            procrustes_rigid = registration.run_procrustes_transform([self.static, moving], "RigidBody")
            moving_transformed = procrustes_rigid.GetOutput().GetBlock(1)
            gui_utilities.visualize_meshes([self.static, moving_transformed], [static_color, moving_color])
            self.assertTrue(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))

        def test_2_similarity_reg(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            transform.Scale(self.scale)
            moving = registration.apply_transformation(self.static, transform)
            gui_utilities.visualize_meshes([self.static, moving], [static_color, moving_color])

            procrustes_similarity = registration.run_procrustes_transform([self.static, moving], "Affine")
            moving_transformed = procrustes_similarity.GetOutput().GetBlock(1)
            gui_utilities.visualize_meshes([self.static, moving_transformed], [static_color, moving_color])
            self.assertTrue(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))

        def test_3_affine_reg(self):
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

            gui_utilities.visualize_meshes([self.static, moving], [static_color, moving_color])

            procrustes_affine = registration.run_procrustes_transform([self.static, moving], "Affine")
            moving_transformed = procrustes_affine.GetOutput().GetBlock(1)
            gui_utilities.visualize_meshes([self.static, moving_transformed], [static_color, moving_color])
            self.assertTrue(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))

        def test_4_diff_topology(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            static_modified_topology = utility.create_stl_different_topology(self.static)
            moving = registration.apply_transformation(static_modified_topology, transform)
            gui_utilities.visualize_meshes([self.static, moving], [static_color, moving_color])

            procrustes_rigid = registration.run_procrustes_transform([self.static, moving], "RigidBody")
            moving_transformed = procrustes_rigid.GetOutput().GetBlock(1)
            gui_utilities.visualize_meshes([self.static, moving_transformed], [static_color, moving_color])
            self.assertFalse(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))

if __name__ == '__main__':
    unittest.main()
