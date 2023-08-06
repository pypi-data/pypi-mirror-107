
import vtk
import numpy as np
import scipy
import pyvista as pv
from SocketFactory.alignment import common
from SocketFactory.utilities import utility

def method_inertial(landmarks, bb_principal_axis, control_axis):

    svd_input = np.matrix(landmarks)
    C = np.mean(landmarks, axis = 0)
   
    A = svd_input - C
    U, S, V = scipy.linalg.svd(A.T)
    temp_axis = U[:, 2]
    
    x_axis = np.cross(temp_axis, bb_principal_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(bb_principal_axis, x_axis)

    axis_control1 = np.abs(np.dot(x_axis, control_axis))
    axis_control2 = np.abs(np.dot(y_axis, control_axis))

    if (axis_control1 < axis_control2):
        x_axis, y_axis = y_axis, x_axis

    if (np.dot(x_axis, control_axis) < 0):
        x_axis = - x_axis

    y_axis = np.cross(bb_principal_axis, x_axis)
    return x_axis, y_axis

def anatomic_method(x_temp_landmark, y_temp_landmark, control_axis_x, control_axis_z):

    svd_input = np.matrix(y_temp_landmark)
    C = np.mean(y_temp_landmark, axis = 0)
    A = svd_input - C
    U, S, V = scipy.linalg.svd(A.T)
    y_axis = U[:, 2]
    y_axis = y_axis / np.linalg.norm(y_axis)

    svd_input = np.matrix(x_temp_landmark)
    C = np.mean(x_temp_landmark, axis = 0)
    A = svd_input - C
    U, S, V = scipy.linalg.svd(A.T)
    x_temp = U[:, 2]
    x_temp = x_temp / np.linalg.norm(x_temp)

    z_axis = np.cross(y_axis, x_temp)
    z_axis = z_axis / np.linalg.norm(z_axis)
    if (np.dot(z_axis, control_axis_z) < 0):
        z_axis = - z_axis

    x_axis = np.cross(y_axis, z_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)
    
    if (np.dot(x_axis, control_axis_x) < 0):
        x_axis = - x_axis

    # Y re-calculation to fix sign 
    y_axis = np.cross(z_axis, x_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)

    return x_axis, y_axis, z_axis

def align_sdr_tf(s1_path, cut_point, reference_point, landmarks, origin, method) :

    extension = ".ply"
    
    original_file_name = s1_path.split(".")[0]
    cut_file_name = original_file_name + "_cut"

    a = reference_point[0]
    l15 = reference_point[1]

    s1 = pv.read(s1_path)
    s1_vertices = utility.get_vertices(s1)
    centroid = np.mean(s1_vertices, axis = 0)
    principal_axis = common.compute_inertia_vector(s1_vertices)

    control_axis_z = cut_point - a # longitudinal axis
    control_axis_z = control_axis_z / np.linalg.norm(control_axis_z)

    control_axis_x = cut_point - l15 # antero-posterioir axis
    control_axis_x = control_axis_x / np.linalg.norm(control_axis_x)

    sign_control = np.dot(principal_axis, control_axis_z)
    if (sign_control < 0):
        principal_axis = - principal_axis

    common.cut(s1, cut_point, - principal_axis, cut_file_name + extension)
    s2 = pv.read(cut_file_name + extension)
    s2_vertices = utility.get_vertices(s2)

    bb_principal_axis = common.box_points_pca(s2, 20)
    sign_control = np.dot(bb_principal_axis, control_axis_z)
    if (sign_control < 0):
        bb_principal_axis = - bb_principal_axis

    common.cut(s1, cut_point, - bb_principal_axis, cut_file_name + extension)
    s2 = pv.read(cut_file_name + extension)

    centroid_cut = np.mean(s2_vertices, axis = 0)
     
    if (method == "inertial"):
        x_axis, y_axis = method_inertial(landmarks, bb_principal_axis, control_axis_x)
        common.apply_rot_trans(s1, s2, x_axis, y_axis, bb_principal_axis, origin)

    # Preferred method
    elif (method == "anatomic"):
        x_temp_landmark = landmarks[0:5]
        y_temp_landmark = landmarks[5:8]
        x_axis, y_axis, z_axis = anatomic_method(x_temp_landmark, y_temp_landmark, control_axis_x, control_axis_z)
        common.apply_rot_trans(s1, s2, x_axis, y_axis, z_axis, origin)

    file_name_1 = cut_file_name + "_aligned_" + method + extension
    file_name_2 = original_file_name + "_aligned_" + method + extension
    utility.write(s2, file_name_1)
    utility.write(s1, file_name_2)

    return file_name_1, file_name_2
