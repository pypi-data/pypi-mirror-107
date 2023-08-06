import vtk
import numpy as np
from vtk.util import numpy_support
from plyfile import PlyData, PlyElement
import pyvista as pv
 
def read_stl(path):
    """
    Reader of an stl file. Returns a polydata.
    """
    readerSTL = vtk.vtkSTLReader()
    readerSTL.SetFileName(path)
    readerSTL.Update()
    polydata = readerSTL.GetOutput()
    return polydata

def read_ply(path):
    """
    Reader of a ply file. Returns a polydata.
    """

    readerPLY = vtk.vtkPLYReader()
    readerPLY.SetFileName(path)
    readerPLY.Update()
    polydata = readerPLY.GetOutput()
    return polydata

def read_vtk(path):
    """
    Reader of an vtk file. Returns a polydata.
    """

    readerVTK = vtk.vtkPolyDataReader()
    readerVTK.SetFileName(path)
    readerVTK.Update()
    polydata = readerVTK.GetOutput()
    return polydata

def read(path):
    """
    General file reader. Returns a polydata.
    """

    file_format = path.split(".")[-1]
    if (file_format == "stl"):
        return read_stl(path)
    elif (file_format == "ply"):
        return read_ply(path)

def write_stl(data, fileName):
    """
    Stl writer. Takes a polydata
    """

    stlWriter = vtk.vtkSTLWriter()
    stlWriter.SetFileName(fileName)
    stlWriter.SetFileTypeToBinary()
    stlWriter.SetInputData(data)
    stlWriter.Write()

def write_ply(data, fileName):
    """
    Ply writer. Takes a polydata
    """

    plyWriter = vtk.vtkPLYWriter()
    plyWriter.SetFileName(fileName)
    plyWriter.SetFileTypeToBinary()
    plyWriter.SetInputData(data)
    plyWriter.Write()

def write_vtk(data, fileName):
    """
    Vtk file writer. Takes a polydata
    """

    polyWriter = vtk.vtkPolyDataWriter()
    polyWriter.SetInputData(data)
    polyWriter.SetFileName(fileName)
    polyWriter.Write()

def write(data, path):
    """
    General file writer. Takes a polydata
    """

    file_format = path.split(".")[-1]
    if (file_format == "stl"):
        return write_stl(data, path)
    elif (file_format == "ply"):
        return write_ply(data, path)

def ply_to_stl(path):
    mesh = read_ply(path)
    stl_path = path.split(".")[0] + ".stl"
    write(mesh, stl_path)
    return stl_path

def get_vertices(mesh):
    """
    Returns vertices of a mesh in numpy array format.
    """

    return numpy_support.vtk_to_numpy(mesh.GetPoints().GetData())

def getFaces(meshFaces):
    """
    Returns faces of a mesh in numpy array format.
    """

    faces = [[meshFaces[i+1], meshFaces[i+2], meshFaces[i+3]] for i in range(0, len(meshFaces), 4)]
    return np.array(faces)

def getConnectedVertices(mesh, i):
    """
    Giveng a mesh and an vertex index, return vertices connectd to that vertex
    """

    vertices = mesh.GetPoints()
    faces = getFaces(mesh.faces)
    connected = []
    connected_faces_indices = np.where(faces == i)[0]
    connected_faces = faces[connected_faces_indices]
    for f in connected_faces:
        if (f[0] == i):
            connected.append(f[1])
            connected.append(f[2])
        elif (f[1] == i):
            connected.append(f[0])
            connected.append(f[2])
        elif (f[2] == i):
            connected.append(f[0])
            connected.append(f[1])
    return set(connected)

