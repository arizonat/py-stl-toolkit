"""
This module provides basic STL parsing, saving, displaying, and post-processing capabilities

File format described at http://people.sc.fsu.edu/~jburkardt/data/stlb/stlb.html
Bytecount described at http://en.wikipedia.org/wiki/STL_(file_format)
Help and original code from: http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file
"""

import struct
import matplotlib

class SolidSTL( object ):
    NORM = 0
    VERTEX1 = 1
    VERTEX2 = 2
    VERTEX3 = 3
    BYTECOUNT = 4

    def __init__(self, title=None, numFacets=0, facets=None):
        self.title = title
        self.numFacets = numFacets
        self.facets = facets        

def parseBSTL(bstl):
    """
    Loads triangles from file, input can be a file path or a file handler
    Returns a SolidSTL object
    """

    try:
        if isinstance(bstl, file):
            f = bstl
        elif isinstance(bstl, str):
            f = open(bstl, 'rb')
        else:
            raise TypeError("must be a string or file")

        header = f.read(80)
        numTriangles = struct.unpack("@i", f.read(4))
        
        triangles = [(0,0,0)]*numTriangles # prealloc, slightly faster than append
        for i in xrange(numFacets):
            # facet records
            norm = struct.unpack("<3f", f.read(12))
            vertex1 = struct.unpack("<3f", f.read(12))
            vertex2 = struct.unpack("<3f", f.read(12))
            vertex3 = struct.unpack("<3f", f.read(12))
            bytecount = struct.unpack("H", f.read(2)) # not sure what this is
            
            triangles[i] = (norm, vertex1, vertex2, vertex3, bytecount)
        return SolidSTL(header, numTriangles, triangles)

    #TODO: Handle the proper exceptions
    except Exception:
        print "Incorrect file format"
        pass

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
