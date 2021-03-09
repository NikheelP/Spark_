import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math
import maya.cmds as cmds

kDefaultStringAttrValue = 'default'
class CORRECTIVEBLENDSHAPE(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeName = 'correctiveBlendshape'
    kPluginNodeId = OpenMaya.MTypeId(0xBA00101)
    blend_value = OpenMaya.MObject()
    blend_mesh = OpenMaya.MObject()
    first_position = OpenMaya.MObject()


    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def get_input_geom(self, data, geom_idx):
        input_attr = data.outputArrayValue( self.input )
        input_handle = data.outputArrayValue(self.input)
        input_handle.jumpToElement(geom_idx)
        input_geom_obj = input_handle.outputValue().child(self.inputGeom).asMesh()
        return input_geom_obj

    def deform(self,
               data, # dataBlock
               geom_iter, # geom iteration class instance
               matrix, # local to worl matrix
               geom_index):

        blend_mesh = data.inputValue(CORRECTIVEBLENDSHAPE.blend_mesh).asMesh()
        envelope = data.inputValue(self.envelope).asFloat()
        blend_val = data.inputValue(CORRECTIVEBLENDSHAPE.blend_value).asFloat()

        first_pos_val = data.inputValue(CORRECTIVEBLENDSHAPE.first_position).asString()
        input_mfnmesh = OpenMaya.MFnMesh(blend_mesh)
        if first_pos_val == 'default':
            value = []
            corrective_obj_mpointArray = OpenMaya.MPointArray()
            input_mfnmesh.getPoints(corrective_obj_mpointArray, OpenMaya.MSpace.kWorld)
            for i in range(corrective_obj_mpointArray.length()):
                x_val = corrective_obj_mpointArray[i].x
                y_val = corrective_obj_mpointArray[i].y
                z_val = corrective_obj_mpointArray[i].z
                val = [x_val, y_val, z_val]
                value.append(val)

            self.default_pos = value
            this_object =  self.thisMObject()
            _node = OpenMaya.MFnDependencyNode(this_object)
            node_name = _node.name()
            cmds.setAttr((node_name + '.FirstPos'), value, type='string' )
            cmds.setAttr((node_name + '.FirstPos'), l=True)
            cmds.setAttr((node_name + '.BlendVal'), 1)

        else:
            corrective_obj_new_mpointArray = OpenMaya.MPointArray()
            input_mfnmesh.getPoints(corrective_obj_new_mpointArray, OpenMaya.MSpace.kWorld)

            while not geom_iter.isDone():
                weight = self.weightValue(data, geom_index, geom_iter.index())
                idx = geom_iter.index()
                val_x = (corrective_obj_new_mpointArray[idx].x - self.default_pos[idx][0]) * envelope * weight * blend_val
                val_y = (corrective_obj_new_mpointArray[idx].y - self.default_pos[idx][1]) * envelope * weight * blend_val
                val_z = (corrective_obj_new_mpointArray[idx].z - self.default_pos[idx][2]) * envelope * weight * blend_val

                pos = geom_iter.position()

                point =OpenMaya.MPoint()
                trans_x = 0
                trans_y = 0
                trans_z = 0
                point.x = (pos[0] + val_x - trans_x)
                point.y = (pos[1] + val_y - trans_y)
                point.z = (pos[2] + val_z - trans_z)

                geom_iter.setPosition(point)

                geom_iter.next()

def creator():
    return OpenMayaMPx.asMPxPtr(CORRECTIVEBLENDSHAPE())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    nMAttr = OpenMaya.MFnMatrixAttribute()
    tAttr = OpenMaya.MFnTypedAttribute()

    # string attr
    stringData = OpenMaya.MFnStringData().create(kDefaultStringAttrValue)
    CORRECTIVEBLENDSHAPE.first_position = tAttr.create("FirstPos", "fp", OpenMaya.MFnData.kString, stringData)
    tAttr.setHidden(False)
    tAttr.setKeyable(True)

    CORRECTIVEBLENDSHAPE.blend_mesh = tAttr.create('blendMesh', 'mesh', OpenMaya.MFnData.kMesh)
    tAttr.setWritable(True)
    tAttr.setStorable(True)
    tAttr.setReadable(True)
    tAttr.setKeyable(True)


    CORRECTIVEBLENDSHAPE.blend_value = nAttr.create( "BlendVal", "bv", OpenMaya.MFnNumericData.kFloat, 0.0 )
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setChannelBox(True)

    CORRECTIVEBLENDSHAPE.addAttribute(CORRECTIVEBLENDSHAPE.blend_value)
    CORRECTIVEBLENDSHAPE.addAttribute(CORRECTIVEBLENDSHAPE.blend_mesh)
    CORRECTIVEBLENDSHAPE.addAttribute(CORRECTIVEBLENDSHAPE.first_position)

    outputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
    CORRECTIVEBLENDSHAPE.attributeAffects(CORRECTIVEBLENDSHAPE.blend_value, outputGeom)
    CORRECTIVEBLENDSHAPE.attributeAffects(CORRECTIVEBLENDSHAPE.blend_mesh, outputGeom)
    CORRECTIVEBLENDSHAPE.attributeAffects(CORRECTIVEBLENDSHAPE.first_position, outputGeom)


    cmds.makePaintable(CORRECTIVEBLENDSHAPE.kPluginNodeName, 'weights', attrType='multiFloat', shapeMode='deformer')





def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode( CORRECTIVEBLENDSHAPE.kPluginNodeName,
                             CORRECTIVEBLENDSHAPE.kPluginNodeId,
                             creator,
                             initialize,
                             OpenMayaMPx.MPxNode.kDeformerNode )
    except:
        raise "Failed to register node: %s" % CORRECTIVEBLENDSHAPE.kPluginNodeName

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(CORRECTIVEBLENDSHAPE.kPluginNodeId)
    except:
        raise "Failed to deregister node: %s" % CORRECTIVEBLENDSHAPE.kPluginNodeName
