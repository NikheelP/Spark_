
import maya.cmds as cmds
import maya.app.general.resourceBrowser as resourceBrowser
from shiboken2 import wrapInstance
import shiboken2
from PySide2 import QtWidgets
import os
import maya.cmds as cmds
import maya.OpenMayaUI as omu
from functools import partial
import maya.api.OpenMaya as om
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaAnim as oma


from maya import OpenMayaUI as omui


class HELP:

    def __init__(self):
        pass

    def set_type(self, obj, type_val, obj_type='obj_type'):
        '''

        :param obj: specify the object
        :param type_val: specify the type val
        :return:
        '''
        if cmds.ls(obj + '.' + obj_type) == []:
            cmds.addAttr(obj, ln=obj_type, dt='string')
            cmds.setAttr((obj + '.' + obj_type), e=True, k=True)
            cmds.setAttr((obj + '.' + obj_type), type_val, type='string')
            cmds.setAttr((obj + '.' + obj_type), l=True)

        #unlock the value
        else:
            cmds.setAttr((obj + '.' + obj_type), l=False)
            cmds.setAttr((obj + '.' + obj_type), type_val, type='string')
            cmds.setAttr((obj + '.' + obj_type), l=True)


        #if obj_type == 'obj_type':
            #cmds.setAttr((obj + '.' + obj_type), l=True)

        return obj

    def set_outline_color(self, obj, val=[0, 0, 0]):
        '''

        :param obj: specify the object
        :param val: specify th elist
        :return:
        '''
        cmds.select(obj)
        cmds.setAttr(obj + '.useOutlinerColor', 1)
        cmds.setAttr(obj + '.outlinerColor', val[0], val[1], val[2])

        return obj

    def getMayaFullDagPath(self, QObject):
        try:
            ptr = long(shiboken2.getCppPointer(QObject)[0])
        except:
            ptr = omui.MQtUtil.fullName(long(QtWidgets.shiboken.unwrapinstance(QObject)))
        mayaFullDagPath = omui.MQtUtil.fullName(ptr)
        return mayaFullDagPath

    def getWorkspaceQtPointer(self, workspaceName):
        qtCtrl = omui.MQtUtil_findControl(workspaceName)
        ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
        return ptr

    def warning(self, string):
        cmds.warning(string)

    def getRelatedNodes(self, rootSelection, inclHierarchy=False, inclShaders=False, inclInputs=False):
        if not type(rootSelection) == list:
            rootSelection = [rootSelection]

        relatedNodes = []
        hierarchyNodes = rootSelection
        hierarchyNodes += self.getShapes(hierarchyNodes)
        relatedNodes += hierarchyNodes
        if inclHierarchy:
            hierarchyNodes += self.getHierarchy(rootSelection)
            relatedNodes += hierarchyNodes
        if inclShaders:
            relatedNodes += self.getShadingNetwork(hierarchyNodes)
        if inclInputs:
            relatedNodes += self.getAllConnections(hierarchyNodes)

        relatedNodes = cmds.ls(relatedNodes, long=False)
        relatedNodes = list(set(relatedNodes))

        return relatedNodes

    def getShapes(self, nodeList):
        nodeOutput = []
        result = cmds.listRelatives(nodeList, shapes=True, fullPath=True)
        if result:
            nodeOutput += result
        return nodeOutput

    def getHierarchy(self, nodeList):
        nodeOutput = []
        for node in nodeList:
            result = cmds.listRelatives(node, allDescendents=True, shapes=False, path=True, fullPath=True)
            if result:
                nodeOutput += result

        nodeOutput = list(set(nodeOutput))
        return nodeOutput

    def getShadingNetwork(self, nodeList=[]):
        if not type(nodeList) == list:
            nodeList = [nodeList]

        nodeOutput = []
        SGs = []
        for node in nodeList:
            shadingEngine = cmds.listConnections(node, type="shadingEngine")
            if shadingEngine:
                SGs += shadingEngine

        SGs = list(set(SGs))
        nodeOutput += SGs

        rootShadingNodes = []
        for SG in SGs:
            SG_connections = cmds.listConnections(SG)
            rootShadingNodes += cmds.ls(SG_connections, materials=True)

        rootShadingNodes = list(set(rootShadingNodes))
        for node in rootShadingNodes:
            nodeOutput += cmds.listHistory(node, allConnections=True, future=False, interestLevel=2)

        nodeOutput = list(set(nodeOutput))
        return nodeOutput

    def getAllConnections(self, nodeList):
        nodeOutput = []
        for node in nodeList:
            result = cmds.listHistory(node, allConnections=True, interestLevel=1)
            if result:
                result = cmds.ls(result, long=True)
                nodeOutput += result

        return nodeOutput

    def getModule(self, moduleName='', reloadModule=False):
        if moduleName.startswith('.'):
            modulePath = moduleName
        else:
            modulePath = moduleName

        try:
            module = importlib.import_module(modulePath)
        except:
            print('\n------------\nKS_NodeOutliner ScriptFilter - Could not find script module:', moduleName, '\n------------')
            return None

    def getModuleFunction(self, module, functionName):
        try:
            function = getattr(module, functionName)
        except:
            print('\n------------\nKS_NodeOutliner ScriptFilter - Could not find script functon:', functionName, module, '\n------------')
            function = None

        return function


    def worldBlendshape(self, obj_one, obj_two):
        blend_shape = cmds.blendShape(obj_one, obj_two, o='world')[0]
        cmds.setAttr(blend_shape + '.' + obj_one, 1)

    def pivot_move(self, obj_name, pos):
        cmds.setAttr((obj_name + '.rotatePivotX'), pos[0])
        cmds.setAttr((obj_name + '.rotatePivotY'), pos[1])
        cmds.setAttr((obj_name + '.rotatePivotZ'), pos[2])
        cmds.setAttr((obj_name + '.scalePivotX'), pos[0])
        cmds.setAttr((obj_name + '.scalePivotY'), pos[1])
        cmds.setAttr((obj_name + '.scalePivotZ'), pos[2])

    def weight_value(self, each_surface, each_transform):
        self.base_MSelection_list = om.MSelectionList()
        self.base_MSelection_list.add(each_surface)
        self.base_geo_dag_path = self.base_MSelection_list.getDagPath(0)

        # get the base vertex position
        self.base_mfn_mesh = om.MFnMesh(self.base_geo_dag_path)
        self.base_vtx_list = self.base_mfn_mesh.getPoints(om.MSpace.kWorld)

        # get the value
        self.clusterMSelection = om.MSelectionList()
        self.clusterMSelection.add(each_transform)
        self.clusterDagPath = self.clusterMSelection.getDagPath(0)
        self.mFnTransform = om.MFnTransform(self.clusterDagPath)
        self.world = self.mFnTransform.translation(om.MSpace.kWorld)
        self.moveWorld = om.MVector(self.world.x + 1.0, self.world.y, self.world.z)
        self.mFnTransform.setTranslation(self.moveWorld, om.MSpace.kWorld)
        self.movePosition = self.base_mfn_mesh.getPoints(om.MSpace.kWorld)
        self.mFnTransform.setTranslation(self.world, om.MSpace.kWorld)

        # get the diff
        weight_val_list = []
        a = 0
        while a < len(self.base_vtx_list):
            diff_val = self.movePosition[a].x - self.base_vtx_list[a].x
            weight_val_list.append(diff_val)
            a += 1
        return weight_val_list

