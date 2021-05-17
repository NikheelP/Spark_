import hou
import toolutils
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


