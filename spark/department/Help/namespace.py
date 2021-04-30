
import maya.cmds as cmds

class NAMESPACE:

    def __init__(self):

        pass

    def getNS(self, obj, topOnly=True):
        '''
        Get the namespace of the specified object
        @param obj: The object to get namespace from
        @type obj: str
        @param topOnly: Return the top level namespace only.
        @type topOnly: bool
        '''
        # Check Object
        if not cmds.objExists(obj):
            raise Exception('Object "' + obj + '" does not exist!')

        # Check namespace
        NS = ''
        if not obj.count(':'): return NS

        # Get Namespace
        if topOnly:
            NS = obj.split(':')[0]
        else:
            NS = obj.replace(':' + obj.split(':')[-1], '')

        # Return namespace
        return NS

    def deleteNS(self, NS):
        '''
        Delete the specified namespace
        @param NS: The namespace to delete
        @type NS: str
        '''
        # Check namespace
        if not NS:
            raise Exception('Invalid namespace specified!')
        if not cmds.namespace(ex=NS):
            raise Exception('Namespace "' + NS + '" does not exist!')

        # Print Message
        print('Deleting Namespace: ' + NS)

        # Delete namespace
        cmds.namespace(mv=[NS, ':'], f=True)
        cmds.namespace(rm=NS)