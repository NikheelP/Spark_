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


class BAKELOC(SAMPLE_WIDGET):
    def __init__(self, title='Bake LOC', height=300, width=350):
        super(BAKELOC, self).__init__(title=title, height=height, width=width)
        self.startTime = cmds.playbackOptions(q=True, minTime=True)
        self.endTime = cmds.playbackOptions(q=True, maxTime=True)
        self.initUI()


    def initUI(self):
        '''

        :return:
        '''
        main_widget = self.get_main_widget()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=main_widget)

        button_size = 150
        a = 0
        new_value = 0
        vertical_val = 0

        time_line_lable = self.sample_widget_template.label(set_text='TimeLine')
        grid_layout.addWidget(time_line_lable, vertical_val, new_value, 1, 1)
        new_value += 1

        self.start_time_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Start Time',
                                                                         set_text=str(self.startTime))
        self.start_time_lineedit.textChanged.connect(self.start_time_lineedit_def)
        grid_layout.addWidget(self.start_time_lineedit, vertical_val, new_value, 1, 1)
        new_value += 1

        self.end_time_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='End Time',
                                                                       set_text=str(self.endTime))
        self.end_time_lineedit.textChanged.connect(self.end_time_lineedit_def)
        grid_layout.addWidget(self.end_time_lineedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        ctrl_name_label = self.sample_widget_template.label(set_text='Ctrl Name')
        grid_layout.addWidget(ctrl_name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.ctrl_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Controller Name')
        grid_layout.addWidget(self.ctrl_lineedit, vertical_val, new_value, 1, 2)
        new_value += 1

        self.ctrl_query_button = self.sample_widget_template.pushButton(set_text='...',
                                                                       connect=self.ctrl_query_button_def)
        grid_layout.addWidget(self.ctrl_query_button, vertical_val, new_value, 1, 2)


        new_value = 0
        vertical_val += 1

        bakeLOC_button = self.sample_widget_template.pushButton(set_text='Bake LOC',
                                                                 connect=self.bakeLOC_button_def)
        grid_layout.addWidget(bakeLOC_button, vertical_val, new_value, 1, 3)


    def bakeLOC_button_def(self):
        '''

        :return:
        '''
        ctrl_name = self.ctrl_lineedit.text()
        loc_name = ctrl_name + '_LOC'
        if not cmds.objExists(loc_name):
            cmds.spaceLocator(n=loc_name)



        cmds.parentConstraint(ctrl_name, loc_name, mo=False)
        cmds.scaleConstraint(ctrl_name, loc_name, mo=False)

        startTime = cmds.playbackOptions(q=True, minTime=True)
        endTime = cmds.playbackOptions(q=True, maxTime=True)

        cmds.playbackOptions(minTime=self.startTime)
        cmds.playbackOptions(maxTime=self.endTime)

        mel.eval('doBakeSimulationArgList 8 { "1","0","10","1","0","0","1","1","0","1","animationList","0","0","0","0","0","1","0","1" };')

        parent_const_name =  loc_name + '_parentConstraint1'
        scale_const_name =  loc_name + '_scaleConstraint1'
        cmds.delete([parent_const_name, scale_const_name])


        cmds.playbackOptions(minTime=startTime)
        cmds.playbackOptions(maxTime=endTime)

    def start_time_lineedit_def(self):
        '''

        :return:
        '''

        self.startTime = float(self.start_time_lineedit.text())

    def end_time_lineedit_def(self):
        '''

        :return:
        '''
        self.endTime = float(self.end_time_lineedit.text())

    def ctrl_query_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            self.ctrl_lineedit.setText(sel_obj[0])


