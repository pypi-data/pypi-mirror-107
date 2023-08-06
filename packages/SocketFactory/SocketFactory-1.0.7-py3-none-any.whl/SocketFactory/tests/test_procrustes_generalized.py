
import unittest
import vtk
import numpy as np
from SocketFactory.utilities import utility, gui_utilities, file_handler
from SocketFactory.registration import registration_methods as registration

class TestProcrustes(unittest.TestCase):

        def setUp(self):

            path_static = "s.stl"
            self.static = utility.read(path_static)

            translation = [10, 10, 10]
            rotationX = 0
            rotationY = 5
            rotationZ = 0
            scale = [0.9, 0.9, 0.9]

            self.transform_1 = vtk.vtkTransform()
            self.transform_1.Translate(translation)
            self.transform_1.RotateX(rotationX)
            self.transform_1.RotateY(rotationY)
            self.transform_1.RotateZ(rotationZ)

            self.transform_2 = vtk.vtkTransform()
            self.transform_2.Scale(scale)

            self.transform_3 = vtk.vtkTransform()
            matrix = vtk.vtkMatrix4x4()
            arr = np.array([[1, -0.03, -0.18, 0.44],
                            [0.18, 0.91, -0.41, 0.3],
                            [0, 0, 1, -0.09],
                            [0, 0, 0, 1]])
            for i in range(0, 4):
                    for j in range(0, 4):
                        matrix.SetElement(i, j, arr[i, j])
            self.transform_3.SetMatrix(matrix)

        def test_1(self):
            moving_1 = registration.apply_transformation(self.static, self.transform_1)
            moving_2 = registration.apply_transformation(self.static, self.transform_2)
            moving_3 = registration.apply_transformation(self.static, self.transform_3)
            meshes = [self.static, moving_1, moving_2, moving_3]

            procrustes_rigid = registration.run_procrustes_transform(meshes, "RigidBody")
            procrustes_similarity = registration.run_procrustes_transform(meshes, "Similarity")
            procrustes_affine = registration.run_procrustes_transform(meshes, "Affine")

            colors = []
            for i in range(len(meshes)):
                colors.append(gui_utilities.generate_random_color())
            gui_utilities.visualize_procrustes_res(meshes, colors, procrustes_rigid, procrustes_similarity, procrustes_affine)

        def test_2(self):
            # This test aims to remember Procrustes limits: it can't work with meshes with different topology
            moving_1 = registration.apply_transformation(utility.create_stl_different_topology(self.static), self.transform_1)
            moving_2 = registration.apply_transformation(utility.create_stl_different_topology(self.static), self.transform_2)
            moving_3 = registration.apply_transformation(utility.create_stl_different_topology(self.static), self.transform_3)
            meshes = [self.static, moving_1, moving_2, moving_3]

            procrustes_rigid = registration.run_procrustes_transform(meshes, "RigidBody")
            procrustes_similarity = registration.run_procrustes_transform(meshes, "Similarity")
            procrustes_affine = registration.run_procrustes_transform(meshes, "Affine")

            colors = []
            for i in range(len(meshes)):
                colors.append(gui_utilities.generate_random_color())
            gui_utilities.visualize_procrustes_res(meshes, colors, procrustes_rigid, procrustes_similarity, procrustes_affine)


if __name__ == '__main__':
    unittest.main()