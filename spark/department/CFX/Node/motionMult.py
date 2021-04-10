import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

kPluginNodeName = 'motionMult'
from spark.department.Help import Math_help

for each in [Math_help]:
    reload(each)

from spark.department.Help.Math_help import MATHUTIL_HELP

class MOTIONMULT(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00047253)
    mInputDriver = OpenMaya.MObject()
    input_grp_t = OpenMaya.MObject()
    output_grp_t = OpenMaya.MObject()
    valuetrans = OpenMaya.MObject()
    valuerot = OpenMaya.MObject()
    rOutput = OpenMaya.MObject()
    connect_trans = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        self.math_class = MATHUTIL_HELP()

    def get_x_y_z_val(self, matrix):
        driverA_x = OpenMaya.MScriptUtil.getDoubleArrayItem(matrix[3], 0)
        driverA_y = OpenMaya.MScriptUtil.getDoubleArrayItem(matrix[3], 1)
        driverA_z = OpenMaya.MScriptUtil.getDoubleArrayItem(matrix[3], 2)
        return driverA_x, driverA_y, driverA_z

    def get_input(self, mobj, plug_name):
        depfn = OpenMaya.MFnDependencyNode(mobj)
        mplug = depfn.findPlug(plug_name)
        mplugarray = OpenMaya.MPlugArray()
        val = mplug.connectedTo(mplugarray, True, False)
        return val, mplugarray

    def get_output(self, mobj, plug_name):
        depfn = OpenMaya.MFnDependencyNode(mobj)
        mplug = depfn.findPlug(plug_name)
        mplugarray = OpenMaya.MPlugArray()
        val = mplug.connectedTo(mplugarray, False, True)
        return val, mplugarray

    def get_val(self, part, total_val, axis_val):
        part = part
        whole = total_val
        value = total_val * float(part) / float(whole)
        val = (float(axis_val) * value) / total_val
        return val

    def getRotation(self, matrix, rotationOrder='xyz'):
        '''
        Return the rotation component of a matrix as euler (XYZ) values.
        @param matrix: Matrix to extract rotation from
        @type matrix: maya.OpenMaya.MMatrix
        @param rotationOrder: Rotation order of the matrix
        @type rotationOrder: str or int
        '''
        # Calculate radian constant
        radian = 180.0 / math.pi

        # Check rotation order
        if type(rotationOrder) == str:
            rotationOrder = rotationOrder.lower()
            rotateOrder = {'xyz': 0, 'yzx': 1, 'zxy': 2, 'xzy': 3, 'yxz': 4, 'zyx': 5}
            if not rotateOrder.has_key(rotationOrder):
                raise Exception('Invalid rotation order supplied!')
            rotationOrder = rotateOrder[rotationOrder]
        else:
            rotationOrder = int(rotationOrder)

        # Get transformation matrix
        transformMatrix = OpenMaya.MTransformationMatrix(matrix)

        # Get Euler rotation from matrix
        eulerRot = transformMatrix.eulerRotation()

        # Reorder rotation
        eulerRot.reorderIt(rotationOrder)

        # Return XYZ rotation values
        return (eulerRot.x * radian, eulerRot.y * radian, eulerRot.z * radian)

    def compute(self, plug, data):

        input_one_trans_val = data.inputValue(MOTIONMULT.input_one_t).asFloat3()
        trans_blend_val = data.inputValue(MOTIONMULT.t_blend).asFloat()

        input_grp_t_Output = data.outputValue(MOTIONMULT.input_grp_t)
        output_grp_t_Output = data.outputValue(MOTIONMULT.output_grp_t)

        #SET_INPUT_GRP_VAL
        input_pos = []
        for each in input_one_trans_val:
            pos_val = each * -1
            pos_val = pos_val * trans_blend_val
            input_pos.append(pos_val)

        #SET OUTPUT GRP_VAL
        output_pos = []
        for each in input_one_trans_val:
            pos_val = each * trans_blend_val
            output_pos.append(pos_val)

        input_grp_t = OpenMaya.MFloatVector(input_pos[0], input_pos[1], input_pos[2])
        input_grp_t_Output.setMFloatVector(input_grp_t)

        output_grp_t = OpenMaya.MFloatVector(output_pos[0], output_pos[1], output_pos[2])
        output_grp_t_Output.setMFloatVector(output_grp_t)



        '''

        average_trans_val = self.math_class.averagePosition(input_one_trans_val, input_two_trans_val, trans_blend_val)
        average_rot_val = self.math_class.averagePosition(input_one_rot_val, input_two_rot_val, rot_blend_val)

        tx_vector = OpenMaya.MFloatVector(average_trans_val[0], average_trans_val[1], average_trans_val[2])
        tOutput.setMFloatVector(tx_vector)

        r_vector = OpenMaya.MFloatVector(average_rot_val[0], average_rot_val[1], average_rot_val[2])
        rOutput.setMFloatVector(r_vector)
        '''




        pass
        '''
        
        input_driver = data.inputValue(MOTIONMULT.mInputDriver).asMatrix()
        valuetrans_val = data.inputValue(MOTIONMULT.valuetrans).asFloat()
        valuerot_val = data.inputValue(MOTIONMULT.valuerot).asFloat()
        tOutput = data.outputValue(MOTIONMULT.output_t)
        rOutput = data.outputValue(MOTIONMULT.output_r)

        # get the translate x y z position
        x_trans, y_trans, z_trans = self.get_x_y_z_val(input_driver)
        x_rot, y_rot, z_rot = self.getRotation(input_driver)

        x_new_trans_val = self.get_val(part=valuetrans_val, total_val=1, axis_val=x_trans)
        y_new_trans_val = self.get_val(part=valuetrans_val, total_val=1, axis_val=y_trans)
        z_new_trans_val = self.get_val(part=valuetrans_val, total_val=1, axis_val=z_trans)
        x_new_rot_val = self.get_val(part=valuerot_val, total_val=1, axis_val=x_rot)
        y_new_rot_val = self.get_val(part=valuerot_val, total_val=1, axis_val=y_rot)
        z_new_rot_val = self.get_val(part=valuerot_val, total_val=1, axis_val=z_rot)

        # print(x_trans, y_trans, z_trans)
        # print valuetrans_val
        # print(x_new_trans_val, y_new_trans_val, z_new_trans_val)

        tx_vector = OpenMaya.MFloatVector(x_new_trans_val, y_new_trans_val, z_new_trans_val)
        rx_vector = OpenMaya.MFloatVector(x_new_rot_val, y_new_rot_val, z_new_rot_val)
        tOutput.setMFloatVector(tx_vector)
        rOutput.setMFloatVector(rx_vector)
        # rOutput.setMFloatVector(resultRot)
        '''


