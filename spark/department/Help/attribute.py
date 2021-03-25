
import maya.cmds as cmds

class ATTRIBUTE:

    def __init__(self):
        self.vector = 'double3'
        self.integer = 'long'
        self.string = 'string'
        self.float = 'double'
        self.boolean = 'bool'
        self.enum = 'enum'



    def add_attr(self, obj, attribute_type, attribute_name='sample', min_val=0, max_val=999999999, default_val=0, enumlist=[]):
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



            print('vector will work')

        elif attribute_type == self.integer:
            attribute_type_val = True
            print('int')

        elif attribute_type == self.string:
            attribute_type_val = True
            print('string')

        elif attribute_type == self.float:
            attribute_type_val = True
            print(self.float)

        elif attribute_type == self.boolean:
            attribute_type_val = True
            print(self.boolean)

        elif attribute_type == self.enum:
            attribute_type_val = True
            print(self.enum)

        else:
            print('NONE OF THE ATTRIBUTE IS SPECIFIED WITH : ', self.vector, self.integer, self.string, self.float, self.boolean, self.enum)





















