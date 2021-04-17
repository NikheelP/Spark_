from spark.department.Help import help
import os

def smooth_node_load_plugin():
    from spark.department.CFX.deformer import smoothNode
    deformer = 'smoothNode'
    help.load_plugin(os.path.abspath(smoothNode.__file__).replace('\\', '/'))

def corrective_blendshape_load_plugin():
    from spark.department.CFX.deformer import correctiveBlendshape
    help.load_plugin(os.path.abspath(correctiveBlendshape.__file__).replace('\\', '/'))

def normalPush_load_plugin():
    from spark.department.CFX.deformer import normalPush
    help.load_plugin(os.path.abspath(normalPush.__file__).replace('\\', '/'))

def motionMult_load_plugin():
    from spark.department.CFX.Node import motionMult
    help.load_plugin(os.path.abspath(motionMult.__file__).replace('\\', '/'))


def run():
    print('PLUGGING IS LOADING')
    #LOAD PLUGIN
    smooth_node_load_plugin()
    corrective_blendshape_load_plugin()
    normalPush_load_plugin()
    motionMult_load_plugin()
    print('PLUGIN GOT LOADED')


print('\n\nthis is the Startup START')
run()
print('this is the Startup  END\n\n')
