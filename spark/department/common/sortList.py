import re
import random
import maya.cmds as cmds

class SORTLIST:
    def __init__(self):
        pass



    def sort_list(self, list_obj):

        dic_val = {}
        for each in list_obj:
            # split the value
            int_val = int(re.search(r'\d+', each).group())
            split_val = each.split(str(int_val))[0]
            dic_val[int_val] = split_val
        sorted_val = sorted(dic_val)
        new_list = []
        for each in sorted_val:
            new_val = dic_val[each] + str(each)
            new_list.append(new_val)

        return new_list


    def sort_selected(self):
        new_agin_list = cmds.ls(sl=True)
        parent_grp_name = cmds.listRelatives(new_agin_list[0], parent=True)

        final_list = self.sort_list(new_agin_list)
        new_test_grp_name = 'new_Test_Grp'
        if cmds.objExists(new_test_grp_name):
            new_grp_name = new_test_grp_name + str(len(cmds.ls(new_test_grp_name)) + 1)
        else:
            new_grp_name = new_test_grp_name

        cmds.group(final_list, n=new_grp_name)
        #IF THE PARENT GRP NAME IS NONE THEN UNPARENT ALL
        if parent_grp_name == None:
            cmds.parent(final_list, w=True)
        else:
            cmds.parent(final_list, parent_grp_name[0])

        cmds.delete(new_test_grp_name)

        return True