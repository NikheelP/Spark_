from spark.department.Help import deformer
for each in [deformer]:
    reload(each)

import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math
import maya.cmds as cmds

from spark.department.Help import DEFORMER


kDefaultStringAttrValue = 'default'


class MESHCOLLIDER(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeName = 'meshCollider'
    kPluginNodeId = OpenMaya.MTypeId(0xBA00112)
    radious = OpenMaya.MObject()
    vtx_no = OpenMaya.MObject()
    connected_mesh = OpenMaya.MObject()
    tranlate = OpenMaya.MObject()
    outBlendWeight = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)
        self.default_val = False
        self.deform_class = DEFORMER()

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
        currentUvSet = cmds.polyUVSet(Geo_name, q=True, cuv=True)
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
        # get all the input
        # GET THE INPUT

        # get the Attribute
        self.node_name = self.get_node_name()
        self.geo_name = self.get_obj_name(node_name=self.node_name, geom_index=geom_index)

        input_mesh_one = data.inputValue(self.input_mesh).asMesh()
        input_mesh_mfnmesh = OpenMaya.MFnMesh(input_mesh_one)
        input_mesh_mpointArray = OpenMaya.MPointArray()
        input_mesh_mfnmesh.getPoints(input_mesh_mpointArray, OpenMaya.MSpace.kWorld)


        collider_mesh = data.inputValue(self.collidr_mesh).asMesh()
        collider_mesh_mfnmesh = OpenMaya.MFnMesh(collider_mesh)

        deformer_geom_obj = self.get_input_geom(data, geom_index)
        deformer_mesh = OpenMaya.MFnMesh(deformer_geom_obj)

        deformer_mesh_mpointArray = OpenMaya.MPointArray()
        deformer_mesh.getPoints(deformer_mesh_mpointArray, OpenMaya.MSpace.kWorld)

        offset_vertex = data.inputValue(self.offset_vertex).asFloat()

        deform_vtx_list = []
        non_deform_vtx_list = {}


        while not geom_iter.isDone():
            index = geom_iter.index()

            #get this is on normal side or opposite
            vtx_point = OpenMaya.MPoint(input_mesh_mpointArray[index].x,
                                        input_mesh_mpointArray[index].y,
                                        input_mesh_mpointArray[index].z)
            closest_point = OpenMaya.MPoint()
            collider_mesh_mfnmesh.getClosestPoint(vtx_point, closest_point, OpenMaya.MSpace.kWorld)
            normals = OpenMaya.MFloatVectorArray()
            collider_mesh_mfnmesh.getVertexNormals(True, normals, OpenMaya.MSpace.kTransform)
            nrm = OpenMaya.MVector(normals[index])
            new_normal_val_x = closest_point.x + nrm[0]
            new_normal_val_y = closest_point.y + nrm[1]
            new_normal_val_z = closest_point.z + nrm[2]

            new_normal_rev_val_x = (closest_point.x - nrm[0])
            new_normal_rev_val_y = (closest_point.y - nrm[1])
            new_normal_rev_val_z = (closest_point.z - nrm[2])

            #get the distance between object
            fist_dist = math.sqrt((new_normal_val_x - input_mesh_mpointArray[index].x)**2 + (new_normal_val_y - input_mesh_mpointArray[index].y)**2 + (new_normal_val_z - input_mesh_mpointArray[index].z)**2)
            secound_dist = math.sqrt((new_normal_rev_val_x - input_mesh_mpointArray[index].x)**2 + (new_normal_rev_val_y - input_mesh_mpointArray[index].y)**2 + (new_normal_rev_val_z- input_mesh_mpointArray[index].z)**2)

            #OFFSET PUSH
            #get the connected vertex

            position = closest_point

            if secound_dist < fist_dist:
                geom_iter.setPosition(position)
                #vtx_list.append(string_name)
                deform_vtx_list.append(index)
            else:
                #print('this is a normal side')
                non_deform_vtx_list[index] = {}
                non_deform_vtx_list[index]['neighbour_vtx'] = neighbour_list[index]
            # Move to next
            geom_iter.next()
        vtx_list = []
        for each in non_deform_vtx_list:
            nearest_vertex = False
            a = 0
            while a < len(deform_vtx_list):
                for each_near in non_deform_vtx_list[each]['neighbour_vtx']:
                    if each_near == deform_vtx_list[a]:
                        nearest_vertex = True
                        break

                a+=1
            if nearest_vertex == True:
                string_val = 'Main_Geo.vtx[%s]' % each
                vtx_list.append(string_val)
                #set the position
                offset_normals = OpenMaya.MFloatVectorArray()
                deformer_mesh.getVertexNormals(True, offset_normals, OpenMaya.MSpace.kTransform)
                nrm = OpenMaya.MVector(offset_normals[each])
                point_val_x = deformer_mesh_mpointArray[each].x + (nrm[0] * offset_vertex)
                point_val_y = deformer_mesh_mpointArray[each].y + (nrm[1] * offset_vertex)
                point_val_z = deformer_mesh_mpointArray[each].z + (nrm[2] * offset_vertex)

                new_pos_point = OpenMaya.MPoint(point_val_x, point_val_y, point_val_z)
                deformer_mesh.setPoint(each, new_pos_point, OpenMaya.MSpace.kWorld)



    def get_input_geom(self, data, geom_idx):
        input_attr = data.outputArrayValue( self.input )
        input_handle = data.outputArrayValue(self.input)
        input_handle.jumpToElement(geom_idx)
        input_geom_obj = input_handle.outputValue().child(self.inputGeom).asMesh()
        return input_geom_obj



    def get_node_name(self):
        self.thisNode = self.thisMObject()
        self.socketNode = OpenMaya.MFnDependencyNode( self.thisNode )
        node_name = self.socketNode.name()
        return node_name

    def get_obj_name(self, node_name, geom_index):
        first_obj_str = self.deform_class.getAffectedGeometry(node_name)
        for each in first_obj_str:
            if first_obj_str[each] == geom_index:
                first_obj = each
        return first_obj



