
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

from spark.department.Help import deformer

for each in [deformer]:
    reload(each)


from spark.department.Help import DEFORMER




kDefaultStringAttrValue = 'default'


class BLENDWRRAP(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeName = 'blendwrap'
    kPluginNodeId = OpenMaya.MTypeId(0xBA00110)
    strength = OpenMaya.MObject()
    connected_mesh = OpenMaya.MObject()
    snap_offset = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)
        self.default_val = False
        self.deformer_class = DEFORMER()

    def get_input_geom(self, data, geom_idx):
        input_attr = data.outputArrayValue(self.input)
        input_handle = data.outputArrayValue(self.input)
        input_handle.jumpToElement(geom_idx)
        input_geom_obj = input_handle.outputValue().child(self.inputGeom).asMesh()
        return input_geom_obj

    def getUV_val(self, Source_Loc_xform, mfnMesh, Geo_name):
        loc_point = OpenMaya.MPoint(Source_Loc_xform[0], Source_Loc_xform[1], Source_Loc_xform[2])
        pos = OpenMaya.MPoint()
        mfnMesh.getClosestPoint(loc_point, pos, OpenMaya.MSpace.kWorld)
        #currentUvSet = cmds.polyUVSet(Geo_name, q=True, cuv=True)
        uv_mPoint = OpenMaya.MPoint(pos.x, pos.y, pos.z, 1.0)
        uv = OpenMaya.MScriptUtil()
        uv.createFromList([0.0, 0.0], 2)
        uvPtr = uv.asFloat2Ptr()
        mfnMesh.getUVAtPoint(uv_mPoint, uvPtr, OpenMaya.MSpace.kWorld)
        u_val = uv.getFloat2ArrayItem(uvPtr, 0, 0)
        v_val = uv.getFloat2ArrayItem(uvPtr, 0, 1)
        return (u_val, v_val)

    def get_point_position(self, mfnMesh, geo_name, u, v):
        meshFn = mfnMesh
        faceCount = cmds.polyEvaluate(geo_name, face=True)

        # convert uv to ptr
        util = OpenMaya.MScriptUtil()
        util.createFromList((u, v), 2)
        uvPtr = util.asFloat2Ptr()

        positionMPoint = OpenMaya.MPoint()
        currentUvSet = cmds.polyUVSet(geo_name, q=True, cuv=True)
        tolerance = 0.01

        # check each face for uv
        # worldPos = {'face#': [x,y,z]}
        worldPos = []

        for faceIndex in range(faceCount):
            try:
                mfnMesh.getPointAtUV(faceIndex, positionMPoint, uvPtr, OpenMaya.MSpace.kWorld, currentUvSet[0],
                                     tolerance)
                worldPos.append(positionMPoint.x)
                worldPos.append(positionMPoint.y)
                worldPos.append(positionMPoint.z)
                # worldPos[faceIndex] = (positionMPoint.x, positionMPoint.y, positionMPoint.z)
            except:
                pass

        return worldPos

    def deform(self,
               data,  # dataBlock
               geom_iter,  # geom iteration class instance
               matrix,  # local to worl matrix
               geom_index):

        # query the geo
        connected_mesh = data.inputValue(self.connected_mesh).asMesh()
        strength = data.inputValue(self.strength).asFloat()
        snap_offset = data.inputValue(self.snap_offset).asShort()
        envelope = data.inputValue(self.envelope).asFloat()

        thisNode = self.thisMObject()
        socketNode = OpenMaya.MFnDependencyNode(thisNode)

        node_name = socketNode.name()
        geo_name = self.deformer_class.getAffectedGeometry(node_name).keys()[0]

        input_mesh = self.get_input_geom(data, geom_index)
        input_mfnMesh = OpenMaya.MFnMesh(input_mesh)
        input_mpointArray = OpenMaya.MPointArray()
        input_mfnMesh.getPoints(input_mpointArray, OpenMaya.MSpace.kWorld)

        connected_mfnmesh = OpenMaya.MFnMesh(connected_mesh)
        connected_mpointArray = OpenMaya.MPointArray()
        connected_mfnmesh.getPoints(connected_mpointArray, OpenMaya.MSpace.kWorld)
        connected_geo_name = cmds.listConnections(node_name + '.ConnectMesh')[0]

        value = cmds.listConnections(node_name + '.ConnectMesh')
        if self.default_val == False:
            if value != None:

                self.vtx_default_pos = {}
                self.uv_pos = {}

                for i in range(input_mpointArray.length()):
                    x_val = input_mpointArray[i].x
                    y_val = input_mpointArray[i].y
                    z_val = input_mpointArray[i].z
                    world_pos_val = [x_val, y_val, z_val]
                    u, v = self.getUV_val(Source_Loc_xform=world_pos_val,
                                          mfnMesh=connected_mfnmesh,
                                          Geo_name=connected_geo_name)

                    position = self.get_point_position(mfnMesh=connected_mfnmesh,
                                                       geo_name=connected_geo_name,
                                                       u=u,
                                                       v=v)

                    self.vtx_default_pos[i] = position
                    self.uv_pos[i] = [u, v]
                self.default_val = True
                if snap_offset == 1:
                    a = 0
                    mpoint_mesh_Array = OpenMaya.MPointArray()
                    while (geom_iter.isDone() == False):
                        new_x_val = self.vtx_default_pos[a][0]
                        new_y_val = self.vtx_default_pos[a][1]
                        new_z_val = self.vtx_default_pos[a][2]

                        pt = OpenMaya.MPoint(new_x_val, new_y_val, new_z_val)
                        mpoint_mesh_Array.append(pt)
                        a += 1
                        geom_iter.next()
                    geom_iter.setAllPositions(mpoint_mesh_Array)

        else:
            a = 0
            mpoint_mesh_Array = OpenMaya.MPointArray()
            while (geom_iter.isDone() == False):
                weight = self.weightValue(data, geom_index, geom_iter.index())
                pointPosition = geom_iter.position()
                u_v_val = self.uv_pos[a]
                position = self.get_point_position(mfnMesh=connected_mfnmesh,
                                                   geo_name=connected_geo_name,
                                                   u=u_v_val[0],
                                                   v=u_v_val[1])

                x_diff = (position[0] - self.vtx_default_pos[a][0]) * strength * envelope * weight
                y_diff = (position[1] - self.vtx_default_pos[a][1]) * strength * envelope * weight
                z_diff = (position[2] - self.vtx_default_pos[a][2]) * strength * envelope * weight

                new_env = envelope - 1
                snap_x_val = (position[0] - pointPosition.x) * new_env
                snap_y_val = (position[1] - pointPosition.y) * new_env
                snap_z_val = (position[2] - pointPosition.z) * new_env

                if snap_offset == 0:
                    new_x_val = pointPosition.x + x_diff
                    new_y_val = pointPosition.y + y_diff
                    new_z_val = pointPosition.z + z_diff
                if snap_offset == 1:
                    new_x_val = position[0] + snap_x_val
                    new_y_val = position[1] + snap_y_val
                    new_z_val = position[2] + snap_z_val

                pt = OpenMaya.MPoint(new_x_val, new_y_val, new_z_val)
                mpoint_mesh_Array.append(pt)
                # geom_iter.setPosition( pt )
                a += 1
                geom_iter.next()
            geom_iter.setAllPositions(mpoint_mesh_Array)


