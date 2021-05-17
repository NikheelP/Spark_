from spark.Houdini.common import help

for each in [help]:
    reload(help)

from spark.Houdini.common.help import HELP


class NODES:

    def __init__(self):
        self.help_class = HELP()

    def create_null_node(self, obj_path, node_type='null', node_name='', pos=[0, 0], color=[0, 0, 0]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''

        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=node_type,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def createAlembicNode(self, obj_path, node_type='alembic', node_name='SampleAlembic', pos=[0, 0], color=[0.996, 0.993, 0]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR 0.996, g=0.933, b=0
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=node_type,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def createAlembicGroupNode(self, obj_path, node_type='alembicgroup', node_name='SampleAlembicGroup', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=node_type,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def convertNode(self, obj_path, node_type='convert', node_name='SampleConvert', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=node_type,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def normalNode(self, obj_path, node_type='normal', node_name='SampleNormal', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=node_type,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

    def cleanNode(self, obj_path, node_type='clean', node_name='SampleClean', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''

        :param obj_path: SPECIFY THE OBJ PATH
        :param node_type: SPECIFY THE NODE TYPE
        :param node_name: SPECIFY THE NODE NAME
        :param pos: SPECIFY POS
        :param color: SPECIFY THE NODE COLOR
        :return:
        '''
        node = self.help_class.createNode(obj_path=obj_path,
                                          node_type=node_type,
                                          node_name=node_name,
                                          pos=pos,
                                          color=color)

        return node

