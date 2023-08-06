
import vtk
import numpy as np
from SocketFactory.registration.ampscan_sanders import core, align
from SocketFactory.utilities import utility

def apply_transformation(mesh, matrix):
    """
    Given a mesh and a matrix, apply transformation to it.
    """

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(mesh)
    transform = vtk.vtkTransform()
    transform.Concatenate(matrix)
    transformFilter.SetTransform(transform)
    transformFilter.Update()
    transformedSource = transformFilter.GetOutput()
    return transformedSource

def run_landmarks_registration(static, moving, static_landmarks, moving_landmarks, landmarkTransformType):
    """
    Based on two landmarks pointset, transform computed gives the best fit mapping one onto the other, in a least squ
    ares sense.

    Parameters
     ----------
     static: vtkPolyData
        static mesh, to which align moving
     moving: vtkPolydata
        moving mesh, to be registered to other
    static_landmarks: vtkPoints
        landmarks taken on static mesh
    static_landmarks: vtkPoints
        landmarks taken on moving mesh
    landmarkTransformType: str
        type of registration to be used (RigidBody, Similarity, Affine)
    """

    transform = vtk.vtkLandmarkTransform()
    transform.SetSourceLandmarks(static_landmarks)
    transform.SetTargetLandmarks(moving_landmarks)

    if landmarkTransformType == "RigidBody":
      transform.SetModeToRigidBody()
    # Similarity: rotation, translation and isotropic scaling. 
    elif landmarkTransformType == "Similarity":
      transform.SetModeToSimilarity()
    # Affine: collinearity is preserved. Ratios of distances along a line are preserved. 
    elif landmarkTransformType == "Affine":    
      transform.SetModeToAffine()
    else:
      print("Method not supported")

    transform.Update()
    outputMatrix = vtk.vtkMatrix4x4()
    transform.GetMatrix(outputMatrix)
    return transform


def run_icp_vtk(static, moving, meanDistanceType, landmarkTransformType, numberOfIterations = 50,
        checkMeanDistance = 0, maxDistance = 0.01, numberOfLandmarks = 200):
    """
    Run icp algorithm provided by vtk.

     Parameters
     ----------
     static: vtkPolyData
        static mesh, to which align moving
     moving: vtkPolydata
        moving mesh, to be registered to other
     meanDistanceType: str
        how to compute distance between closest points
     landmarkTransformType: str
        type of registration to be used (RigidBody, Similarity, Affine)
     numberOfIterations: int, default 50
        maximum number of iterations
     checkMeanDistance: boolean, default False
        whether to force the algorithm to check the mean distance between two iterations
     maxDistance: float, default 0.01
        maximum mean distance between two iteration. If the mean
        distance is lower than this, the convergence stops
     numberOfLandmarks: int, default 200
        maximum number of landmarks sampled in your dataset
    """
    
    icp = vtk.vtkIterativeClosestPointTransform()

    icp.SetSource(static)
    icp.SetTarget(moving)

    # Rigidbody: rotation and translation only. 
    if landmarkTransformType == "RigidBody":
      icp.GetLandmarkTransform().SetModeToRigidBody()
    # Similarity: rotation, translation and isotropic scaling. 
    elif landmarkTransformType == "Similarity":
      icp.GetLandmarkTransform().SetModeToSimilarity()
    # Affine: collinearity is preserved. Ratios of distances along a line are preserved. 
    elif landmarkTransformType == "Affine":    
      icp.GetLandmarkTransform().SetModeToAffine()
    else:
      print("Method not supported")

    # RMS mode is the square root of the average of the sum of squares of the closest point distances. 
    if meanDistanceType == "RMS":
      icp.SetMeanDistanceModeToRMS()
    # Absolute Value mode is the mean of the sum of absolute values of the closest point distances. 
    elif meanDistanceType == "Absolute Value":
      icp.SetMeanDistanceModeToAbsoluteValue()

    icp.SetMaximumNumberOfIterations(numberOfIterations)
    icp.SetMaximumMeanDistance(maxDistance)
    icp.SetMaximumNumberOfLandmarks(numberOfLandmarks)
    icp.SetCheckMeanDistance(int(checkMeanDistance))

    # Starts the process by translating source centroid to target centroid.
    icp.StartByMatchingCentroidsOn()

    icp.Update()
    outputMatrix = vtk.vtkMatrix4x4()
    icp.GetMatrix(outputMatrix)
    
    return icp

def run_thinPlateSpline_transform(mesh, static_landmarks, moving_landmarks, sigma = 1.0):
    """
    Apply thin plate spline transform to mesh. Warping will be done by landmarks alignment.
    
    Parameters
    ----------
    mesh: vtkPolyData
        mesh to which transform will be applied
    static_landmarks: vtkPoints
        landmarks taken on static mesh
    static_landmarks: vtkPoints
        landmarks taken on moving mesh
    sigma: float, optional, default 1.0
        'stiffness' (rigidity) of the spline
    """

    tps = vtk.vtkThinPlateSplineTransform()
    tps.SetSourceLandmarks(static_landmarks)
    tps.SetTargetLandmarks(moving_landmarks)
    tps.SetBasisToR() # Use of R kernel
    tps.Inverse()
    tps.SetSigma(sigma)
    tps.Modified()
    tps.Update()

    t1 = vtk.vtkGeneralTransform()
    t1.SetInput(tps)
    tf = vtk.vtkTransformPolyDataFilter()
    tf.SetInputData(mesh)
    tf.SetTransform(t1)
    tf.Update()
    warped = tf.GetOutput()
    return warped

def run_procrustes_transform(meshes, method):
    """
    Run procrustes algorithm using a group of meshes.
    
    Parameters
    ----------
    meshes: array of vtkPolyData
        meshes taken as input by algorithm
    method: str
        type of registration to be used (RigidBody, Similarity, Affine)
    """

    meshes_group = vtk.vtkMultiBlockDataGroupFilter()
    for mesh in meshes:
        meshes_group.AddInputData(mesh)

    procrustes = vtk.vtkProcrustesAlignmentFilter()
    procrustes.SetInputConnection(meshes_group.GetOutputPort())
    if method == "RigidBody" :
        procrustes.GetLandmarkTransform().SetModeToRigidBody()
    elif method == "Similarity" :
        procrustes.GetLandmarkTransform().SetModeToSimilarity()
    elif method == "Affine" :
        procrustes.GetLandmarkTransform().SetModeToAffine()
    else:
        print("Method not supported")
    procrustes.Update()

    outputMatrix = vtk.vtkMatrix4x4()
    procrustes.GetLandmarkTransform().GetMatrix(outputMatrix)
    return procrustes

def load_ampscan_meshes(static_path, moving_path):

    if (static_path.split(".")[-1] == "ply") :
        static_path = utility.ply_to_stl(static_path)
        
    if (moving_path.split(".")[-1] == "ply") :
        moving_path = utility.ply_to_stl(moving_path)

    static = core.AmpObject(static_path)
    moving = core.AmpObject(moving_path)
    return static, moving

def run_sanders_alignment(static, moving, max_iteration, weights = [(1, 0), (0.8, 0.2)]):
    """
    Run J.E. Sanders algorithm implemented inside ampscan libary.

     Parameters
     ----------
     static: AmpObject
        static mesh, to which align moving
     moving: AmpObject
        moving mesh, to be registered to other
    max_iteration: int
        maximum number of iterations to be performed
    weights:
        sets of weights for registration steps (first is RE weight, second is similarity weight)
    """

    al = align.align(moving, static, maxiter = 0)
    al.runICP(maxiter = max_iteration, weights = weights)
    return al
