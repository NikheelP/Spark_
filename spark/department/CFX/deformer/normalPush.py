import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math
import maya.cmds as cmds


class NORMALPUSH(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeName = 'normalPush'
    kPluginNodeId = OpenMaya.MTypeId(0xBA00102)
    inflation_attr = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def get_input_geom(self, data, geom_idx):
        input_attr = data.outputArrayValue(self.input)
        input_handle = data.outputArrayValue(self.input)
        input_handle.jumpToElement(geom_idx)
        input_geom_obj = input_handle.outputValue().child(self.inputGeom).asMesh()
        return input_geom_obj

    def deform(self,
               data,  # dataBlock
               geom_iter,  # geom iteration class instance
               matrix,  # local to worl matrix
               geom_index):
        # envelope_attr = OpenMayaMPx.cvar.MPxDeformerNode_envelope

        envelope = data.inputValue(self.envelope).asFloat()

        inflation_handle = data.inputValue(NORMALPUSH.inflation_attr)
        inflation = inflation_handle.asDouble()

        input_geom_obj = self.get_input_geom(data, geom_index)
        normals = OpenMaya.MFloatVectorArray()
        mesh = OpenMaya.MFnMesh(input_geom_obj)
        mesh.getVertexNormals(True, normals, OpenMaya.MSpace.kTransform)

        while not geom_iter.isDone():
            idx = geom_iter.index()
            nrm = OpenMaya.MVector(normals[idx])
            pos = geom_iter.position()
            weight = self.weightValue(data, geom_index, geom_iter.index())
            new_pos = pos + (nrm * inflation * envelope * weight)
            geom_iter.setPosition(new_pos)
            geom_iter.next()


def creator():
    return OpenMayaMPx.asMPxPtr(NORMALPUSH())


def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    nMAttr = OpenMaya.MFnMatrixAttribute()

    NORMALPUSH.inflation_attr = nAttr.create("inflation", "in", OpenMaya.MFnNumericData.kDouble, 0.0)
    nAttr.setMin(0.0)
    nAttr.setChannelBox(True)

    NORMALPUSH.addAttribute(NORMALPUSH.inflation_attr)

    outputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
    NORMALPUSH.attributeAffects(NORMALPUSH.inflation_attr, outputGeom)

    cmds.makePaintable(NORMALPUSH.kPluginNodeName, 'weights', attrType='multiFloat', shapeMode='deformer')


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode(NORMALPUSH.kPluginNodeName,
                            NORMALPUSH.kPluginNodeId,
                            creator,
                            initialize,
                            OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise "Failed to register node: %s" % NORMALPUSH.kPluginNodeName


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(NORMALPUSH.kPluginNodeId)
    except:
        raise "Failed to deregister node: %s" % NORMALPUSH.kPluginNodeName
