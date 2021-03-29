
import maya.cmds as cmds
from shiboken2 import wrapInstance
import os
import subprocess
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')



class HELP():

    def is_type(self, obj):
        return type(obj)

    def getMainWindowPtr():
        mayaMainWindowPtr = maya.OpenMayaUI.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
        return mayaMainWindow


    def snap_object(self, source_obj, target_obj):
        pass

    def add_tag(self, obj, tag_name, tag_value):
        '''
        ADD TAG
        :param obj : SPECIFY THE OBJECT TO TAG
        :param tag_name: SPECIFY THE TAG NAME
        :param tag_value: SPECIFY THE  TAG VALUE
        :return:
        '''

        if cmds.objExist(obj):
            pass

    def explore(self, path):
        # explorer would choke on forward slashes
        path = os.path.normpath(path)

        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):

            subprocess.run([FILEBROWSER_PATH, '/select,', path])




def load_plugin(plugin_path):
    '''

    :param plugin_path:
    :return:
    '''
    print('this is the plugin path: ', plugin_path)
    cmds.loadPlugin(plugin_path)