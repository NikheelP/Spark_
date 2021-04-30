
import maya.cmds as cmds
import maya.mel as mel
from spark.department.Help import namespace

for each in [namespace]:
    reload(each)

from spark.department.Help.namespace import NAMESPACE

class MODELING_CHECKLIST:

    def __init__(self):
        self.namespace_class = NAMESPACE()

    def deleteHistory(self):
        '''

        :return:
        '''

        sel_obj = cmds.ls()
        for each in sel_obj:
            cmds.select(each)
            cmds.DeleteHistory()

    def freez_transform(self):
        '''

        :return:
        '''

        sel_obj = cmds.ls()
        for each in sel_obj:
            cmds.select(each)
            cmds.FreezeTransformations()

    def delete_namespace(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls()
        for each in sel_obj:
            try:
                name_space = self.namespace_class.getNS(each)
                if name_space:
                    try:
                        self.namespace_class.deleteNS(name_space)
                    except:
                        pass
            except:
                pass

    def delUnusedNodes(self):
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")')

    def make_center_pivot(self):
        '''

        :return:
        '''
        transform_list = cmds.ls(type='transform')
        for each in transform_list:
            cmds.move(0, 0, 0, each + '.scalePivot', each + '.rotatePivot')
