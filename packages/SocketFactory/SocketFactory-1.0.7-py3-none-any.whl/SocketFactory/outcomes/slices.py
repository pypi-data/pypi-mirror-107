
import vtk
from vtk.util import numpy_support
import numpy as np
import pyvista as pv
import os
from SocketFactory.utilities import utility, file_handler, gui_utilities

def compute_perimeter(slice):
    """
    Compute slice perimeter.
    """

    points = slice.GetPoints()
    polygon = slice.GetPolys()
       
    np_data = numpy_support.vtk_to_numpy(polygon.GetData())
    np_data = np_data[1:]
    d = []
    p_prec = None
    for i in np_data:
        if p_prec is None:
            p_prec = points.GetPoint(i)
        else:
            p_succ = points.GetPoint(i)
            d.append(np.linalg.norm(np.array(p_prec) - np.array(p_succ)))
            p_prec = p_succ

    return np.sum(d)


def compute_surface_area(slice):
    """
    Compute slice surface area.
    """

    mesh = pv.PolyData(slice)
    return mesh.area
    

def compute_residual_volume(mesh, h):
    """
    Compute slice residual volume.
    """

    cut_planes = vtk.vtkPlaneCollection()
    p = vtk.vtkPlane()
    p.SetOrigin(0, 0, h)
    p.SetNormal(0, 0, -1)
    cut_planes.AddItem(p)

    stripper = vtk.vtkStripper()
    stripper.SetInputData(mesh)
    clipper = vtk.vtkClipClosedSurface()
    clipper.SetInputConnection(stripper.GetOutputPort())
    clipper.SetClippingPlanes(cut_planes)
    clipper.Update()
    polydata = clipper.GetOutput()

    trimmed_mesh_properties = vtk.vtkMassProperties()
    trimmed_mesh_properties.SetInputData(polydata)
    trimmed_mesh_properties.Update()

    return trimmed_mesh_properties.GetVolume()

def compute_ap_ml_elongation(slice):
    """
    Compute maximum coordinates difference along x and y axis
    """

    vertices = utility.get_vertices(slice)
    x_coordinates = vertices[:, 0]
    y_coordinates = vertices[:, 1]
    ap_elongation = np.max(x_coordinates) - np.min(x_coordinates)
    ml_elongation = np.max(y_coordinates) - np.min(y_coordinates)
    return ap_elongation, ml_elongation


def create_slices(mesh, heights_data, file, ws):
    """
    Create slices at specified z height. 
    """

    if (isinstance(heights_data, dict)):
        heights = list(heights_data.keys())

    else :
        heights = np.sort(heights_data)
        heights = np.unique(heights) # Reorder and remove duplicates in slice heights.

    pActors = []
    main_path, dir_path, file_name = file_handler.create_dir_by_filename(file, '_slices')
    df_row = [file_name]

    for h in heights:

        # Creating planes to cut mesh
        p = vtk.vtkPlane()
        p.SetOrigin(0, 0, h)
        p.SetNormal(0, 0, 1)

        c = vtk.vtkCutter()
        c.SetCutFunction(p)
        c.SetInputData(mesh)
        c.GenerateCutScalarsOn()
        c.Update()

        cutStrips = vtk.vtkStripper()
        cutStrips.SetInputConnection(c.GetOutputPort())
        cutStrips.Update()

        cutPoly = vtk.vtkPolyData()
        cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
        cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

        perimeter = compute_perimeter(cutPoly)

        if (isinstance(heights_data, dict)):
            slice_name = heights_data[h]
        else :
            slice_name = str(round(h, 2)) + "mm"

        file = os.path.join(dir_path, slice_name + ".stl")
        utility.write_stl(cutPoly, file)
        area = compute_surface_area(utility.read(file))
        residual_volume = compute_residual_volume(mesh, h)
        ap_elongation, ml_elongation = compute_ap_ml_elongation(cutPoly)

        if (isinstance(heights_data, dict)):
           df_row.extend([slice_name])

        df_row.extend([h, perimeter, area, residual_volume, ap_elongation, ml_elongation, ""])

        cM = vtk.vtkPolyDataMapper()
        cM.SetInputConnection(c.GetOutputPort())
        pA = vtk.vtkActor()

        pA.GetProperty().SetLineWidth(4)
        pA.GetProperty().SetInterpolationToFlat()
        pA.GetProperty().EdgeVisibilityOn()
        pA.GetProperty().SetRenderLinesAsTubes(True)
        pA.SetMapper(cM)
        
        pActors.append(pA)

    gui_utilities.visualize_slices(mesh, pActors)
    ws.append(df_row)
    return ws, main_path
