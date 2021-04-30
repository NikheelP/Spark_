
import maya.cmds as cmds
import maya.mel as mel

from spark.department.Help import help
for each in [help]:
    reload(help)

from spark.department.Help.help import HELP


class RENAME():

    def __init__(self):
        self.help_class = HELP()

    def search_replace(self, list_object, search_name, replace_name):
        if self.help_class.is_type(list_object) == list:
            for each in list_object:
                new_name = each.replace(search_name, replace_name)
                cmds.rename(each, new_name)
            return True
        return False

    def add_prefix(self, list_object, prefix_name):
        if self.help_class.is_type(list_object) == list:
            for each in list_object:
                if '|' in each:
                    last_name = each.split('|')[-1]
                else:
                    last_name = each

                new_name = prefix_name + last_name
                cmds.rename(each, new_name)


    def add_suffix(self, list_object, suffix_name):
        if self.help_class.is_type(list_object) == list:
            for each in list_object:
                if '|' in each:
                    first_name = each.split('|')[-1]
                else:
                    first_name = each

                new_name = first_name + suffix_name
                cmds.rename(each, new_name)


    def rename(self, list_object, object_name, start_val, padding):
        '''
        rename the object
        '''
        start_val = int(start_val)
        padding = int(padding)


        a = 0
        while a < len(list_object):
            number = str(format(start_val, '0%s' % (padding)))
            name = object_name + number


            cmds.rename(list_object[a], name)
            start_val += 1
            a += 1


    def remove_lastword(self, list_object):
        for each in list_object:
            cmds.rename(each, each.split(each[-1])[0])

    def remove_firstword(self, list_object):
        for each in list_object:
            cmds.rename(each, each.split(each[0])[1])




'''
def rename_object(list_object, obj_name, desimal=2, step=1):
    a = 0
    string_val = '0'
    while a < desimal:
        string_val += '0'

        a+=1
    b = 0
    for each_obj in list_object:
        name = obj_name + '_' + str(string_val) + str(b)
        b+= step
        cmds.rename(each_obj, name)



import maya.mel as mel
sel_obj = cmds.ls(sl=True)
for each in sel_obj:
    cmds.select(each)
    mel.eval('mirrorJoint -mirrorYZ -mirrorBehavior -searchReplace "Left" "Right";')

sel_jnt = cmds.ls(sl=True)
for each in sel_jnt:
    name = each + '_LOC'
    grp_name = name + '_Grp'
    cmds.spaceLocator(n=name, p=[0, 0, 0])
    shape_name = cmds.listRelatives(name, s=True)[0]
    for each_scale in ['localScaleX', 'localScaleY', 'localScaleZ']:
        cmds.setAttr(shape_name + '.' + each_scale, 0.02)
    cmds.createNode('transform', n=grp_name)
    cmds.delete(cmds.pointConstraint(each, name, mo=False))
    cmds.delete(cmds.pointConstraint(each, grp_name, mo=False))
    cmds.select(name, grp_name)
    cmds.DeleteHistory()
    cmds.FreezeTransformations()
    cmds.parent(name, grp_name)
    cmds.parentConstraint(name, each, mo=True)
    cmds.scaleConstraint(name, each, mo=True)

sel_list = cmds.ls(sl=True)
rename_object(sel_list, 'Test_file')
'''




