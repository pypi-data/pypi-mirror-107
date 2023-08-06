
import pyvista as pv
import os
import numpy as np
from sklearn.decomposition import PCA
import vtk
from vtk.util import numpy_support
from SocketFactory.utilities import utility

def compute_inertia_vector(vertices):  
    """
    Apply PCA to compute principal inertia vector.
    """

    pca = PCA(n_components = 1)
    pca.fit(vertices)
    return pca.components_[0]
    
def cut(mesh, cut_point, axis, fileName):
    """
    Cut mesh in considering a plane and a point.
    """

    cut_planes = vtk.vtkPlaneCollection()
    p = vtk.vtkPlane()
    p.SetOrigin(cut_point)
    p.SetNormal(axis)
    cut_planes.AddItem(p)

    stripper = vtk.vtkStripper()
    stripper.SetInputData(mesh)
    clipper = vtk.vtkClipClosedSurface()
    clipper.SetInputConnection(stripper.GetOutputPort())
    clipper.SetClippingPlanes(cut_planes)

    clipper.Update()
    polydata = clipper.GetOutput()
    utility.write(polydata, fileName)

def apply_rot_trans(s1, s2, x_axis, y_axis, z_axis, origin):
    """
    Apply rotation, given a 4x4 matrix, and translation, given a point.
    """

    translation_matrix = np.eye(4)
    if (origin != ()) :
        translation_matrix[0:4, 3] = [-origin[0], -origin[1], -origin[2], 1]
        matrix = vtk.vtkMatrix4x4()
        for i in range(0, 4):
                for j in range(0, 4):
                    matrix.SetElement(i, j, translation_matrix[i, j])
        s2.transform(matrix)
        s1.transform(matrix)

    rotation_matrix = np.matrix([x_axis, y_axis, z_axis, [0,0,0]])
    rotation_matrix = np.append(rotation_matrix, [[0],[0],[0],[1]], axis = 1)

    matrix = utility.npmatrix_to_vtk(rotation_matrix)
    s2.transform(matrix)
    s1.transform(matrix)

    s2_vertices_rotated = numpy_support.vtk_to_numpy(s2.GetPoints().GetData())
    z_coordinates = s2_vertices_rotated[:, 2]

    if (origin == ()):
        z_min = np.min(z_coordinates)
        index_z_min = np.where(z_coordinates == z_min)
        min_s2 = s2_vertices_rotated[index_z_min].flatten()
        translation_matrix[0:4, 3] = [-min_s2[0], -min_s2[1], -min_s2[2], 1]
        matrix = vtk.vtkMatrix4x4()
        for i in range(0, 4):
                for j in range(0, 4):
                    matrix.SetElement(i, j, translation_matrix[i, j])

        s2.transform(matrix)
        s1.transform(matrix)

def box_points_pca(mesh, npoint):
    """
    Compute PCA on a uniform distribution of points inside mesh volume.
    """

    bb_limits = mesh.GetBounds()
    x_bound = bb_limits[0:2]
    y_bound = bb_limits[2:4]
    z_bound = bb_limits[4:6]
    nr_points = npoint
    gridx, gridy, gridz = np.meshgrid(np.linspace(x_bound[0], x_bound[1], nr_points),
                                        np.linspace(y_bound[0], y_bound[1], nr_points),
                                        np.linspace(z_bound[0], z_bound[1], nr_points))

    vtk_points = vtk.vtkPoints()
    for point in zip(gridx.flatten(), gridy.flatten(), gridz.flatten()):
        vtk_points.InsertNextPoint(point)

    points_polydata = vtk.vtkPolyData()
    points_polydata.SetPoints(vtk_points)

    points_np = numpy_support.vtk_to_numpy(vtk_points.GetData())
    enclosed_points_filter = vtk.vtkSelectEnclosedPoints()
    enclosed_points_filter.SetSurfaceData(mesh)
    enclosed_points_filter.SetInputData(points_polydata)
    enclosed_points_filter.SetCheckSurface(1)

    enclosed_points_filter.Update()

    inside_points = enclosed_points_filter.GetOutput().GetPointData().GetArray("SelectedPoints")

    enclosed_points_filter.ReleaseDataFlagOn()
    enclosed_points_filter.Complete()
    inside_array = np.asarray(numpy_support.vtk_to_numpy(inside_points),'bool')
    filtred_point = points_np[inside_array]
    principal_axis2 = compute_inertia_vector(filtred_point)
    return principal_axis2