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

class SolidSTL( object ):

    def __init__(self, title=None, numTriangles=0, triangles=None, norms=None, bytecount=None, maxLen=-1.0):
        self.title = title
        self.numTriangles = numTriangles
        self.triangles = triangles
        self.norms = norms
        self.bytecount = bytecount
    
    def display(self):
        fig = plt.figure()
        ax = Axes3D(fig)
        
        for triangle in self.triangles:
            if self.maxLen > 0:
                tri = []
                for vert in triangle:
                    tri.append(map(lambda x: x/self.maxLen, vert))
            ax.add_collection3d(Poly3DCollection([tri]))
        

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
    main()
