from vtk.util import numpy_support
import numpy as np
from SocketFactory.utilities import utility, file_handler
import os 

def find_point_geodesic_path(polydata, distance, percentage):

    new_distance = distance * (1 - percentage)
    points = polydata.GetPoints() 
    np_data = numpy_support.vtk_to_numpy(points.GetData())
    p_prec = None
    for p in np_data:
        if p_prec is None:
            p_prec = p
        else:
            p_succ = p
            d = np.linalg.norm(np.array(p_prec) - np.array(p_succ))
            p_prec = p_succ
            new_distance -= d
            if new_distance <= 0 :
                return p_prec

def compute_path_distance(mesh, starting_point_index, ending_point_index, file_name):

    path = mesh.geodesic(starting_point_index, ending_point_index)
    distance = (mesh.geodesic_distance(starting_point_index, ending_point_index))
    utility.write(path, file_name)
    return path, distance


def compute_all_lmk_paths_distances(mesh, lmk_dict, file_path, ending_point_name, ws):
    
    # Get index of ending point
    ending_point_index = int(lmk_dict[ending_point_name])
    # Dictionary: landmark name -> landmark id
    lmk_dict = {k: int(v) for k, v in lmk_dict.items()}
    # Remove ending point from dictionary (can't compute distance from same point)
    del lmk_dict[ending_point_name]
    # Order landmarks by name to have comparable data among meshes
    lmk_sorted_names = np.sort(list(lmk_dict.keys()))
    main_path, dir_path, fileName = file_handler.create_dir_by_filename(file_path, '_geodesic_paths')
    df_row = [fileName]

    paths = []

    for starting_point_name in lmk_sorted_names:
        points_name = starting_point_name + '_' + ending_point_name
        starting_point_index = lmk_dict[starting_point_name]
        df_row.extend([points_name])

        file_name = os.path.join(dir_path, points_name + '.ply')
        path, distance = compute_path_distance(mesh, starting_point_index, ending_point_index, file_name)
        
        paths.append(path)

        df_row.extend([distance, ""])
        
    ws.append(df_row)
    return ws, main_path, paths




    





