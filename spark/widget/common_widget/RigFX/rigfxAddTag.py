from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
from functools import partial
import string

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.common import rename
from spark.department.CFX.cfx_tools.rigFX import rigFX_
from spark.department.common import Outliner
from spark.widget import widget_help
for each in [sample_color_variable, sample_widget_template, style_sheet_template, rename, rigFX_, widget_help, Outliner]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.sample_color_variable import COLOR_VARIABLE
from spark.department.CFX.cfx_tools.rigFX.rigFX_ import RIGFX
from spark.widget.widget_help import WIDGET_HELP
from spark.department.common.Outliner import outlinerWidget

from spark.widget.common_widget import rigFX_icon
rigFxIconPath = os.path.abspath(rigFX_icon.__file__).replace('\\', '/')
last_obj = rigFxIconPath.split('/')[-1]
rigfxIconPath_ = rigFxIconPath.split(last_obj)[0]


class RIGFXADDTAG(SAMPLE_WIDGET):
    def __init__(self, title='RigFxAddTag',height=150, width=300):
        super(RIGFXADDTAG, self).__init__(title=title, height=height, width=width)
        self.rigfx_class= RIGFX()

        self.initUI()

    def initUI(self):
        main_widget = self.get_main_widget()

        grid_Layout = self.sample_widget_template.grid_layout(parent_self=main_widget, set_spacing=5)

        new_value = 0
        vertical_val = 0

        # ADD COMBOBOX
        rigFx_tag_text = 'RigFxTag'
        addItems = [self.rigfx_class.rigFx_type, self.rigfx_class.input_type, self.rigfx_class.inputcloth_type, self.rigfx_class.restcloth_type, self.rigfx_class.cloth_type,
                    self.rigfx_class.techanim_type, self.rigfx_class.techanim_final_type, self.rigfx_class.sim_type, self.rigfx_class.techanim_cloth_type, self.rigfx_class.techanim_cloth_final_type,
                    self.rigfx_class.hairSystem_type, self.rigfx_class.final_type, self.rigfx_class.version_type, self.rigfx_class.collution_nRigit, self.rigfx_class.component_type, self.rigfx_class.component_to_component_type,
                    self.rigfx_class.forcefield_type, self.rigfx_class.pointtosurface_type, self.rigfx_class.pointtosurface_nRigit, self.rigfx_class.slidetosurface_type, self.rigfx_class.slidetosurface_nRigit,
                    self.rigfx_class.tearablesurface_type, self.rigfx_class.transoformconstraint_type, self.rigfx_class.airfield_type, self.rigfx_class.dragfield_type, self.rigfx_class.gravityfield_type,
                    self.rigfx_class.newtonfield_type, self.rigfx_class.radiusfield_type, self.rigfx_class.turbulancefield_type, self.rigfx_class.uniformfield_type, self.rigfx_class.vortexfield_type,
                    self.rigfx_class.volumefield_type, self.rigfx_class.volumecurve_type]
        rigFx_tag_comboBox = self.sample_widget_template.comboBox( addItems=addItems)
        grid_Layout.addWidget(rigFx_tag_comboBox, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        rigFx_tag_create_text = 'RigFxTag Create'
        rigFx_tag_create_comboBox = self.sample_widget_template.pushButton(set_text=rigFx_tag_create_text, min_size=[60,30])
        grid_Layout.addWidget(rigFx_tag_create_comboBox, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1


        grid_Layout.addItem(self.sample_widget_template.spaceItem(), vertical_val, new_value, 1, 1)







