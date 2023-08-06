
from scipy import spatial
import pymeshlab as ml
import numpy as np

def find_closest_points(ref_vert, mea_vert, ref_norms):
    """
    For each vertex of measured mesh, find the closest point in the reference mesh
    """
    kdTree = spatial.cKDTree(ref_vert)
    [dist, idx] = kdTree.query(mea_vert, 1)
    return ref_vert[idx], ref_norms[idx]

def compute_vv_distance(ref_vert, mea_vert, ref_norm):
    """
    Signed vertex-to-vertex distance with the same index
    """
    dist = mea_vert - ref_vert
    values = np.linalg.norm(dist, axis = 1)
    polarity = np.sum(dist * ref_norm, axis = 1) < 0
    values[polarity] *= -1.0
    return values 

def compute_re_distance(ref_vert, mea_vert, ref_norms):
    """
    Signed distance between vertex and closest point
    Resulting distance is projected on the reference normal
    """
    dist = mea_vert - ref_vert
    proj_dist = np.sum(dist * ref_norms, axis = 1)
    return proj_dist

def compute_ms_distance(path_ref, path_mea, path_out):
    """
    Compute the signed per vertex distance between (measured) mesh and reference mesh
    Pymeshlab filter --> Distance from reference mesh
    """
    ms = ml.MeshSet()
    ms.load_new_mesh(path_ref)
    ms.load_new_mesh(path_mea)
    ms.apply_filter('distance_from_reference_mesh', signeddist = True, measuremesh = 1, refmesh = 0)
    ms.save_current_mesh(path_out, save_vertex_quality = True)


def compute_normal_similarity(ref_norm, mea_norm):
    '''
    J.E. Sanders Parameters
    Mean hyperbolic arctangent of the dot product of the normals
    '''
    result = np.sum(ref_norm * mea_norm, axis = 1) - 10e-7
    atanh = np.arctanh(result)
    return atanh

def compute_snae(ref_norm, mea_norm):
    '''
    J.E. Sanders Parameters
    Mean Surface Normal Angle Error
    Arccos(degrees) of the dot product of the normals
    '''
    result = np.sum(ref_norm * mea_norm, axis = 1)
    index_error = np.where(result > 1)
    result[index_error] = 1
    acos = np.arccos(result)
    return np.rad2deg(acos) 

def compute_colorize(mesh_path_in, mesh_path_out):
    ms = ml.MeshSet()
    ms.load_new_mesh(mesh_path_in)
    ms.apply_filter('quality_mapper_applier', tfslist = 'French RGB')
    ms.save_current_mesh(mesh_path_out)