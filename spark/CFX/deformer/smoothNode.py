import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math
import maya.cmds as cmds


class SMOOTHNODE(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeName = 'smoothNode'
    kPluginNodeId = OpenMaya.MTypeId(0xBA00103)
    strength_attr = OpenMaya.MObject()
    iteration_attr = OpenMaya.MObject()
    steps_attr = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def get_weighted_componenents(self, geom_iter, geom_index, data):
        '''Return a dictionary a weighted components index and weights
        '''
        # Init weight dictionary
        weights = dict()

        # Parse components
        while not geom_iter.isDone():
            index = geom_iter.index()

            # Get current component deformer weight
            weight = self.weightValue(data, geom_index, index)

            # Store component index and related weight
            if weight:
                weights[index] = weight

            # Move to next
            geom_iter.next()
        return weights

    def get_input_mesh(self, data, geom_index):
        '''Return input mesh for geometry input index
        '''
        input_attr_handle = data.outputArrayValue(self.input)
        input_attr_handle.jumpToElement(geom_index)
        geom_handle = input_attr_handle.outputValue().child(self.inputGeom)
        input_geom = geom_handle.asMesh()

        return input_geom

    def get_component_average_position(self, vtx_index):
        '''Will return component neighbors average position
        '''
        # Set iterator index
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        prev_ptr = util.asIntPtr()
        self.vtx_iterator.setIndex(vtx_index, prev_ptr)

        # Get connected vertices
        vertices = OpenMaya.MIntArray()
        self.vtx_iterator.getConnectedVertices(vertices)

        # Get total position
        total_pos = OpenMaya.MPoint()
        for j in vertices:
            total_pos += OpenMaya.MVector(self.all_positions[j])

        # Return averaged position
        return total_pos / vertices.length()

    def deform(self,
               data,  # dataBlock
               geom_iter,  # geom iteration class instance
               matrix,  # local to worl matrix
               geom_index):
        env_value = data.inputValue(self.envelope).asFloat()
        if not env_value:
            return False

        iter_value = data.inputValue(self.iteration_attr).asInt()
        if not iter_value:
            return False

        steps_value = data.inputValue(self.steps_attr).asInt()
        if not steps_value:
            return False

        strength_value = data.inputValue(self.strength_attr).asFloat()
        if not strength_value:
            return False

        # Get weighted components
        comp_weight_data = self.get_weighted_componenents(geom_iter, geom_index, data)
        if not comp_weight_data:
            return False

        # Get input mesh
        input_mesh = self.get_input_mesh(data, geom_index)

        # Get polygon iteration tool
        self.vtx_iterator = OpenMaya.MItMeshVertex(input_mesh)

        # Get all start positions
        self.all_positions = OpenMaya.MPointArray()
        geom_iter.allPositions(self.all_positions)

        # Compute deformation
        for i in range(iter_value):
            for step in range(steps_value):
                # Init new position array
                new_positions = OpenMaya.MPointArray(self.all_positions)
                new_positions.copy(self.all_positions)

                for index in comp_weight_data:
                    # Get current component weight and position
                    weight = comp_weight_data[index]
                    current_pos = self.all_positions[index]

                    # Get average position
                    average_pos = self.get_component_average_position(index)

                    # Compute new component position
                    offset_pos = (average_pos - current_pos) * weight * env_value * strength_value
                    new_pos = current_pos + offset_pos / (steps_value - step)

                    # Update new position
                    new_positions.set(new_pos, index)

                # Update stored position for next iteration
                self.all_positions.copy(new_positions)

        # Set new positions:
        geom_iter.setAllPositions(self.all_positions)

        return True

def creator():
    return OpenMayaMPx.asMPxPtr(SMOOTHNODE())


def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    nMAttr = OpenMaya.MFnMatrixAttribute()

    SMOOTHNODE.strength_attr = nAttr.create("strength", "str", OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0)
    nAttr.setMax(1)
    nAttr.setDefault(0.5)

    SMOOTHNODE.iteration_attr = nAttr.create("iterations", "itr", OpenMaya.MFnNumericData.kInt)
    nAttr.setKeyable(True)
    nAttr.setMin(0)

    SMOOTHNODE.steps_attr = nAttr.create("steps", "stp", OpenMaya.MFnNumericData.kInt)
    nAttr.setKeyable(True)
    nAttr.setMin(0)
    # nAttr.setDefault(3)

    SMOOTHNODE.addAttribute(SMOOTHNODE.strength_attr)
    SMOOTHNODE.addAttribute(SMOOTHNODE.iteration_attr)
    SMOOTHNODE.addAttribute(SMOOTHNODE.steps_attr)

    outputGeom = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom
    SMOOTHNODE.attributeAffects(SMOOTHNODE.strength_attr, outputGeom)
    SMOOTHNODE.attributeAffects(SMOOTHNODE.iteration_attr, outputGeom)
    SMOOTHNODE.attributeAffects(SMOOTHNODE.steps_attr, outputGeom)

    cmds.makePaintable(SMOOTHNODE.kPluginNodeName, 'weights', attrType='multiFloat', shapeMode='deformer')


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode(SMOOTHNODE.kPluginNodeName,
                            SMOOTHNODE.kPluginNodeId,
                            creator,
                            initialize,
                            OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise "Failed to register node: %s" % SMOOTHNODE.kPluginNodeName


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(SMOOTHNODE.kPluginNodeId)
    except:
        raise "Failed to deregister node: %s" % SMOOTHNODE.kPluginNodeName