def creator():
    return OpenMayaMPx.asMPxPtr(MOTIONMULT())


def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    nMAttr = OpenMaya.MFnMatrixAttribute()

    MOTIONMULT.input_one_t = nAttr.createPoint("inputOneTrans", "iot")
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(True)

    MOTIONMULT.t_blend = nAttr.create('tBlend', 'tbl', OpenMaya.MFnNumericData.kFloat, 1)
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setMin(0)
    nAttr.setMax(1)
    nAttr.setKeyable(True)



    MOTIONMULT.input_grp_t = nAttr.createPoint("inputTrans", "it")
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    #nAttr.setKeyable(True)

    MOTIONMULT.output_grp_t = nAttr.createPoint("outputTrans", "ot")
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    # nAttr.setKeyable(True)





    '''

    MOTIONMULT.mInputDriver = nMAttr.create('Input', 'in', OpenMaya.MFnMatrixAttribute.kDouble)
    nMAttr.setWritable(True)
    nMAttr.setStorable(True)
    nMAttr.setReadable(True)
    nMAttr.setKeyable(True)

    MOTIONMULT.valuetrans = nAttr.create('FirstT', 'ft', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setMin(0)
    nAttr.setMax(1)
    nAttr.setKeyable(True)

    MOTIONMULT.valuerot = nAttr.create('ValueR', 'vr', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setMin(0)
    nAttr.setMax(1)
    nAttr.setKeyable(True)

    MOTIONMULT.output_t = nAttr.createPoint("translate", "t")
    nAttr.setWritable(False)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)

    MOTIONMULT.connect_trans = nAttr.createPoint("connectt", "ct")
    nAttr.setWritable(True)
    nAttr.setStorable(False)
    nAttr.setReadable(False)
    nAttr.setKeyable(True)

    MOTIONMULT.output_r = nAttr.createPoint("rotate", "r")
    nAttr.setWritable(False)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)
    
    '''

    MOTIONMULT.addAttribute(MOTIONMULT.input_one_t)
    MOTIONMULT.addAttribute(MOTIONMULT.t_blend)
    MOTIONMULT.addAttribute(MOTIONMULT.input_grp_t)
    MOTIONMULT.addAttribute(MOTIONMULT.output_grp_t)




    MOTIONMULT.attributeAffects(MOTIONMULT.input_one_t, MOTIONMULT.input_grp_t)
    MOTIONMULT.attributeAffects(MOTIONMULT.input_one_t, MOTIONMULT.output_grp_t)
    MOTIONMULT.attributeAffects(MOTIONMULT.t_blend, MOTIONMULT.input_grp_t)
    MOTIONMULT.attributeAffects(MOTIONMULT.t_blend, MOTIONMULT.output_grp_t)




    #MOTIONMULT.attributeAffects(MOTIONMULT.input_one_r, MOTIONMULT.output_r)
    #MOTIONMULT.attributeAffects(MOTIONMULT.input_two_r, MOTIONMULT.output_r)
    #MOTIONMULT.attributeAffects(MOTIONMULT.r_blend, MOTIONMULT.output_r)

    '''
    MOTIONMULT.addAttribute(MOTIONMULT.mInputDriver)
    MOTIONMULT.addAttribute(MOTIONMULT.valuetrans)
    MOTIONMULT.addAttribute(MOTIONMULT.valuerot)
    MOTIONMULT.addAttribute(MOTIONMULT.output_t)
    MOTIONMULT.addAttribute(MOTIONMULT.output_r)
    MOTIONMULT.addAttribute(MOTIONMULT.connect_trans)
    


    MOTIONMULT.attributeAffects(MOTIONMULT.valuetrans, MOTIONMULT.output_t)
    MOTIONMULT.attributeAffects(MOTIONMULT.valuerot, MOTIONMULT.output_r)
    MOTIONMULT.attributeAffects(MOTIONMULT.connect_trans, MOTIONMULT.output_t)
    MOTIONMULT.attributeAffects(MOTIONMULT.connect_trans, MOTIONMULT.output_r)
    '''

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode(kPluginNodeName, MOTIONMULT.kPluginNodeId, creator, initialize)
    except:
        raise "Failed to register node: %s" % MOTIONMULT.kPluginNodeName


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(MOTIONMULT.kPluginNodeId)
    except:
        raise "Failed to deregister node: %s" % MOTIONMULT.kPluginNodeName
