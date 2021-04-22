
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

class BASE:
    def __init__(self):
        pass

    def getMObject(self, object):
        '''
        Return an MObject for the input scene object
        @param object: Object to get MObject for
        @type object: str
        '''
        # Check input object
        if not cmds.objExists(object):
            raise Exception('Object "' + object + '" does not exist!!')
        # Get selection list
        selectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getSelectionListByName(object, selectionList)
        mObject = OpenMaya.MObject()
        selectionList.getDependNode(0, mObject)
        # Return result
        return mObject