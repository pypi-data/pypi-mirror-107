
import vtk
from plyfile import PlyData, PlyElement
import numpy as np
import pyvista as pv
import pymeshlab as ml
from SocketFactory.utilities import utility

def erode_border(path):
    """
    Delete border of selected area.
    """

    ms = ml.MeshSet()
    ms.load_new_mesh(path)
    ms.apply_filter("select_border")
    ms.apply_filter("delete_selected_vertices")
    ms.save_current_mesh(path)
    

def trim_selected_area(mesh, points, output_path):
    """
    Trimmer of specified area, given ponts on mesh.

    Parameters
    ----------
    mesh: vtkPolyData
        mesh to trim
    points: array of tuples
        points that delimit region of interest on mesh
    output_path: str
        path where save trimmed area
    """

    selectionPoints = vtk.vtkPoints()

    for i, p in enumerate(points):
        selectionPoints.InsertPoint(i, p[0], p[1], p[2])

    loop = vtk.vtkSelectPolyData()
    loop.SetInputData(mesh)
    loop.SetLoop(selectionPoints)
    loop.GenerateSelectionScalarsOn()
    loop.SetSelectionModeToSmallestRegion()
    loop.Update()

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(selectionPoints)

    clip = vtk.vtkClipPolyData()
    clip.SetInputConnection(loop.GetOutputPort())
    clip.GenerateClippedOutputOn()
    clip.Update()
    roi = clip.GetClippedOutput()

    utility.write(roi, output_path) # ROI saving
    erode_border(output_path)
    return utility.read(output_path)

def create_dictionary(path):
    """
    Creates dictionary with vertex in key and quality in value, from a ply file.
    """

    print("Creating dictionary...")
    plydata = PlyData.read(path)
    qualities = plydata.elements[0]["quality"]
    x = plydata["vertex"].data["x"]
    y = plydata["vertex"].data["y"]
    z = plydata["vertex"].data["z"]
    vertices = list(zip(x, y, z))
    dict = {}
    for v, q in zip(vertices, qualities):
        dict[v] = q
    return dict

