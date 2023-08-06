
from plyfile import PlyData, PlyElement
import numpy as np
import pandas as pd
import vtk
from SocketFactory.utilities import utility
from openpyxl import Workbook
import os

def read_points(path):
    """
    Reader of landmarks file.
    """

    file = open(path, "r")
    lines  = file.read().split('\n')
    points = []
    for line in lines:
        if (len(line) > 0):
            tmp = line.split(" - ")
            point_id = tmp[0]
            point_name = tmp[1]
            points.append((point_id, point_name))
    file.close()
    lmk_dict = utility.tuples_to_dict(points)
    return lmk_dict

def write_point(file, point_id, point_name):
    """
    Writes a landmark in a file.
    """

    file.write(str(point_id) + " - " + 
               str(point_name) + "\n")

def read_alignment_file(path):
    """
    Reader of alignment file.
    """

    def get(input):
        return input.split(": ")[1]

    file = open(path, "r")
    lines  = file.read().split("\n")
    
    cut_point = get(lines[0]).lower()
    reference_alignment_points = [x.lower() for x in get(lines[1]).split(" ")]
    alignment_method = get(lines[2])
    landmarks_names = [x.lower() for x in get(lines[3]).split(" ")]
    origin = get(lines[4]).lower()
    file.close()
    return cut_point, reference_alignment_points, alignment_method, landmarks_names, origin

def split_name(path):
    """
    Returns splitted file name: folder path and file name
    """

    mainPath = os.path.dirname(path)
    fileName = os.path.basename(path).split(".")[0]
    return mainPath, fileName


def create_ply_with_colour(vert, faces, values, valueType, name, minValueSaturation, maxValueSaturation, comment = ''):
    """
    Given vertices and faces, creates a ply file associating quality and color to vertices.
    """

    def toTuple(z): 
        return tuple(z)

    def associate_colour(values, valueType, minValueSaturation, maxValueSaturation):
        ctf = vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToRGB()

        if ((valueType == 'normal_similarity') |  (valueType == 'snae')):
            ctf.AddRGBPoint(minValueSaturation, 1.0, 1.0, 1.0)
            ctf.AddRGBPoint(maxValueSaturation, 0.0, 0.0, 1.0) 

        elif ((valueType == 're') | (valueType == 'vv')):
            ctf.SetColorSpaceToDiverging() 
            ctf.AddRGBPoint(minValueSaturation, 1.0, 0.0, 0.0) #set lower whisker to red
            ctf.AddRGBPoint(0,1,1,1) #set zero to white
            ctf.AddRGBPoint(maxValueSaturation, 0.0, 0.0, 1.0) #set higher whisker to blue

        colour = [] 
        for i in range(len(values)):
            c = ctf.GetColor(values[i]) 
            colour.append((round(c[0]*255), round(c[1]*255), round(c[2]*255)))
        return colour

    def appendQuality_colour(vertices, values, colour):
        result = []
        for x, y, z in zip(vertices, values, colour):
            result.append(x + (y,) + z)
        return result

    vertices = list(map(toTuple, vert))            
    colour =  associate_colour(values, valueType, minValueSaturation, maxValueSaturation)
    vertices_value = appendQuality_colour(vertices, values, colour)
    vertex = np.array(vertices_value, dtype = [('x', 'f4'), ('y', 'f4'),('z', 'f4'),('quality','f4'), 
                                                ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])

    face = np.array(faces, dtype='i4')
    ply_faces = np.empty(len(face), dtype=[('vertex_indices', 'i4', (3,))])
    ply_faces['vertex_indices'] = face

    ply = PlyData(
        [
            PlyElement.describe(
                vertex, 'vertex',
                comments = [comment]
            ),
            PlyElement.describe(ply_faces, 'face')
        ],text = True)

    PlyData(ply).write(name)

def convertPlyToXlsx(path):
    """
    From ply to xlsx file converter.
    """

    plydata = PlyData.read(path)
    qualities = plydata['vertex']['quality']
    df = pd.DataFrame(qualities, columns=['quality'])
    df.to_excel(path.split(".")[0] + ".xlsx", index=False)

def getFaces(meshFaces):
    faces = []
    for i in range(0, len(meshFaces), 4):
        faces.append([meshFaces[i+1], meshFaces[i+2], meshFaces[i+3]])
    return np.array(faces)

def get_common_landmarks(static, moving, static_lmk_path, moving_lmk_path):
    """
    Given two sets of landmarks, returns only common one coordinates.
    """

    static_lmk_dict = read_points(static_lmk_path)
    moving_lmk_dict = read_points(moving_lmk_path)
    common_lmk = list(set(static_lmk_dict.keys()).intersection(set(moving_lmk_dict.keys())))
    static_lmk = utility.query_dict(static_lmk_dict, common_lmk, static.GetPoints())
    moving_lmk = utility.query_dict(moving_lmk_dict, common_lmk, moving.GetPoints())
    return static_lmk, moving_lmk

def read_alignment_points(static, moving, static_lmk_path, moving_lmk_path):
    """
    Read two sets of landmarks and returns common landmarks coordinates as vtkPoints.
    """

    static_lmk, moving_lmk = get_common_landmarks(static, moving, static_lmk_path, moving_lmk_path)
    static_landmarks = vtk.vtkPoints()
    moving_landmarks = vtk.vtkPoints()

    for point in static_lmk:
        static_landmarks.InsertNextPoint(point)
    for point in moving_lmk:
        moving_landmarks.InsertNextPoint(point)
    return static_landmarks, moving_landmarks

def create_pts_file(ref_path, tar_path, ref_landmark_path, tar_landmark_path):
    """
    Given a reference and a target mesh, creates a .pts file comparing common landmarks.
    """

    output_file_path = ref_path.split(".")[0] + ".pts"
   
    reference_mesh = utility.read(ref_path)
    target_mesh = utility.read(tar_path)

    reference_coordinates, target_coordinates = get_common_landmarks(reference_mesh, target_mesh, ref_landmark_path, tar_landmark_path)
    landmarks_displacement = target_coordinates - reference_coordinates

    file = open(output_file_path, "w+")
    file.write(str(len(reference_coordinates)) + "\n")

    def create_point_string(point):
        return str(point[0]) + " " + str(point[1]) + " " + str(point[2]) + " "

    for l, d in zip(target_coordinates, landmarks_displacement):
        file.write(create_point_string(l) + create_point_string(d) + "0 0 s p\n")

    file.close()

def create_dir(mesh_path, name_add_to_folder):
    main_path = os.path.dirname(mesh_path)
    dir_name = os.path.join(main_path, name_add_to_folder)
    try:
        os.mkdir(dir_name)
    except OSError:
        print("")
    return dir_name

def create_dir_by_filename(mesh_path, name_add_to_folder = ""):

    main_path, file_name = split_name(mesh_path)
    dir_name = os.path.join(main_path, file_name + name_add_to_folder)
    try:
        os.mkdir(dir_name)
    except OSError:
        print("")
    return main_path, dir_name, file_name


def create_pca_output_file(pca, output_path):

    wb = Workbook()
    ws = wb.active
    ws.append(["Eigenvalues"])
    ws.append(list(map(lambda x : float(x), pca.lambda_r)))
    ws.append(["Eigenvectors"])
    for v in pca.V_r:
        ws.append(list(map(lambda x : float(x), v)))
    ws.append(["Explained variance"])
    ws.append(list(map(lambda x : float(x), pca.lamda_ratios_r)))
    wb.save(output_path)