This python package is used for parsing, displaying, and post-processing of
STL files. Specifically useful for 3D printing jobs.

Example Usage:

    import stlparser
    stlmodel = stlparser.parseBSTL("demoparts/angleT.STL")
    stlparser.__shiftUp(stlmodel,5)
    stlparser.addCuboidSupports(stlmodel)
    stlparser.display(stlmodel, showNorms=True)
    stlparser.isSimple(stlmodel)

Prereqs:
  - python2.7
  - matplotlib
  - numpy

Currently supports:
  - Parsing STL binary files
  - Parsing STL normal files
  - Displaying STL solids
  - Displaying possible support directions
  - Adding cuboid supports at all triangle locations that need them (can only do perfectly flat faces currently)
  - Save to new STL files

TODO:
  - Add supports for angled faces
  - Add supports to a particular conglomerate face
  - Conglomerate triangles to faces(for each triangle, find its neighbours, if the neighbour
    shares a normal vector, then it is part of the same face)
  - Save in BSTL instead of STL

