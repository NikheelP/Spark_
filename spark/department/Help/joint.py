
import maya.cmds as cmds



class JOINT():
    def __init__(self):
        pass

    def isJoint(self, joint):
        '''
        	Check if the specified object is a valid joint
        	@param joint: Object to check
        	@type joint: str
        	'''
        # Check object exists
        if not cmds.objExists(joint): return False

        # Check joint
        if not cmds.ls(type='joint').count(joint): return False

        # Return result
        return True


    def createJointOnCurve(self, curve_name):
        '''
        CREATE A JOINT ON CURVE POINT
        :param curve_name:
        :return:
        '''

        noCV = cmds.getAttr(curve_name + '.degree') + cmds.getAttr(curve_name + '.spans')
        a = 0
        old_jnt = ''
        jnt_list = []
        while a < noCV:
            point_position = cmds.pointPosition(curve_name + '.cv[%s]' % (a))
            jnt_name = curve_name + '_' + str(a + 1) + '_Jnt'
            cmds.select(cl=True)
            cmds.joint(n=jnt_name, p=point_position)
            if not old_jnt == '':
                cmds.parent(jnt_name, jnt_list[-1])

            jnt_list.append(jnt_name)
            old_jnt = None
            a += 1

        return jnt_list[0], jnt_list