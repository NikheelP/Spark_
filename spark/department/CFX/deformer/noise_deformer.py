import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
from spark.department.Help import simpleNoise

for each in [simpleNoise]:
    reload(each)

from spark.department.Help.simpleNoise import SIMPLENOISE


###################################################
kDefaultStringAttrValue = 'default'
plugin_name = 'noiseDeformer'
mtype_id = 0xBA00117
###################################################

EPSILON = 0.0000001
class NOISEDEFORMER(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeName = plugin_name
    kPluginNodeId = OpenMaya.MTypeId(mtype_id)

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)
        self.simple_noise_class = SIMPLENOISE()


    def deform(self,
               data,  # dataBlock
               geom_iter,  # geom iteration class instance
               matrix,  # local to worl matrix
               geom_index):

        # get envelope value, return if sufficiently near to 0
        envDataHandle = data.inputValue(self.envelope)
        envFloat = envDataHandle.asFloat()
        if envFloat <= EPSILON:
            return

        # get attribute values
        ampDataHandle = data.inputValue(self.amp)
        ampFloats = ampDataHandle.asFloat3()
        freqDataHandle = data.inputValue(self.freq)
        freqFloats = freqDataHandle.asFloat3()
        offsetDataHandle = data.inputValue(self.offset)
        offsetFloats = offsetDataHandle.asFloat3()
        octavesDataHandle = data.inputValue(self.octaves)
        octavesInt = octavesDataHandle.asInt()
        lacunarityDataHandle = data.inputValue(self.lacunarity)
        lacunarityFloat = lacunarityDataHandle.asFloat()
        persistenceDataHandle = data.inputValue(self.persistence)
        persistenceFloat = persistenceDataHandle.asFloat()
        locatorWorldSpaceDataHandle = data.inputValue(self.locatorWorldSpace)
        locatorWorldSpaceMat = locatorWorldSpaceDataHandle.asMatrix()

        # precompute some transformation matrices
        localToLocatorSpaceMat = matrix * locatorWorldSpaceMat.inverse()
        locatorToLocalSpaceMat = locatorWorldSpaceMat * matrix.inverse()

        # iterate through all the points
        while not geom_iter.isDone():

            # get weight value for this point, continue if sufficiently near to 0
            weightFloat = self.weightValue(data, geom_index, geom_iter.index())
            if weightFloat <= EPSILON:
                continue

            # get locator space position
            pos = geom_iter.position()
            pos *= localToLocatorSpaceMat

            # precompute some values
            noiseInputX = freqFloats[0] * pos.x - offsetFloats[0]
            noiseInputY = freqFloats[1] * pos.y - offsetFloats[1]
            noiseInputZ = freqFloats[2] * pos.z - offsetFloats[2]
            envTimesWeight = envFloat * weightFloat

            # calculate new position
            pos.x += ampFloats[0] * self.simple_noise_class.snoise3(x=noiseInputX, y=noiseInputY, z=noiseInputZ,
                                                                 octaves=octavesInt, lacunarity=lacunarityFloat,
                                                                 persistence=persistenceFloat) * envTimesWeight

            pos.y += ampFloats[1] * self.simple_noise_class.snoise3(x=noiseInputX + 123, y=noiseInputY + 456, z=noiseInputZ + 789,
                                                                 octaves=octavesInt, lacunarity=lacunarityFloat,
                                                                 persistence = persistenceFloat) *envTimesWeight

            pos.z += ampFloats[2] * self.simple_noise_class.snoise3(x=noiseInputX + 234, y=noiseInputY + 567, z=noiseInputZ + 890,
                                                                 octaves=octavesInt, lacunarity=lacunarityFloat,
                                                                 persistence=persistenceFloat) * envTimesWeight

            # convert back to local space
            pos *= locatorToLocalSpaceMat

            # set new position
            geom_iter.setPosition(pos)

            geom_iter.next()


    def accessoryNodeSetup(self, dagMod):
        thisObj = self.thisMObject()

        # get current object name
        thisFn = OpenMaya.MFnDependencyNode(thisObj)
        thisObjName = thisFn.name()

        # create an accessory locator for user to manipulate a local deformation space
        locObj = dagMod.createNode('locator')
        dagMod.doIt()

        # rename transform and shape nodes
        dagMod.renameNode(locObj, thisObjName + '_loc')
        locDagPath = OpenMaya.MDagPath()
        locDagFn = OpenMaya.MFnDagNode(locObj)
        locDagFn.getPath(locDagPath)
        locDagPath.extendToShape()
        locShapeObj = locDagPath.node()
        dagMod.renameNode(locShapeObj, thisObjName + '_locShape')

        # connect locator's worldMatrix to locatorWorldSpace
        locFn = OpenMaya.MFnDependencyNode(locObj)
        worldMatrixAttr = locFn.attribute('worldMatrix')
        dagMod.connect(locObj, worldMatrixAttr, thisObj, self.locatorWorldSpace)

    def accessoryAttribute(self):
        return self.locatorWorldSpace


