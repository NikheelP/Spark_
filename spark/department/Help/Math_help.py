import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

class MATHUTIL_HELP:

    def __init__(self):
        pass

    def isEqual(self, x, y,tolerance=0.00001):

        return abs(x-y) < tolerance

    def mag(self, vector=(0,0,0)):

        return OpenMaya.MVector(vector[0],vector[1],vector[2]).length()

    def normalizeVector(self, vector=(0,0,0)):

        normal = OpenMaya.MVector(vector[0],vector[1],vector[2]).normal()
        return (normal.x,normal.y,normal.z)

    def dotProduct(self, vector1=(0.0,0.0,0.0),vector2=(0.0,0.0,0.0)):

        vec1 = OpenMaya.MVector(vector1[0],vector1[1],vector1[2])
        vec2 = OpenMaya.MVector(vector2[0],vector2[1],vector2[2])
        return vec1 * vec2

    def distanceBetween(self, point1=[0.0,0.0,0.0],point2=[0.0,0.0,0.0]):

        pnt1 = OpenMaya.MPoint(point1[0],point1[1],point1[2],1.0)
        pnt2 = OpenMaya.MPoint(point2[0],point2[1],point2[2],1.0)
        return OpenMaya.MVector(pnt1-pnt2).length()

    def offsetVector(self, point1=(0.0,0.0,0.0),point2=(0.0,0.0,0.0)):

        pnt1 = OpenMaya.MPoint(point1[0],point1[1],point1[2],1.0)
        pnt2 = OpenMaya.MPoint(point2[0],point2[1],point2[2],1.0)
        vec = pnt2 - pnt1
        return (vec.x,vec.y,vec.z)

    def crossProduct(self, vector1=(0.0,0.0,0.0),vector2=(0.0,0.0,0.0)):

        vec1 = OpenMaya.MVector(vector1[0],vector1[1],vector1[2])
        vec2 = OpenMaya.MVector(vector2[0],vector2[1],vector2[2])
        crossProduct = vec1 ^ vec2
        return (crossProduct.x,crossProduct.y,crossProduct.z)

    def averagePosition(self, pos1=(0.0,0.0,0.0),pos2=(0.0,0.0,0.0),weight=0.5):

        return (pos1[0]+((pos2[0]-pos1[0])*weight),pos1[1]+((pos2[1]-pos1[1])*weight),pos1[2]+((pos2[2]-pos1[2])*weight))

    def closestPointOnLine(self, pt, lineA,lineB,clampSegment=False):

        # Get Vector Offsets
        ptOffset = self.offsetVector(lineA,pt)
        lineOffset = self.offsetVector(lineA,lineB)

        # Vector Comparison
        dot = self.dotProduct(ptOffset,lineOffset)

        # Clamp Segment
        if clampSegment:
            if dot < 0.0: return lineA
            if dot > 1.0: return lineB

        # Project Vector
        return [lineA[0]+(lineOffset[0]*dot),lineA[1]+(lineOffset[1]*dot),lineA[2]+(lineOffset[2]*dot)]

    def smoothStep(self, value,rangeStart=0.0,rangeEnd=1.0,smooth=1.0):

        # Get range
        rangeVal = rangeEnd - rangeStart
        # Normalize value
        nValue = value / rangeVal
        # Get smooth value
        sValue = pow(nValue,2) * (3-(nValue*2))
        sValue = nValue + ((sValue-nValue)*smooth)
        value = rangeStart + (rangeVal * sValue)
        # Return result
        return value

    def distributeValue(self, samples, spacing=1.0, rangeStart=0.0, rangeEnd=1.0):

        # Get Value Range
        vList = [rangeStart]
        vDist = abs(rangeEnd - rangeStart)
        unit = 1.0

        # Find the Unit Distance
        factor = 1.0
        for i in range(samples-2):
            unit += factor * spacing
            factor *= spacing
        unit = vDist/unit
        totalUnit = unit

        # Build Sample List
        for i in range(samples-2):
            multFactor = totalUnit/vDist
            vList.append(rangeStart-((rangeStart - rangeEnd) * multFactor))
            unit *= spacing
            totalUnit += unit

        # Append Final Sample
        vList.append(rangeEnd)

        # Return Result
        return vList

    def inverseDistanceWeight1D(self, valueArray, sampleValue, valueDomain=(0,1), cycleValue=False):

        # Initialize method varialbles
        distArray = []
        totalInvDist = 0.0

        # Initialize weightArray
        wtArray = []

        # Calculate inverse distance weight
        for v in range(len(valueArray)):
            # Calculate distance
            dist = abs(sampleValue - valueArray[v])

            # Check cycle value
            if cycleValue:
                valueDomainLen = valueDomain[1]-valueDomain[0]
                fCycDist = abs(sampleValue - (valueArray[v] + valueDomainLen))
                rCycDist = abs(sampleValue - (valueArray[v] - valueDomainLen))
                if fCycDist < dist: dist = fCycDist
                if rCycDist < dist: dist = rCycDist

            # Check zero distance
            if dist < 0.00001: dist = 0.00001

            # Append distance
            distArray.append(dist)
            totalInvDist += 1.0/dist

        # Normalize value weights
        wtArray = [(1.0/d)/totalInvDist for d in distArray]

        # Return result
        return wtArray

    def inverseDistanceWeight3D(self, pointArray,samplePoint):
        # Initialize Method Variables
        distArray = []
        totalInvDist = 0.0

        # Initialize weightArray
        wtArray = []

        # Calculate inverse distance weight
        for i in range(len(pointArray)):
            # Calculate Distance
            dist = self.distanceBetween(samplePoint, pointArray[i])

            # Check Zero Distance
            if dist < 0.00001: dist = 0.00001

            # Append distance
            distArray.append(dist)
            totalInvDist += 1.0/dist

        # Normalize Value Weights
        wtArray = [(1.0/d)/totalInvDist for d in distArray]

        # Return Result
        return wtArray
