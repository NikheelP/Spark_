from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template

for each in [sample_color_variable, sample_widget_template, style_sheet_template]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.style_sheet_template import STYLE_SHEET_TEMPLATE

class CFX(SAMPLE_WIDGET):
    def __init__(self, title='CFX'):
        super(CFX, self).__init__(title=title)
        self.sample_widget_template = SAMPLE_WIDGET_TEMPLATE()

        self.ui()

    def ui(self):
        #GET THE DEFAULT LAYOUT
        default_main_widget = self.get_main_widget()

        self.tab_widget(default_main_widget)

    def tab_widget(self, widget):
        #VERTICAL LAYOUT
        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #TAB WIDGET
        tab_widget = self.sample_widget_template.tab_widget(parent_self=widget)
        vertical_layout.addWidget(tab_widget)

        #CLOTH TAB
        cloth_name = 'Cloth'
        cloth_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        tab_widget.addTab(cloth_tab, cloth_name.upper())

        #HAIR TAB
        hair_name = 'Hair'
        hair_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        tab_widget.addTab(hair_tab, hair_name.upper())

        #FUR TAB
        fur_name = 'Fur'
        fur_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        tab_widget.addTab(fur_tab, fur_name.upper())

        #COMMON TAB
        common_name = 'Common'
        common_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        tab_widget.addTab(common_tab, common_name.upper())

        #USER TAB
        user_name = 'User Name'
        user_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        tab_widget.addTab(user_tab, user_name.upper())











