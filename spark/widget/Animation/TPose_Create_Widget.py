

from spark.widget.import_module import *
# from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.widget import widget_help
for each in [sample_color_variable, sample_widget_template, style_sheet_template, widget_help]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET


class TPOSECREATE(SAMPLE_WIDGET):
    def __init__(self, title='Smart TPose', height=500, width=350):
        super(TPOSECREATE, self).__init__(title=title, height=height, width=width)

        self.iniUI()

    def iniUI(self):
        '''

        :return:
        '''

        main_widget = self.get_main_widget()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=main_widget)

        #FRAME WIDGET
        verticalLayout.addWidget(self.frame_widget())

        #LIST OF THE CONTROL WIDGET
        verticalLayout.addWidget(self.list_controller_widget())

        #CREATE PRE AND POST TPOSE WIDGET
        verticalLayout.addWidget(self.pre_pose_TPose_def())


    def frame_widget(self):
        '''

        :return:
        '''

        widget = self.sample_widget_template.widget_def()

        gridLayout = self.sample_widget_template.grid_layout(parent_self=widget)

        new_value = 0
        vertical_val = 0

        #FRAME LABEL
        frame_label = self.sample_widget_template.label(set_text='Frame')
        gridLayout.addWidget(frame_label, vertical_val, new_value, 1, 1)
        new_value += 1

        #BUFFER FRAME
        self.buffer_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Buffer Frame')
        gridLayout.addWidget(self.buffer_frame_lineedit, vertical_val, new_value, 1, 2)
        vertical_val += 1
        new_value = 0

        #TPOSE FRAME
        self.tpose_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='T-Pose Frame')
        gridLayout.addWidget(self.tpose_frame_lineedit, vertical_val, new_value, 2, 1)
        new_value += 1

        #ANIMATION REST FRAME
        self.animation_rest_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Animation Rest Frame')
        gridLayout.addWidget(self.animation_rest_frame_lineedit, vertical_val, new_value, 3, 1)
        new_value += 1

        #ANIMATION START FRAME
        self.animation_start_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Animation Start Frame')
        gridLayout.addWidget(self.animation_start_frame_lineedit, vertical_val, new_value, 4, 1)
        new_value += 1

        return widget

    def list_controller_widget(self):
        '''

        :return:
        '''

        widget = self.sample_widget_template.widget_def()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=widget)

        self.assets_comboBox = self.sample_widget_template.comboBox()
        vertical_layout.addWidget(self.assets_comboBox)

        self.controller_listWidget = self.sample_widget_template.list_widget()
        vertical_layout.addWidget(self.controller_listWidget)

        return widget

    def pre_pose_TPose_def(self):
        '''

        :return:
        '''
        widget = self.sample_widget_template.widget_def()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=widget)

        self.pre_tpose_button = self.sample_widget_template.pushButton(set_text='Pre TPose')
        verticalLayout.addWidget(self.pre_tpose_button)

        self.post_tpose_button = self.sample_widget_template.pushButton(set_text='Pose TPose')
        verticalLayout.addWidget(self.post_tpose_button)

        return widget

    def get_list_controller(self):
        '''

        :return:
        '''
        pass








'''
from spark.widget.Animation import TPose_Create_Widget
reload(TPose_Create_Widget)
from spark.widget.Animation.TPose_Create_Widget import TPOSECREATE
tpose = TPOSECREATE()
tpose.show()
'''