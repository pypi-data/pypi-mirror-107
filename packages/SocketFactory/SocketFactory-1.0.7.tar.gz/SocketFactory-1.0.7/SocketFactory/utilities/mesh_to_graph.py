
import networkx as nx
import vtk
import numpy as np
from networkx_query import search_nodes, search_edges
from SocketFactory.utilities import utility

def meshVertexGraph(mesh, weightMode):
    """ 
    Creates a networkx graph with mesh vertices as nodes and mesh edges as edges.
    """
    
    # Create graph
    g = nx.Graph()
    points = mesh.GetPoints()
    
    for i in range(points.GetNumberOfPoints()):
        pt3D = points.GetPoint(i)
        
        # Add node to graph and get its neighbours
        g.add_node(i, point = pt3D)
        neighbours = utility.getConnectedVertices(mesh, i)
        # Add edges to graph
        for n in neighbours:
            if n > i:
                p1 = points.GetPoint(i)
                p2 = points.GetPoint(n)
                line = vtk.vtkLineSource()
                line.SetPoint1(p1)
                line.SetPoint2(p2)
                line.Update()
                
                if weightMode == "edgeLength":
                    w = np.linalg.norm(np.array(p1) - np.array(p2))
                elif weightMode == "sameWeight":
                    w = 1
                g.add_edge(i, n, weight = w, line = line)
    return g

def meshQualityGraph(mesh, qualities):
    """ 
    Creates a networkx graph with mesh vertices as nodes and mesh edges as edges.
    """
    
    # Create graph
    print("Creating graph...")
    g = nx.Graph()
    points = mesh.GetPoints()
    
    for i in range(points.GetNumberOfPoints()):
        pt3D = points.GetPoint(i)
        
        # Add node to graph and get its neighbours
        g.add_node(i, point = pt3D, weight = qualities[i])
        neighbours = utility.getConnectedVertices(mesh, i)
        # Add edges to graph
        for n in neighbours:
            if n > i:
                p1 = points.GetPoint(i)
                p2 = points.GetPoint(n)
                line = vtk.vtkLineSource()
                line.SetPoint1(p1)
                line.SetPoint2(p2)
                line.Update()
                g.add_edge(i, n, line = line)
    return g

def query_graph(graph, comparison, threshold):
    """
    Query graph: return vertices ids that respond to query.
    """

    return [node_id for node_id in search_nodes(graph, {comparison: [("weight",), threshold]})]