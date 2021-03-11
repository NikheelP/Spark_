import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

from spark.department.Help import openMayaBaisc

for each in [openMayaBaisc]:
    reload(each)

from spark.department.Help.openMayaBaisc import OPENMAYABASIC


class DEFORMER:

    def __init__(self):
        self.openMayaBaic = OPENMAYABASIC()

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