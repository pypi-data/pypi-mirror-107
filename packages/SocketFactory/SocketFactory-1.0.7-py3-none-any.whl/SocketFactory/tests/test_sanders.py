
import unittest
import vtk
import numpy as np
from SocketFactory.registration.ampscan_sanders.core import AmpObject
from SocketFactory.utilities import utility, gui_utilities, file_handler
from SocketFactory.registration import registration_methods as registration
from SocketFactory.tests import common

class TestSandersAlgorithm(unittest.TestCase):

        def setUp(self):

            path_static = "s.stl"
            self.static_1 = AmpObject(path_static)
            self.static_2 = AmpObject(path_static)
            self.static_3 = AmpObject(path_static)
            self.moving = AmpObject(path_static) 
            self.translation = [10, 10, 10]
            self.rotation = [0, 5, 0]

        def test_1_translation(self):
            
            self.static_1.translate(self.translation)
            output_transformation = registration.run_sanders_alignment(self.static_1, self.moving, 40).tForm
            original_transform = np.eye(4)
            original_transform[3,:] = np.append(np.array(self.translation), 1)
            self.assertTrue(common.matrices_comparison(original_transform, output_transformation))

        def test_2_rotation(self):
            
            self.static_2.rotateAng(self.rotation, ang = 'deg')
            output_transformation = registration.run_sanders_alignment(self.static_2, self.moving, 40).tForm

            original_transform = utility.get_transformation_matrix(self.rotation, 'deg')
            self.assertTrue(common.matrices_comparison(original_transform, output_transformation))
        
        def test_3_translation_rotation(self):

            self.static_3.rotateAng(self.rotation, ang = 'deg')
            self.static_3.translate(self.translation)
            output_transformation = registration.run_sanders_alignment(self.static_3, self.moving, 40).tForm

            original_transform = utility.get_transformation_matrix(self.rotation, 'deg', self.translation)
            self.assertTrue(common.matrices_comparison(original_transform, output_transformation))

if __name__ == '__main__':
    unittest.main()

