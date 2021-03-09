import os
import maya.cmds as cmds
import maya.mel as mel


def smooth_deformer():
    from spark.CFX.deformer import smoothNode
    deformer = 'smoothNode'
    load_plugin(os.path.abspath(smoothNode.__file__).replace('\\', '/'))

    sel_obj = cmds.ls(sl=True)
    if sel_obj:
        for each in sel_obj:
            cmds.select(each)
            deformer_name = cmds.deformer(type=deformer)[0]
            mel.eval('cycleCheck -e off')


def corrective_blendshape():
    from spark.CFX.deformer import correctiveBlendshape
    load_plugin(os.path.abspath(correctiveBlendshape.__file__).replace('\\', '/'))
    deformer = 'correctiveBlendshape'
    #Create a corrective
    # load Plugin
    sel_obj = cmds.ls(sl=True)
    if sel_obj:
        current_time = str(int(cmds.currentTime(q=True)))
        full_name = sel_obj[0] + '_' + str(current_time) + '_Corrective'
        shape_name = full_name + 'Shape'
        cmds.select(sel_obj[0])
        cmds.duplicate(n=full_name)
        cmds.select(sel_obj[0])
        corrective_blendshape_name = cmds.deformer(type=deformer)[0]
        cmds.connectAttr((shape_name + '.worldMesh[0]'), (corrective_blendshape_name + '.blendMesh'))

        #move duplicate in one grouo
        grp_name = 'Corrective_Shape'
        if not cmds.objExists(grp_name):
            cmds.createNode('transform', n=grp_name)
        cmds.parent(full_name, grp_name)


def normalPush():
    from spark.CFX.deformer import normalPush
    load_plugin(os.path.abspath(normalPush.__file__).replace('\\', '/'))
    deformer = 'normalPush'

    sel_obj = cmds.ls(sl=True)
    if sel_obj:
        for each in sel_obj:
            cmds.select(each)
            deformer_name = cmds.deformer(type=deformer)[0]



def load_plugin(plugin_path):
    '''

    :param plugin_path:
    :return:
    '''
    print('this is the plugin path: ', plugin_path)
    cmds.loadPlugin(plugin_path)

