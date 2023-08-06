
import unittest
import vtk
import numpy as np
from SocketFactory.utilities import utility, gui_utilities, file_handler
from SocketFactory.registration import registration_methods as registration
from SocketFactory.tests import common

static_color = (1, 0.77, 0.6)
moving_color = (0.8, 1, 0.8)

def test_tps(static, moving, lmk_coordinates, transform):

        static_landmarks = vtk.vtkPoints()
        moving_landmarks = vtk.vtkPoints()

        for point in lmk_coordinates:
            static_landmarks.InsertNextPoint(point)

        transformed_points = utility.transform_points(transform.GetMatrix(), lmk_coordinates)
            
        for point in transformed_points:
            moving_landmarks.InsertNextPoint(point)

        color1 = static_color
        color2 = moving_color
            
        gui_utilities.visualize_meshes([static, moving], [color1, color2], [lmk_coordinates, transformed_points])

        warped = registration.run_thinPlateSpline_transform(moving, static_landmarks, moving_landmarks)
        gui_utilities.visualize_meshes([static, warped], [color1, color2])
        return static, warped

class TestThinPlateSpline(unittest.TestCase):

        def setUp(self):

            path_static = "s.stl"
            path_static_lmk = "s.txt"
            self.static = utility.read(path_static)
            landmarks_dict = file_handler.read_points(path_static_lmk)
            self.lmk_coordinates = utility.query_dict(landmarks_dict, landmarks_dict.keys(), self.static.GetPoints())

            self.translation = [10, 10, 10]
            self.rotationX = 0
            self.rotationY = 5
            self.rotationZ = 0
            self.scale = [1.3, 1.3, 1.3]

        def test_1_rigid_tps(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            moving = registration.apply_transformation(self.static, transform)
            static, warped = test_tps(self.static, moving, self.lmk_coordinates, transform)
            self.assertTrue(common.check_rmse(utility.get_vertices(static), utility.get_vertices(warped)))

        def test_2_similarity_tps(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            transform.Scale(self.scale)
            moving = registration.apply_transformation(self.static, transform)
            static, warped = test_tps(self.static, moving, self.lmk_coordinates, transform)
            self.assertTrue(common.check_rmse(utility.get_vertices(static), utility.get_vertices(warped)))

        def test_3_affine_tps(self):

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
            static, warped = test_tps(self.static, moving, self.lmk_coordinates, transform)
            self.assertTrue(common.check_rmse(utility.get_vertices(static), utility.get_vertices(warped)))

        def test_4_different_topology(self):

            transform = vtk.vtkTransform()
            transform.Translate(self.translation)
            transform.RotateX(self.rotationX)
            transform.RotateY(self.rotationY)
            transform.RotateZ(self.rotationZ)
            static_modified_topology = utility.create_stl_different_topology(self.static)
            moving = registration.apply_transformation(static_modified_topology, transform)
            static, warped = test_tps(self.static, moving, self.lmk_coordinates, transform)
            self.assertTrue(common.check_rmse(utility.get_vertices(static), utility.get_vertices(warped)))

if __name__ == '__main__':
    unittest.main()