def get_transformation_matrix(rotation, ang = 'rad', translation = [0,0,0]):
    if ang == 'deg':
        rotation = np.deg2rad(rotation)

    [angx, angy, angz] = rotation
    Rx = np.array([[1, 0, 0, 0],
                    [0, np.cos(angx), -np.sin(angx), 0],
                    [0, np.sin(angx), np.cos(angx), 0], 
                    [0, 0, 0, 1]])
    Ry = np.array([[np.cos(angy), 0, np.sin(angy), 0],
                    [0, 1, 0, 0],
                    [-np.sin(angy), 0, np.cos(angy), 0],
                    [0, 0, 0, 1]])
    Rz = np.array([[np.cos(angz), -np.sin(angz), 0, 0],
                    [np.sin(angz), np.cos(angz), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    R = np.dot(np.dot(Rz, Ry), Rx)
    R[3,:] = np.append(translation, 1)
    return R

def vtkmatrix_to_numpy(matrix):
    """
    Converts a vtk matrix to a numpy one.
    """

    m = np.ones((4, 4))
    for i in range(4):
        for j in range(4):
            m[i, j] = matrix.GetElement(i, j)
    return m

def npmatrix_to_vtk(matrix):
    """
    Converts a numpy matrix to a vtk one.
    """

    vtk_matrix = vtk.vtkMatrix4x4()
    for i in range(0, 4):
        for j in range(0, 4):
            vtk_matrix.SetElement(i, j, matrix[i, j])
    return vtk_matrix


def transform_point(matrix, point):
    """
    Takes a point an apply a transformation matrix to it.
    """

    transformed = np.dot(vtkmatrix_to_numpy(matrix), np.append(point, 1))
    final = [transformed[0], transformed[1], transformed[2]]
    return final

def transform_points(matrix, points):
    """
    Takes a point an apply a transformation matrix to it.
    """
    result = [transform_point(matrix, p) for p in points]
    return np.array(result)

def normalize_values(values):
    """
    Normalizes an array of vectors.
    """

    result = [i / np.linalg.norm(i) for i in values]
    return np.array(result)

def tuples_to_dict(tuples):
    """
    Creates a dictionary: point_name -> point_id
    """

    dictionary = {}
    for t in tuples:
        dictionary[t[1].lower()] = t[0]
    return dictionary

def query_dict(dict, points, vertices):
    """
    Given dictionary, array of landmark names and mesh vertices, returns array of landmark coordinates.
    """

    result = []
    for p in points:
        id = (int)(dict[p])
        result.append(np.array(vertices.GetPoint(id)))
    return np.array(result)

def create_stl_different_topology(mesh):

    vertices = get_vertices(mesh)
    faces = getFaces(pv.PolyData(mesh).faces)
    indices = np.arange(len(vertices))
    indices_random = np.arange(len(vertices))
    np.random.shuffle(indices_random)
    vertices_randomized = vertices[indices_random]
    correspondences = dict(zip(indices_random, indices))
    faces_new = []
    for face in faces :
        elem = (3, correspondences[face[0]], correspondences[face[1]], correspondences[face[2]])
        faces_new.append(elem)

    return pv.PolyData(vertices_randomized, np.array(faces_new))

def get_landmarks_for_registration(static_lmk, moving_lmk):

    static_landmarks = vtk.vtkPoints()
    moving_landmarks = vtk.vtkPoints()

    for point in static_lmk:
        static_landmarks.InsertNextPoint(point)
    for point in moving_lmk:
        moving_landmarks.InsertNextPoint(point)
    return static_landmarks, moving_landmarks

def appendPD(pathList):
    appendFilter = vtk.vtkAppendPolyData()
    for p in pathList:
        appendFilter.AddInputData(p)
    appendFilter.Update()
    return appendFilter.GetOutput()

def calcQuartile(values):
    """
    Calculate the first and third quartiles to find whiskers for setting of color map
    """
    quartiles = np.percentile(values, [25, 75])
    min = quartiles[0] - 1.5*(quartiles[1] - quartiles[0])
    max = quartiles[1] + 1.5*(quartiles[1]  - quartiles[0])
    return min, max