def creator():
    return OpenMayaMPx.asMPxPtr(NOISEDEFORMER())


def initialize():
    # ATTRIBUTE LIST
    nAttr = OpenMaya.MFnNumericAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # ATTRIBUTE CREATE
    NOISEDEFORMER.amp = nAttr.createPoint('amplitude', 'amp')
    nAttr.setDefault(1.0, 1.0, 1.0)
    nAttr.setKeyable(True)

    # frequency attr
    NOISEDEFORMER.freq = nAttr.createPoint('frequency', 'freq')
    nAttr.setDefault(1.0, 1.0, 1.0)
    nAttr.setKeyable(True)

    # offset attr
    NOISEDEFORMER.offset = nAttr.createPoint('offset', 'off')
    nAttr.setDefault(0.0, 0.0, 0.0)
    nAttr.setKeyable(True)

    # octaves attr
    NOISEDEFORMER.octaves = nAttr.create('octaves', 'oct', OpenMaya.MFnNumericData.kInt, 1)
    nAttr.setMin(1)
    nAttr.setKeyable(True)

    # lacunarity attr
    NOISEDEFORMER.lacunarity = nAttr.create('lacunarity', 'lac', OpenMaya.MFnNumericData.kFloat, 2.0)
    nAttr.setKeyable(True)

    # persistence attr
    NOISEDEFORMER.persistence = nAttr.create('persistence', 'per', OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)

    # locatorWorldSpace attr
    NOISEDEFORMER.locatorWorldSpace = mAttr.create('locatorWorldSpace', 'locsp')
    mAttr.setStorable(False)
    mAttr.setHidden(True)

    # ATTRIBUTE ADD
    NOISEDEFORMER.addAttribute(NOISEDEFORMER.amp)
    NOISEDEFORMER.addAttribute(NOISEDEFORMER.freq)
    NOISEDEFORMER.addAttribute(NOISEDEFORMER.offset)
    NOISEDEFORMER.addAttribute(NOISEDEFORMER.octaves)
    NOISEDEFORMER.addAttribute(NOISEDEFORMER.lacunarity)
    NOISEDEFORMER.addAttribute(NOISEDEFORMER.persistence)
    NOISEDEFORMER.addAttribute(NOISEDEFORMER.locatorWorldSpace)

    # ATTRIBUTE AFFECT
    outputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
    NOISEDEFORMER.attributeAffects(NOISEDEFORMER.amp, outputGeom)
    NOISEDEFORMER.attributeAffects(NOISEDEFORMER.freq, outputGeom)
    NOISEDEFORMER.attributeAffects(NOISEDEFORMER.offset, outputGeom)
    NOISEDEFORMER.attributeAffects(NOISEDEFORMER.octaves, outputGeom)
    NOISEDEFORMER.attributeAffects(NOISEDEFORMER.lacunarity, outputGeom)
    NOISEDEFORMER.attributeAffects(NOISEDEFORMER.persistence, outputGeom)
    NOISEDEFORMER.attributeAffects(NOISEDEFORMER.locatorWorldSpace, outputGeom)

    cmds.makePaintable(NOISEDEFORMER.kPluginNodeName, 'weights', attrType='multiFloat', shapeMode='deformer')


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode(NOISEDEFORMER.kPluginNodeName,
                            NOISEDEFORMER.kPluginNodeId,
                            creator,
                            initialize,
                            OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise "Failed to register node: %s" % NOISEDEFORMER.kPluginNodeName


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(NOISEDEFORMER.kPluginNodeId)
    except:
        raise "Failed to deregister node: %s" % NOISEDEFORMER.kPluginNodeName