def creator():
    return OpenMayaMPx.asMPxPtr(BLENDWRRAP())


def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    nMAttr = OpenMaya.MFnMatrixAttribute()
    cAttr = OpenMaya.MFnCompoundAttribute()
    tAttr = OpenMaya.MFnTypedAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    # string attr

    BLENDWRRAP.strength = nAttr.create("strength", "str", OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)

    BLENDWRRAP.connected_mesh = tAttr.create('ConnectMesh', 'cm', OpenMaya.MFnData.kMesh)
    tAttr.setWritable(True)
    tAttr.setStorable(True)
    tAttr.setReadable(True)
    tAttr.setKeyable(True)

    BLENDWRRAP.snap_offset = eAttr.create("Condition", "con", 0)
    eAttr.addField("offset", 0)
    eAttr.addField("snap", 1)
    eAttr.setHidden(False)
    eAttr.setKeyable(True)
    eAttr.setStorable(True)

    BLENDWRRAP.addAttribute(BLENDWRRAP.strength)
    BLENDWRRAP.addAttribute(BLENDWRRAP.connected_mesh)
    BLENDWRRAP.addAttribute(BLENDWRRAP.snap_offset)

    outputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
    BLENDWRRAP.attributeAffects(BLENDWRRAP.strength, outputGeom)
    BLENDWRRAP.attributeAffects(BLENDWRRAP.connected_mesh, outputGeom)
    BLENDWRRAP.attributeAffects(BLENDWRRAP.snap_offset, outputGeom)

    cmds.makePaintable(BLENDWRRAP.kPluginNodeName, 'weights', attrType='multiFloat', shapeMode='deformer')


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode(BLENDWRRAP.kPluginNodeName,
                            BLENDWRRAP.kPluginNodeId,
                            creator,
                            initialize,
                            OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise "Failed to register node: %s" % BLENDWRRAP.kPluginNodeName


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(BLENDWRRAP.kPluginNodeId)
    except:
        raise "Failed to deregister node: %s" % BLENDWRRAP.kPluginNodeName
