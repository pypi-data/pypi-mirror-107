
import vtk
import numpy as np
from SocketFactory.utilities import utility
import pyvista as pv

def generate_random_color():
    return [np.random.uniform(), np.random.uniform(), np.random.uniform()]

def draw_point(point, ren, color = [1,1,1], radius = 0.8):
    """
    Draw a point as a sphere in a vtk window.
    """

    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(point)
    sphereSource.SetRadius(radius)
    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
    sphereActor = vtk.vtkActor()
    sphereActor.GetProperty().SetColor(color)
    sphereActor.SetMapper(sphereMapper)
    ren.AddActor(sphereActor)
    return sphereActor

def add_text(name, pos, ren):
    """
    Add text to vtk visualization.
    """

    text = vtk.vtkTextSource()
    text.SetText(name)
    text.SetForegroundColor(1,0,0)
    text.SetBackgroundColor(1,1,1)
    textMapper = vtk.vtkPolyDataMapper()
    textMapper.SetInputConnection(text.GetOutputPort())

    textActor = vtk.vtkActor()
    x, y, z = pos[0], pos[1], pos[2]
    slack = 4
    z -= slack * 2
    if (x > 0) & (y > 0):
        x += slack
        y += slack
        textActor.SetOrientation(90,90,0)
    elif (x > 0) & (y < 0):
        x += slack
        y -= slack
        textActor.SetOrientation(90,0,0)
    elif (x < 0) & (y > 0):
        x -= slack
        y += slack
        textActor.SetOrientation(90,180,0)
    else :
        x -= slack
        y -= slack
        textActor.SetOrientation(90,90,180)
    textActor.AddPosition(x, y, z)
    textActor.SetScale(1, 1, 1)
    textActor.SetMapper(textMapper)

    ren.AddActor(textActor)
    return textActor

def draw_axes_custom(renderer, origin = [0,0,0], points = [(200,0,0), (0,200,0), (0,0,200)]) : 

    for i, point in enumerate(points) :
        color = [0,0,0]
        # set same colors of global axes: first (x) red, second (y) green, third (z) blue
        color[i] = 1
        line = vtk.vtkLineSource()
        line.SetPoint1(origin)
        line.SetPoint2(point)
        line.Update()
 
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(point)
        sphereSource.SetRadius(1)

        lineMapper = vtk.vtkPolyDataMapper()
        lineMapper.SetInputConnection(line.GetOutputPort())
        lineActor = vtk.vtkActor()
        lineActor.GetProperty().SetColor(color)
        lineActor.SetMapper(lineMapper)
        lineActor.GetProperty().SetLineWidth(2);

        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
        sphereActor = vtk.vtkActor()
        sphereActor.GetProperty().SetColor(color)
        sphereActor.SetMapper(sphereMapper)

        renderer.AddActor(sphereActor)
        renderer.AddActor(lineActor)


def visualize_mesh(mesh, show_axes = False):
    """
    Set up a simple vtk visualization of  mesh.
    """

    ren = vtk.vtkRenderer()
    if(show_axes):
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(100, 100, 100)
        ren.AddActor(axes)
 
    draw_axes_custom(ren)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(1200, 800)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iren.SetRenderWindow(renWin)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(mesh)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    ren.AddActor(actor) 
    
    iren.Initialize()
    camera = ren.GetActiveCamera()
    camera.ParallelProjectionOn()
    camera.OrthogonalizeViewUp()
    #camera.SetPosition(0, 50, 0)
            
    ren.ResetCamera()
    renWin.Render()
    iren.Start()

def visualize_meshes(meshes, colors = [], point_sets = []):
    """
    Set up a simple vtk visualization of some meshes with different colours.
    """

    if (len(colors) == 0):
        for i in range(len(meshes)):
            colors.append(generate_random_color())

    ren = vtk.vtkRenderer()
   
    for i, points in enumerate(point_sets):
 
        color = [0, 0, 0]
        color[i] = 0.9
        for p in points:
            draw_point(p, ren, radius = 2, color = color)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(1200, 800)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iren.SetRenderWindow(renWin)

    for mesh, color in zip(meshes, colors) :
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(color)
        actor.SetMapper(mapper)
        ren.AddActor(actor)    
    
    #draw_axes_custom(ren)
    iren.Initialize()
    camera = ren.GetActiveCamera()
    camera.ParallelProjectionOn()
    camera.OrthogonalizeViewUp()
            
    ren.ResetCamera()
    renWin.Render()
    iren.Start()


def render_geodesic(paths, mesh, point = []):
    p = pv.Plotter(notebook=0)
    for path in paths:
        p.add_mesh(path, line_width = 5, color = "red")
    if (len(point) > 0 ):
        p.add_mesh(point, render_points_as_spheres = True, point_size = 10, color = "blue")
    p.add_mesh(mesh, show_edges = False)
    p.show()

def visualize_procrustes_res(meshes, colors, procrustes1, procrustes2, procrustes3):

    def create_actor(mesh, color):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetDiffuseColor(color)
        return actor

    ren = vtk.vtkRenderer()
    ren2 = vtk.vtkRenderer()
    ren3 = vtk.vtkRenderer()
    ren4 = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.AddRenderer(ren2)
    renWin.AddRenderer(ren3)
    renWin.AddRenderer(ren4)
    renWin.SetSize(1200, 800)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iren.SetRenderWindow(renWin)

    for m, c in zip(meshes, colors):
        ren.AddActor(create_actor(m, c))

    for i, c in zip(range(len(meshes)), colors):
        ren2.AddActor(create_actor(procrustes1.GetOutput().GetBlock(i), c))
   
    for i, c in zip(range(len(meshes)), colors):
        ren3.AddActor(create_actor(procrustes2.GetOutput().GetBlock(i), c))
     
    for i, c in zip(range(len(meshes)), colors):
        ren4.AddActor(create_actor(procrustes3.GetOutput().GetBlock(i), c))

    ren.SetViewport(0.0, 0.5, 0.5, 1.0)
    ren.ResetCamera()

    ren2.SetViewport(0.5, 0.5, 1.0, 1.0)
    ren2.ResetCamera()

    ren3.SetViewport(0.0, 0.0, 0.5, 0.5)
    ren3.ResetCamera()

    ren4.SetViewport(0.5, 0.0, 1.0, 0.5)
    ren4.ResetCamera()

    iren.Initialize()
    renWin.Render()
    iren.Start()

def visualize_slices(mesh, pActors):

    ren = vtk.vtkRenderer()
    mesh_mapper = vtk.vtkPolyDataMapper()
    mesh_mapper.SetInputData(mesh)
    mesh_actor = vtk.vtkActor()
    mesh_actor.SetMapper(mesh_mapper)
    ren.AddActor(mesh_actor)   

    for actor in pActors:
        ren.AddActor(actor)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(1200, 800)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iren.SetRenderWindow(renWin)
    ren.SetBackground(0, 0, 0)
    renWin.Render()
    iren.Start()
