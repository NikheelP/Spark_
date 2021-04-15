
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


    def createJointOnCurve(self, curve_name, addCtrl=False):
        '''
        CREATE A JOINT ON CURVE POINT
        :param curve_name:
        :return:
        '''

        noCV = cmds.getAttr(curve_name + '.degree') + cmds.getAttr(curve_name + '.spans')
        a = 0
        old_jnt = ''
        jnt_list = []
        jnt_all_list = []
        while a < noCV:
            point_position = cmds.pointPosition(curve_name + '.cv[%s]' % (a))
            jnt_name = curve_name + '_' + str(a + 1) + '_Jnt'
            cmds.select(cl=True)
            cmds.joint(n=jnt_name, p=point_position)
            jnt_all_list.append(jnt_name)
            if a == 0:
                first_jnt = jnt_name
            if addCtrl:
                if not a+1 == noCV:
                    ctrl_name = jnt_name + '_Ctrl'
                    name = cmds.circle(n=ctrl_name, nr=(1, 0, 0), c=(0, 0, 0), r=2 )
                    cmds.delete(cmds.parentConstraint(jnt_name, ctrl_name, mo=False))
                    cmds.select(ctrl_name)
                    cmds.DeleteHistory()
                    cmds.FreezeTransformations()
                    cmds.parent(ctrl_name, jnt_name)

            if jnt_list:
                cmds.parent(jnt_name, jnt_list[-1])

            if addCtrl:
                if not a + 1 == noCV:
                    jnt_list.append(ctrl_name)
                else:
                    jnt_list.append(jnt_name)
            else:
                jnt_list.append(jnt_name)

            a += 1
        return first_jnt, jnt_all_list