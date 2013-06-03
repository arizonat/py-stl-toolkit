This python package is used for parsing, displaying, and post-processing of
STL files. Specifically useful for 3D printing jobs.

Example Usage:
> python 
>>> import stlparser
>>> stlmodel = stlparser.parseBSTL("Part1.STL")
>>> stlmodel.display()

or
> python stlparser Part1.STL

Prereqs:
- matplotlib

Currently supports:
- Parsing STL binary files
- Displaying STL binary files

Known Issues:
- Display axes are all wrong