import hou, nodesearch
import toolutils, random
class HELP:

    def __init__(self):
        pass

    def createNode(self, obj_path, node_type, node_name='', pos=[0, 0], color=[0.8, 0.8, 0.8]):
        '''
        this will create a node from the name and make the position default at 0
        :param obj_path:  SPECIFY THE OBJECT PATH
        :param node_name:  SPECIFY THE NODE NAME
        :param pos:  SPECIFY THE NODE POSITION
        :param color:  SPECIFY THE NODE COLOR
        :return: NODE
        '''

        node = obj_path.createNode(node_type, node_name)
        node.setPosition((pos[0], pos[1]))
        node.setColor(hou.Color(color[0], color[1], color[2]))

        return node

    def get_pointNumber_selected(self):
        '''

        :return:
        '''
        selection = toolutils.sceneViewer().selectGeometry()
        selection = selection.selectionStrings()
        selection = list(selection)

        return selection

    def get_no_of_node_type(self, obj_path, type):
        '''

        :param obj_path: specify the object path
        :param type: specify the nodeType
        :return: no of the nodes
        '''
        matcher = nodesearch.NodeType(type)
        nodes = matcher.nodes(obj_path)

        return len(nodes)

    def setFlag(self, node, displayFlag=False, templateFlag=False, renderFlag=False, clear_all_selected=True):
        '''
                        softTransform.setDisplayFlag(True)
                softTransform.setTemplateFlag(True)
                softTransform.setSelected(True)
        :return:
        '''
        #set all the template flag off in the parent geo

        parent_obj = node.parent()
        for each in parent_obj.children():
            each.setTemplateFlag(False)

        node.setDisplayFlag(displayFlag)
        node.setRenderFlag(renderFlag)
        node.setTemplateFlag(templateFlag)
        node.setSelected(True, clear_all_selected=clear_all_selected)
        return node

    def set_node_new_position(self, node, previousNode=None):
        '''

        :param node:
        :param previousNode:
        :return:
        '''
        if previousNode is not None:
            node_position = previousNode.position()
            new_pos = hou.Vector2(node_position[0], node_position[1]-1)

        else:
            new_pos = hou.Vector2(0, 0)

        node.setPosition(new_pos)

        return node


    def get_random_color(self):
        '''

        :return:
        '''
        red_random_val = random.random()
        green_random_val = random.random()
        blue_random_val = random.random()
        hou_color = hou.Color([red_random_val, green_random_val, blue_random_val])
        return hou_color


