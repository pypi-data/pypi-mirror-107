import vtk

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