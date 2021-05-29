from spark.department.Help.Houdini import nodes, help

for each in [help, nodes]:
    reload(each)

from spark.department.Help.Houdini.help import HELP
from spark.department.Help.Houdini.nodes import NODES

import hou
from collections import OrderedDict




class HOUDINI_CLOTHSETUP():
    def __init__(self):
        self.help_class = HELP()
        self.node_class = NODES()


        self.init_run()

    def init_run(self):
        '''
        this thing will run the initial
        :return:
        '''
        self.obj = '/obj'
        self.obj_path = hou.node(self.obj)
        self.distance = 1

        self.input = OrderedDict()
        self.input_name = 'INPUT'
        self.input['Name'] = self.input_name
        self.input['pos'] = [-11.1846, 2.20906]
        self.input['color'] = [0.8, 0.8, 0.8]

        self.techanim = OrderedDict()
        self.techanim['Name'] = 'TECHANIM'
        self.techanim['pos'] = [-6.94669, 3.53633]
        self.techanim['color'] = [0.8, 0.8, 0.8]

        self.techanim_final = OrderedDict()
        self.techanim_final['Name'] = 'TECHANIM_FINAL'
        self.techanim_final['pos'] = [-6.75584, 0.881796]
        self.techanim_final['color'] = [0.8, 0.8, 0.8]

        self.sim = OrderedDict()
        self.sim['Name'] = 'SIM'
        self.sim['pos'] = [-2.57963, 3.53633]
        self.sim['color'] = [0.8, 0.8, 0.8]

        self.sim_final = OrderedDict()
        self.sim_final['Name'] = 'SIM_FINAL'
        self.sim_final['pos'] = [-2.57963, 1.38297]
        self.sim_final['color'] = [0.8, 0.8, 0.8]

        self.techanim_cloth = OrderedDict()
        self.techanim_cloth['Name'] = 'TECHANIM_CLOTH'
        self.techanim_cloth['pos'] = [1.74885, 3.55808]
        self.techanim_cloth['color'] = [0.8, 0.8, 0.8]

        self.techanim_cloth_final = OrderedDict()
        self.techanim_cloth_final['Name'] = 'TECHANIM_CLOTH_FINAL'
        self.techanim_cloth_final['pos'] = [1.92286, 0.708685]
        self.techanim_cloth_final['color'] = [0.8, 0.8, 0.8]

        self.final = OrderedDict()
        self.final['Name'] = 'FINAL'
        self.final['pos'] = [6.57759, 2.44788]
        self.final['color'] = [0.8, 0.8, 0.8]

        #INPUT NODES
        ###################
        self.base_node_dic = OrderedDict()
        self.base_node_dic['Name'] = 'BASE'
        grp_pos_x = 2
        grp_pos_Y = 0
        self.base_node_dic['pos'] = [grp_pos_x,  grp_pos_Y]

        self.base_alembic_grp_node_def = OrderedDict()
        self.base_alembic_grp_node_def['Name'] = 'base_alembic_grp'
        grp_pos_Y = grp_pos_Y - self.distance
        self.base_alembic_grp_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.base_alembic_grp_node_def['color'] = [0.8, 0.8, 0.8]

        self.base_convert_node_def = OrderedDict()
        self.base_convert_node_def['Name'] = 'base_alembic_convert'
        grp_pos_Y = grp_pos_Y - self.distance
        self.base_convert_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.base_convert_node_def['color'] = [0.8, 0.8, 0.8]

        self.base_normal_node_def = OrderedDict()
        self.base_normal_node_def['Name'] = 'base_alembic_normal'
        grp_pos_Y = grp_pos_Y - self.distance
        self.base_normal_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.base_normal_node_def['color'] = [0.8, 0.8, 0.8]

        self.base_clean_node_def = OrderedDict()
        self.base_clean_node_def['Name'] = 'base_alembic_clean'
        grp_pos_Y = grp_pos_Y - self.distance
        self.base_clean_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.base_clean_node_def['color'] = [0.8, 0.8, 0.8]

        self.base_null_node_def = OrderedDict()
        self.base_null_node_def['Name'] = 'BASE_OUT'
        grp_pos_Y = grp_pos_Y - self.distance
        self.base_null_node_def['pos'] = [grp_pos_x, grp_pos_Y]

        ###################
        self.model_node_dic = OrderedDict()
        self.model_node_dic['Name'] = 'MODEL'
        grp_pos_x += 6
        grp_pos_Y = 0
        self.model_node_dic['pos'] = [grp_pos_x, grp_pos_Y]

        self.model_alembic_grp_node_def = OrderedDict()
        self.model_alembic_grp_node_def['Name'] = 'model_alembic_grp'
        grp_pos_Y = grp_pos_Y - self.distance
        self.model_alembic_grp_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.model_alembic_grp_node_def['color'] = [0.8, 0.8, 0.8]

        self.model_convert_node_def = OrderedDict()
        self.model_convert_node_def['Name'] = 'model_alembic_convert'
        grp_pos_Y = grp_pos_Y - self.distance
        self.model_convert_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.model_convert_node_def['color'] = [0.8, 0.8, 0.8]

        self.model_normal_node_def = OrderedDict()
        self.model_normal_node_def['Name'] = 'model_alembic_normal'
        grp_pos_Y = grp_pos_Y - self.distance
        self.model_normal_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.model_normal_node_def['color'] = [0.8, 0.8, 0.8]

        self.model_clean_node_def = OrderedDict()
        self.model_clean_node_def['Name'] = 'model_alembic_clean'
        grp_pos_Y = grp_pos_Y - self.distance
        self.model_clean_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.model_clean_node_def['color'] = [0.8, 0.8, 0.8]

        self.model_null_node_def = OrderedDict()
        self.model_null_node_def['Name'] = 'MODEL_OUT'
        grp_pos_Y = grp_pos_Y - self.distance
        self.model_null_node_def['pos'] = [grp_pos_x, grp_pos_Y]



        ############ANIMATION
        self.animation_node_dic = OrderedDict()
        self.animation_node_dic['Name'] = 'ANIMATION'
        grp_pos_x += 6
        grp_pos_Y = 0
        self.animation_node_dic['pos'] = [grp_pos_x, grp_pos_Y]


        self.animation_alembic_grp_node_def = OrderedDict()
        self.animation_alembic_grp_node_def['Name'] = 'animation_alembic_grp'
        grp_pos_Y = grp_pos_Y - self.distance
        self.animation_alembic_grp_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.animation_alembic_grp_node_def['color'] = [0.8, 0.8, 0.8]

        self.animation_convert_node_def = OrderedDict()
        self.animation_convert_node_def['Name'] = 'animation_alembic_convert'
        grp_pos_Y = grp_pos_Y - self.distance
        self.animation_convert_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.animation_convert_node_def['color'] = [0.8, 0.8, 0.8]

        self.animation_normal_node_def = OrderedDict()
        self.animation_normal_node_def['Name'] = 'animation_alembic_normal'
        grp_pos_Y = grp_pos_Y - self.distance
        self.animation_normal_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.animation_normal_node_def['color'] = [0.8, 0.8, 0.8]

        self.animation_clean_node_def = OrderedDict()
        self.animation_clean_node_def['Name'] = 'animation_alembic_clean'
        grp_pos_Y = grp_pos_Y - self.distance
        self.animation_clean_node_def['pos'] = [grp_pos_x, grp_pos_Y]
        self.animation_clean_node_def['color'] = [0.8, 0.8, 0.8]

        self.animation_null_node_def = OrderedDict()
        self.animation_null_node_def['Name'] = 'ANIMATION_OUT'
        grp_pos_Y = grp_pos_Y - self.distance
        self.animation_null_node_def['pos'] = [grp_pos_x, grp_pos_Y]


        #INPUT FINAL
        self.input_object_merge_node_dic = OrderedDict()
        self.input_object_merge_node_dic['Name'] = 'input_object_merge'
        grp_pos_Y = grp_pos_Y - self.distance
        self.input_object_merge_node_dic['pos'] = [grp_pos_x, grp_pos_Y]

        self.input_file_cache_node_dic = OrderedDict()
        self.input_file_cache_node_dic['Name'] = 'Input_File_Cache'
        grp_pos_Y = grp_pos_Y - self.distance
        self.input_file_cache_node_dic['pos'] = [grp_pos_x, grp_pos_Y]

        self.input_out_dic = OrderedDict()
        self.input_out_dic['Name'] = 'INPUT_OUT'
        grp_pos_Y = grp_pos_Y - self.distance
        self.input_out_dic['pos'] = [grp_pos_x, grp_pos_Y]

    def create(self):
        '''

        :return:
        '''

        for each in [self.input, self.techanim, self.techanim_final, self.sim, self.sim_final, self.techanim_cloth, self.techanim_cloth_final, self.final]:

            node_name = each['Name']
            node_pos = each['pos']
            node_color = each['color']

            self.help_class.createNode(obj_path=self.obj_path,
                                       node_type='geo',
                                       node_name=node_name,
                                       pos=node_pos,
                                       color=node_color)

        #CREATE INPUT DIR
        self.input_node_def()



    def input_node_def(self):
        '''

        :return:
        '''
        input = self.obj + '/' + self.input_name
        obj_path = hou.node(input)

        self.create_base_nodes(obj_path)

        self.create_model_nodes(obj_path)

        self.create_animation_nodes(obj_path)




    def create_base_nodes(self, obj_path):
        '''

        :return:
        '''
        # CREATEA A ALEMBIC NODE
        self.base_Alembic_node = self.node_class.createAlembicNode(obj_path=obj_path,
                                                                  node_name=self.base_node_dic['Name'],
                                                                  pos=self.base_node_dic['pos'])

        # ALEMBIC GROUP
        self.base_alembic_grp_node = self.node_class.createAlembicGroupNode(obj_path=obj_path,
                                                                       node_name=self.base_alembic_grp_node_def[
                                                                           'Name'],
                                                                       pos=self.base_alembic_grp_node_def['pos'],
                                                                       color=self.base_alembic_grp_node_def[
                                                                           'color'])
        self.base_alembic_grp_node.setInput(0, self.base_Alembic_node)

        # CONVERT
        self.base_convert_node = self.node_class.convertNode(obj_path=obj_path,
                                                                  node_name=self.base_convert_node_def['Name'],
                                                                  pos=self.base_convert_node_def['pos'],
                                                                  color=self.base_convert_node_def['color'])
        self.base_convert_node.setInput(0, self.base_alembic_grp_node)

        # NORMAL
        self.base_normal_node = self.node_class.normalNode(obj_path=obj_path,
                                                                node_name=self.base_normal_node_def['Name'],
                                                                pos=self.base_normal_node_def['pos'],
                                                                color=self.base_normal_node_def['color'])
        self.base_normal_node.setInput(0, self.base_convert_node)

        # CLEAN
        self.base_clean_node = self.node_class.cleanNode(obj_path=obj_path,
                                                              node_name=self.base_clean_node_def['Name'],
                                                              pos=self.base_clean_node_def['pos'],
                                                              color=self.base_clean_node_def['color'])
        self.base_clean_node.setInput(0, self.base_normal_node)

        # CLEAN
        self.base_null_node = self.node_class.create_null_node(obj_path=obj_path,
                                                                    node_name=self.base_null_node_def['Name'],
                                                                    pos=self.base_null_node_def['pos'])
        self.base_null_node.setInput(0, self.base_clean_node)



    def create_model_nodes(self, obj_path):
        '''

        :return:
        '''
        # CREATEA A ALEMBIC NODE
        self.model_Alembic_node = self.node_class.createAlembicNode(obj_path=obj_path,
                                                                  node_name=self.model_node_dic['Name'],
                                                                  pos=self.model_node_dic['pos'])

        # ALEMBIC GROUP
        self.model_alembic_grp_node = self.node_class.createAlembicGroupNode(obj_path=obj_path,
                                                                       node_name=self.model_alembic_grp_node_def[
                                                                           'Name'],
                                                                       pos=self.model_alembic_grp_node_def['pos'],
                                                                       color=self.model_alembic_grp_node_def[
                                                                           'color'])
        self.model_alembic_grp_node.setInput(0, self.model_Alembic_node)

        # CONVERT
        self.model_convert_node = self.node_class.convertNode(obj_path=obj_path,
                                                                  node_name=self.model_convert_node_def['Name'],
                                                                  pos=self.model_convert_node_def['pos'],
                                                                  color=self.model_convert_node_def['color'])
        self.model_convert_node.setInput(0, self.model_alembic_grp_node)

        # NORMAL
        self.model_normal_node = self.node_class.normalNode(obj_path=obj_path,
                                                                node_name=self.model_normal_node_def['Name'],
                                                                pos=self.model_normal_node_def['pos'],
                                                                color=self.model_normal_node_def['color'])
        self.model_normal_node.setInput(0, self.model_convert_node)

        # CLEAN
        self.model_clean_node = self.node_class.cleanNode(obj_path=obj_path,
                                                              node_name=self.model_clean_node_def['Name'],
                                                              pos=self.model_clean_node_def['pos'],
                                                              color=self.model_clean_node_def['color'])
        self.model_clean_node.setInput(0, self.model_normal_node)

        # CLEAN
        self.model_null_node = self.node_class.create_null_node(obj_path=obj_path,
                                                                    node_name=self.model_null_node_def['Name'],
                                                                    pos=self.model_null_node_def['pos'])
        self.model_null_node.setInput(0, self.model_clean_node)

    def create_animation_nodes(self, obj_path):
        '''

        :return:
        '''


        #CREATEA A ALEMBIC NODE
        self.animationAlembic_node = self.node_class.createAlembicNode(obj_path=obj_path,
                                                                  node_name=self.animation_node_dic['Name'],
                                                                  pos=self.animation_node_dic['pos'])

        #ALEMBIC GROUP
        self.alembic_grp_node = self.node_class.createAlembicGroupNode(obj_path=obj_path,
                                                                      node_name=self.animation_alembic_grp_node_def['Name'],
                                                                      pos=self.animation_alembic_grp_node_def['pos'],
                                                                      color=self.animation_alembic_grp_node_def['color'])
        self.alembic_grp_node.setInput(0, self.animationAlembic_node)


        #CONVERT
        self.animation_convert_node = self.node_class.convertNode(obj_path=obj_path,
                                                                  node_name=self.animation_convert_node_def['Name'],
                                                                  pos=self.animation_convert_node_def['pos'],
                                                                  color=self.animation_convert_node_def['color'])
        self.animation_convert_node.setInput(0, self.alembic_grp_node)

        #NORMAL
        self.animation_normal_node = self.node_class.normalNode(obj_path=obj_path,
                                                                node_name=self.animation_normal_node_def['Name'],
                                                                  pos=self.animation_normal_node_def['pos'],
                                                                  color=self.animation_normal_node_def['color'])
        self.animation_normal_node.setInput(0, self.animation_convert_node)

        #CLEAN
        self.animation_clean_node = self.node_class.cleanNode(obj_path=obj_path,
                                                              node_name=self.animation_clean_node_def['Name'],
                                                              pos=self.animation_clean_node_def['pos'],
                                                              color=self.animation_clean_node_def['color'])
        self.animation_clean_node.setInput(0, self.animation_normal_node)

        # CLEAN
        self.animation_null_node = self.node_class.create_null_node(obj_path=obj_path,
                                                                     node_name=self.animation_null_node_def['Name'],
                                                                     pos=self.animation_null_node_def['pos'])
        self.animation_null_node.setInput(0, self.animation_clean_node)




'''
new_path = 'C:/Users/Admin/Desktop/Nikheel/Spark_Project/Spark_'
import sys
sys.path.append(new_path)
from spark.Houdini.department.CFX import cloth_setup
reload(cloth_setup)
from spark.Houdini.department.CFX.cloth_setup import HOUDINI_CLOTHSETUP
cloth_setup = HOUDINI_CLOTHSETUP()
cloth_setup.create()


'''
