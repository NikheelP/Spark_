from spark.department.Help.Houdini import help

for each in [help]:
    reload(help)

from spark.department.Help.Houdini.help import HELP


class NODES:

    def __init__(self):
        self.help_class = HELP()

        #NODE NAME
        self.null_node_name = 'null'
        self.alembic_node_name = 'alembic'
        self.alembic_group_node_name = 'alembicgroup'
        self.convert_node_name = 'convert'
        self.normal_node_name = 'normal'
        self.clean_node_name = 'clean'
        self.smooth_node_name = 'smooth::2.0'




    def create_null_node(self, obj_path, node_name='', pos=[0, 0], color=[0, 0, 0]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''

        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=self.null_node_name,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def createAlembicNode(self, obj_path, node_name='SampleAlembic', pos=[0, 0], color=[0.996, 0.993, 0]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR 0.996, g=0.933, b=0
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=self.alembic_node_name,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def createAlembicGroupNode(self, obj_path, node_name='SampleAlembicGroup', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=self.alembic_group_node_name,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def convertNode(self, obj_path, node_name='SampleConvert', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=self.convert_node_name,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def normalNode(self, obj_path, node_name='SampleNormal', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=self.normal_node_name,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def cleanNode(self, obj_path, node_name='SampleClean', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=self.clean_node_name,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def smoothNode(self, obj_path, node_name='sampleSmooth', pos=[0, 0], color=[0.8, 0.8, 0.8], setInput=None, parent_obj=None):
        '''

        :param obj_path:
        :param node_name:
        :param pos:
        :param color:
        :param setInput:
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=self.smooth_node_name,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        if setInput is not None:
            if parent_obj is not None:
                node.setInput(0, parent_obj)

        return node


