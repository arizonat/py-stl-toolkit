import struct
import matplotlib

normals = []
points = []
triangles = []
bytecount = []

fb = []

# from (will be modified soon)
# http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file
def unpack(f, sig, l):
    s = f.read(l)
    fb.append(s)
    return struct.unpack(sig, s)

# from (will be modified soon)
# http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file    
def read_triangle(f):
    n = unpack(f, "<3f", 12)
    p1 = unpack(f, "<3f", 12)
    p2 = unpack(f, "<3f", 12)
    p3 = unpack(f, "<3f", 12)
    b = unpack(f, "<h", 2)

    normals.append(n)
    l = len(points)
    points.append(p1)
    points.append(p2)
    points.append(p3)
    triangles.append((l, l+1, l+2))
    bytecount.append(b[0])

# from (will be modified soon)
# http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file    
def read_length(f):
    length = struct.unpack("@i", f.read(4))
    return length[0]

# from (will be modified soon)
# http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file    
def read_header(f):
    f.seek(f.tell()+80)
    
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

# from (will be modified soon)
# http://stackoverflow.com/questions/7566825/python-parsing-binary-stl-file    
def main():
    f = open("Part1.STL", "rb")
    
    read_header(f)
    l = read_length(f)
    try:
        while True:
            read_triangle(f)
    except Exception, e:
        print "Exception ", e[0]

    print len(normals), len(points), len(triangles), 1
    print "*"*10
    print repr(triangles)
if __name__ == "__main__":
    main()
