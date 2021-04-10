import os

import pymel.core as pml


class RIVET:

    def __init__(self):
        pass


    def rivet(self, name="rivet"):
        """
        Create a rivet attached to the selected edges or nurbs surface point

        :param name: string name for new rivet
        :return: pyNode of new locator created
        """
        if pml.filterExpand(sm=32):
            parts = pml.filterExpand(sm=32)

            if len(parts) != 2:
                print("Two edges need to be selected")
                return None

            parts = [pml.PyNode(part) for part in parts]

            cfm1 = pml.createNode("curveFromMeshEdge", n="{0}_crvMshEdge1".format(name))
            cfm1.isHistoricallyInteresting.set(1)
            cfm1.edgeIndex[0].set(parts[0].index())

            cfm2 = pml.createNode("curveFromMeshEdge", n="{0}_crvMshEdge2".format(name))
            cfm2.isHistoricallyInteresting.set(1)
            cfm2.edgeIndex[0].set(parts[1].index())

            lft = pml.createNode("loft", n="{0}_loft".format(name))
            lft.inputCurve.set(s=2)
            lft.uniform.set(1)
            lft.reverseSurfaceNormals.set(1)

            posi = pml.createNode("pointOnSurfaceInfo", n="{0}_posi".format(name))
            posi.turnOnPercentage.set(1)
            posi.parameterU.set(0.5)
            posi.parameterV.set(0.5)

            pml.connectAttr(lft.outputSurface, posi.inputSurface)
            pml.connectAttr(cfm1.outputCurve, lft.inputCurve[0])
            pml.connectAttr(cfm2.outputCurve, lft.inputCurve[1])
            pml.connectAttr(parts[0].node().worldMesh, cfm1.inputMesh)
            pml.connectAttr(parts[0].node().worldMesh, cfm2.inputMesh)

        elif pml.filterExpand(sm=41):
            parts = pml.filterExpand(sm=41)
            if not parts:
                print("Please select at least 1 surface point for a nurbs object")
                return None

                # TODO - Remove the string splitting and find a better way to get the UV from the pyNode
            uvVals = [float(item.replace(']', '')) for item in parts.split('[')[1:]]
            parts = [pml.PyNode(part) for part in parts]

            posi = pml.createNode("pointOnSurfaceInfo", n="{0}_posi".format(name))
            posi.turnOnPercentage.set(0)
            posi.parameterU.set(uvVals[0])
            posi.parameterV.set(uvVals[1])
            pml.connectAttr(parts[0].node().worldSpace, posi.inputSurface)

        else:
            os.error("Select either 2 edges for a mesh or 1 surface point for a nurbs object")
            return None

        locTrans = pml.createNode("transform", n=name)
        locShape = pml.createNode("locator", n="{0}Shape".format(locTrans.name()), p=locTrans)

        aimCon = pml.createNode("aimConstraint", p=locTrans, n="{0}_aimConst".format(locTrans.name()))
        aimCon.tg[0].tw.set(1)
        aimCon.aimVector.set((0, 1, 0))
        aimCon.upVector.set((0, 0, 1))
        for attr in ["v", "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]:
            aimCon.setAttr(attr, k=0)

        pml.connectAttr(posi.position, locTrans.translate)
        pml.connectAttr(posi.normal, aimCon.tg[0].targetTranslate)
        pml.connectAttr(posi.tangentV, aimCon.worldUpVector)
        pml.connectAttr(aimCon.constraintRotateX, locTrans.rotateX)
        pml.connectAttr(aimCon.constraintRotateY, locTrans.rotateY)
        pml.connectAttr(aimCon.constraintRotateZ, locTrans.rotateZ)

        # Add custom attributes to manipulate the locatorShape
        locShape.overrideEnabled.set(1)
        locShape.overrideColor.set(30)
        pml.addAttr(locTrans, longName='______________', at='enum', en='_____', k=1)
        pml.addAttr(locTrans, longName='locColor', at='long', min=0, max=31, dv=30, k=1)
        pml.connectAttr(locTrans.locColor, locShape.overrideColor, f=1)
        pml.addAttr(locTrans, longName='scaleHandle', at='double', min=.1, max=121212, dv=1, k=1)
        pml.addAttr(locTrans, longName='handleVis', at='bool', dv=1, k=1)
        pml.connectAttr(locTrans.scaleHandle, locShape.localScaleX, f=1)
        pml.connectAttr(locTrans.scaleHandle, locShape.localScaleY, f=1)
        pml.connectAttr(locTrans.scaleHandle, locShape.localScaleZ, f=1)
        pml.connectAttr(locTrans.handleVis, locShape.visibility, f=1)

        return locTrans

    def create(self, name='rivet'):
        """
        Main create function to build a rivet

        :param name: string name for new rivet to create
        :return: new locator created
        """
        locTrans = self.rivet(name)
        if locTrans:
            pml.select(locTrans, r=1)

        return locTrans

