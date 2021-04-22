import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

from spark.department.Help import openMayaBaisc
from spark.department.Help import base

for each in [openMayaBaisc, base]:
    reload(each)

from spark.department.Help.openMayaBaisc import OPENMAYABASIC
from spark.department.Help.base import BASE

class DEFORMER:

    def __init__(self):
        self.openMayaBaic = OPENMAYABASIC()
        self.base_class = BASE()

    def is_deformer(self, deformer):
        '''
        test if node is valid deformer or not
        '''
        # chck deforer is exists or not
        if not cmds.objExists(deformer):
            return False

        nodetype = cmds.nodeType(deformer, i=True)
        if not nodetype.count('geometryFilter'): return False

        return True

    def getAffectedGeometry(self, deformer_name, returnShapes=False, fullPathNames=False):
        '''
        if not self.isDeformer(deformer_name):
            raise Exception('Object "'+ deformer_name + '" is not a valid deformer!')
        '''
        # Initialize Return Array (dict)
        affectedObjects = {}

        # Get MFnGeometryFilter
        deformerObj = self.openMayaBaic.get_mObject(deformer_name)
        geoFilterFn = OpenMayaAnim.MFnGeometryFilter(deformerObj)

        # Get Output Geometry
        outputObjectArray = OpenMaya.MObjectArray()
        geoFilterFn.getOutputGeometry(outputObjectArray)

        # Iterate Over Affected Geometry
        for i in range(outputObjectArray.length()):
            # Get Output Connection at Index
            outputIndex = geoFilterFn.indexForOutputShape(outputObjectArray[i])
            outputNode = OpenMaya.MFnDagNode(outputObjectArray[i])

            # Check Return Shapes
            if not returnShapes: outputNode = OpenMaya.MFnDagNode(outputNode.parent(0))

            # Check Full Path
            if fullPathNames:
                affectedObjects[outputNode.fullPathName()] = outputIndex
            else:
                affectedObjects[outputNode.partialPathName()] = outputIndex

        # Return Result
        return affectedObjects

    def setWeights(self, deformer, weights, geometry=None):
        '''
        set the weight to the specific defirer to weight value
        @param deformer: Deformer to set weights for
        @type deformer: str
        @param weights: Input weight value list
        @type weights: list
        @param geometry: Target geometry to apply weights to. If None, use first affected geometry.
        @type geometry: str
        '''
        # Check Deformer
        if not self.is_deformer(deformer):
            raise Exception('Object "' + deformer + '" is not a valid deformer!')

        # Check Geometry
        if not geometry:
            geometry = self.getAffectedGeometry(deformer).keys()[0]

        # Get Geometry Shape
        geoShape = geometry
        geoObj = self.base_class.getMObject(geometry)
        if geometry and geoObj.hasFn(OpenMaya.MFn.kTransform):
            geoShape = cmds.listRelatives(geometry, s=True, ni=True)[0]

        # Get deformer function set and members
        deformerFn = self.getDeformerFn(deformer)
        deformerSetMem = self.getDeformerSetMembers(deformer, geoShape)

        # Build weight array
        weightList = OpenMaya.MFloatArray()
        [weightList.append(i) for i in weights]

        # Set weights
        deformerFn.setWeight(deformerSetMem[0], deformerSetMem[1], weightList)

    def getDeformerFn(self, deformer):
        '''
        Initialize and return an MFnWeightGeometryFilter function set attached to the specified deformer
        @param deformer: Name of deformer to create function set for
        @type deformer: str
        '''
        # Checks
        if not cmds.objExists(deformer):
            raise Exception('Deformer ' + deformer + ' does not exist!')

        # Get MFnWeightGeometryFilter
        deformerObj = self.base_class.getMObject(deformer)
        try:
            deformerFn = OpenMayaAnim.MFnWeightGeometryFilter(deformerObj)
        except:  # is there a good exception type for this?
            raise Exception('Could not get a geometry filter for deformer "' + deformer + '"!')

        # Return result
        return deformerFn

    def getDeformerSetMembers(self, deformer, geometry=''):
        '''
        Return the deformer set members of the specified deformer.
        You can specify a shape name to query deformer membership for.
        Otherwise, membership for the first affected geometry will be returned.
        Results are returned as a list containing an MDagPath to the affected shape and an MObject for the affected components.
        @param deformer: Deformer to query set membership for
        @type deformer: str
        @param geometry: Geometry to query deformer set membership for. Optional.
        @type geometry: str
        '''
        # Get deformer function sets
        deformerSetFn = self.getDeformerSetFn(deformer)

        # Get deformer set members
        deformerSetSel = OpenMaya.MSelectionList()
        deformerSetFn.getMembers(deformerSetSel, True)
        deformerSetPath = OpenMaya.MDagPath()
        deformerSetComp = OpenMaya.MObject()

        # Get geometry index
        if geometry:
            geomIndex = self.getGeomIndex(geometry, deformer)
        else:
            geomIndex = 0

        # Get number of selection components
        deformerSetLen = deformerSetSel.length()
        if geomIndex >= deformerSetLen:
            raise Exception(
                'Geometry index out of range! (Deformer: "' + deformer + '", Geometry: "' + geometry + '", GeoIndex: ' + str(
                    geomIndex) + ', MaxIndex: ' + str(deformerSetLen) + ')')

        # Get deformer set members
        deformerSetSel.getDagPath(geomIndex, deformerSetPath, deformerSetComp)

        # Return result
        return [deformerSetPath, deformerSetComp]

    def getDeformerSetFn(self, deformer):
        '''
        Initialize and return an MFnSet function set attached to the deformer set of the specified deformer
        @param deformer: Name of deformer attached to the deformer set to create function set for
        @type deformer: str
        '''
        # Checks
        if not cmds.objExists(deformer):
            raise Exception('Deformer ' + deformer + ' does not exist!')

        # Get deformer set
        deformerSet = self.getDeformerSet(deformer)

        # Get MFnWeightGeometryFilter
        deformerSetObj = self.base_class.getMObject(deformerSet)
        deformerSetFn = OpenMaya.MFnSet(deformerSetObj)

        # Return result
        return deformerSetFn

    def getDeformerSet(self, deformer):
        '''
        Return the deformer set name associated with the specified deformer
        @param deformer: Name of deformer to return the deformer set for
        @type deformer: str
        '''
        # Checks
        if not cmds.objExists(deformer):
            raise Exception('Deformer ' + deformer + ' does not exist!')
        if not self.is_deformer(deformer):
            raise Exception('Object ' + deformer + ' is not a valid deformer!')

        # Get Deformer Set
        deformerObj = self.base_class.getMObject(deformer)
        deformerFn = OpenMayaAnim.MFnGeometryFilter(deformerObj)
        deformerSetObj = deformerFn.deformerSet()
        if deformerSetObj.isNull():
            raise Exception('Unable to determine deformer set for "' + deformer + '"!')

        # Return Result
        return OpenMaya.MFnDependencyNode(deformerSetObj).name()

    def getGeomIndex(self, geometry, deformer):
        '''
        Returns the geometry index of a shape to a specified deformer.
        @param geometry: Name of shape or parent transform to query
        @type geometry: str
        @param deformer: Name of deformer to query
        @type deformer: str
        '''
        # Verify input
        if not self.is_deformer(deformer):
            raise Exception('Object "' + deformer + '" is not a valid deformer!')

        # Check geometry
        geo = geometry
        if cmds.objectType(geometry) == 'transform':
            try:
                geometry = cmds.listRelatives(geometry, s=True, ni=True, pa=True)[0]
            except:
                raise Exception('Object "' + geo + '" is not a valid geometry!')
        geomObj = self.base_class.getMObject(geometry)

        # Get geometry index
        deformerObj = self.base_class.getMObject(deformer)
        deformerFn = OpenMayaAnim.MFnGeometryFilter(deformerObj)
        try:
            geomIndex = deformerFn.indexForOutputShape(geomObj)
        except:
            raise Exception('Object "' + geometry + '" is not affected by deformer "' + deformer + '"!')

        # Retrun result
        return geomIndex