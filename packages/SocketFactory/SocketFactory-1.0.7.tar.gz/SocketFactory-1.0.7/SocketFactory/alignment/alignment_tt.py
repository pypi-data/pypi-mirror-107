
from sklearn.decomposition import PCA
import pyvista as pv
import vtk
import numpy as np
import scipy
from SocketFactory.alignment import common
from SocketFactory.utilities import utility

def compute_anatomic_vector(a, mpt, pf):
    """
    Creates anatomic vector, from apex to middle point between mid patellar tendon and popliteal fossa.
    """

    mpt_pf = np.mean([mpt, pf], axis = 0)
    tmp_axis = mpt_pf - a
    return tmp_axis / np.linalg.norm(tmp_axis)

def alignment_method(principal_axis, landmarks, control_axis_x):

    svd_input = np.matrix(landmarks)
    C = np.mean(landmarks, axis = 0)
    A = svd_input - C
    U, S, V = scipy.linalg.svd(A.T)
    tmp_axis = U[:, 2]
   
    x_axis = np.cross(tmp_axis, principal_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(principal_axis, x_axis)

    axis_control1 = np.abs(np.dot(x_axis, control_axis_x))
    axis_control2 = np.abs(np.dot(y_axis, control_axis_x))

    if (axis_control1 < axis_control2):
        x_axis, y_axis = y_axis, x_axis

    if (np.dot(x_axis, control_axis_x) < 0):
        x_axis = - x_axis

    y_axis = np.cross(principal_axis, x_axis)

    return x_axis, y_axis 


def align_sdr_tt(s1_path, cut_point, anatomical_axis_points, landmarks, origin, method = "") :

    extension = ".ply"
    original_file_name = s1_path.split(".")[0]
    cut_file_name = original_file_name + "_cut"

    s1 = pv.read(s1_path)
    s1_vertices =  utility.get_vertices(s1)
    centroid = np.mean(s1_vertices, axis = 0)

    a = anatomical_axis_points[0]
    mpt = anatomical_axis_points[1]
    pf = anatomical_axis_points[2]

    anatomical_axis = compute_anatomic_vector(a, mpt, pf)
    control_axis_x = mpt - pf # antero-posterioir axis

    common.cut(s1, cut_point, - anatomical_axis, cut_file_name + extension)
    s2 = pv.read(cut_file_name + extension)
    s2_vertices =  utility.get_vertices(s2)
    centroid_cut = np.mean(s2_vertices, axis = 0)

    # All these method rely on inertial axis (computed on a uniform distribution of points inside mesh volume)
    if ((method == "1") | (method == "inertial")):

        bb_principal_axis = common.box_points_pca(s2, 20)
        sign_control = np.dot(bb_principal_axis, anatomical_axis)
        if (sign_control < 0):
            bb_principal_axis = - bb_principal_axis

        common.cut(s1, cut_point, - bb_principal_axis, cut_file_name + extension)
        s2 = pv.read(cut_file_name + extension)
        s2_vertices =  utility.get_vertices(s2)
        centroid_cut = np.mean(s2_vertices, axis = 0)

        if (method == "1"):
            x_axis, y_axis = alignment_method(bb_principal_axis, np.append(landmarks, [centroid_cut], axis = 0), control_axis_x)
            common.apply_rot_trans(s1, s2, x_axis, y_axis, bb_principal_axis, origin)
           
        # 2° preferred method
        elif (method == "inertial"):
            tt = landmarks[0]
            fat = landmarks[1]
            pf = landmarks[2]
            x_axis, y_axis = alignment_method(bb_principal_axis, landmarks, control_axis_x)
            common.apply_rot_trans(s1, s2, x_axis, y_axis, bb_principal_axis, origin)
           
    # Preferred method
    elif (method == "anatomic"):
        x_axis, y_axis = alignment_method(anatomical_axis, landmarks, control_axis_x)
        common.apply_rot_trans(s1, s2, x_axis, y_axis, anatomical_axis, origin)

    file_name_1 = cut_file_name + "_aligned_" + method + extension
    file_name_2 = original_file_name + "_aligned_" + method + extension
    utility.write(s2, file_name_1)
    utility.write(s1, file_name_2)

    return file_name_1, file_name_2
