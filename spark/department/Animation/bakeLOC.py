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

    def parent_scale_const(self,first_obj ,secound_obj):
        '''

        :return:
        '''

        list_attr = cmds.listAttr(secound_obj, k=True)
        trans_x = False
        trans_y = False
        trans_z = False
        rot_x = False
        rot_y = False
        rot_z = False
        scale_x = False
        scale_y = False
        scale_z = False

        for each in list_attr:

            if 'rotate' in each:
                if 'x' in each.lower():
                    rot_x = True
                elif 'y' in each.lower():
                    rot_y = True
                elif 'z' in each.lower():
                    rot_z = True

            if 'translate' in each:
                if 'x' in each.lower():
                    trans_x = True
                elif 'y' in each.lower():
                    trans_y = True
                elif 'z' in each.lower():
                    trans_z = True

            if 'scale' in each:
                if 'x' in each.lower():
                    scale_x = True
                elif 'y' in each.lower():
                    scale_y = True
                elif 'z' in each.lower():
                    scale_z = True

        # get the list
        translate_list = []
        rotate_list = []
        scale_list = []
        axis = ['x', 'y', 'z']
        a = 0
        for each in [trans_x, trans_y, trans_z]:
            if each == False:
                translate_list.append(axis[a])

            a += 1

        a = 0
        for each in [rot_x, rot_y, rot_z]:
            if each == False:
                rotate_list.append(axis[a])

            a += 1

        a = 0
        for each in [scale_x, scale_y, scale_z]:
            if each == False:
                scale_list.append(axis[a])

            a += 1

        cmds.parentConstraint(first_obj, secound_obj, sr=rotate_list, st=translate_list, mo=False)
        cmds.scaleConstraint(first_obj, secound_obj, skip=scale_list, mo=False)

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
                                listConnection = cmds.listConnections(child_ctrl_list[a] + '.' + each_attr)
                                if listConnection != None:
                                    cmds.delete(listConnection)
                                #mel.eval('CBdeleteConnection "%s.%s";' %(child_ctrl_list[a], each_attr))


                        self.parent_scale_const(each, child_ctrl_list[a])


                        object_list_to_bake.append(child_ctrl_list[a])


                        a+=1
            else:
                raise RuntimeError('Ctrl list and Child Controller list is not same')

        else:
            for each in ctrl_list:
                if each != '':
                    loc_name = each + '_LOC'
                    if not cmds.objExists(loc_name):
                        cmds.spaceLocator(n=loc_name)

                    self.parent_scale_const(each, loc_name)

                    object_list_to_bake.append(loc_name)


        cmds.select(object_list_to_bake)
        mel.eval('doBakeSimulationArgList 8 { "1","0","10","1","0","0","1","1","0","1","animationList","0","0","0","0","0","1","0","1" };')


        for each in object_list_to_bake:
            scale__ = cmds.listConnections(each, type='scaleConstraint')
            parent__ = cmds.listConnections(each, type='parentConstraint')
            if scale__:
                for each_scale in scale__:
                    if cmds.objExists(each_scale):
                        cmds.delete(each_scale)

            if parent__:
                for each_parent in parent__:
                    if cmds.objExists(each_parent):
                        cmds.delete(each_parent)


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

