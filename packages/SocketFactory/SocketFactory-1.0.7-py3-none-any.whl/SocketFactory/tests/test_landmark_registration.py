
import unittest
import vtk
import numpy as np
from SocketFactory.utilities import utility, gui_utilities, file_handler
from SocketFactory.registration import registration_methods as registration
from SocketFactory.tests import common

static_color = (0.6, 0.85, 0.7)
moving_color = (0.87, 0.62, 0.62)

def test_lmk_reg(static, moving, s_coordinates, m_coordinates, transform):

        static_landmarks = vtk.vtkPoints()
        moving_landmarks = vtk.vtkPoints()

        for point in s_coordinates:
            static_landmarks.InsertNextPoint(point)

        for point in m_coordinates:
            moving_landmarks.InsertNextPoint(point)
            
        gui_utilities.visualize_meshes([static, moving], [static_color, moving_color], [s_coordinates, m_coordinates])
        reg = registration.run_landmarks_registration(static, moving, static_landmarks, moving_landmarks, transform)

        outputMatrix = vtk.vtkMatrix4x4()
        reg.GetMatrix(outputMatrix)
            
        reg.Inverse() # Need to invert output matrix to compare initial transformation matrix
        transformMatrix = vtk.vtkMatrix4x4()
        reg.GetMatrix(transformMatrix)
    
        moving_transformed = registration.apply_transformation(moving, transformMatrix)
        gui_utilities.visualize_meshes([static, moving_transformed], [static_color, moving_color])

        return outputMatrix, moving_transformed

class LmkRegistration(unittest.TestCase):

        def setUp(self):

            path_static = "s.stl"
            path_static_lmk = "s.txt"
            self.static = utility.read(path_static)
            self.landmarks_dict = file_handler.read_points(path_static_lmk)
            self.s_lmk_coordinates = utility.query_dict(self.landmarks_dict, self.landmarks_dict.keys(), self.static.GetPoints())

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
            m_lmk_coordinates = utility.query_dict(self.landmarks_dict, self.landmarks_dict.keys(), moving.GetPoints())

            original_transform = utility.vtkmatrix_to_numpy(transform.GetMatrix())
            outputMatrix, moving_transformed = test_lmk_reg(self.static, moving, self.s_lmk_coordinates, m_lmk_coordinates, "RigidBody")
            reg_transform = utility.vtkmatrix_to_numpy(outputMatrix)

            self.assertTrue(common.matrices_comparison(original_transform, reg_transform))
            self.assertTrue(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))

        def test_2_similarity_reg(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            transform.Scale(self.scale)
            moving = registration.apply_transformation(self.static, transform)
            m_lmk_coordinates = utility.query_dict(self.landmarks_dict, self.landmarks_dict.keys(), moving.GetPoints())

            original_transform = utility.vtkmatrix_to_numpy(transform.GetMatrix())
            outputMatrix, moving_transformed = test_lmk_reg(self.static, moving, self.s_lmk_coordinates, m_lmk_coordinates, "Similarity")
            reg_transform = utility.vtkmatrix_to_numpy(outputMatrix)

            self.assertTrue(common.matrices_comparison(original_transform, reg_transform))
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

            m_lmk_coordinates = utility.query_dict(self.landmarks_dict, self.landmarks_dict.keys(), moving.GetPoints())

            original_transform = utility.vtkmatrix_to_numpy(transform.GetMatrix())
            outputMatrix, moving_transformed = test_lmk_reg(self.static, moving, self.s_lmk_coordinates, m_lmk_coordinates, "Affine")
            reg_transform = utility.vtkmatrix_to_numpy(outputMatrix)

            self.assertTrue(common.matrices_comparison(original_transform, reg_transform))
            self.assertTrue(common.check_rmse(utility.get_vertices(self.static), utility.get_vertices(moving_transformed)))

if __name__ == '__main__':
    unittest.main()
