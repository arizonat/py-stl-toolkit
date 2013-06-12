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

class SolidSTL( object ):

    def __init__(self, title=None, numTriangles=0, triangles=None, norms=None, bytecount=None, maxLen=-1.0):
        self.title = title
        self.numTriangles = numTriangles
        self.triangles = triangles
        self.norms = norms
        self.bytecount = bytecount
        self.maxLen = maxLen

        self.faces = None
        self.vertices = None
        self.edges = None

    def getNumEdges(self):
        return len(self.getEdges())

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
            print str(tri_edges)
            self.edges.update(tri_edges)
        
        return self.edges
    
    def getNumFaces(self):
        return len(self.getFaces())

    def getFaces(self):
        """
        WARNING: THIS IS THE NUMBER OF TRIANGLE EDGES, NOT THE OVERALL EDGES OF THE SOLID
        """
        return self.triangles

    def getNumVertices(self):
        return len(self.getVertices())

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

    def isSimple(self):
        """
        Uses Euler's formula for polyhedron's to determine if the 
        solid is simple (has no "holes" and is convex)
        
        In short, verifies: V - E + F = 2
        """
        V = self.getNumVertices()
        E = self.getNumEdges()
        F = self.getNumFaces()
        return V - E + F == 2

    def display(self):
        fig = plt.figure()
        #ax = Axes3D(fig)
        ax = fig.gca(projection='3d')

        def __getNormalLine(origin, vector):
            return tuple([np.linspace(start, stop, 10) for start, stop in zip(origin, vector)])

        def __getCentroid(triangle):
            # group the xs, ys, and zs
            coordGroups = zip(triangle[0], triangle[1], triangle[2])
            centroid = tuple([sum(coordGroup)/3.0 for coordGroup in coordGroups])
            return centroid

        for i in xrange(len(self.triangles)):
            
            triangle = self.triangles[i]
            
            #self.maxLen = -1
            #if self.maxLen > 0:
            #    tri = []
            #    for vert in triangle:
            #        tri.append(map(lambda x: x/self.maxLen, vert))
            #else:
            #    tri = triangle
            
            face = Poly3DCollection([triangle])
            face.set_alpha(0.5)
            ax.add_collection3d(face)
            
            centroid = __getCentroid(triangle)
            print str(centroid)
            norm = self.norms[i]
            xs, ys, zs = __getNormalLine(centroid, norm)
            ax.plot(xs, ys, zs)

        plt.show()

def parseBSTL(bstl):
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
    maxLen = 0.0

    for i in xrange(numTriangles):
        # facet records
        norms[i] = struct.unpack("<3f", f.read(12))
        vertex1 = struct.unpack("<3f", f.read(12))
        vertex2 = struct.unpack("<3f", f.read(12))
        vertex3 = struct.unpack("<3f", f.read(12))
        bytecounts[i] = struct.unpack("H", f.read(2)) # not sure what this is

        m = max(max(vertex1), max(vertex2), max(vertex3))
        if m > maxLen:
            maxLen = m

        triangles[i] = (vertex1, vertex2, vertex3)
    
    return SolidSTL(header, numTriangles, triangles, norms, bytecounts, maxLen)

# from (will be modified soon)
# http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file    
def write_as_ascii(outfilename):
    f = open(outfilename, "w")
    f.write("solid "+outfilename+"\n")
    for n in range(len(triangles)):
        f.write("facet normal {}{}{}\n".format(normals[n][0], normals[n][1], normals[n][2]))
        f.write("outer loop\n")
        f.write("vertex {} {} {}\n".format())
        f.write("vertex {} {} {}\n".format())
        f.write("vertex {} {} {}\n".format())
        f.write("endloop\n")
        f.write("endfacet\n")
    f.write("endsolid "+outfilename+"\n")
    f.close()

def main():
    pass

if __name__ == "__main__":
    model = parseBSTL(sys.argv[1])
    model.display()

