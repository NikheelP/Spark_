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
        self.checkbox_val = False


        self.initUI()


    def timeline_widget(self):
        '''

        :return:
        '''
        widget = self.sample_widget_template.widget_def()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=widget)

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

        return widget

    def ctrl_widget(self):
        '''

        :return:
        '''
        widget = self.sample_widget_template.widget_def()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=widget)

        new_value = 0
        vertical_val = 0

        ctrl_name_label = self.sample_widget_template.label(set_text='CtrlName')
        grid_layout.addWidget(ctrl_name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.ctrl_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Specify the ctrl list')
        grid_layout.addWidget(self.ctrl_lineedit, vertical_val, new_value, 1, 1)
        new_value += 1

        self.ctrl_query_button = self.sample_widget_template.pushButton(set_text='...',
                                                                        connect=self.ctrl_query_button_def)
        grid_layout.addWidget(self.ctrl_query_button, vertical_val, new_value, 1, 1)
        new_value += 1

        return widget

    def select_checbox_widget(self):
        '''

        :return:
        '''
        widget = self.sample_widget_template.widget_def()
        grid_layout = self.sample_widget_template.grid_layout(parent_self=widget)

        new_value = 0
        vertical_val = 0

        checkbox_text = 'Please Keep it Off if you want to create Locator and Bake that'.upper()
        self.checkbox = self.sample_widget_template.checkbox(set_text=checkbox_text,
                                                             stateChanged=self.checkbox_def)
        grid_layout.addWidget(self.checkbox, vertical_val, new_value, 1, 2)
        new_value = 0
        vertical_val += 1

        ctrl_name_label = self.sample_widget_template.label(set_text='CtrlName')
        grid_layout.addWidget(ctrl_name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.child_ctrl_linedit = self.sample_widget_template.line_edit(set_PlaceholderText='Specify the Child ctrl list')
        if self.checkbox_val == False:
            self.child_ctrl_linedit.setDisabled(True)
        else:
            self.child_ctrl_linedit.setDisabled(False)
        grid_layout.addWidget(self.child_ctrl_linedit, vertical_val, new_value, 1, 1)
        new_value += 1

        self.ctrl_toolButton = self.sample_widget_template.pushButton(set_text='...',
                                                                      connect=self.ctrl_toolButton_def)
        if self.checkbox_val == False:
            self.ctrl_toolButton.setDisabled(True)
        else:
            self.ctrl_toolButton.setDisabled(False)
        grid_layout.addWidget(self.ctrl_toolButton, vertical_val, new_value, 1, 1)
        new_value += 1

        return widget

    def bakeLoc_widget(self):
        '''

        :return:
        '''
        widget = self.sample_widget_template.widget_def()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=widget)

        new_value = 0
        vertical_val = 0

        bake_Button = self.sample_widget_template.pushButton(set_text='Bake LOC or Ctrl',
                                                             connect=self.bakeLOC_button_def)
        grid_layout.addWidget(bake_Button, vertical_val, new_value, 1, 1)
        new_value += 1

        return widget


    def initUI(self):
        '''

        :return:
        '''
        main_widget = self.get_main_widget()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=main_widget)

        #TIMELINE WIDGET
        vertical_layout.addWidget(self.timeline_widget())

        #SELECT FIRST CONTROLLER WIDGET
        vertical_layout.addWidget(self.ctrl_widget())

        #SELECT CHECKBOX AND NEW CONTROLLER WIDGET
        vertical_layout.addWidget(self.select_checbox_widget())

        #BUTTON WIDGET
        vertical_layout.addWidget(self.bakeLoc_widget())



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

        self.ctrl_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='select Bunch of Control or One Control')
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
        '''
    def update_child_ctrl(self):
        if self.checkbox_val == False:
            self.child_ctrl_linedit.setDisabled(False)
            self.ctrl_toolButton.setDisabled(False)
        else:
            self.child_ctrl_linedit.setDisabled(True)
            self.ctrl_toolButton.setDisabled(True)


    def checkbox_def(self):
        '''

        :return:
        '''

        if self.checkbox.isChecked():
            self.checkbox_val = False
            self.update_child_ctrl()
        else:
            self.checkbox_val = True
            self.update_child_ctrl()

    def bakeLOC_button_def(self):
        '''

        :return:
        '''
        parent_scale_const_list = []
        object_list_to_bake = []

        ctrl_list = self.ctrl_lineedit.text().split(' ')
        startTime = cmds.playbackOptions(q=True, minTime=True)
        endTime = cmds.playbackOptions(q=True, maxTime=True)

        cmds.playbackOptions(minTime=self.startTime)
        cmds.playbackOptions(maxTime=self.endTime)


        if self.checkbox.isChecked():
            child_ctrl_list = self.child_ctrl_linedit.text().split(' ')

            if len(child_ctrl_list) == len(ctrl_list):
                a = 0
                for each in ctrl_list:
                    if each != '':

                        #DISCONNECT CONNTION

                        list_attr = cmds.listAttr(child_ctrl_list[a], k=True, v=True)
                        attr_we_want = [ 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
                        for each_attr in list_attr:
                            if each_attr in attr_we_want:
                                mel.eval('CBdeleteConnection "%s.%s";' %(child_ctrl_list[a], each_attr))


                        cmds.parentConstraint(each, child_ctrl_list[a], mo=False)
                        cmds.scaleConstraint(each, child_ctrl_list[a], mo=False)

                        parent_const_name = child_ctrl_list[a] + '_parentConstraint1'
                        scale_const_name = child_ctrl_list[a] + '_scaleConstraint1'

                        object_list_to_bake.append(child_ctrl_list[a])
                        parent_scale_const_list.append(parent_const_name)
                        parent_scale_const_list.append(scale_const_name)


                        a+=1
            else:
                raise RuntimeError('Ctrl list and Child Controller list is not same')

        else:
            for each in ctrl_list:
                if each != '':
                    loc_name = each + '_LOC'
                    if not cmds.objExists(loc_name):
                        cmds.spaceLocator(n=loc_name)

                    cmds.parentConstraint(each, loc_name, mo=False)
                    cmds.scaleConstraint(each, loc_name, mo=False)

                    parent_const_name = loc_name + '_parentConstraint1'
                    scale_const_name = loc_name + '_scaleConstraint1'

                    object_list_to_bake.append(loc_name)
                    parent_scale_const_list.append(parent_const_name)
                    parent_scale_const_list.append(scale_const_name)



        cmds.select(object_list_to_bake)
        mel.eval('doBakeSimulationArgList 8 { "1","0","10","1","0","0","1","1","0","1","animationList","0","0","0","0","0","1","0","1" };')

        cmds.delete(parent_scale_const_list)

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
            string_val = ''
            for each in sel_obj:
                string_val = string_val + each + ' '

            self.ctrl_lineedit.setText(string_val)

    def ctrl_toolButton_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            string_val = ''
            for each in sel_obj:
                string_val = string_val + each + ' '

            self.child_ctrl_linedit.setText(string_val)

