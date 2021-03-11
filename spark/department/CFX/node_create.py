
import os
from spark.department.Help import help


def motionMult():
    from spark.department.CFX.Node import motionMult
    help.load_plugin(os.path.abspath(motionMult.__file__).replace('\\', '/'))
    node_name = 'motionMult'



