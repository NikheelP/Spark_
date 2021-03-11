import os
import maya.cmds as cmds
import maya.mel as mel
from spark.department.Help import help


def smooth_deformer():
    from spark.department.CFX.deformer import smoothNode
    deformer = 'smoothNode'
    help.load_plugin(os.path.abspath(smoothNode.__file__).replace('\\', '/'))

    sel_obj = cmds.ls(sl=True)
    if sel_obj:
        for each in sel_obj:
            cmds.select(each)
            deformer_name = cmds.deformer(type=deformer)[0]
            mel.eval('cycleCheck -e off')


def corrective_blendshape():
    from spark.department.CFX.deformer import correctiveBlendshape
    help.load_plugin(os.path.abspath(correctiveBlendshape.__file__).replace('\\', '/'))
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
    from spark.department.CFX.deformer import normalPush
    help.load_plugin(os.path.abspath(normalPush.__file__).replace('\\', '/'))
    deformer = 'normalPush'

    sel_obj = cmds.ls(sl=True)
    if sel_obj:
        for each in sel_obj:
            cmds.select(each)
            deformer_name = cmds.deformer(type=deformer)[0]




def blendWrap():
    '''
    select the to object to wrap
    selec the from object to wrap
    :return:
    '''

    from spark.department.CFX.deformer import blendWrap
    help.load_plugin(os.path.abspath(blendWrap.__file__).replace('\\', '/'))
    deformer = 'blendwrap'

    sel_obj = cmds.ls(sl=True)
    if len(sel_obj) == 2:
        first_obj = sel_obj[0]
        secound_obj = sel_obj[1]
        secound_obj_shape = cmds.listRelatives(secound_obj, s=True)[0]

        # load Plugin
        cmds.select(first_obj)
        deformer_name = cmds.deformer(type=deformer)
        cmds.connectAttr((secound_obj_shape + '.worldMesh[0]'), (deformer_name[0] + '.ConnectMesh'), f=True)


def noiseDeformer():
    '''

    :return:
    '''

    from spark.department.CFX.deformer import noise_deformer
    help.load_plugin(os.path.abspath(noise_deformer.__file__).replace('\\', '/'))
    deformer = 'noiseDeformer'
    sel_obj = cmds.ls(sl=True)
    if sel_obj:
        for each in sel_obj:
            cmds.select(each)
            deformer_name = cmds.deformer(type=deformer)[0]

def meshCollution():
    '''

    :return:
    '''

    from spark.department.CFX.deformer import meshCollution
    help.load_plugin(os.path.abspath(meshCollution.__file__).replace('\\', '/'))





def load_plugin(plugin_path):
    '''

    :param plugin_path:
    :return:
    '''
    print('this is the plugin path: ', plugin_path)
    cmds.loadPlugin(plugin_path)

