
import maya.cmds as cmds




class SHADER:
    def __init__(self):
        pass

    def assign_shader(self, obj, sg_name=''):
        '''
        assign the shader with the list of th object
        :param obj_list: list of the object
        :param sg_name: specify the sg name
        :return:
        '''

        if sg_name != '':
            if cmds.objExists(obj):
                cmds.select(obj)
                cmds.sets(sg_name, e=True, forceElement=True)
                return True

    def create_shader(self, shader_type='lambert', name=''):
        '''
        create a shader as specified
        :param shader_type: specify the shader name Ex: lambert, blinn, phong, phongE
        :param name: specify the shader name
        :return:
        '''

        laber_shader_name = cmds.shadingNode(shader_type, asShader=True)
        if name == '':
            shader_name = shader_type + '_' + str(len(cmds.ls(type='lambert')))
            cmds.rename(laber_shader_name, shader_name)
        else:
            shader_name = name
            cmds.rename(laber_shader_name, shader_name)

        return shader_name

    def getSG(self, geo):
        '''
        Get shading group assigned to specified geometry.
        @param geo: Geometry to get shading group from
        @type geo: str
        '''
        # Get Face Sets
        sets = cmds.listSets(extendToShape=True, type=1, object=geo) or []

        # Return Result
        return list(set(sets))


