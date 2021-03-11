import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from spark.department.Help import Math_help

for each in [Math_help]:
    reload(Math_help)

from spark.department.Help.Math_help import MATHUTIL_HELP

import math

class MATRIX_HELP:

    def __init__(self):
        self.math_util_help_class = MATHUTIL_HELP()


    def getMatrix(self, transform,local=False,time=None):
        # Check transform
        if not cmds.objExists(transform):
            raise Exception('Object "'+transform+'" does not exist!!')

        # Define Matrix attribute
        matAttr = 'worldMatrix[0]'
        if local: matAttr = 'matrix'

        # Get time
        mat = OpenMaya.MMatrix()
        if time != None: mat = cmds.getAttr(transform+'.'+matAttr,t=time)
        else: mat = cmds.getAttr(transform+'.'+matAttr)

        # Build Matrix
        matrix = self.buildMatrix(translate=(mat[12],mat[13],mat[14]),
                                  xAxis=(mat[0],mat[1],mat[2]),
                                  yAxis=(mat[4],mat[5],mat[6]),
                                  zAxis=(mat[8],mat[9],mat[10]))

        # Return result
        return matrix

    def buildMatrix(self, translate=(0,0,0), xAxis=(1,0,0), yAxis=(0,1,0), zAxis=(0,0,1)):
        # Create transformation matrix from input vectors
        matrix = OpenMaya.MMatrix()
        values = []
        OpenMaya.MScriptUtil.setDoubleArray(matrix[0], 0, xAxis[0])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[0], 1, xAxis[1])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[0], 2, xAxis[2])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[1], 0, yAxis[0])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[1], 1, yAxis[1])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[1], 2, yAxis[2])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[2], 0, zAxis[0])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[2], 1, zAxis[1])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[2], 2, zAxis[2])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[3], 0, translate[0])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[3], 1, translate[1])
        OpenMaya.MScriptUtil.setDoubleArray(matrix[3], 2, translate[2])
        return matrix

    def vectorMatrixMultiply(self, vector, matrix, transformAsPoint=False, invertMatrix=False):
        # Create MPoint/MVector object for transformation
        if transformAsPoint: vector = OpenMaya.MPoint(vector[0],vector[1],vector[2],1.0)
        else: vector = OpenMaya.MVector(vector[0],vector[1],vector[2])

        # Check input is of type MMatrix
        if type(matrix) != OpenMaya.MMatrix:
            raise Exception('Matrix input variable is not of expected type! Expecting MMatrix, received '+str(type(matrix))+'!!')

        # Transform vector
        if matrix != OpenMaya.MMatrix.identity:
            if invertMatrix: matrix = matrix.inverse()
            vector *= matrix

        # Return new vector
        return [vector.x,vector.y,vector.z]

    def getTranslation(self, matrix):
        x = OpenMaya.MScriptUtil.getDoubleArrayItem(matrix[3],0)
        y = OpenMaya.MScriptUtil.getDoubleArrayItem(matrix[3],1)
        z = OpenMaya.MScriptUtil.getDoubleArrayItem(matrix[3],2)
        return (x,y,z)

    def getRotation(self, matrix,rotationOrder='xyz'):

        # Calculate radian constant
        radian = 180.0 / Math_help.pi

        # Check rotation order
        if type(rotationOrder) == str:
            rotationOrder = rotationOrder.lower()
            rotateOrder = {'xyz':0,'yzx':1,'zxy':2,'xzy':3,'yxz':4,'zyx':5}
            if not rotateOrder.has_key(rotationOrder):
                raise Exception('Invalid rotation order supplied!')
            rotationOrder = rotateOrder[rotationOrder]
        else:
            rotationOrder = int(rotationOrder)

        # Get transformation matrix
        transformMatrix = OpenMaya.MTransformationMatrix(matrix)

        # Get Euler rotation from matrix
        eulerRot = transformMatrix.eulerRotation()

        # Reorder rotation
        eulerRot.reorderIt(rotationOrder)

        # Return XYZ rotation values
        return (eulerRot.x*radian,eulerRot.y*radian,eulerRot.z*radian)

    def buildRotation(self, aimVector,upVector=(0,1,0),aimAxis='x',upAxis='y'):

        # Check negative axis
        negAim = False
        negUp = False
        if aimAxis[0] == '-':
            aimAxis = aimAxis[1]
            negAim = True
        if upAxis[0] == '-':
            upAxis = upAxis[1]
            negUp = True

        # Check valid axis
        axisList = ['x','y','z']
        if not axisList.count(aimAxis): raise Exception('Aim axis is not valid!')
        if not axisList.count(upAxis): raise Exception('Up axis is not valid!')
        if aimAxis == upAxis: raise Exception('Aim and Up axis must be unique!')

        # Determine cross axis
        axisList.remove(aimAxis)
        axisList.remove(upAxis)
        crossAxis = axisList[0]
    #####################################################################################
        # Normaize aimVector
        aimVector = self.math_util_help_class.normalizeVector(aimVector)
        if negAim: aimVector = (-aimVector[0],-aimVector[1],-aimVector[2])
        # Normaize upVector
        upVector = self.math_util_help_class.normalizeVector(upVector)
        if negUp: upVector = (-upVector[0],-upVector[1],-upVector[2])

        # Get cross product vector
        crossVector = (0,0,0)
        if (aimAxis == 'x' and upAxis == 'z') or (aimAxis == 'z' and upAxis == 'y'):
            crossVector = self.math_util_help_class.crossProduct(upVector,aimVector)
        else:
            crossVector = self.math_util_help_class.crossProduct(aimVector,upVector)
        # Recalculate upVector (orthogonalize)
        if (aimAxis == 'x' and upAxis == 'z') or (aimAxis == 'z' and upAxis == 'y'):
            upVector = self.math_util_help_class.crossProduct(aimVector,crossVector)
        else:
            upVector = self.math_util_help_class.crossProduct(crossVector,aimVector)

        # Build axis dictionary
        axisDict={aimAxis: aimVector,upAxis: upVector,crossAxis: crossVector}
        # Build rotation matrix
        mat = self.buildMatrix(xAxis=axisDict['x'],yAxis=axisDict['y'],zAxis=axisDict['z'])

        # Return rotation matrix
        return mat

    def inverseTransform(self, source, destination, translate=True, rotate=True, scale=True):


        if not cmds.objExists(source): raise Exception('Transform "'+source+'" does not exist!!')
        if not cmds.objExists(destination): raise Exception('Transform "'+destination+'" does not exist!!')

        # Load decomposeMatrix plugin
        if not cmds.pluginInfo('decomposeMatrix',q=True,l=True):
            try: cmds.loadPlugin('decomposeMatrix')
            except: raise MissingPluginError('Unable to load "decomposeMatrix" plugin!!')

        # =================================
        # - Apply Inverse Transformations -
        # =================================

        # Create and name decomposeMatrix node
        dcm = cmds.createNode('decomposeMatrix',n=source+'_decomposeMatrix')

        # Make connections
        cmds.connectAttr(source+'.inverseMatrix',dcm+'.inputMatrix',f=True)
        if translate: cmds.connectAttr(dcm+'.outputTranslate',destination+'.translate',f=True)
        if rotate: cmds.connectAttr(dcm+'.outputRotate',destination+'.rotate',f=True)
        if scale: cmds.connectAttr(dcm+'.outputScale',destination+'.scale',f=True)

        # =================
        # - Return Result -
        # =================

        return dcm

    def fromList(self, valueList):
        # Check Value List
        if len(valueList) != 16:
            raise Exception('Invalid value list! Expecting 16 element, found '+str(len(valueList)))

        # Create transformation matrix from input vaules
        matrix = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList(valueList,matrix)

        return matrix

    def asList(self, matrix):
        return [	matrix(0,0),matrix(0,1),matrix(0,2),matrix(0,3),
                    matrix(1,0),matrix(1,1),matrix(1,2),matrix(1,3),
                    matrix(2,0),matrix(2,1),matrix(2,2),matrix(2,3),
                    matrix(3,0),matrix(3,1),matrix(3,2),matrix(3,3),	]

    def printMatrix(self, matrix):
        '''
        Print the specified matrix values to the script editor
        @param matrix: Matrix to print
        @type matrix: maya.OpenMaya.MMatrix
        '''
        print ('%.3f' % matrix(0,0))+', '+('%.3f' % matrix(0,1))+', '+('%.3f' % matrix(0,2))+', '+('%.3f' % matrix(0,3))
        print ('%.3f' % matrix(1,0))+', '+('%.3f' % matrix(1,1))+', '+('%.3f' % matrix(1,2))+', '+('%.3f' % matrix(1,3))
        print ('%.3f' % matrix(2,0))+', '+('%.3f' % matrix(2,1))+', '+('%.3f' % matrix(2,2))+', '+('%.3f' % matrix(2,3))
        print ('%.3f' % matrix(3,0))+', '+('%.3f' % matrix(3,1))+', '+('%.3f' % matrix(3,2))+', '+('%.3f' % matrix(3,3))
