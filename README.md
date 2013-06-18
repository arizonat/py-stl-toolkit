This python package is used for parsing, displaying, and post-processing of
STL files. Specifically useful for 3D printing jobs.

Example Usage:
> python 
>> import stlparser
>> stlmodel = stlparser.parseBSTL("demoparts/holeT.STL")
>> stlparser.display(stlmodel)
>> stlparser.isSimple(stlmodel)

Prereqs:
- python2.7
- matplotlib
- numpy

TODO:
  - Add supports to a particular triangle
  - Add supports to a particular conglomerate face
  - Conglomerate triangles to faces(for each triangle, find its neighbours, if the neighbour
    shares a normal vector, then it is part of the same face)
  - Check if saving works properly
  - Save in BSTL instead of STL
  - Parse normal STL

Currently supports:
- Parsing STL binary files
- Displaying STL binary files
- Displaying possible support directions