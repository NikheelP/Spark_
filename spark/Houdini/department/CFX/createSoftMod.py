
from spark.Houdini.common import help
from spark.Houdini.common import nodes
for each in [help, nodes]:
    reload(each)
from spark.Houdini.common.help import HELP
from spark.Houdini.common.nodes import NODES

import hou, random
from collections import OrderedDict


class SOFTMOD:

    def __init__(self):
        self.help_class = HELP()
        self.node_class = NODES()

    def create(self):
        '''

        :return:
        '''
        #GET THE POINT NUMBER
        selected_points = self.help_class.get_pointNumber_selected()
        if selected_points:
            selected_points = selected_points[0]
            selected_nodes = list(hou.selectedNodes())
            if selected_nodes:
                selected_nodes = selected_nodes[0]
                selected_node_position = selected_nodes.position()
                new_position = hou.Vector2(selected_node_position[0], selected_node_position[1] - 1.5)

                parent_obj = selected_nodes.parent()
                red_random_val = random.random()
                green_random_val = random.random()
                blue_random_val = random.random()
                hou_color = hou.Color([red_random_val, green_random_val, blue_random_val])

                #NOW GET LIST OF THE SOFTTRANSFORM OBJECT
                list_softtransform = list(parent_obj.recursiveGlob('*SoftTransform*'))


                #CREATE A GROP NODE AND PUT LOWER THE SELECTION
                softTransform = 'softMod_' + str(len(list_softtransform) + 1) + '_SoftTransform'

                '''
                group_name = parent_obj.createNode('groupcreate', group_name)
                group_name.setInput(0, selected_nodes)
                group_name.setPosition(new_position)
                group_name.parm('grouptype').set(1)
                group_name.parm('basegroup').set(str(selected_points))
                group_name.setColor(hou_color)
                '''
                #CREATE A SOFT TRABSFORM softxform

                softTransform = parent_obj.createNode('softxform', softTransform)
                softTransform.setInput(0, selected_nodes)
                softTransform.setPosition(new_position)
                softTransform.parm('group').set(str(selected_points))
                softTransform.parm('px').setExpression('point(0, %s, \'P\', 0)' %(selected_points))
                softTransform.parm('py').setExpression('point(0, %s, \'P\', 1)' %(selected_points))
                softTransform.parm('pz').setExpression('point(0, %s, \'P\', 2)' %(selected_points))
                softTransform.setColor(hou_color)
                softTransform.setDisplayFlag(True)
                softTransform.setTemplateFlag(True)
                softTransform.setSelected(True)










'''
new_path = 'C:/Users/Admin/Desktop/Nikheel/Spark_Project/Spark_'
import sys
sys.path.append(new_path)
from spark.Houdini.department.CFX import createSoftMod
reload(createSoftMod)
from spark.Houdini.department.CFX.createSoftMod import SOFTMOD

softmod = SOFTMOD()
softmod.create()

'''