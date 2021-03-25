
import maya.cmds as cmds
import maya.mel as mel

from spark.department import help
for each in [help]:
    reload(each)

from spark.department.help import HELP

class RIGFX:

    def __init__(self):
        self.help_class = HELP()

    def create_Cloth(self, obj):
        '''

        :return: cloth, input, rest, ncloth, nucleus
        '''
        nucleus_name = None
        #CREATE A CLOTH GEO AND ADD TAG
        cloth_name = obj + '_Cloth'
        input_name = obj + '_Input'
        rest_name = obj + '_Rest'
        ncloth_name = obj + '_nCloth'
        for each_cloth_mesh in [cloth_name, input_name, rest_name]:
            if not cmds.objExists(each_cloth_mesh):
                cmds.duplicate(obj, n=each_cloth_mesh)
            if 'cloth' in each_cloth_mesh.lower():
                self.help_class.set_type(obj=each_cloth_mesh, type_val='cloth')
            if 'input' in each_cloth_mesh.lower():
                self.help_class.set_type(each_cloth_mesh, type_val='input')
            if 'rest' in each_cloth_mesh.lower():
                self.help_class.set_type(obj=each_cloth_mesh, type_val='rest')

        #MAKE A BLENDSHAPE
        input_blndshape_name = cmds.blendShape(obj, input_name)[0]
        cmds.setAttr(input_blndshape_name + '.' + obj, 1)
        cloth_blendshape_name = cmds.blendShape(input_name, cloth_name)[0]
        cmds.setAttr(cloth_blendshape_name + '.' + input_name, 1)


        #CREATE A NCLOTH
        mel.eval('createNCloth 0;')
        shape_list = cmds.listRelatives(cloth_name, s=True)
        for each_shape in shape_list:
            ncloth_list = cmds.listConnections(each_shape, type='nCloth')
            if ncloth_list != None:
                cmds.rename(ncloth_list[0], ncloth_name)
                ncloth_shape_name = cmds.listRelatives(ncloth_name, s=True)[0]
                nucleus_name = cmds.listConnections(ncloth_shape_name, type='nucleus')[0]
                #CONNECT THE REST SHAPE NAME
                #connectAttr -f pant_Geo_RestShape.outMesh pant_Geo_nClothShape.restShapeMesh;
                rest_shape_name = cmds.listRelatives(rest_name, s=True)[0]
                cmds.connectAttr((rest_shape_name + '.outMesh'), (ncloth_shape_name + '.restShapeMesh'), f=True)
                break
            else:
                nucleus_name = None

        #CHANGE CLOTH SHAPE NAME
        list_connections = cmds.listRelatives(cloth_name)
        a = 1
        for each in list_connections:
            name = obj + str(a) + 'Shape'
            cmds.rename(each, name)
            a += 1

        #now set the color
        self.help_class.set_outline_color(cloth_name, val=[0, 1, 1])
        self.help_class.set_outline_color(input_name, val=[1, 1, 0])
        self.help_class.set_outline_color(rest_name, val=[0, 1, 0])
        self.help_class.set_outline_color(ncloth_name, val=[1, 0, 0])


        return cloth_name, input_name, rest_name, ncloth_name, nucleus_name