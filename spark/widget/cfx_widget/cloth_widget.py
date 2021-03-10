from spark.widget.import_module import *

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
import os
import maya.cmds as cmds
import maya.mel as mel

for each in [sample_color_variable, sample_widget_template, style_sheet_template]:
    reload(each)

from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE

class CLOTH_WIDGET():
    def __init__(self):
        self.sample_widget_template = SAMPLE_WIDGET_TEMPLATE()

    def ui(self, widget):
        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #SEARCH WIDGET
        search_widget = self.search_widget_ui()
        vertical_layout.addWidget(search_widget)

        #BUTTON WIDGET
        button_widget = self.button_def()
        vertical_layout.addWidget(button_widget)
        pass

    def search_widget_ui(self):
        search_widget = self.sample_widget_template.widget_def(min_size=[0, 26], max_size=[self.sample_widget_template.max_size, 26])

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=search_widget)

        self.filter_linedit = self.sample_widget_template.line_edit(set_PlaceholderText='Filter with Name')
        self.filter_linedit.textChanged.connect(self.filter_linedit_def)

        vertical_layout.addWidget(self.filter_linedit)

        return search_widget

    def button_def(self):
        main_widget = self.sample_widget_template.widget_def()

        main_widget_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=main_widget)

        scroll_area = self.sample_widget_template.scrollArea(parent_self=main_widget)

        scroll_widget = self.sample_widget_template.widget_def()
        scroll_area.setWidget(scroll_widget)
        main_widget_vertical_layout.addWidget(scroll_area)


        #button_widget = self.sample_widget_template.widget_def()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=scroll_widget, set_spacing=3)

        button_size = 150
        a = 0
        new_value = 0
        vertical_val = 0

        #SMOOTH
        smooth_text = 'SmoothNode'
        smooth_button = self.sample_widget_template.pushButton(set_text=smooth_text,
                                                               min_size=[button_size, button_size])
        smooth_button.clicked.connect(self.smooth_button_def)
        grid_layout.addWidget(smooth_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # CORRECTIVE BLENDSHAPE
        corrective_text = 'CorrectiveBlendshape'
        corrective_button = self.sample_widget_template.pushButton(set_text=corrective_text,
                                                                   min_size=[button_size, button_size])
        corrective_button.clicked.connect(self.corrective_button_def)
        grid_layout.addWidget(corrective_button, vertical_val, new_value, 1, 1)
        new_value += 1

        #NORMAL PUSH
        normal_push_text = 'normalPush'
        normal_push_button = self.sample_widget_template.pushButton(set_text=normal_push_text,
                                                                   min_size=[button_size, button_size])
        normal_push_button.clicked.connect(self.normal_push_def)
        grid_layout.addWidget(normal_push_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # SOFT MOD



        #CLUSTER TWEAK



        #WRAP
        #NOISE DEFORMER

        #MESH COLLUTION


        #CFX TWEAK LIKE SONY

        #RigFx


        #
        vertical_val +=1
        grid_layout.addItem(self.sample_widget_template.spaceItem(), vertical_val,new_value, 1, 1)


        return main_widget

    def filter_linedit_def(self):
        '''

        :return:
        '''

        text = self.filter_linedit.text()

        print('this is the text: ' , text)

    def smooth_button_def(self):
        from spark.CFX import deformer_create
        deformer_create.smooth_deformer()

    def corrective_button_def(self):
        from spark.CFX import deformer_create
        reload(deformer_create)
        deformer_create.corrective_blendshape()

    def normal_push_def(self):
        from spark.CFX import deformer_create
        reload(deformer_create)
        deformer_create.normalPush()









