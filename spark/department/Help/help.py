
import maya.cmds as cmds
from shiboken2 import wrapInstance




class HELP():

    def is_type(self, obj):
        return type(obj)

    def getMainWindowPtr():
        mayaMainWindowPtr = maya.OpenMayaUI.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
        return mayaMainWindow


    def snap_object(self, source_obj, target_obj):
        pass

def load_plugin(plugin_path):
    '''

    :param plugin_path:
    :return:
    '''
    print('this is the plugin path: ', plugin_path)
    cmds.loadPlugin(plugin_path)