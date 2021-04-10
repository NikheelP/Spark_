
import maya.cmds as cmds

class ATTRIBUTE:

    def __init__(self):
        self.vector = 'double3'
        self.integer = 'long'
        self.string = 'string'
        self.float = 'double'
        self.boolean = 'bool'
        self.enum = 'enum'



    def add_attr(self, obj, attribute_type, attribute_name='sample', min_val=-999999999, max_val=999999999, default_val=0, enumlist=[]):
        '''
        ADD ATTRIBUTE VALYE
        :param obj: SPECIFY THE OBJECT TO ADD ATTRIBUTE
        :param attribute_type: SPECIFY THE ATTRIBUTE TYPE EX : VECTOR/INTEGER/STRING/FLOAT/BOOLEAN/ENUM
        :param attribute_name: SPCIFY THE ATTRIBUTE NAME
        :param min_val: SPECIFY THE MIN VALUE
        :param max_val: SPECIFY THE MAX VALUE
        :param default_val: SPECIFY THE DEFAULT VALUE
        :param enumlist: SPECIFY THE ENUMELIST
        :return:
        '''
        attribute_type_val = False


        #IF IT IS A STRING
        if attribute_type == self.vector:
            cmds.addAttr(obj, ln=attribute_name, at=self.vector)
            cmds.addAttr(obj, ln=attribute_name + 'X', at=self.float)
            cmds.addAttr(obj, ln=attribute_name + 'Y', at=self.float)
            cmds.addAttr(obj, ln=attribute_name + 'Z', at=self.float)
            cmds.setAttr(obj + '.' + attribute_name, k=True, e=True)


            print('vector will work')

        elif attribute_type == self.integer:
            attribute_type_val = True
            cmds.addAttr(obj, ln=attribute_name, at='long', min=min_val, max=max_val, dv=default_val)
            cmds.setAttr(obj + '.' + attribute_name, k=True, e=True)

        elif attribute_type == self.string:
            attribute_type_val = True
            cmds.addAttr(obj, ln=attribute_name, dt='string')
            cmds.setAttr(obj + '.' + attribute_name, k=True, e=True)

        elif attribute_type == self.float:
            attribute_type_val = True
            cmds.addAttr(obj, ln=attribute_name, at='double', min=min_val, max=max_val, dv=default_val)
            cmds.setAttr(obj + '.' + attribute_name, k=True, e=True)

        elif attribute_type == self.boolean:
            attribute_type_val = True
            print(self.boolean)
            cmds.addAttr(obj, ln=attribute_name, at='bool', min=min_val, max=max_val, dv=default_val)
            cmds.setAttr(obj + '.' + attribute_name, k=True, e=True)

        elif attribute_type == self.enum:
            attribute_type_val = True
            print(self.enum)
            middle_ = ''
            for each_enumlist in enumlist:
                middle_ += each_enumlist + ':'
            cmds.addAttr(obj, ln=attribute_name, at='enum', en=middle_)
            cmds.setAttr(obj + '.' + attribute_name, k=True, e=True)


        else:
            print('NONE OF THE ATTRIBUTE IS SPECIFIED WITH : ', self.vector, self.integer, self.string, self.float, self.boolean, self.enum)


    def get_all_attr_val(self, obj_name):
        '''

        :return:
        '''
        attr_list = {}
        list_attr = cmds.listAttr(obj_name, k=True)
        for each_attr in list_attr:
            try:
                attr_list[each_attr] = cmds.getAttr(obj_name + '.' + each_attr)
            except:
                pass

        return attr_list























