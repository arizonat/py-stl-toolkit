This python package is used for parsing, displaying, and post-processing of
STL files. Specifically useful for 3D printing jobs.

Example Usage:

import stlparser
    stlmodel = stlparser.parseBSTL("demoparts/angleT.STL")
    stlmodel.__shiftUp(5)
    stlparser.addCuboidSupports(stlmodel)
    stlparser.display(stlmodel, showNorms=True)
    stlparser.isSimple(stlmodel)

Prereqs:
  - python2.7
  - matplotlib
  - numpy

Currently supports:
  - Parsing STL binary files
  - Displaying STL binary files
  - Displaying possible support directions
  - Adding cuboid supports (can only do perfectly flat faces currently)

TODO:
  - Add supports for angled faces
  - Add supports to a particular conglomerate face
  - Conglomerate triangles to faces(for each triangle, find its neighbours, if the neighbour
    shares a normal vector, then it is part of the same face)
  - Check if saving works properly
  - Save in BSTL instead of STL
  - Parse normal STL
