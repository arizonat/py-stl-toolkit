"""
This module provides basic STL parsing, saving, displaying, and post-processing capabilities

File format described at http://people.sc.fsu.edu/~jburkardt/data/stlb/stlb.html
Bytecount described at http://en.wikipedia.org/wiki/STL_(file_format)
Help and original code from: http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file
"""

import struct
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys

SCALE_INCH = 1.0
SCALE_CM = 1.0

class SolidSTL(object):

    def __init__(self, title=None, numTriangles=0, triangles=None, norms=None, bytecount=None):
        self.title = title
        self.numTriangles = numTriangles
        self.triangles = triangles
        self.norms = norms
        self.bytecount = bytecount

        self.faces = None
        self.vertices = None
        self.edges = None

    def getEdges(self):
        """
        WARNING: THIS IS THE NUMBER OF TRIANGLE EDGES, NOT THE OVERALL EDGES OF THE SOLID
        """
        if self.edges:
            return self.edges

        def getSortedEdges(triangle):
            edges = set()
            for vertex1 in triangle:
                for vertex2 in triangle:
                    if not vertex1 == vertex2:
                        edge = ((vertex1, vertex2), (vertex2, vertex1))[vertex1 > vertex2]
                        edges.add(edge)
            return edges

        self.edges = set()
        for triangle in self.triangles:
            tri_edges = getSortedEdges(triangle)
            self.edges.update(tri_edges)
        
        return self.edges
    
    def getFaces(self):
        """
        WARNING: THIS IS THE NUMBER OF TRIANGLE EDGES, NOT THE OVERALL EDGES OF THE SOLID
        """
        return self.triangles

    def getVertices(self):
        """
        WARNING: THIS IS THE NUMBER OF TRIANGLE EDGES, NOT THE OVERALL EDGES OF THE SOLID
        """
        if self.vertices:
            return self.vertices
        
        self.vertices = set()
        for triangle in self.triangles:
            for vertex in triangle:
                self.vertices.add(vertex)

        return self.vertices

def addCuboidSupport(stlsolid, triangle):
    pass

def addCuboidSupports(stlsolid, area=1.0, minHeight=1.0):
    # iterate through each triangle
    
    # add a cuboid from each negative z-normal to the base

    pass

def rotate(theta, axis="x", units="degrees"):
    pass

def stretch():
    pass

def isSimple(stlsolid):
    """
    Uses Euler's formula for polyhedron's to determine if the 
    solid is simple (has no "holes" and is convex)
    
    In short, verifies: V - E + F = 2
    """
    
    if not isinstance(stlsolid, SolidSTL):
        raise TypeError("Incorrect type, expected stlparser.SolidSTL")

    V = len(stlsolid.getVertices())
    E = len(stlsolid.getEdges())
    F = len(stlsolid.getFaces())
    return V - E + F == 2
    
def __getNormalLine(origin, vector, scale=1.0):
    """
    Returns a plottable line represented by a 3-tuple where each element is an array
    for a single axis. First element is all x-coordinates, second is all y-coordinates, etc...
    """
    vector = np.array(vector) * scale
    endpoint = tuple([sum(el) for el in zip(origin, vector)])
    return tuple([np.linspace(start, stop, 10) for start, stop in zip(origin, endpoint)])

def __getTriangleCentroid(triangle):
    """
    Returns the centroid of a triangle in 3D-space
    """
    # group the xs, ys, and zs
    coordGroups = zip(triangle[0], triangle[1], triangle[2])
    centroid = tuple([sum(coordGroup)/3.0 for coordGroup in coordGroups])
    return centroid

def __getSupportDirection(origin, vector, scale=1.0):
    z = vector[2]
    
    if z < 0:
        down = [0, 0, -1]
        return __getNormalLine(origin, down, scale)
    # Does not require support material, don't plot anything
    return ([],[],[])
    
def display(stlsolid, showNorms=False, showSupportDirections=True):
    """
    Renders the solid and normal vectors using matplotlib
    """
    fig = plt.figure()
    #ax = Axes3D(fig)
    ax = fig.gca(projection='3d')
    
    triangles = stlsolid.triangles
    norms = stlsolid.norms

    for i in xrange(len(triangles)):
            
        triangle = triangles[i]
        
        face = Poly3DCollection([triangle])
        face.set_alpha(0.5)
        ax.add_collection3d(face)

        if showNorms or showSupportDirections:
            centroid = __getTriangleCentroid(triangle)
            norm = norms[i]
        
            if showNorms:
                xs, ys, zs = __getNormalLine(centroid, norm, 10)
                ax.plot(xs, ys, zs)

            if showSupportDirections:
                xs, ys, zs = __getSupportDirection(centroid, norm, 10)
                ax.plot(xs, ys, zs)

    plt.show()

def loadBSTL(bstl):
    """
    Loads triangles from file, input can be a file path or a file handler
    Returns a SolidSTL object
    """

    if isinstance(bstl, file):
        f = bstl
    elif isinstance(bstl, str):
        f = open(bstl, 'rb')
    else:
        raise TypeError("must be a string or file")
    
    header = f.read(80)
    numTriangles = struct.unpack("@i", f.read(4))
    numTriangles = numTriangles[0]

    triangles = [(0,0,0)]*numTriangles # prealloc, slightly faster than append
    norms = [(0,0,0)]*numTriangles
    bytecounts = [(0,0,0)]*numTriangles

    for i in xrange(numTriangles):
        # facet records
        norms[i] = struct.unpack("<3f", f.read(12))
        vertex1 = struct.unpack("<3f", f.read(12))
        vertex2 = struct.unpack("<3f", f.read(12))
        vertex3 = struct.unpack("<3f", f.read(12))
        bytecounts[i] = struct.unpack("H", f.read(2)) # not sure what this is

        triangles[i] = (vertex1, vertex2, vertex3)
    
    return SolidSTL(header, numTriangles, triangles, norms, bytecounts)

# from (will be modified soon)
# http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file    
def saveSTL(stlsolid, outfilename):
    """
    Saves the solid in standard STL format
    """

    if not isinstance(stlsolid, SolidSTL):
        raise TypeError("Must be of type SolidSTL")

    triangles = stlsolid.triangles
    norms = stlsolid.norms

    with open(outfilename, "w") as f:

        f.write("solid "+outfilename+"\n")
        for i in xrange(len(triangles)):
            norm = norms[i]
            triangle = triangles[i]
            f.write("facet normal %f %f %f\n"%(norm))
            f.write("outer loop\n")
            f.write("vertex %f %f %f\n"%triangle[0])
            f.write("vertex %f %f %f\n"%triangle[1])
            f.write("vertex %f %f %f\n"%triangle[2])
            f.write("endloop\n")
            f.write("endfacet\n")
        f.write("endsolid "+outfilename+"\n")

if __name__ == "__main__":
    model = parseBSTL(sys.argv[1])
    model.display()