def creator():
    return OpenMayaMPx.asMPxPtr(MESHCOLLIDER())


def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    nMAttr = OpenMaya.MFnMatrixAttribute()
    cAttr = OpenMaya.MFnCompoundAttribute()
    tAttr = OpenMaya.MFnTypedAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    # string attr

    # INPUT MESH
    MESHCOLLIDER.input_mesh = tAttr.create('InputMeshOne', 'inm', OpenMaya.MFnData.kMesh)
    tAttr.setWritable(True)
    tAttr.setStorable(True)
    tAttr.setReadable(True)
    tAttr.setKeyable(True)

    MESHCOLLIDER.collidr_mesh = tAttr.create('ColliderMesh', 'com', OpenMaya.MFnData.kMesh)
    tAttr.setWritable(True)
    tAttr.setStorable(True)
    tAttr.setReadable(True)
    tAttr.setKeyable(True)


    # OFFSETPUSHVERTEX
    MESHCOLLIDER.offset_vertex = nAttr.create("Offsetvert", "ofv", OpenMaya.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)




    # PAINT FOR SMOOTH
    MESHCOLLIDER.connected_mesh = tAttr.create('ConnectMesh', 'cm', OpenMaya.MFnData.kMesh)
    tAttr.setWritable(True)
    tAttr.setStorable(True)
    tAttr.setReadable(True)
    tAttr.setKeyable(True)

    MESHCOLLIDER.addAttribute(MESHCOLLIDER.offset_vertex)
    MESHCOLLIDER.addAttribute(MESHCOLLIDER.connected_mesh)
    MESHCOLLIDER.addAttribute(MESHCOLLIDER.input_mesh)
    MESHCOLLIDER.addAttribute(MESHCOLLIDER.collidr_mesh)

    outputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
    MESHCOLLIDER.attributeAffects(MESHCOLLIDER.offset_vertex, outputGeom)
    MESHCOLLIDER.attributeAffects(MESHCOLLIDER.connected_mesh, outputGeom)
    MESHCOLLIDER.attributeAffects(MESHCOLLIDER.input_mesh, outputGeom)
    MESHCOLLIDER.attributeAffects(MESHCOLLIDER.collidr_mesh, outputGeom)

    cmds.makePaintable(MESHCOLLIDER.kPluginNodeName, 'weights', attrType='multiFloat', shapeMode='deformer')


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode(MESHCOLLIDER.kPluginNodeName,
                            MESHCOLLIDER.kPluginNodeId,
                            creator,
                            initialize,
                            OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise "Failed to register node: %s" % MESHCOLLIDER.kPluginNodeName


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(MESHCOLLIDER.kPluginNodeId)
    except:
        raise "Failed to deregister node: %s" % MESHCOLLIDER.kPluginNodeName
