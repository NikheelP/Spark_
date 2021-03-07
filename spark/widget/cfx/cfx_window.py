from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.widget.cfx import cloth_widget, hair_widget, fur_widget, common_widget, user_widget

for each in [sample_color_variable, sample_widget_template, style_sheet_template, cloth_widget, hair_widget, fur_widget, common_widget,
             user_widget]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.style_sheet_template import STYLE_SHEET_TEMPLATE
from spark.widget.cfx.cloth_widget import CLOTH_WIDGET
from spark.widget.cfx.hair_widget import HAIR_WIDGET
from spark.widget.cfx.fur_widget import FUR_WIDGET
from spark.widget.cfx.common_widget import COMMON_WIDGET
from spark.widget.cfx.user_widget import USER_WIDGET

class CFX(SAMPLE_WIDGET):
    def __init__(self, title='CFX'):
        super(CFX, self).__init__(title=title)
        self.sample_widget_template = SAMPLE_WIDGET_TEMPLATE()
        self.cloth_widget_class = CLOTH_WIDGET()
        self.hair_widget_class = HAIR_WIDGET()
        self.fur_widget_class = FUR_WIDGET()
        self.common_widget_class = COMMON_WIDGET()
        self.user_widget_class = USER_WIDGET()

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
        self.cloth_widget_class.ui(cloth_tab)
        tab_widget.addTab(cloth_tab, cloth_name.upper())

        #HAIR TAB
        hair_name = 'Hair'
        hair_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.hair_widget_class.ui(hair_tab)
        tab_widget.addTab(hair_tab, hair_name.upper())

        #FUR TAB
        fur_name = 'Fur'
        fur_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.fur_widget_class.ui(fur_tab)
        tab_widget.addTab(fur_tab, fur_name.upper())

        #COMMON TAB
        common_name = 'Common'
        common_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.common_widget_class.ui(common_tab)
        tab_widget.addTab(common_tab, common_name.upper())

        #USER TAB
        user_name = 'User Name'
        user_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.user_widget_class.ui(user_tab)
        tab_widget.addTab(user_tab, user_name.upper())











