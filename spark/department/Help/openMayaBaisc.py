import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


class OPENMAYABASIC:
    def __init__(self):
        pass

    def get_mObject(self, obj_name):
        '''

        :param obj_name: specify the object
        :return:
        '''
        selection_list = OpenMaya.MSelectionList()
        selection_list.add(obj_name)

        mObject = OpenMaya.MObject()
        selection_list.getDependNode(0, mObject)
        return mObject