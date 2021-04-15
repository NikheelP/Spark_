from collections import OrderedDict

import maya.cmds as cmds
import maya.mel as mel

from spark.department import help as depHelp
from spark.department.Help import joint
from spark.department.Help import help as helpHelp

for each in [depHelp, helpHelp, joint]:
    reload(each)

from spark.department.help import HELP as DEPHELP
from spark.department.Help.help import HELP as HelpHELP
from spark.department.Help.joint import JOINT


class RIGFX:

    def __init__(self):
        self.help_class = DEPHELP()
        self.help_help_class = HelpHELP()
        self.joint_class = JOINT()

        self.rigFx_type = 'RigFx'
        self.input_type = 'Input'
        self.inputcloth_type = 'InputCloth'
        self.restcloth_type = 'RestCloth'
        self.cloth_type = 'Cloth'
        self.techanim_type = 'TechAnim'
        self.techanim_final_type = 'TechAnimFinal'
        self.sim_type = 'Sim'
        self.techanim_cloth_type = 'TechAnimCloth'
        self.techanim_cloth_final_type = 'TechAnimClothFinal'
        self.hairSystem_type = 'hairSystem'
        self.final_type = 'Final'
        self.version_type = 'VersionNo'
        self.collution_nRigit = 'CollutionRigit'
        self.component_type = 'Component'
        self.component_to_component_type = 'ComponentToComponent'
        self.forcefield_type = 'ForceField'
        self.pointtosurface_type = 'PointTOSurface'
        self.pointtosurface_nRigit = 'PointTOSurfaceRigit'
        self.slidetosurface_type = 'SlideToSurface'
        self.slidetosurface_nRigit = 'SlideToSurfaceRigit'

        self.tearablesurface_type = 'TearableSurface'
        self.transoformconstraint_type = 'TransoformConstraint'
        self.airfield_type = 'AirField'
        self.dragfield_type = 'DragField'
        self.gravityfield_type = 'GravityField'
        self.newtonfield_type = 'NewtonField'
        self.radiusfield_type = 'RadiusField'
        self.turbulancefield_type = 'TurbulanceField'
        self.uniformfield_type = 'UniformField'
        self.vortexfield_type = 'VortexField'
        self.volumefield_type = 'VolumeField'
        self.volumecurve_type = 'VolumeCurve'

        self.input_lyr_name = 'Input_Lyr'
        self.cloth_lyr_name = 'Cloth_Lyr'
        self.nCloth_lyr_name = 'nCloth_Lyr'
        self.input_rest_lyr_name = 'Input_Rest_Lyr'
        self.collution_lyr_name = 'Collution_Lyr'
        self.constraint_lyr_name = 'Constraint_Lyr'
        self.field_lyr_name = 'Field_Lyr'
        self.extra_lyr_name = 'Extra_Lyr'
        self.folical_lyr_name = 'Folical_Lyr'
        self.outputCurve_lyr_name = 'OutputCurve_Lyr'
        self.final_lyr_name = 'Final_Lyr'

        self.input_grp = 'Input_Grp'
        self.techAnim_grp = 'TechAnim_Grp'
        self.techAnim_Final_Grp = 'TechAnim_Final_Grp'
        self.sim_grp = 'Sim_Grp'
        self.helper_grp = 'Helper_Grp'
        self.cloth_grp = 'Cloth_Grp'
        self.hair_grp = 'Hair_Grp'
        self.techAnim_Cloth_Grp = 'TechAnimCloth_Grp'
        self.techAnim_Cloth_Final_Grp = 'TechAnimCloth_Final_Grp'
        self.final_Grp = 'Final_Grp'

        #SETS NAME
        self.input_sets = 'Input_Sets'
        self.techanim_sets = 'Techanim_Sets'
        self.cloth_sets = 'Cloth_Sets'
        self.nCloth_sets = 'nCloth_Sets'
        self.hairSystem_sets = 'HairSystem_Sets'
        self.techAnimCloth_sets = 'TechAnimCloth_Sets'
        self.final_sets = 'Final_Sets'
        self.simulation_sets = 'Simulation_Set'


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
                if each_cloth_mesh == input_name or each_cloth_mesh == rest_name:
                    cmds.setAttr(each_cloth_mesh + '.v', 0)
            if 'cloth' in each_cloth_mesh.lower():
                self.help_class.set_type(obj=each_cloth_mesh, type_val=self.cloth_type)
            if 'input' in each_cloth_mesh.lower():
                self.help_class.set_type(each_cloth_mesh, type_val=self.inputcloth_type)
            if 'rest' in each_cloth_mesh.lower():
                self.help_class.set_type(obj=each_cloth_mesh, type_val=self.restcloth_type)

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
                self.help_class.set_type(obj=ncloth_name, type_val='nCloth')
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

        #SET NCLOTH VAL TO VISIBLE
        cmds.connectAttr((ncloth_name + '.isDynamic'), (ncloth_name + '.v'), f=True)

        #now set the color
        self.help_class.set_outline_color(cloth_name, val=[0, 1, 1])
        self.help_class.set_outline_color(input_name, val=[1, 1, 0])
        self.help_class.set_outline_color(rest_name, val=[0, 1, 0])
        self.help_class.set_outline_color(ncloth_name, val=[1, 0, 0])


        return cloth_name, input_name, rest_name, ncloth_name, nucleus_name

    def create_hair(self, curvelist=[]):
        '''
        CREATE HAIR SYYSTEM FROM THE CURVE
        :param curve_name:
        :return:
        '''

        #CREATE A HAIR SYSTEM
        cmds.select(curvelist)
        mel.eval('doMakeCurvesNDynamic 2 { "1", "0", "1", "1", "0"  } ')


        #CREATE A STATIC JOINT
        #CREATE A DYNAMIC JOINT
        folical_list = []
        output_curve_list = []

        hairSystem_name = ''
        for each_curve in curvelist:
            static_curve, folical_name, outputCurve, hairSystem = self.get_folical_outputcurve_hairsystem(each_curve)

            folical_new_name = each_curve + '_Folical'
            outputCurve_new_name = each_curve + '_Dyn_Crv'
            cmds.rename(folical_name, folical_new_name)
            folical_list.append(folical_new_name)

            cmds.rename(outputCurve, outputCurve_new_name)
            output_curve_list.append(outputCurve_new_name)

            hairSystem_name = hairSystem



        return folical_list, output_curve_list, hairSystem_name

    def get_folical_outputcurve_hairsystem(self, curve_name):
        static_curve = curve_name
        static_curve_shape_name = cmds.listRelatives(static_curve, s=True)

        # GET THE FOLICAL NAME
        folical_name = ''
        for each_shape in static_curve_shape_name:
            list_connection = cmds.listConnections(each_shape, type='follicle')
            if list_connection:
                folical_name = list_connection[0]

        folical_shape_name = cmds.listRelatives(folical_name, s=True)[0]
        cmds.setAttr(folical_shape_name + '.pointLock', 1)

        # GET THE OUTPUT CURVE
        outputCurve = cmds.listConnections(folical_name + '.outCurve')[0]

        hairSystem = cmds.listConnections(cmds.listRelatives(folical_name, s=True)[0], type='hairSystem')[0]

        return static_curve, folical_name, outputCurve, hairSystem



    def get_cloth_folder_structure(self, cloth_name):
        '''
        CLOTH FOLDER STRUCTURE
        :param cloth_name: SPECIFY THE CLOTH NAME
        :return:
        '''
        collider_grp = cloth_name + '_Collider_Grp'
        constraint_grp = cloth_name + '_Constraint_Grp'
        field_grp = cloth_name + '_Field_Grp'
        extra_grp = cloth_name + '_Extra_Grp'

        return collider_grp, constraint_grp, field_grp, extra_grp

    def create_hair_folder_structure(self, hair_name):
        '''
        CREATE A HAIR FOLDER STRUCTURE
        :param hair_name:
        :return:
        '''
        if not cmds.objExists('Hair_Grp'):
            raise RuntimeError('Hair_Grp is not Exists Could you able to create one')

        collider_grp, constraint_grp, field_grp, extra_grp = self.get_cloth_folder_structure(cloth_name=hair_name)
        hair_grp_name = hair_name + '_Grp'
        folical_grp_name = hair_name + '_Folical_Grp'
        outputCurve_grp_name = hair_name + '_Output_Crv_Grp'
        if not cmds.objExists(hair_grp_name):
            cmds.createNode('transform', n=hair_grp_name)

        for each in [collider_grp, constraint_grp, field_grp, extra_grp, folical_grp_name, outputCurve_grp_name]:
            cmds.createNode('transform', n=each)

        self.help_class.set_type(obj=hair_grp_name, type_val='HairGrp')

        self.help_class.set_type(obj=collider_grp, type_val='ColliderGrp')
        self.help_class.set_type(obj=collider_grp, obj_type='ObjName', type_val=hair_name)
        cmds.editDisplayLayerMembers(self.collution_lyr_name, collider_grp, noRecurse=True)

        self.help_class.set_type(obj=constraint_grp, type_val='ConstraintGrp')
        self.help_class.set_type(obj=constraint_grp, obj_type='ObjName', type_val=hair_name)
        cmds.editDisplayLayerMembers(self.constraint_lyr_name, constraint_grp, noRecurse=True)

        self.help_class.set_type(obj=field_grp, type_val='FieldGrp')
        self.help_class.set_type(obj=field_grp, obj_type='ObjName', type_val=hair_name)
        cmds.editDisplayLayerMembers(self.field_lyr_name, field_grp, noRecurse=True)

        self.help_class.set_type(obj=extra_grp, type_val='ExtraGrp')
        self.help_class.set_type(obj=extra_grp, obj_type='ObjName', type_val=hair_name)
        cmds.editDisplayLayerMembers(self.extra_lyr_name, extra_grp, noRecurse=True)

        self.help_class.set_type(obj=folical_grp_name, type_val='FolicalGrp')
        self.help_class.set_type(obj=folical_grp_name, obj_type='ObjName', type_val=hair_name)
        cmds.editDisplayLayerMembers(self.folical_lyr_name, folical_grp_name, noRecurse=True)

        self.help_class.set_type(obj=outputCurve_grp_name, type_val='OutputCurveGrp')
        self.help_class.set_type(obj=outputCurve_grp_name, obj_type='ObjName', type_val=hair_name)
        cmds.editDisplayLayerMembers(self.outputCurve_lyr_name, outputCurve_grp_name, noRecurse=True)

        cmds.parent([collider_grp, constraint_grp, field_grp, extra_grp, folical_grp_name, outputCurve_grp_name], hair_grp_name)
        cmds.parent(hair_grp_name, 'Hair_Grp')

        return hair_grp_name



    def create_cloth_folder_structure(self, cloth_name):
        '''
        CREATE A CLOTH FOLDER STRUCTURE
        :param cloth_name:
        :return:
        '''
        if not cmds.objExists('Cloth_Grp'):
            raise RuntimeError('Cloth_Grp is not Exists Could you able to create one')

        collider_grp, constraint_grp, field_grp, extra_grp = self.get_cloth_folder_structure(cloth_name=cloth_name)
        cloth_grp_name = cloth_name + '_Grp'
        if not cmds.objExists(cloth_grp_name):
            cmds.createNode('transform', n=cloth_grp_name)

        for each in [collider_grp, constraint_grp, field_grp, extra_grp]:
            if not cmds.objExists(each):
                cmds.createNode('transform', n=each)

        self.help_class.set_type(obj=cloth_grp_name, type_val='ClothGrp')

        self.help_class.set_type(obj=collider_grp, type_val='ColliderGrp')
        self.help_class.set_type(obj=collider_grp, obj_type='ObjName', type_val=cloth_name)
        cmds.editDisplayLayerMembers(self.collution_lyr_name, collider_grp, noRecurse=True)

        self.help_class.set_type(obj=constraint_grp, type_val='ConstraintGrp')
        self.help_class.set_type(obj=constraint_grp, obj_type='ObjName', type_val=cloth_name)
        cmds.editDisplayLayerMembers(self.constraint_lyr_name, constraint_grp, noRecurse=True)

        self.help_class.set_type(obj=field_grp, type_val='FieldGrp')
        self.help_class.set_type(obj=field_grp, obj_type='ObjName', type_val=cloth_name)
        cmds.editDisplayLayerMembers(self.field_lyr_name, field_grp, noRecurse=True)

        self.help_class.set_type(obj=extra_grp, type_val='ExtraGrp')
        self.help_class.set_type(obj=extra_grp, obj_type='ObjName', type_val=cloth_name)
        cmds.editDisplayLayerMembers(self.extra_lyr_name, extra_grp, noRecurse=True)

        cmds.parent([collider_grp, constraint_grp, field_grp, extra_grp], cloth_grp_name)
        cmds.parent(cloth_grp_name, 'Cloth_Grp')

        return cloth_grp_name



    def create_cloth_rigfx_def(self, geo_name, cloth_grp_name):
        '''
        CREATE CLOTH RIGFX
        :return:
        '''
        if not cmds.objExists(self.techanim_type + '_Grp'):
            raise Exception(self.techanim_type + '_Grp is not Exists')

        #ADD INPUT TAG TO GEO
        self.help_class.set_type(obj=geo_name, type_val=self.input_type)

        #GET THE OF THE TECHANIM FILE
        techanim_child_list = cmds.listRelatives(self.techanim_type + '_Grp', c=True)
        blendshape_obj = geo_name
        for each in techanim_child_list:
            name = cmds.getAttr(each + '.obj_type') + '_' + cmds.getAttr(each + '.' + self.version_type)
            techanim_geo_name = name + '_' + geo_name
            cmds.duplicate(geo_name, n=techanim_geo_name)
            cmds.parent(techanim_geo_name, each)
            self.help_class.set_type(obj=techanim_geo_name, type_val=name)

            blend_shape = cmds.blendShape(blendshape_obj, techanim_geo_name, o='world')[0]
            cmds.setAttr(blend_shape + '.' + blendshape_obj, 1)

            #self.connect_inmesh_to_outmesh(blendshape_obj, techanim_geo_name)
            blendshape_obj = techanim_geo_name

        #TECHANIM CLOTH FINAL
        techanim_final_grp = 'TechAnim_Final_Grp'
        techanim_final = 'TechAnim_Final_' + geo_name
        cmds.duplicate(geo_name, n=techanim_final)
        cmds.parent(techanim_final, techanim_final_grp)

        blend_shape = cmds.blendShape(blendshape_obj, techanim_final, o='world')[0]
        cmds.setAttr(blend_shape + '.' + blendshape_obj, 1)
        #self.connect_inmesh_to_outmesh(blendshape_obj, techanim_final)


        #CREATE NCLOTH
        cloth_name, input_name, rest_name, ncloth_name, nucleus_name = self.create_Cloth(obj=techanim_final)
        #add to the layr
        for each in [input_name, rest_name]:
            cmds.editDisplayLayerMembers(self.input_rest_lyr_name, each, noRecurse=True)

        cmds.editDisplayLayerMembers(self.cloth_lyr_name, cloth_name, noRecurse=True)
        cmds.editDisplayLayerMembers(self.nCloth_lyr_name, ncloth_name, noRecurse=True)


        cmds.parent([cloth_name, input_name, rest_name,ncloth_name], cloth_grp_name)
        cloth_new_name = geo_name + '_Cloth'
        cloth_new_input_name = geo_name + '_Input'
        cloth_new_rest_name = geo_name + '_Rest'
        cloth_new_ncloth_name = geo_name + '_nCloth'
        cmds.rename(cloth_name, cloth_new_name)
        cmds.rename(input_name, cloth_new_input_name)
        cmds.rename(rest_name, cloth_new_rest_name)
        cmds.rename(ncloth_name, cloth_new_ncloth_name)

        parent_obj = cmds.listRelatives('Sim_Grp', p=True)[0]
        child_obj = cmds.listRelatives(parent_obj, c=True)
        if nucleus_name not in child_obj:
            cmds.parent(nucleus_name, parent_obj)


        #CREATE TECHANIMCLOTH

        techanim_child_list = cmds.listRelatives(self.techanim_cloth_type + '_Grp', c=True)
        blendshape_obj = cloth_new_name
        for each in techanim_child_list:
            name = cmds.getAttr(each + '.obj_type') + '_' + cmds.getAttr(each + '.' + self.version_type)
            techanim_cloth_geo_name = name + '_' + geo_name
            cmds.duplicate(geo_name, n=techanim_cloth_geo_name)
            cmds.parent(techanim_cloth_geo_name, each)
            blend_shape = cmds.blendShape(blendshape_obj, techanim_cloth_geo_name, o='world')[0]

            cmds.setAttr(blend_shape + '.' + blendshape_obj, 1)
            blendshape_obj = techanim_cloth_geo_name

        #TECHANIM CLOTH FINAL
        techanim_final_grp = 'TechAnimCloth_Final_Grp'
        techanim_final = 'TechAnimCloth_Final_' + geo_name
        cmds.duplicate(geo_name, n=techanim_final)
        cmds.parent(techanim_final, techanim_final_grp)
        blend_shape = cmds.blendShape(blendshape_obj, techanim_final, o='world')[0]
        cmds.setAttr(blend_shape + '.' + blendshape_obj, 1)

        self.update_sets_layer()

    def create_hair_rigfx_def(self, hair_list, grp_name, auto_parent_root_joint=False):
        '''

        :param hair_list:
        :param grp_name:
        :return:
        '''
        #CREATE A BLNDSHAPE ALL THE HAUR

        new_curve_list = []
        for each in hair_list:
            self.help_class.set_type(obj=each, type_val=self.input_type)

            duplicate_name = each + '_Static_Crv'
            new_curve_list.append(duplicate_name)
            cmds.duplicate(each, n=duplicate_name)
            self.help_class.worldBlendshape(each, duplicate_name)

        #CREATE A HAIR
        folical_list, output_curve_list, hairSystem_name = self.create_hair(new_curve_list)
        self.help_class.set_type(obj=hairSystem_name, type_val=self.hairSystem_type)

        #GET THE PARENT OBJECT
        folical_parent_obj = hairSystem_name + 'Follicles'
        output_curve_parent_obj = hairSystem_name + 'OutputCurves'

        #move object to position
        cmds.parent(hairSystem_name, grp_name)
        child_hair_obj = cmds.listRelatives(grp_name, c=True)
        for each_child_hair_obj in child_hair_obj:
            list_all_attr = cmds.listAttr(each_child_hair_obj)
            if 'obj_type' in list_all_attr:
                if cmds.getAttr(each_child_hair_obj + '.obj_type') == 'FolicalGrp':
                    cmds.parent(folical_list, each_child_hair_obj)
                if cmds.getAttr(each_child_hair_obj + '.obj_type') == 'OutputCurveGrp':
                    cmds.parent(output_curve_list, each_child_hair_obj)

        for each in [folical_parent_obj, output_curve_parent_obj]:
            if cmds.objExists(each):
                cmds.delete(each)
        hair_system_new_name = grp_name.split('_Grp')[0]
        cmds.rename(hairSystem_name, hair_system_new_name)

        #move nucl
        nucleus_list = cmds.ls(type='nucleus')
        for each_nucleus in nucleus_list:
            parent_obj = cmds.listRelatives('Sim_Grp', p=True)[0]
            try:
                cmds.parent(each_nucleus, parent_obj)
            except:
                pass
        #CREATE A RIG
        #STATIC JOINT RIG
        static_joint_list = []
        for each in new_curve_list:
            first_jnt, jnt_list = self.joint_class.createJointOnCurve(each,addCtrl=True)

            static_joint_list.append(first_jnt)
            #BIND TO CURVE
            cmds.select(jnt_list, each)
            mel.eval('SmoothBindSkin')

        static_jnt_grp_name = grp_name + '_Static_Jnt_Grp'
        cmds.createNode('transform', n=static_jnt_grp_name)
        cmds.parent(static_joint_list, static_jnt_grp_name)


        #DYNAMIC JOINT RIG
        dynamic_joint_list = []
        handle_list = []
        handle_grp_name = grp_name + '_Handle_Grp'
        for each in output_curve_list:
            first_jnt, jnt_list = self.joint_class.createJointOnCurve(each, addCtrl=True)
            dynamic_joint_list.append(first_jnt)

            parent_obj = cmds.listRelatives(each, p=True)[0]

            cmds.select(first_jnt, jnt_list[-1], each)
            print('this is jointlist[0]', first_jnt)
            print('this is jnt_list[-1]', jnt_list[-1])
            print('this is each', each)
            handle_name = each + '_Output_Handle'
            handle = mel.eval('ikHandle -sol ikSplineSolver -ccv false;')
            #MOVE OUTPUT CURVE TO PARENT
            cmds.parent(each, parent_obj)
            #RENAME HANDLE
            handle_name = self.help_help_class.obj_rename(handle[0], handle_name)
            cmds.setAttr(handle_name + '.v', 0)
            if not cmds.objExists(handle_grp_name):
                cmds.createNode('transform', n=handle_grp_name)

            cmds.parent(handle_name, handle_grp_name)

        dyn_jnt_grp_name = grp_name + '_Dyn_Jnt_Grp'
        cmds.createNode('transform', n=dyn_jnt_grp_name)
        cmds.parent(dynamic_joint_list, dyn_jnt_grp_name)
        extra_grp = ''
        for each in cmds.listRelatives(grp_name, c=True):
            if cmds.getAttr(each + '.obj_type') == 'ExtraGrp':
                cmds.parent(static_jnt_grp_name, each)
                cmds.parent(dyn_jnt_grp_name, each)
                cmds.parent(handle_grp_name, each)
                extra_grp = each

        #UPDATE THE LAYER
        self.update_sets_layer()

        if auto_parent_root_joint:
            #CREATE A ROOT JOINT AN PARENT ALL THE STATIC AND DYNAMIC JOINT TO THAT
            root_joint = 'Root_Jnt'
            if not cmds.objExists(root_joint):
                cmds.select(cl=True)
                cmds.joint(n=root_joint, p=(0, 0, 0))
                for each in [static_joint_list, dynamic_joint_list]:
                    cmds.parent(each, root_joint)

            cmds.parent(root_joint, extra_grp)






    def passive_collider_def(self, obj_name, grp_name=''):
        '''
        CREATE A PASSIVE COLLIDER
        :param obj_name: specify the object to create a collider
        :param grp_name: specify the grp name to parent the collider it should ends with '*_Collider_Grp' and should have tag '*.obj_type = Collider'
        :return:
        '''
        if grp_name == '':
            collider_grp_name = 'helper_Collider_Grp'
        else:
            collider_grp_name = grp_name

        if not cmds.objExists(collider_grp_name):
            raise RuntimeError(collider_grp_name + ' is not exists')

        self.help_class.set_type(obj=obj_name, type_val=self.input_type)

        collution_obj = obj_name + '_Collution'
        collution_nrigit_name = collution_obj + '_nRigit'

        cmds.duplicate(obj_name, n=collution_obj)
        input_blndshape_name = cmds.blendShape(obj_name, collution_obj)[0]
        input_blndshape_new_name = collution_obj + '_Blend'
        cmds.rename(input_blndshape_name, input_blndshape_new_name)
        cmds.setAttr(input_blndshape_new_name + '.' + obj_name, 1)


        cmds.select(collution_obj)
        collider = mel.eval('makeCollideNCloth;')[0]
        parent_obj = cmds.listRelatives(collider, p=True)[0]
        cmds.rename(parent_obj, collution_nrigit_name)

        #ADD A TAG TO BOTH OBJECT
        self.help_class.set_type(obj=collution_obj, type_val='Collider')
        self.help_class.set_type(obj=collution_nrigit_name, type_val='nRigit')


        cmds.parent([collution_obj, collution_nrigit_name], collider_grp_name)

        self.update_sets_layer()




    def ncloth_DeleteHistory(self):
        '''
        NCLOTH nClothDeleteHistory
        :return:
        '''

        for each in cmds.ls(sl=True):
            cmds.select(each)
            mel.eval('nClothDeleteHistory;')

    def displayCurrentMesh(self):
        '''

        :return:
        '''
        for each in cmds.ls(sl=True):
            cmds.select(each)
            mel.eval('nClothDisplayCurrentMesh;')

    def displayInputMesh(self):
        '''

        :return:
        '''
        for each in cmds.ls(sl=True):
            cmds.select(each)
            mel.eval('nClothDisplayInputMesh;')

    def removenCloth(self):
        '''

        :return:
        '''
        for each in cmds.ls(sl=True):
            cmds.select(each)
            mel.eval('removeNCloth "selected";')

    def connect_inmesh_to_outmesh(self, obj_one, obj_two):
        '''

        :param obj_one:
        :param obj_two:
        :return:
        '''
        obj_one_shape = cmds.listRelatives(obj_one, s=True)[0]
        obj_two_shape = cmds.listRelatives(obj_two, s=True)[0]
        cmds.connectAttr((obj_one_shape + '.worldMesh[0]'), (obj_two_shape + '.inMesh'), f=True)

    def rigFx_grp_def(self, grp_name='Example', noTechAnimGrp=4, noTechAnimCloth=4):
        '''
        create a Basic RigFx Grp Structure
        :return:
        '''

        #CHECK IF THE GRP IS EXIST OR NOT
        rig_fx_name = grp_name + 'RigFX'
        if cmds.objExists(rig_fx_name):
            raise RuntimeError(grp_name + ' RigFx is Already exists Please Set New Name if you want to Create New Basic Folder Structure')

        input_grp = 'Input_Grp'
        techAnim_grp = 'TechAnim_Grp'
        techAnim_Final_Grp = 'TechAnim_Final_Grp'
        sim_grp = 'Sim_Grp'
        helper_grp = 'Helper_Grp'
        helper_collider_grp, helper_constraint_grp , helper_field_grp , helper_extra_grp = self.get_cloth_folder_structure('helper')
        cloth_grp = 'Cloth_Grp'
        hair_grp = 'Hair_Grp'
        techAnim_Cloth_Grp = 'TechAnimCloth_Grp'
        techAnim_Cloth_Final_Grp = 'TechAnimCloth_Final_Grp'
        final_Grp = 'Final_Grp'

        #LIST OF THE TECHANIM GRP
        techAnim_list = []
        a = 0
        while a < noTechAnimGrp:
            name = 'TechAnim_' + str(a+1) + '_Grp'
            techAnim_list.append(name)
            a+=1

        #LIST OF THE TECHANIM CLOTH GRP
        techAnim_Cloth_List = []
        a = 0
        while a < noTechAnimCloth:
            name = 'TechAnimCloth_' + str(a+1) + '_Grp'
            techAnim_Cloth_List.append(name)
            a += 1


        grp_list = [rig_fx_name, input_grp, techAnim_grp, techAnim_Final_Grp, sim_grp, helper_grp, helper_collider_grp, helper_constraint_grp, helper_field_grp,
                    helper_extra_grp, cloth_grp, hair_grp, techAnim_Cloth_Grp, techAnim_Cloth_Final_Grp, final_Grp]
        grp_list.extend(techAnim_list)
        grp_list.extend(techAnim_Cloth_List)


        for each in grp_list:
            if not cmds.objExists(each):
                cmds.createNode('transform', n=each)

        for each in [techAnim_Final_Grp, techAnim_Cloth_Final_Grp]:
            cmds.setAttr(each + '.v', 0)

        #DO THE PARENTING
        for each in [input_grp, techAnim_grp, techAnim_Final_Grp, sim_grp, techAnim_Cloth_Grp, techAnim_Cloth_Final_Grp, final_Grp]:
            cmds.parent(each, rig_fx_name)

        for each in techAnim_list:
            cmds.parent(each, techAnim_grp)

        for each in techAnim_Cloth_List:
            cmds.parent(each, techAnim_Cloth_Grp)

        for each in [helper_grp, cloth_grp, hair_grp]:
            cmds.parent(each, sim_grp)

        for each in [helper_collider_grp, helper_constraint_grp, helper_field_grp, helper_extra_grp]:
            cmds.parent(each, helper_grp)

        #CREATE A nucleus  AND PARENT TO MAIN GRP

        name = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
        cmds.polySphere(n=name)
        cloth_val = mel.eval('createNCloth 0;')
        nucleus_name = list(set(cmds.listConnections(cloth_val, type='nucleus')))
        if nucleus_name:
            nucleus_name = nucleus_name[0]

        cmds.delete(name)
        try:
            cmds.parent(nucleus_name, rig_fx_name)
            mel.eval('expression -s "%s.startFrame = `playbackOptions -q -min`;"  -o %s -ae 1 -uc all ;' % (nucleus_name, nucleus_name))
            cmds.currentTime(cmds.playbackOptions(q=True, minTime=True))

        except:
            pass

        #START ADDING THE TAG IN THE GRP
        #RIG FX
        self.help_class.set_type(obj=rig_fx_name, obj_type='Character_Name', type_val=grp_name)
        self.help_class.set_type(obj=rig_fx_name, type_val=self.rigFx_type)

        #INPUT
        self.help_class.set_type(obj=input_grp, type_val=self.input_type)

        #TECH ANIM
        self.help_class.set_type(obj=techAnim_grp, type_val=self.techanim_type)
        self.help_class.set_type(obj=techAnim_grp, type_val='Main', obj_type=self.version_type)

        #TECHANIM FINAL
        self.help_class.set_type(obj=techAnim_Final_Grp, type_val=self.techanim_final_type)

        #SIM
        self.help_class.set_type(obj=sim_grp, type_val=self.sim_type)
        self.help_class.set_type(obj=helper_grp, type_val='Helper')
        self.help_class.set_type(obj=cloth_grp, type_val='Cloth')
        self.help_class.set_type(obj=hair_grp, type_val='Hair')

        #HELPER
        self.help_class.set_type(obj=helper_collider_grp, type_val='ColliderGrp')
        self.help_class.set_type(obj=helper_collider_grp, obj_type='ObjName', type_val='Helper')

        self.help_class.set_type(obj=helper_constraint_grp, type_val='ConstraintGrp')
        self.help_class.set_type(obj=helper_constraint_grp, obj_type='ObjName', type_val='Helper')

        self.help_class.set_type(obj=helper_field_grp, type_val='FieldGrp')
        self.help_class.set_type(obj=helper_field_grp, obj_type='ObjName', type_val='Helper')

        self.help_class.set_type(obj=helper_extra_grp, type_val='ExtraGrp')
        self.help_class.set_type(obj=helper_extra_grp, obj_type='ObjName', type_val='Helper')


        #TECHANIM CLOTH
        self.help_class.set_type(obj=techAnim_Cloth_Grp, type_val=self.techanim_cloth_type)

        #TECHANIMCLOTH FINAL
        self.help_class.set_type(obj=techAnim_Cloth_Final_Grp, type_val=self.techanim_cloth_final_type)

        #FINAL
        self.help_class.set_type(obj=final_Grp, type_val=self.final_type)

        a = 0
        while a < len(techAnim_list):
            self.help_class.set_type(obj=techAnim_list[a], type_val=self.techanim_type)
            self.help_class.set_type(obj=techAnim_list[a], obj_type=self.version_type, type_val=str(a+1))
            a+=1

        a = 0
        while a < len(techAnim_Cloth_List):
            self.help_class.set_type(obj=techAnim_Cloth_List[a], type_val=self.techanim_cloth_type)
            self.help_class.set_type(obj=techAnim_Cloth_List[a], obj_type=self.version_type, type_val=str(a + 1))
            a += 1


        self.update_sets_layer()



    def createDisplayLayer(self, displayLayerName, obj_name=''or []):
        '''
        CREATE A DISPLAY LAYER
        :param obj_name: specify the object name
        :return:
        '''
        cmds.select(obj_name)
        cmds.createDisplayLayer(noRecurse=True, name=displayLayerName)

    def get_obj_type(self, obj_type_name=''):
        '''
        GET OBJECT TYPE NAME
        :param obj_type_name: specify the object type name
        :return:
        '''
        obj_type = cmds.ls('*.obj_type')
        list_obj = []
        for each in obj_type:
            if cmds.getAttr(each) == obj_type_name:
                list_obj.append(each.split('.')[0])

        return list_obj



    def get_child_list(self, parent_obj):
        '''

        :return:
        '''
        #GET THE LIST OF THE OBJECT IN THE TECHANIM GRP
        child_obj = cmds.listRelatives(parent_obj, c=True)
        return child_obj

    def get_techanim_or_techanimcloth_def(self, techanim_grp):
        '''
        GET THE LIST OF THE OBJECT IN THE TECHANIM GRP
        :param techanim_grp:
        :return:
        '''


        #GET THE NO OF THE TECHANIM FILE
        techanim_child = cmds.listRelatives(techanim_grp, c=True, f=True)
        techanim_dic = OrderedDict()
        for each_techanim_child in techanim_child:
            if '|' in each_techanim_child:
                new_each_techanim_child = each_techanim_child.split('|')[-1]
            else:
                new_each_techanim_child = each_techanim_child
            child_each_techanim_child = cmds.listRelatives(each_techanim_child, c=True)
            if child_each_techanim_child == None:
                child_each_techanim_child = []

            techanim_dic[new_each_techanim_child] = child_each_techanim_child

        return techanim_dic

    def get_techanim_techanimcloth_final_def(self, techanim_final_grp):
        '''
        GET THE TECHANIM FINAL DEF
        :return:
        '''

        #GET THE NO OF THE TECAHNIM FINAL FILE
        techanim_final_child = cmds.listRelatives(techanim_final_grp, c=True, f=True)
        techanim_final_dic = []
        if techanim_final_child != None:
            for each_techanim_final_child in techanim_final_child:
                if '|' in each_techanim_final_child:
                    each_techanim_final_child = each_techanim_final_child.split('|')[-1]
                techanim_final_dic.append(each_techanim_final_child)


        return techanim_final_dic

    def get_sim_def(self, sim_grp):
        '''
        GET ALL THE DATA FROM SIM
        :param sim_grp: specify the sim grp name
        :return:
        '''

        sim_dic = {}

        print('this is the sim gro: ', sim_grp)
        child_sim_grp = cmds.listRelatives(sim_grp, c=True, f=True)
        if child_sim_grp:
            for each_child_sim_grp in child_sim_grp:
                if '|' in each_child_sim_grp:
                    name = each_child_sim_grp.split('|')[-1]
                else:
                    name = each_child_sim_grp
                sim_dic[name] = OrderedDict()
                if 'Helper_Grp' in each_child_sim_grp:
                    pass

                if 'Cloth_Grp' in each_child_sim_grp:
                    pass

                if 'Hair_Grp' in each_child_sim_grp:
                    pass


        return sim_dic


    def get_layer(self):
        '''
        GET ALL THE LATER WHAT WE HAVE

        :return:
        '''
        display_layer = cmds.ls(type='displayLayer')
        display_layer_list = []
        for each_layer in display_layer:
            list_attr = cmds.listAttr(each_layer)
            if 'obj_type' in list_attr:
                display_layer_list.append(each_layer)

        return display_layer_list



    def update_crate_layer(self):
        '''
        THIS WILL UPDATE THE LAYER WHAT YOU WOULD SEE IN THE OUTLINER
        :return: 
        '''
        #DELETE LAYER IF WE HAVE
        if self.get_layer():
            for each in self.get_layer():
                if cmds.objExists(each):
                    cmds.delete(each)

        
        # CREATE A DISPLAY LAYER
        # INPUT
        display_layer_name = self.input_lyr_name
        if not cmds.objExists(display_layer_name):
            self.createDisplayLayer(displayLayerName=display_layer_name, obj_name=self.input_grp)
            self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # TECHANIM
        techAnim_list = cmds.listRelatives('TechAnim_Grp', c=True)
        for each in techAnim_list:
            display_layer_name = each + '_Lyr'
            self.createDisplayLayer(display_layer_name, each)
            self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # CLOTH
        cloth_list = self.get_obj_type('cloth')
        display_layer_name = self.cloth_lyr_name
        self.createDisplayLayer(display_layer_name, cloth_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # NCLOTH
        ncloth_list = self.get_obj_type('nCloth')
        display_layer_name = self.nCloth_lyr_name
        self.createDisplayLayer(display_layer_name, ncloth_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # INPUT/REST
        input_rest_list = self.get_obj_type('input').extend(self.get_obj_type('rest'))
        display_layer_name = self.input_rest_lyr_name
        self.createDisplayLayer(display_layer_name, input_rest_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # COLLUTION
        collution_grp_list = self.get_obj_type('ColliderGrp')
        display_layer_name = self.collution_lyr_name
        self.createDisplayLayer(display_layer_name, collution_grp_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # CONSTRAINT
        constraint_grp_list = self.get_obj_type('ConstraintGrp')
        display_layer_name = self.constraint_lyr_name
        self.createDisplayLayer(display_layer_name, constraint_grp_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # FIELD
        field_grp_list = self.get_obj_type('FieldGrp')
        display_layer_name = self.field_lyr_name
        self.createDisplayLayer(display_layer_name, field_grp_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # EXTRA
        extra_grp_list = self.get_obj_type('ExtraGrp')
        display_layer_name = self.extra_lyr_name
        self.createDisplayLayer(display_layer_name, extra_grp_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # FOLLICAL
        folical_grp_list = self.get_obj_type('FolicalGrp')
        display_layer_name = self.folical_lyr_name
        self.createDisplayLayer(display_layer_name, folical_grp_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # OUTPUTCURVE
        output_curve_grp_list = self.get_obj_type('OutputCurveGrp')
        display_layer_name = self.outputCurve_lyr_name
        self.createDisplayLayer(display_layer_name, output_curve_grp_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # TECHANIM
        techAnim_Cloth_List = cmds.listRelatives('TechAnimCloth_Grp', c=True)
        for each in techAnim_Cloth_List:
            display_layer_name = each + '_Lyr'
            self.createDisplayLayer(display_layer_name, each)
            self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

        # FINAL
        final_grp_list = self.get_obj_type('Final')
        display_layer_name = self.final_lyr_name
        self.createDisplayLayer(display_layer_name, final_grp_list)
        self.help_class.set_type(obj=display_layer_name, type_val=display_layer_name)

    def create_set(self, obj_list, set_name):
        '''
        IF THE SETS ARE THERE IN THE FILE IT WILL DELETE THE FILE
        :param obj_list: SPECIFY THE THE LIST OF THE OBJECT
        :param set_name: SPECIFY THE SET NAME
        :return:
        '''
        if cmds.objExists(set_name):
            cmds.delete(set_name)

        cmds.sets(obj_list, n=set_name)

    def update_set(self):
        '''
        UPDATE THE SETS
        :return:
        '''
        rigfx_set_name = ''

        #GET RIGFX FILE
        set_obj = cmds.ls('*.obj_type')
        for each in set_obj:
            if cmds.getAttr(each) == 'RigFx':
                rigFx_name = each.split('.')[0]

                #DELETE THE SETS IF WE HAVE ANY
                rigfx_set_name = rigFx_name + 'Sets'
                for each in [rigfx_set_name, self.input_sets, self.techanim_sets, self.cloth_sets, self.nCloth_sets,
                             self.hairSystem_sets, self.simulation_sets, self.techAnimCloth_sets, self.final_sets]:
                    if cmds.objExists(each):
                        cmds.delete(each)



                child_rifx = cmds.listRelatives(rigFx_name, c=True)
                #INPUT SET
                if 'Input_Grp' in child_rifx:
                    self.create_set(['Input_Grp'], self.input_sets)

                #TECHANIM SET
                if 'TechAnim_Grp' in child_rifx:
                    techanim_child = cmds.listRelatives('TechAnim_Grp', c=True)
                    self.create_set(techanim_child, self.techanim_sets)

                #CLOTH SET
                cloth_list = self.get_obj_type('cloth')
                self.create_set(cloth_list, self.cloth_sets)


                #HAIRSYSTEM SET
                hairSystem_list = self.get_obj_type('hairSystem')
                self.create_set(hairSystem_list, self.hairSystem_sets)

                #NCLOTH SET
                nCloth_list = self.get_obj_type('nCloth')
                self.create_set(nCloth_list, self.nCloth_sets)

                #TECHANIMCLOTH SET
                if 'TechAnimCloth_Grp' in child_rifx:
                    techanim_child = cmds.listRelatives('TechAnimCloth_Grp', c=True)
                    self.create_set(techanim_child, self.techAnimCloth_sets)

                #FINAL SET
                if 'Final_Grp' in child_rifx:
                    self.create_set(['Final_Grp'], self.final_sets)


                self.create_set([self.cloth_sets, self.nCloth_sets, self.hairSystem_sets], self.simulation_sets)
                self.create_set([rigFx_name, self.input_sets, self.techanim_sets, self.simulation_sets, self.techAnimCloth_sets, self.final_sets], rigfx_set_name)

    def update_sets_layer(self):
        '''
        COMBINE SETS AND LAYER FUNCTION
        :return:
        '''
        self.update_crate_layer()
        self.update_set()




    def get_rigfx_data_from_maya(self):
        '''

        :return:
        '''
        #get the rigFX
        obj_type_list = cmds.ls('*.obj_type')
        rigFx_list = OrderedDict()
        for each_obj_type_list in obj_type_list:
            if cmds.getAttr(each_obj_type_list) == 'RigFx':
                rigfx_name = each_obj_type_list.split('.')[0]
                print(rigfx_name)
                '''
                
                
                
                rigfx_name = each_obj_type_list.split('.')[0]
                rigFx_list[rigfx_name] = OrderedDict()

                #GET THE LIST OF THE OBJECT
                rig_fx_child = cmds.listRelatives(rigfx_name, c=True, f=True)

                for each_rig_fx_child in rig_fx_child:

                    #INPUT
                    if 'Input_Grp' in each_rig_fx_child:
                        rigFx_list[rigfx_name]['Input_Grp'] = OrderedDict()

                    #TECHANIM
                    if 'TechAnim_Grp' in each_rig_fx_child:
                        rigFx_list[rigfx_name]['TechAnim_Grp'] = self.get_techanim_or_techanimcloth_def(each_rig_fx_child)

                    #TECHANIM FINAL
                    if 'TechAnim_Final_Grp' in each_rig_fx_child:
                        rigFx_list[rigfx_name]['TechAnim_Final_Grp'] = self.get_techanim_techanimcloth_final_def(each_rig_fx_child)

                    #SIM
                    if 'Sim_Grp' in each_rig_fx_child:
                        rigFx_list[rigfx_name]['Sim_Grp'] = self.get_sim_def(each_rig_fx_child)

                    #TECHANIM CLOTH
                    if 'TechAnimCloth_Grp' in each_rig_fx_child:
                        rigFx_list[rigfx_name]['TechAnimCloth_Grp'] = self.get_techanim_or_techanimcloth_def(each_rig_fx_child)

                    #TECHANIM CLOTH FINAL
                    if 'TechAnimCloth_Final_Grp' in each_rig_fx_child:
                        rigFx_list[rigfx_name]['TechAnimCloth_Final_Grp'] = self.get_techanim_techanimcloth_final_def(each_rig_fx_child)

                    #FINAL
                    if 'Final_Grp' in each_rig_fx_child:
                        rigFx_list[rigfx_name]['Final_Grp'] = OrderedDict()

                    '''
        print('Final>>> \n', rigFx_list)


    def getHairExample(self):
        '''

        :return:
        '''
        mel.eval('GetHairExample')

    def paintHairFolical(self):
        '''

        :return:
        '''
        mel.eval('PaintHairFollicles')


    def component_constraint(self, sel_obj, type='Component'):
        '''
        CREATE A COMPONENT CONSTRAINT
        :return:
        '''
        if sel_obj:
            grp_name = sel_obj[-1]
            if cmds.objectType(grp_name) == 'transform':
                constraint_grp_name = grp_name
            else:
                if cmds.objExists('helper_Constraint_Grp'):
                    constraint_grp_name = 'helper_Constraint_Grp'
                else:
                    raise Exception('helper_Constraint_Grp is not Exists')

            #GET THE OBJECT NAME
            sel_obj.remove(grp_name)
            obj_name = list(set(cmds.ls(sel_obj, objectsOnly=True)))
            if obj_name:
                obj_name = cmds.listRelatives(obj_name, p=True)[0]

            #GET VERTEX LIST
            flat = cmds.ls(sel_obj, fl=True)
            vertex_list = []
            for each in flat:
                if 'vtx' in each:
                    vertex_list.append(int(each.split('vtx[')[1].split(']')[0]))


            #CREATE A DYNAMIC CONSTRAINT
            cmds.select(sel_obj)

            if type == self.component_type:
                mel.eval('doCreateComponentNConstraint 1 0 0 0')
                dynamic_const = cmds.ls('dynamicConstraint1')[0]
                dyn_constraint_name = obj_name + '_Cmponent'
                dyn_constraint_name = self.help_help_class.obj_rename(dynamic_const, dyn_constraint_name)
                #cmds.rename(dynamic_const, dyn_constraint_name)
                self.help_class.set_type(obj=dyn_constraint_name, type_val=self.component_type)

            elif type == self.component_to_component_type:
                mel.eval('doCreateNConstraint pointToPoint 0')
                dynamic_const = cmds.ls('dynamicConstraint1')[0]
                dyn_constraint_name = obj_name + '_Component_to_Component'
                dyn_constraint_name = self.help_help_class.obj_rename(dynamic_const, dyn_constraint_name)
                #cmds.rename(dynamic_const, dyn_constraint_name)
                self.help_class.set_type(obj=dyn_constraint_name, type_val=self.component_to_component_type)

            else:
                mel.eval('doCreateNConstraint force 0')
                dynamic_const = cmds.ls('dynamicConstraint1')[0]
                dyn_constraint_name = obj_name + '_Force_Field'
                dyn_constraint_name = self.help_help_class.obj_rename(dynamic_const, dyn_constraint_name)
                #cmds.rename(dynamic_const, dyn_constraint_name)
                self.help_class.set_type(obj=dyn_constraint_name, type_val=self.forcefield_type)

            cmds.parent(dyn_constraint_name, constraint_grp_name)


    def point_to_surface_constriant(self, sel_obj, type='PointTOSurface'):
        '''
        CREATE POINT TO SURFACE
        :param sel_obj: [VERTEX SELECTION LIST, OBJECT TO CONSTRAINT, CONSTRAINT GROUP IF NEEDED]
        :return:
        '''

        if sel_obj:
            print(sel_obj)
            #CHECK LAST OPTION
            last_obj = sel_obj[-1]
            if cmds.objectType(last_obj) == 'transform':
                #now check if it has a shape or not
                shape_name = cmds.listRelatives(last_obj, s=True)
                if shape_name == None:
                    print('its just a transform node only')
                    constraint_grp_name = last_obj
                    surface_geo = sel_obj[-2]
                    shape_surface_geo = cmds.listRelatives(surface_geo, s=True)
                    if shape_surface_geo == None:
                        raise Exception('Select last Object is not surface Could you Follow this procss\n'
                                        '1 - Select All the Vertex\n'
                                        '2 - Select Geo to Create a Point to Surfacet\n'
                                        '3 - if needed select the Constraint Group to Move Constraint to that Grp')

                    sel_obj.remove(constraint_grp_name)
                    sel_obj.remove(surface_geo)

                else:
                    if cmds.objExists('helper_Constraint_Grp'):
                        constraint_grp_name = 'helper_Constraint_Grp'
                        surface_geo = sel_obj[-1]
                        shape_surface_geo = cmds.listRelatives(surface_geo, s=True)
                        if shape_surface_geo == None:
                            raise Exception('Select last Object is not surface Could you Follow this procss\n'
                                            '1 - Select All the Vertex\n'
                                            '2 - Select Geo to Create a Point to Surfacet\n'
                                            '3 - if needed select the Constraint Group to Move Constraint to that Grp')
                        sel_obj.remove(surface_geo)
                    else:
                        raise Exception('helper_Constraint_Grp is not Exists')


            else:
                raise RuntimeError('please Select any geo Node at the end and if you want to move COnstraint on Specific Contraint Grp'
                                   'then select later then select')


            obj_name = list(set(cmds.ls(sel_obj, objectsOnly=True)))
            if obj_name:
                obj_name = cmds.listRelatives(obj_name, p=True)[0]

            cmds.select(sel_obj, surface_geo)
            if type == self.pointtosurface_type:
                mel.eval('doCreateNConstraint pointToSurface 0')
            else:
                mel.eval('doCreateNConstraint slideOnSurface 0')

            dynamic_const = cmds.ls('dynamicConstraint1')[0]

            if type == self.pointtosurface_type:
                dyn_constraint_name = obj_name + '_Point_To_Surface'
                dyn_constraint_name = self.help_help_class.obj_rename(dynamic_const, dyn_constraint_name)
                self.help_class.set_type(obj=dyn_constraint_name, type_val=self.pointtosurface_type)
            else:
                dyn_constraint_name = obj_name + '_Slide_To_Surface'
                dyn_constraint_name = self.help_help_class.obj_rename(dynamic_const, dyn_constraint_name)
                self.help_class.set_type(obj=dyn_constraint_name, type_val=self.slidetosurface_type)


            cmds.parent([dyn_constraint_name], constraint_grp_name)

            dynamic_const = cmds.ls('nRigid1')
            if dynamic_const:
                dynamic_const = dynamic_const[0]

                dyn_constraint_nrigit_name = obj_name + '_Point_To_Surface_nRigit'
                dyn_constraint_nrigit_name = self.help_help_class.obj_rename(dynamic_const, dyn_constraint_nrigit_name)
                # cmds.rename(dynamic_const, dyn_constraint_name)
                if type == self.pointtosurface_type:
                    self.help_class.set_type(obj=dyn_constraint_name, type_val=self.pointtosurface_nRigit)
                else:
                    self.help_class.set_type(obj=dyn_constraint_name, type_val=self.slidetosurface_nRigit)

                cmds.parent([dyn_constraint_nrigit_name], constraint_grp_name)
                


    def tearable_transform_constriant(self, sel_obj, type='TearableSurface'):
        '''
        CREATE A TEARABLE CONSTRAINT
        :param sel_obj: sleect all the vertex list
        :return:
        '''
        if sel_obj:
            grp_name = sel_obj[-1]
            if cmds.objectType(grp_name) == 'transform':
                constraint_grp_name = grp_name
            else:
                if cmds.objExists('helper_Constraint_Grp'):
                    constraint_grp_name = 'helper_Constraint_Grp'
                else:
                    raise Exception('helper_Constraint_Grp is not Exists')


            cmds.select(sel_obj)
            if type == self.tearablesurface_type:
                mel.eval('doCreateNConstraint tearableSurface 0')
            else:
                mel.eval('doCreateNConstraint transform 0')

            if not constraint_grp_name == 'helper_Constraint_Grp':
                sel_obj.remove(grp_name)


            obj_name = list(set(cmds.ls(sel_obj, objectsOnly=True)))
            if obj_name:
                obj_name = cmds.listRelatives(obj_name, p=True)[0]

            dynamic_const = cmds.ls('dynamicConstraint1')[0]
            if type == self.tearablesurface_type:
                dyn_constraint_name = obj_name + '_Tearable'

            else:
                dyn_constraint_name = obj_name + '_Transform'
            dyn_constraint_name = self.help_help_class.obj_rename(dynamic_const, dyn_constraint_name)
            cmds.parent([dyn_constraint_name], constraint_grp_name)

            if type == self.tearablesurface_type:
                self.help_class.set_type(obj=dyn_constraint_name, type_val=self.tearablesurface_type)
            else:
                self.help_class.set_type(obj=dyn_constraint_name, type_val=self.transoformconstraint_type)


    def field_def(self, sel_obj, type='airfield_type'):
        '''
        CREATE A FIELD
        :param sel_obj: SELECT OBJECT AND GROUP IF ANY
        :param type: specify the field type
        :return:
        '''

        if len(sel_obj) > 2:
            raise RuntimeError('Select either or Two object 1- Object 2 - Field Grp')


        if sel_obj:
            if len(sel_obj) == 2:
                grp_name = sel_obj[-1]
                if cmds.objectType(grp_name) == 'transform':
                    field_grp_name = grp_name
                else:
                    if cmds.objExists('helper_Field_Grp'):
                        field_grp_name = 'helper_Field_Grp'
                    else:
                        raise Exception('helper_Field_Grp is not Exists')

                if not field_grp_name == 'helper_Field_Grp':
                    sel_obj.remove(grp_name)
            else:
                field_grp_name = 'helper_Field_Grp'
            temp_name = 'Field_name'
            print(sel_obj)

            if type == self.airfield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Air_Field'
                temp_name = mel.eval('air -pos 0 0 0 -m 4 -att 1 -dx 0 -dy 1 -dz 0 -s 5 -iv 1 -iro 1 -vco 0 -es 0  -mxd 20  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.airfield_type)

            elif type == self.dragfield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Drag_Field'
                temp_name = mel.eval('drag -pos 0 0 0 -m 0.05 -att 1 -dx 0 -dy 0 -dz 0 -ud 0  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.dragfield_type)

            elif type == self.gravityfield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Gravity_Field'
                temp_name = mel.eval('gravity -pos 0 0 0 -m 9.8 -att 0 -dx 0 -dy -1 -dz 0  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.gravityfield_type)

            elif type == self.newtonfield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Newton_Field'
                temp_name = mel.eval('newton -pos 0 0 0 -m 5 -att 1 -mnd 0.2  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.newtonfield_type)

            elif type == self.radiusfield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Radius_Field'
                temp_name = mel.eval('radial -pos 0 0 0 -m 5 -att 1 -typ 0  -mxd 20  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.radiusfield_type)

            elif type == self.turbulancefield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Turbulance_Field'
                temp_name = mel.eval('turbulence -pos 0 0 0 -m 5 -att 1 -f 1 -phaseX 0 -phaseY 0 -phaseZ 0 -noiseLevel 0 -noiseRatio 0.707  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.turbulancefield_type)

            elif type == self.uniformfield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Uniform_Field'
                temp_name = mel.eval('uniform -pos 0 0 0 -m 5 -att 1 -dx 1 -dy 0 -dz 0  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.uniformfield_type)

            elif type == self.vortexfield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Vortex_Field'
                temp_name = mel.eval('vortex -pos 0 0 0 -m 5 -att 1 -ax 0 -ay 1 -az 0  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.vortexfield_type)

            elif type == self.volumefield_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Volume_Field'
                temp_name = mel.eval('volumeAxis -pos 0 0 0 -m 5 -att 0 -ia 0 -afc 1 -afx 1 -arx 0 -alx 0 -drs 0 -dx 1 -dy 0 -dz 0 -trb 0 -trs 0.2 -tfx 1 -tfy 1 -tfz 1 -tox 0 -toy 0 -toz 0 -dtr 0  -mxd -1  -vsh cube -vof 0 0 0 -vsw 360 -tsr 0.5 ;')[0]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.volumefield_type)

            elif type == self.volumecurve_type:
                cmds.select(sel_obj)
                field_name = sel_obj[0] + '_Volume_Curve'
                temp_name = cmds.vortex(name=temp_name, m=5.0, mxd=2.0)[1]
                self.help_help_class.obj_rename(temp_name, field_name)
                cmds.parent(field_name, field_grp_name)
                self.help_class.set_type(obj=field_name, type_val=self.volumecurve_type)











