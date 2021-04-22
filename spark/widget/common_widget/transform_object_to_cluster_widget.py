from spark.widget.import_module import *
# from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
from functools import partial

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.common import rename
from spark.widget import widget_help
from spark.department.Rigging.rigging_tool import transform_object_to_cluster
for each in [sample_color_variable, sample_widget_template, style_sheet_template, rename, widget_help, transform_object_to_cluster]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.sample_color_variable import COLOR_VARIABLE
from spark.department.common.rename import RENAME
from spark.widget.widget_help import WIDGET_HELP
from spark.department.Rigging.rigging_tool.transform_object_to_cluster import TRANSFORM_OBJECT_TO_CLUSTER


class TRANSFORM_OBJECT_TO_CLUSTER_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='Transfom Object to Cluster', height=600, width=350):
        super(TRANSFORM_OBJECT_TO_CLUSTER_WIDGET, self).__init__(title=title, height=height, width=width)
        self.transform_object_to_cluster_class = TRANSFORM_OBJECT_TO_CLUSTER()
        self.transform_list = []
        self.surface_list = []


        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        main_widget = self.get_main_widget()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=main_widget)


        self.transform_obj_listWidget = self.sample_widget_template.list_widget()
        vertical_layout.addWidget(self.transform_obj_listWidget)

        transform_obj_button = self.sample_widget_template.pushButton(set_text='get Transform Object',
                                                                      connect=self.transform_obj_button_def)
        vertical_layout.addWidget(transform_obj_button)


        self.surface_obj_listwidget = self.sample_widget_template.list_widget()
        vertical_layout.addWidget(self.surface_obj_listwidget)

        surface_obj_button = self.sample_widget_template.pushButton(set_text='Get Surface Object',
                                                                    connect=self.surface_obj_button_def)
        vertical_layout.addWidget(surface_obj_button)

        create_cluster = self.sample_widget_template.pushButton(set_text='Create Cluster',
                                                                connect=self.create_cluster_def)
        vertical_layout.addWidget(create_cluster)

    def transform_obj_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            self.transform_list = []
            for each in sel_obj:
                self.transform_obj_listWidget.addItem(each)
                self.transform_list.append(each)

    def surface_obj_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            self.surface_list = []
            for each in sel_obj:
                self.surface_obj_listwidget.addItem(each)
                self.surface_list.append(each)

    def create_cluster_def(self):
        '''

        :return:
        '''
        self.transform_object_to_cluster_class.extract_cluster(transform_obj_list=self.transform_list,
                                                               surface_obj_list=self.surface_list)
