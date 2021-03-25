import maya.cmds as mc
import maya.mel as mel


class SOFTMOD:

    def __init__(self):
        pass



    def joeMod(self, compSel):

        if (not mc.objExists(compSel)):
            return ([])
        defSurface = mel.eval('plugNode(\"' + compSel + '\")')
        cvSelCheck = mc.filterExpand(sm=39)
        vertSelCheck = mc.filterExpand(sm=31)
        surfpSelCheck = mc.filterExpand(sm=41)

        if not cvSelCheck == None:
            # create softmod and connect geo compensation matrix
            curveName = mc.ls(hilite=1)
            softmod = mc.softMod(defSurface, name='joeMod0')
            inputshapeplug = mc.listConnections(softmod[0] + '.input[0].inputGeometry', plugs=1)
            for attr in ['.rp', '.rpt', '.sp', '.spt', '.origin']:
                mc.setAttr(softmod[1] + attr, 0, 0, 0)
            mc.setAttr(softmod[1] + '.v', keyable=0)
            mc.setAttr(softmod[1] + '.displayHandle', 1)
            mc.setAttr(softmod[0] + '.falloffAroundSelection', 0)
            mc.connectAttr(defSurface + '.worldMatrix', softmod[0] + '.geomMatrix[0]', f=1)

            # create curveFromMeshEdge and pointOnCurveInfo to get position of cp
            pointOnCurve = ''
            poc = mc.createNode('pointOnCurveInfo', name=defSurface + '_' + softmod[1] + '_curvePoint')
            paramStr = mel.eval('match(\"[^[]*$\", \"' + compSel + '\")')
            paramStr = mel.eval('match(\"^[^]]*\", \"' + paramStr + '\")')
            mc.addAttr(poc, longName='targetGeometry', dataType='string')
            mc.setAttr(pointOnCurve + '.targetGeometry', defSurface, type='string')
            mc.setAttr(poc + '.parameter', float(paramStr))
            mc.connectAttr(inputshapeplug[0], poc + '.inputCurve')

            # create a null for softmod parent transform, no constraint for curves
            nul = mc.createNode('transform', name=softmod[0] + '_nul')
            mc.setAttr(nul + '.inheritsTransform', 0)
            mc.setAttr(nul + '.v', keyable=0)
            mc.setAttr(nul + '.tx', keyable=1)
            mc.setAttr(nul + '.ty', keyable=1)
            mc.setAttr(nul + '.tz', keyable=1)
            mc.setAttr(nul + '.rx', keyable=1)
            mc.setAttr(nul + '.ry', keyable=1)
            mc.setAttr(nul + '.rz', keyable=1)
            mc.setAttr(nul + '.sx', keyable=0)
            mc.setAttr(nul + '.sy', keyable=0)
            mc.setAttr(nul + '.sz', keyable=0)
            mc.connectAttr(poc + '.position', nul + '.translate', f=1)

            # use buildRotation to orient softmod nul to curve tangent
            buildRot = mc.createNode('buildRotation', name=nul + '_buildRotation')
            mc.connectAttr(poc + '.normal', buildRot + '.up', f=1)
            mc.connectAttr(poc + '.tangent', buildRot + '.forward', f=1)
            mc.connectAttr(nul + '.ro', buildRot + '.rotateOrder', f=1)
            mc.connectAttr(buildRot + '.rotate', nul + '.r', f=1)

            # parent softmod under null connect bindPreMatrix
            offset = mc.createNode('transform', name=softmod[1] + '_offset', parent=nul)
            offsetWorldTx = mc.createNode('transform', name=softmod[1] + '_offset_worldtx', parent=nul)
            mc.setAttr(offsetWorldTx + '.io', 1)
            mc.setAttr(offset + '.v', keyable=0)
            mc.setAttr(offsetWorldTx + '.inheritsTransform', 0)
            mc.pointConstraint(offset, offsetWorldTx)
            mc.parent(softmod[1], offset, relative=1)
            mc.connectAttr(offsetWorldTx + '.t', softmod[0] + '.falloffCenter', f=1)
            mc.connectAttr(softmod[1] + '.pim', softmod[0] + '.bindPreMatrix', f=1)

            # set softmod influence to 0 for 0 and 1 CVs for your protection
            # percent -value 0 (softmod[0]) '*.cv[0:1]'

            # create circles for interactive falloff radius
            xCircleX = mc.circle(c=(0, 0, 0), normal=(1, 0, 0), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cx')
            mc.parent(softmod[1] + '_cxShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            yCircleY = mc.circle(c=(0, 0, 0), normal=(0, 1, 0), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cy')
            mc.parent(softmod[1] + '_cyShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            zCircleZ = mc.circle(c=(0, 0, 0), normal=(0, 0, 1), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cz')
            mc.parent(softmod[1] + '_czShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            mc.setAttr(softmod[0] + '.falloffCenterX', keyable=0)
            mc.setAttr(softmod[0] + '.falloffCenterY', keyable=0)
            mc.setAttr(softmod[0] + '.falloffCenterZ', keyable=0)
            mc.rename(xCircleX[1], softmod[1] + '_cxRad')
            mc.rename(yCircleY[1], softmod[1] + '_cyRad')
            mc.rename(zCircleZ[1], softmod[1] + '_czRad')
            mc.delete(softmod[1] + '_cx')
            mc.delete(softmod[1] + '_cy')
            mc.delete(softmod[1] + '_cz')
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_cxRad.radius', f=1)
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_cyRad.radius', f=1)
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_czRad.radius', f=1)
            mc.setAttr(softmod[1] + '_cxShape.template', 1)
            mc.setAttr(softmod[1] + '_cyShape.template', 1)
            mc.setAttr(softmod[1] + '_czShape.template', 1)

            # locator for handle and quick select
            mc.spaceLocator(position=(0, 0, 0), name=softmod[0] + '_loc')
            mc.setAttr(softmod[0] + '_locShape.overrideEnabled', 1)
            mc.setAttr(softmod[0] + '_locShape.overrideColor', 17)
            mc.parent(softmod[0] + '_locShape', softmod[1], relative=1, shape=1)
            mc.delete(softmod[0] + '_loc')
            mc.addAttr(softmod[1], longName='______________', at='enum', en='_____')
            mc.setAttr(softmod[1] + '.______________', keyable=1)
            mc.addAttr(softmod[1], longName='aimTangent', at='bool', dv=0)
            mc.addAttr(softmod[1], longName='LocColor', at='long', min=0, max=31, dv=17)
            mc.setAttr(softmod[1] + '.LocColor', keyable=1)
            mc.connectAttr(softmod[1] + '.LocColor', softmod[0] + '_locShape.overrideColor', f=1)
            mc.addAttr(softmod[1], longName='ScaleHandle', at='double', min=.1, max=121212, dv=1)
            mc.addAttr(softmod[1], longName='CircVis', at='bool', dv=1)
            mc.addAttr(softmod[1], longName='SMod_Env', at='double', min=0, max=1, dv=1)
            mc.addAttr(softmod[1], longName='FallOffRad', at='double', min=0, max=8888, dv=5)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleX', f=1)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleY', f=1)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleZ', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircVis', softmod[0] + 'Handle_cxShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircVis', softmod[0] + 'Handle_cyShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircVis', softmod[0] + 'Handle_czShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.SMod_Env', softmod[0] + '.envelope', f=1)
            mc.connectAttr(softmod[0] + 'Handle.FallOffRad', softmod[0] + '.falloffRadius', f=1)

            # the color list for attr 'Loc Color'  . . . . .
            # / 0 = dark grey #/ 1 = black #/ 2 = mid grey #/ 3 = light grey #/ 4 = dark red
            # / 5 = dark blue #/ 6 = mid blue #/ 7 = dark green #/ 8 = dark purple #/ 9 = mid purple
            # /10 = light brown #/11 = dark brown #/12 = brown #/13 = red #/14 = bright green
            # /15 = faded blue #/16 = white #/17 = yellow #/18 = cyan #/19 = sel green
            # /20 = pink #/21 = light orange #/22 = light yellow #/23 = mid green #/24 = mid brown
            # /25 = dark yellow #/26 = light green #/27 = low green #/28 = dark cyan #/29 = light blue
            # /30 = purple #/31 = magenta

            # hide unnecessary attrs on handle
            mc.setAttr(softmod[0] + 'Handle.ScaleHandle', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.CircVis', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.SMod_Env', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.FallOffRad', keyable=1)
            mc.setAttr(softmod[0] + '.falloffInX', keyable=0)
            mc.setAttr(softmod[0] + '.falloffInY', keyable=0)
            mc.setAttr(softmod[0] + '.falloffInZ', keyable=0)
            mc.setAttr(softmod[0] + '.falloffMasking', keyable=0)
            mc.setAttr(softmod[0] + '.falloffAroundSelection', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle.displayHandle', 0)
            mc.setAttr(softmod[0] + 'HandleShape.visibility', 0)
            mc.pickWalk(direction='up')

            return (softmod)

        elif not vertSelCheck == None:
            # create softmod and connect geo compensation matrix
            softmod = mc.softMod(defSurface, name='joeMod0')
            insertshapeplug = mc.listConnections(softmod[0] + '.input[0].inputGeometry', plugs=1)
            for attr in ['.rp', '.rpt', '.sp', '.spt', '.origin']:
                mc.setAttr(softmod[1] + attr, 0, 0, 0)
            mc.setAttr(softmod[1] + '.v', keyable=0)
            mc.setAttr(softmod[1] + '.displayHandle', 1)
            mc.setAttr(softmod[0] + '.falloffAroundSelection', 0)
            mc.connectAttr(defSurface + '.worldMatrix', softmod[0] + '.geomMatrix[0]', f=1)

            # create curveFromMeshEdge and use pointOnCurveInfo to get vert position
            vertexEdges = mc.polyInfo(compSel, vertexToEdge=1)
            edgeIdsTemps = vertexEdges[0].split(' ')
            edgeIds = []
            for edgeIdsTemp in edgeIdsTemps:
                if not edgeIdsTemp == '':
                    if ":" in edgeIdsTemp:
                        edgeIds.append(edgeIdsTemp[:-1])
                    else:
                        edgeIds.append(edgeIdsTemp)
            curveMeshEdge = mc.createNode('curveFromMeshEdge', name=defSurface + '_edge' + edgeIds[2] + '_curve')
            mc.setAttr(curveMeshEdge + '.edgeIndex[0]', int(edgeIds[2]))
            mc.connectAttr(insertshapeplug[0], curveMeshEdge + '.inputMesh')
            pointOnCurve = mc.createNode('pointOnCurveInfo',
                                         name=defSurface + '_edge' + edgeIds[2] + '_vtx' + edgeIds[1] + '_curvePoint')
            vtxId = edgeIds[1]
            mc.addAttr(pointOnCurve, longName='targetVertex', attributeType='long')
            mc.setAttr(pointOnCurve + '.targetVertex', int(vtxId))
            mc.addAttr(pointOnCurve, longName='targetGeometry', dataType='string')
            mc.setAttr(pointOnCurve + '.targetGeometry', defSurface, type='string')
            mc.setAttr(pointOnCurve + '.turnOnPercentage', 1)
            mc.connectAttr(curveMeshEdge + '.outputCurve', pointOnCurve + '.inputCurve')

            # create a null for softmod parent transform, then create null's normal constraint
            nul = mc.createNode('transform', name=softmod[0] + '_nul')
            mc.setAttr(nul + '.inheritsTransform', 0)
            mc.setAttr(nul + '.v', keyable=0)
            mc.connectAttr(pointOnCurve + '.result.position', nul + '.translate')
            check1 = mc.xform(nul, q=1, ws=1, t=1)
            check2 = mc.xform(compSel, q=1, ws=1, t=1)
            if (not check1[0] == check2[0]) or (not check1[1] == check2[1]) or (not check1[2] == check2[2]):
                mc.setAttr(pointOnCurve + '.parameter', 1)
            constraint = mc.createNode('normalConstraint', name=nul + '_normalConstraint1', parent=nul)
            mc.setAttr(constraint + '.enableRestPosition', 0)
            mc.setAttr(constraint + '.aimVector', 0, 1, 0)
            mc.setAttr(constraint + '.upVector', 1, 0, 0)
            mc.setAttr(constraint + '.lockOutput', 1)
            mc.setAttr(constraint + '.io', 1)
            mc.connectAttr(constraint + '.constraintRotateX', nul + '.rx', f=1)
            mc.connectAttr(constraint + '.constraintRotateY', nul + '.ry', f=1)
            mc.connectAttr(constraint + '.constraintRotateZ', nul + '.rz', f=1)
            mc.connectAttr(insertshapeplug[0], constraint + '.target[0].targetGeometry', f=1)
            mc.connectAttr(pointOnCurve + '.tangent', constraint + '.worldUpVector', f=1)
            mc.connectAttr(nul + '.parentInverseMatrix', constraint + '.constraintParentInverseMatrix', f=1)
            mc.connectAttr(nul + '.t', constraint + '.constraintTranslate', f=1)
            mc.connectAttr(nul + '.rp', constraint + '.constraintRotatePivot', f=1)
            mc.connectAttr(nul + '.rpt', constraint + '.constraintRotateTranslate', f=1)
            mc.connectAttr(nul + '.ro', constraint + '.constraintRotateOrder', f=1)

            # parent softmod under null and connect bindPreMatrix
            offset = mc.createNode('transform', name=softmod[1] + '_offset', parent=nul)
            offsetWorldTx = mc.createNode('transform', name=softmod[1] + '_offset_worldtx', parent=nul)
            mc.setAttr(offsetWorldTx + '.io', 1)
            mc.setAttr(offset + '.v', keyable=0)
            mc.setAttr(offsetWorldTx + '.inheritsTransform', 0)
            mc.pointConstraint(offset, offsetWorldTx)
            mc.parent(softmod[1], offset, relative=1)
            mc.connectAttr(offsetWorldTx + '.t', softmod[0] + '.falloffCenter', force=1)
            mc.connectAttr(softmod[1] + '.pim', softmod[0] + '.bindPreMatrix', force=1)
            xCircleX = mc.circle(c=(0, 0, 0), normal=(1, 0, 0), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cx')
            mc.parent(softmod[1] + '_cxShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            xCircleY = mc.circle(c=(0, 0, 0), normal=(0, 1, 0), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cy')
            mc.parent(softmod[1] + '_cyShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            zCircleZ = mc.circle(c=(0, 0, 0), normal=(0, 0, 1), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cz')
            mc.parent(softmod[1] + '_czShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            mc.setAttr(softmod[0] + '.falloffCenterX', keyable=0)
            mc.setAttr(softmod[0] + '.falloffCenterY', keyable=0)
            mc.setAttr(softmod[0] + '.falloffCenterZ', keyable=0)

            # create circles for interactive falloff radius
            mc.rename(xCircleX[1], softmod[1] + '_cxRad')
            mc.rename(xCircleY[1], softmod[1] + '_cyRad')
            mc.rename(zCircleZ[1], softmod[1] + '_czRad')
            mc.delete(softmod[1] + '_cx')
            mc.delete(softmod[1] + '_cy')
            mc.delete(softmod[1] + '_cz')
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_cxRad.radius', f=1)
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_cyRad.radius', f=1)
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_czRad.radius', f=1)
            mc.setAttr(softmod[1] + '_cxShape.template', 1)
            mc.setAttr(softmod[1] + '_cyShape.template', 1)
            mc.setAttr(softmod[1] + '_czShape.template', 1)

            # locator for handle and quick select
            mc.spaceLocator(position=(0, 0, 0), name=softmod[0] + '_loc')
            mc.setAttr(softmod[0] + '_locShape.overrideEnabled', 1)
            mc.setAttr(softmod[0] + '_locShape.overrideColor', 17)
            mc.parent(softmod[0] + '_locShape', softmod[1], relative=1, shape=1)
            mc.delete(softmod[0] + '_loc')
            mc.addAttr(softmod[1], longName='______________', at='enum', en='_____')
            mc.setAttr(softmod[1] + '.______________', keyable=1)
            mc.addAttr(softmod[1], longName='LocColor', at='long', min=0, max=31, dv=17)
            mc.setAttr(softmod[1] + '.LocColor', keyable=1)
            mc.connectAttr(softmod[1] + '.LocColor', softmod[0] + '_locShape.overrideColor', f=1)
            mc.addAttr(softmod[1], longName='ScaleHandle', at='double', min=.1, max=121212, dv=1)
            mc.addAttr(softmod[1], longName='CircVis', at='bool', dv=1)
            mc.addAttr(softmod[1], longName='SMod_Env', at='double', min=0, max=1, dv=1)
            mc.addAttr(softmod[1], longName='FallOffRad', at='double', min=0, max=8888, dv=5)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleX', f=1)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleY', f=1)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleZ', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircVis', softmod[0] + 'Handle_cxShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircVis', softmod[0] + 'Handle_cyShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircVis', softmod[0] + 'Handle_czShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.SMod_Env', softmod[0] + '.envelope', f=1)
            mc.connectAttr(softmod[0] + 'Handle.FallOffRad', softmod[0] + '.falloffRadius', f=1)

            # hide unnecessary attrs on handle
            mc.setAttr(softmod[0] + 'Handle.ScaleHandle', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.CircVis', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.SMod_Env', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.FallOffRad', keyable=1)
            mc.setAttr(softmod[0] + '.falloffInX', keyable=0)
            mc.setAttr(softmod[0] + '.falloffInY', keyable=0)
            mc.setAttr(softmod[0] + '.falloffInZ', keyable=0)
            mc.setAttr(softmod[0] + '.falloffMasking', keyable=0)
            mc.setAttr(softmod[0] + '.falloffAroundSelection', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle.displayHandle', 0)
            mc.setAttr(softmod[0] + 'HandleShape.visibility', 0)
            mc.pickWalk(direction='up')

            return (softmod)

        if not surfpSelCheck == None:
            # create softmod and connect geo compensation matrix
            uvSel = mc.ls(sl=1, fl=1)
            softmod = mc.softMod(defSurface, name='joeMod0')
            insertshapeplug = mc.listConnections(softmod[0] + '.input[0].inputGeometry', plugs=1)
            for attr in ['.rp', '.rpt', '.sp', '.spt', '.origin']:
                mc.setAttr(softmod[1] + attr, 0, 0, 0)
            mc.setAttr(softmod[1] + '.v', keyable=0)
            mc.setAttr(softmod[1] + '.displayHandle', 1)
            mc.setAttr(softmod[0] + '.falloffAroundSelection', 0)
            nurbsSurfShape = mc.listRelatives(compSel, shapes=1)
            mc.connectAttr(defSurface + '.worldMatrix', softmod[0] + '.geomMatrix[0]', f=1)

            # get the u and v values from surface point selection
            compTokens = uvSel[0].split('[')
            compTokenNum = len(compTokens)

            compU = compTokens[(compTokenNum - 2)].replace(']', '')
            compV = compTokens[(compTokenNum - 1)].replace(']', '')
            compUi = float(compU)
            compVi = float(compV)

            # create a pointOnSurfaceInfo node for parent null attachment
            pos = mc.createNode('pointOnSurfaceInfo', name=softmod[0] + '_posInfo')
            mc.connectAttr(insertshapeplug[0], pos + '.inputSurface')
            mc.setAttr(softmod[0] + '_posInfo.parameterU', compUi)
            mc.setAttr(softmod[0] + '_posInfo.parameterV', compVi)

            # create a null for softmod parent transform, then create null's normal constraint
            nul = mc.createNode('transform', name=softmod[0] + '_nul')
            mc.setAttr(nul + '.inheritsTransform', 0)
            mc.setAttr(nul + '.v', keyable=0)
            mc.setAttr(nul + '.tx', keyable=0)
            mc.setAttr(nul + '.ty', keyable=0)
            mc.setAttr(nul + '.tz', keyable=0)
            mc.setAttr(nul + '.rx', keyable=0)
            mc.setAttr(nul + '.ry', keyable=0)
            mc.setAttr(nul + '.rz', keyable=0)
            mc.setAttr(nul + '.sx', keyable=0)
            mc.setAttr(nul + '.sy', keyable=0)
            mc.setAttr(nul + '.sz', keyable=0)

            # create an aim constraint to keep the parent null oriented to surface
            nameAC = mc.createNode('aimConstraint', p=nul, n=nul + '_AC')
            mc.setAttr(nameAC + '.offsetX', keyable=0)
            mc.setAttr(nameAC + '.offsetY', keyable=0)
            mc.setAttr(nameAC + '.offsetZ', keyable=0)
            mc.setAttr(nameAC + '.rotateX', keyable=0)
            mc.setAttr(nameAC + '.rotateY', keyable=0)
            mc.setAttr(nameAC + '.rotateZ', keyable=0)
            mc.setAttr(nameAC + '.scaleX', keyable=0)
            mc.setAttr(nameAC + '.scaleY', keyable=0)
            mc.setAttr(nameAC + '.scaleZ', keyable=0)
            mc.setAttr(nameAC + '.translateX', keyable=0)
            mc.setAttr(nameAC + '.translateY', keyable=0)
            mc.setAttr(nameAC + '.translateZ', keyable=0)
            mc.setAttr(nameAC + '.visibility', keyable=0)
            mc.connectAttr(pos + '.position', nul + '.translate', f=1)
            mc.connectAttr(pos + '.n', nameAC + '.tg[0].tt', f=1)
            mc.connectAttr(pos + '.tv', nameAC + '.wu', f=1)
            mc.connectAttr(nameAC + '.crx', nul + '.rx', f=1)
            mc.connectAttr(nameAC + '.cry', nul + '.ry', f=1)
            mc.connectAttr(nameAC + '.crz', nul + '.rz', f=1)

            # parent softmod under null and connect bindPreMatrix
            offset = mc.createNode('transform', name=softmod[1] + '_offset', parent=nul)
            offsetWorldTx = mc.createNode('transform', name=softmod[1] + '_offset_worldtx', parent=nul)
            mc.setAttr(offsetWorldTx + '.io', 1)
            mc.setAttr(offset + '.v', keyable=0)
            mc.setAttr(offsetWorldTx + '.inheritsTransform', 0)
            mc.pointConstraint(offset, offsetWorldTx)
            mc.parent(softmod[1], offset, relative=1)
            mc.connectAttr(offsetWorldTx + '.t', softmod[0] + '.falloffCenter', f=1)
            mc.connectAttr(softmod[1] + '.pim', softmod[0] + '.bindPreMatrix', f=1)

            # create circles for interactive falloff radius
            xCircleX = mc.circle(c=(0, 0, 0), normal=(1, 0, 0), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cx')
            mc.parent(softmod[1] + '_cxShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            yCircleY = mc.circle(c=(0, 0, 0), normal=(0, 1, 0), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cy')
            mc.parent(softmod[1] + '_cyShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            zCircleZ = mc.circle(c=(0, 0, 0), normal=(0, 0, 1), sweep=360, radius=1, degree=3, ut=0, tol=0.01,
                                 sections=8, ch=1, name=softmod[1] + '_cz')
            mc.parent(softmod[1] + '_czShape', softmod[0] + 'Handle_offset', relative=1, shape=1)
            mc.setAttr(softmod[0] + '.falloffCenterX', keyable=0)
            mc.setAttr(softmod[0] + '.falloffCenterY', keyable=0)
            mc.setAttr(softmod[0] + '.falloffCenterZ', keyable=0)

            # create circles for interactive falloff radius
            mc.rename(xCircleX[1], softmod[1] + '_cxRad')
            mc.rename(yCircleY[1], softmod[1] + '_cyRad')
            mc.rename(zCircleZ[1], softmod[1] + '_czRad')
            mc.delete(softmod[1] + '_cx')
            mc.delete(softmod[1] + '_cy')
            mc.delete(softmod[1] + '_cz')
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_cxRad.radius', f=1)
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_cyRad.radius', f=1)
            mc.connectAttr(softmod[0] + '.falloffRadius', softmod[1] + '_czRad.radius', f=1)
            mc.setAttr(softmod[1] + '_cxShape.template', 1)
            mc.setAttr(softmod[1] + '_cyShape.template', 1)
            mc.setAttr(softmod[1] + '_czShape.template', 1)

            # locator for handle and quick select
            mc.spaceLocator(position=(0, 0, 0), name=softmod[0] + '_loc')
            mc.setAttr(softmod[0] + '_locShape.overrideEnabled', 1)
            mc.setAttr(softmod[0] + '_locShape.overrideColor', 17)
            mc.parent(softmod[0] + '_locShape', softmod[1], relative=1, shape=1)
            mc.delete(softmod[0] + '_loc')
            mc.addAttr(softmod[1], longName='______________', at='enum', en='_____')
            mc.setAttr(softmod[1] + '.______________', keyable=1)
            mc.addAttr(softmod[1], longName='LocColor', at='long', min=0, max=31, dv=17)
            mc.setAttr(softmod[1] + '.LocColor', keyable=1)
            mc.connectAttr(softmod[1] + '.LocColor', softmod[0] + '_locShape.overrideColor', f=1)
            mc.addAttr(softmod[1], longName='ScaleHandle', at='double', min=.1, max=121212, dv=1)
            mc.addAttr(softmod[1], longName='CircleVis', at='bool', dv=1)
            mc.addAttr(softmod[1], longName='Envelope', at='double', min=0, max=1, dv=1)
            mc.addAttr(softmod[1], longName='FalloffRadius', at='double', min=0, max=8888, dv=5)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleX', f=1)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleY', f=1)
            mc.connectAttr(softmod[0] + 'Handle.ScaleHandle', softmod[0] + '_locShape.localScaleZ', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircleVis', softmod[0] + 'Handle_cxShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircleVis', softmod[0] + 'Handle_cyShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.CircleVis', softmod[0] + 'Handle_czShape.visibility', f=1)
            mc.connectAttr(softmod[0] + 'Handle.Envelope', softmod[0] + '.envelope', f=1)
            mc.connectAttr(softmod[0] + 'Handle.FalloffRadius', softmod[0] + '.falloffRadius', f=1)

            # hide unnecessary attrs on handle and aim constraint
            mc.setAttr(softmod[0] + 'Handle.ScaleHandle', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.CircleVis', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.Envelope', keyable=1)
            mc.setAttr(softmod[0] + 'Handle.FalloffRadius', keyable=1)
            mc.setAttr(softmod[0] + '.falloffInX', keyable=0)
            mc.setAttr(softmod[0] + '.falloffInY', keyable=0)
            mc.setAttr(softmod[0] + '.falloffInZ', keyable=0)
            mc.setAttr(softmod[0] + '.falloffMasking', keyable=0)
            mc.setAttr(softmod[0] + '.falloffAroundSelection', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cxRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_cyRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.centerZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.degree', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalX', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalY', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.normalZ', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.radius', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.sections', keyable=0)
            mc.setAttr(softmod[0] + 'Handle_czRad.sweep', keyable=0)
            mc.setAttr(softmod[0] + 'Handle.displayHandle', 0)
            mc.setAttr(softmod[0] + 'HandleShape.visibility', 0)
            mc.setAttr(softmod[0] + '_locShape.localPositionX', channelBox=0)
            mc.setAttr(softmod[0] + '_locShape.localPositionY', channelBox=0)
            mc.setAttr(softmod[0] + '_locShape.localPositionZ', channelBox=0)
            mc.setAttr(softmod[0] + '_locShape.localScaleX', channelBox=0)
            mc.setAttr(softmod[0] + '_locShape.localScaleY', channelBox=0)
            mc.setAttr(softmod[0] + '_locShape.localScaleZ', channelBox=0)
            mc.pickWalk(direction='up')
            return (softmod)
        else:
            mc.error(
                'for cfxSoftMod, select one poly vertex, one surface point, or one curve point only - then click the button')
            return ([])

    def joeAddSets(self):
        softModHandleName = mc.ls(sl=1, o=1)
        if not any(softModHandleName):
            mc.error('Select a softModHandle first, then toggle select all geo to add to its set')

        if mc.nodeType(softModHandleName[0] + 'Shape') == 'softModHandle':
            smodTokens = softModHandleName[0].split('H')
            smodTokenNum = len(smodTokens)
            smodSet = smodTokens[0] + 'Set'
            selectedSurfs = mc.ls(sl=1, dag=1, type=('nurbsSurface', 'nurbsCurve', 'mesh'))
            if not selectedSurfs == []:
                mc.sets(selectedSurfs, include=smodSet)
            print('new softMod created, selected objects added to set:    ' + smodSet + '     -     BOOM!!!')
        else:
            mc.error('Select a softModHandle first, then toggle select all geo to add to its set')

    def cfx_softMod(self):
        broadSelection = mc.ls(sl=1)

        if (len(broadSelection)):
            print(broadSelection)
            # integrating addSets functionality at softMod creation time . . .

            self.joeMod(broadSelection[0])
            softmodName = mc.ls(sl=1)

            mc.select(broadSelection, toggle=1)
            mc.select(broadSelection[0], deselect=1)

            self.joeAddSets()
            mc.select(softmodName[0])
        else:
            mc.error(
                'for cfxSoftMod, select one poly vertex, one surface point, or one curve point only - then click the button')

