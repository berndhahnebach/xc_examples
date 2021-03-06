# -*- coding: utf-8 -*-
'''
Example from http://feacluster.com/CalculiX/ccx_2.13/doc/ccx/node7.html#beam5
done with 2D shell elements
'''

__author__= "Bernd Hahnebach"
__copyright__= "Copyright 2015, Bernd Hahnebach"
__license__= "GPL"
__version__= "3.0"
__email__= "bernd@bimstatik.org"


import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model.mesh import finit_el_model
from materials import typical_materials
from materials.sections import section_properties


# *********Problem definition*********
feProblem = xc.FEProblem()
preprocessor = feProblem.getPreprocessor
modelSpace = predefined_spaces.StructuralMechanics3D(preprocessor.getNodeHandler)


# *********geometry*********
points = preprocessor.getMultiBlockTopology.getPoints  # Point container.
pt0 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0)) 
pt1 = points.newPntFromPos3d(geom.Pos3d(1.0,0.0,0.0)) 
pt2 = points.newPntFromPos3d(geom.Pos3d(1.0,0.0,8.0)) 
pt3 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,8.0))  # Right end

surfaces = preprocessor.getMultiBlockTopology.getSurfaces  # Face container.
surfaces.defaultTag = 1
face0 = surfaces.newQuadSurfacePts(pt0.tag, pt1.tag, pt2.tag, pt3.tag)
face0.setElemSizeIJ(0.5,0.25) #Element size in (pt0->pt1,pt1->pt2) directions 

# Ascii art:
#
#    ^ y
#    |
#    |
#
#   pt1                           pt2
#    +-----------------------------+
#    |                             |
#    |                             |
#    |                             |
#    +-----------------------------+ ---> z
#   pt0                           pt3
#
# We have finished with the definition of the geometry.


# *********Material*********
width_cantilever = 1.0
canti_mat = typical_materials.defElasticMembranePlateSection(preprocessor, "canti_mat", 210000.0e6, 0.3, 0.0, width_cantilever)


# *********Elements*********
seedElemHandler = preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial = "canti_mat"
elem = seedElemHandler.newElement("ShellMITC4", xc.ID([0,0,0,0]))


# *********Mesh*********
f1 = preprocessor.getSets.getSet("f1")
f1.genMesh(xc.meshDir.I)


# *********Boundary conditions*********
# Fix all the 3 displacement DOF of the nodes pt0 and pt1, better would be all nodes on the line ln0 (TODO)
#   We ask for the line to fix:
lineToFix= preprocessor.getMultiBlockTopology.getLineWithEndPoints(pt0.tag,pt1.tag)
#   We ask for the nodes on this line
nodesToFix= lineToFix.getNodes()
#   We fix them
for n in nodesToFix:
    modelSpace.fixNode000_000(n.tag) # node fixed.


# *********Load*********
lPatterns = preprocessor.getLoadHandler.getLoadPatterns  # Load pattern container.
# Variation of load with time.
ts = lPatterns.newTimeSeries("constant_ts","ts")  # Constant load, no variation.
lPatterns.currentTimeSeries= "ts"  # Time series to use for the new load patterns.
# Load pattern definition
lp0 = lPatterns.newLoadPattern("default","0")  # New load pattern named 0

# Nodes to load.
#   We ask for the line to load:
lineToLoad= preprocessor.getMultiBlockTopology.getLineWithEndPoints(pt3.tag,pt2.tag)
#   We ask for the nodes on this line
nodesToLoad= lineToLoad.getNodes()
loadForEachNode= 9.0e6/len(nodesToLoad)
#   We load them
for n in nodesToLoad:
    lp0.newNodalLoad(n.tag,xc.Vector([0.0,loadForEachNode,0.0,0.0,0.0,0.0]))

# We add the load case to domain.
lPatterns.addToDomain(lp0.getName())


# *********xcTotalSet*********
# Convenience set (all the nodes, all the elements, all the points,
# all the surfaces,...).
xcTotalSet = preprocessor.getSets.getSet("total")


# *********Solution*********
analysis = predefined_solutions.simple_static_linear(feProblem)
result = analysis.analyze(1)

deltaYpt2 = pt2.getNode().getDisp[1]  # y displacement of node at point pt2.
deltaYpt3 = pt3.getNode().getDisp[1]  # y displacement of node at point pt3.

print 'deltaYpt2= ', deltaYpt2
print 'deltaYpt3= ', deltaYpt3
