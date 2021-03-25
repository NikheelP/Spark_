
from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
import random
from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.Help import shader
for each in [sample_color_variable, sample_widget_template, style_sheet_template, shader]:
    reload(each)

from spark.widget.sample.sample_color_variable import COLOR_VARIABLE
from spark.department.Help.shader import SHADER

class RANDOMSHADER:

    def __init__(self):
        self.sample_color_variable = COLOR_VARIABLE()
        self.shader_class = SHADER()

    def random_shader(self):
        '''
        assign random shader to the selected object
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            for each in sel_obj:
                shader_name = self.shader_class.create_shader()

                #get color and change
                cmds.setAttr(shader_name + ".color", random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), type='double3')
                cmds.select(each)
                cmds.hyperShade(assign=shader_name)





