# import modulers
import os
import maya.cmds as cmds
import maya.OpenMayaUI as omu
from functools import partial
import maya.api.OpenMaya as om
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaAnim as oma

from spark.department import help
from spark.department.Help import deformer

for each in [help, deformer]:
    reload(help)

from spark.department.help import HELP
from spark.department.Help.deformer import DEFORMER

class TRANSFORM_OBJECT_TO_CLUSTER:
    def __init__(self):
        self.help_class = HELP()
        self.deformer_class = DEFORMER()


    def extract_cluster(self, transform_obj_list, surface_obj_list):
        for each_transform in transform_obj_list:
            jointMSelection = om.MSelectionList()
            jointMSelection.add(each_transform)
            jointDagPath = jointMSelection.getDagPath(0)
            for each_surface in surface_obj_list:
                # get the weight  value
                weight_list = self.help_class.weight_value(each_surface=each_surface,
                                                               each_transform=each_transform)
                # set the defaule and move object vertex value
                # self.set_base_move_pos_list(each_transform, each_surface)

                # create a cluster and set the position
                self.create_cluster_set_position(each_transform, each_surface)

                # set weight value
                self.deformer_class.setWeights(self.cluster_name, weight_list)

    def create_cluster_set_position(self, each_transform, each_surface):
        cmds.select(each_surface)
        self.cluster_name = each_transform + '_' + each_surface + '_Cluster'
        cmds.cluster(n=self.cluster_name)
        self.cluster_handle_name = self.cluster_name + 'Handle'
        self.cluster_shape_name = cmds.listRelatives(self.cluster_handle_name, s=True)[0]

        self.point_position = cmds.xform(each_transform, q=1, ws=1, rp=1)

        #move the pivot
        self.help_class.pivot_move(self.cluster_handle_name,self.point_position)

        cmds.setAttr((self.cluster_shape_name + '.originX'), self.point_position[0])
        cmds.setAttr((self.cluster_shape_name + '.originY'), self.point_position[1])
        cmds.setAttr((self.cluster_shape_name + '.originZ'), self.point_position[2])