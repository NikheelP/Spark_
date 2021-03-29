
import maya.cmds as cmds



class HELP:

    def __init__(self):
        pass

    def set_type(self, obj, type_val, obj_type='obj_type'):
        '''

        :param obj: specify the object
        :param type_val: specify the type val
        :return:
        '''
        if cmds.ls(obj + '.' + obj_type) == []:
            cmds.addAttr(obj, ln=obj_type, dt='string')
            cmds.setAttr((obj + '.' + obj_type), e=True, k=True)

        cmds.setAttr((obj + '.' + obj_type), type_val, type='string')

        return obj

    def set_outline_color(self, obj, val=[0,0,0]):
        '''

        :param obj: specify the object
        :param val: specify th elist
        :return:
        '''
        cmds.select(obj)
        cmds.setAttr(obj + '.useOutlinerColor', 1)
        cmds.setAttr(obj + '.outlinerColor', val[0], val[1], val[2])

        return obj

