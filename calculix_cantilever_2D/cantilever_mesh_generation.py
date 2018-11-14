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
from materials import typical_materials
from materials.sections import section_properties

# Problem definition.
feProblem = xc.FEProblem()
preprocessor = feProblem.getPreprocessor
modelSpace = predefined_spaces.StructuralMechanics3D(preprocessor.getNodeHandler)

# Problem geometry (only geometry, no mesh yet).
points = preprocessor.getMultiBlockTopology.getPoints  # Point container.
# Position of the bottom start of the beam:
pt0 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0)) 
# Position of the top start end of the beam:
pt1 = points.newPntFromPos3d(geom.Pos3d(0.0,1.0,0.0)) 
# Position of the bottom end of the beam:
pt2 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0)) 
# Position of the top end of the beam:
pt3 = points.newPntFromPos3d(geom.Pos3d(0.0,1.0,8.0))  # Right end

lines = preprocessor.getMultiBlockTopology.getLines  # Line container.
ln0 = lines.newLine(pt0.tag, pt1.tag)  # From pt0 to pt1.
ln1 = lines.newLine(pt1.tag, pt2.tag)  # From pt1 to pt2.
ln2 = lines.newLine(pt2.tag, pt3.tag)  # From pt2 to pt3.
ln3 = lines.newLine(pt3.tag, pt0.tag)  # From pt3 to pt0.

# Ascii art:
#
#    ^ y
#    |
#    |
#
#   pt1           ln1             pt2
#    +-----------------------------+
#    |                             |
#    | ln0                         |ln2
#    |            ln3              |
#    +-----------------------------+ ---> z
#   pt0                           pt3
#
# We have finished with the definition of the geometry.

# Material definition.
# We need a material to assign to the elements that we create
# with the mesh generation.
# Material properties
EL = typical_materials.MaterialData(name='EL', E=210000.0e6, nu=0.3, rho=0.0)

# Cross section properties (1x1 m square section)
#sectionGeometry = section_properties.RectangularSection("SQ_1x1", b=1.0, h=1.0)
#beamSection = sectionGeometry.defElasticShearSection3d(preprocessor,EL)

'''
# Mesh generation.

# Definition of the "seed element": the element that will copied into each
# mesh cell.

# Orientation of the element axis:
lin= modelSpace.newLinearCrdTransf("lin",xc.Vector([1,0,0]))

seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultTransformation= lin.getName()  # Orientation of the element axis.
seedElemHandler.defaultMaterial= beamSection.name #Material name.
beam3d= seedElemHandler.newElement("ElasticBeam3d",xc.ID([0,0]));

# We tell the line the size of the elements we want.
ln.setElemSize(1.0) # 1 m so 8 elements along the line.

# Mesh generation.
ln.genMesh(xc.meshDir.I) #Now we have a finite element mesh.


# Boundary conditions.

modelSpace.fixNode000_000(pt0.getNode().tag) # Fix all the 6 DOF of the node
                                             # at pt0.

# Load
lPatterns= preprocessor.getLoadHandler.getLoadPatterns #Load pattern container.
# Variation of load with time.
ts= lPatterns.newTimeSeries("constant_ts","ts") #Constant load, no variation.
lPatterns.currentTimeSeries= "ts" #Time series to use for the new load patterns.
#Load pattern definition
lp0= lPatterns.newLoadPattern("default","0") #New load pattern named 0
lp0.newNodalLoad(pt1.tag,xc.Vector([0.0,9.0e6,0.0,0.0,0.0,0.0]))
#We add the load case to domain.
lPatterns.addToDomain(lp0.getName())

# Convenience set (all the nodes, all the elements, all the points,
# all the surfaces,...).
xcTotalSet= preprocessor.getSets.getSet("total")

# Solution
analisis= predefined_solutions.simple_static_linear(feProblem)
result= analisis.analyze(1)

deltaY= pt1.getNode().getDisp[1] #y displacement of node at point pt1.

print 'deltaY= ', deltaY
'''
