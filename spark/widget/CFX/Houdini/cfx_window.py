
from spark.widget.import_module import *
import os
import hou
from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.widget.sample import sample_houdini_widget
from spark.widget.CFX.Houdini import cloth_widget

for each in [sample_color_variable, sample_widget_template, style_sheet_template, sample_houdini_widget, cloth_widget]:
    reload(each)



from spark.widget.sample.sample_houdini_widget import SAMPLE_WIDGET
from spark.widget.CFX.Houdini.cloth_widget import CLOTH_WIDGET


#os.path.abspath(smoothNode.__file__).replace('\\', '/')

class CFX(SAMPLE_WIDGET):
    def __init__(self, title='CFX'):
        super(CFX, self).__init__(title=title)
        #LOAD ALL THE DIGITAL ASSTS
        self.load_all_otls()

        self.cloth_widget_class = CLOTH_WIDGET()


        self.ui()


    def ui(self):
        # GET THE DEFAULT LAYOUT
        default_main_widget = self.get_main_widget()

        self.tab_widget(default_main_widget)

    def tab_widget(self, widget):
        # VERTICAL LAYOUT
        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=widget)

        # TAB WIDGET
        tab_widget = self.sample_widget_template.tab_widget(parent_self=widget)
        vertical_layout.addWidget(tab_widget)

        # CLOTH TAB
        cloth_name = 'Cloth'
        cloth_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.cloth_widget_class.ui(cloth_tab)
        tab_widget.addTab(cloth_tab, cloth_name.upper())

        # HAIR TAB
        hair_name = 'Hair'
        hair_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        #self.hair_widget_class.ui(hair_tab)
        tab_widget.addTab(hair_tab, hair_name.upper())

        # FUR TAB
        fur_name = 'Fur'
        fur_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        #self.fur_widget_class.ui(fur_tab)
        tab_widget.addTab(fur_tab, fur_name.upper())

        # COMMON TAB
        common_name = 'Common'
        common_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        #self.common_widget_class.ui(common_tab)
        tab_widget.addTab(common_tab, common_name.upper())

        # USER TAB
        user_name = 'User Name'
        user_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        #self.user_widget_class.ui(user_tab)
        tab_widget.addTab(user_tab, user_name.upper())

    def load_all_otls(self):
        from spark.department.CFX.Houdini import otls
        dirname = os.path.dirname(otls.__file__).replace('\\', '/')
        dirfiles = os.listdir(dirname)
        for each_file in dirfiles:
            full_path = os.path.join(dirname, each_file)
            if os.path.isdir(full_path):
                otl_file = dirname + '/' + each_file + '/' + each_file + '.hdanc'
                hou.hda.installFile(otl_file)



cfx_window = CFX()

'''
new_path = 'C:/Users/Admin/Desktop/Nikheel/Spark_Project/Spark_'
import sys
sys.path.append(new_path)

from spark.widget.CFX.Houdini import cfx_window
reload(cfx_window)



'''