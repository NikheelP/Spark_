

from spark.widget.import_module import *
# from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import json
import ast

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.widget import widget_help
for each in [sample_color_variable, sample_widget_template, style_sheet_template, widget_help]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET


class TPOSECREATE(SAMPLE_WIDGET):
    def __init__(self, title='Smart TPose', height=500, width=350):
        super(TPOSECREATE, self).__init__(title=title, height=height, width=width)

        self.buffer_val = 30
        self.animation_start_val = 1001
        self.animation_rest_val = self.animation_start_val - 10
        self.tpose_frame_val = self.animation_rest_val - self.buffer_val
        self.ctrl_list = []

        self.prePose = True

        self.iniUI()

    def set_rest_animation_val(self):
        self.animation_rest_val = self.animation_start_val - 10
        self.tpose_frame_val = self.animation_rest_val - self.buffer_val

    def update_val(self):
        '''

        :return:
        '''

        self.buffer_frame_lineedit.setText(str(self.buffer_val))
        self.tpose_frame_lineedit.setText(str(self.tpose_frame_val))
        self.animation_rest_frame_lineedit.setText(str(self.animation_rest_valstr))
        self.animation_start_frame_lineedit.setText(str(self.animation_start_val))


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

        self.get_list_controller()


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
        self.buffer_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Buffer Frame',
                                                                           set_text=str(self.buffer_val))
        self.buffer_frame_lineedit.textChanged.connect(self.buffer_frame_lineedit_def)
        gridLayout.addWidget(self.buffer_frame_lineedit, vertical_val, new_value, 1, 2)
        vertical_val += 1
        new_value = 0

        #TPOSE FRAME
        self.tpose_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='T-Pose Frame',
                                                                          set_text=str(self.tpose_frame_val))
        self.tpose_frame_lineedit.textChanged.connect(self.tpose_frame_lineedit_def)
        gridLayout.addWidget(self.tpose_frame_lineedit, vertical_val, new_value, 2, 1)
        new_value += 1

        #ANIMATION REST FRAME
        self.animation_rest_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Animation Rest Frame',
                                                                                   set_text=str(self.animation_rest_val))
        self.animation_rest_frame_lineedit.textChanged.connect(self.animation_rest_frame_lineedit_def)
        gridLayout.addWidget(self.animation_rest_frame_lineedit, vertical_val, new_value, 3, 1)
        new_value += 1

        #ANIMATION START FRAME
        self.animation_start_frame_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Animation Start Frame',
                                                                                    set_text=str(self.animation_start_val))
        self.animation_start_frame_lineedit.textChanged.connect(self.animation_start_frame_lineedit_def)
        gridLayout.addWidget(self.animation_start_frame_lineedit, vertical_val, new_value, 4, 1)
        new_value += 1

        return widget


    def animation_start_frame_lineedit_def(self):
        '''

        :return:
        '''

        text = float(self.animation_start_frame_lineedit.text())
        self.animation_start_val = text

        self.set_rest_animation_val()
        self.tpose_frame_lineedit.setText(str(self.tpose_frame_val))
        self.animation_rest_frame_lineedit.setText(str(self.animation_rest_val))


    def buffer_frame_lineedit_def(self):
        '''

        :return:
        '''

        text = float(self.buffer_frame_lineedit.text())
        self.buffer_val = text
        self.set_rest_animation_val()
        self.tpose_frame_lineedit.setText(str(self.tpose_frame_val))

    def tpose_frame_lineedit_def(self):
        '''

        :return:
        '''

        text = float(self.tpose_frame_lineedit.text())
        self.tpose_frame_val = text


    def animation_rest_frame_lineedit_def(self):
        '''

        :return:
        '''

        text = float(self.animation_rest_frame_lineedit.text())
        self.animation_rest_val = text
        self.set_rest_animation_val()
        self.tpose_frame_lineedit.setText(str(self.tpose_frame_val))


    def get_character_obj(self):
        assets_type = cmds.ls('*.Assets_Type')
        obj_list = []
        if assets_type == []:
            assets_type = cmds.ls('*:*.Assets_Type')
            for each in assets_type:
                if cmds.getAttr(each) == 'Character':
                    if '.' in each:
                        obj_list.append(each.split('.')[0])
        else:
            for each in assets_type:
                if cmds.getAttr(each) == 'Character':
                    if '.' in each:
                        obj_list.append(each.split('.')[0])

        return obj_list



    def list_controller_widget(self):
        '''

        :return:
        '''

        widget = self.sample_widget_template.widget_def()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=widget)

        self.assets_comboBox = self.sample_widget_template.comboBox(addItems=self.get_character_obj())
        vertical_layout.addWidget(self.assets_comboBox)

        self.controller_listWidget = self.sample_widget_template.list_widget()
        self.update_listwidget()
        self.controller_listWidget.itemSelectionChanged.connect(self.controller_listWidget_def)
        vertical_layout.addWidget(self.controller_listWidget)

        return widget

    def pre_pose_TPose_def(self):
        '''

        :return:
        '''
        widget = self.sample_widget_template.widget_def()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=widget)

        self.pre_tpose_button = self.sample_widget_template.pushButton(set_text='Pre TPose',
                                                                           connect=self.pre_tpose_button_def)
        verticalLayout.addWidget(self.pre_tpose_button)

        self.post_tpose_button = self.sample_widget_template.pushButton(set_text='Pose TPose',
                                                                        connect=self.post_tpose_button_def)
        self.post_tpose_button.setVisible(False)
        verticalLayout.addWidget(self.post_tpose_button)

        return widget

    def get_list_controller(self):
        '''

        :return:
        '''
        current_grp_name = self.assets_comboBox.currentText()
        controller_list = cmds.listConnections(current_grp_name + '_Controller_Sets.dagSetMembers')
        self.ctrl_list = controller_list
        return controller_list

    def update_listwidget(self):
        controller_list = self.get_list_controller()

        for each in controller_list:
            self.controller_listWidget.addItem(each)

    def controller_listWidget_def(self):
        item = self.controller_listWidget.selectedItems()[0]
        obj_name = item.text()
        if cmds.objExists(obj_name):
            cmds.select(obj_name)


    def pre_tpose_button_def(self):
        grp_name = self.assets_comboBox.currentText()
        value = ast.literal_eval(cmds.getAttr(grp_name + '.Attribute_Val'))

        #DELETE THE KEY FROM THE ANIMATION START FRAME
        cmds.select(self.ctrl_list)
        previous_frame = self.animation_start_val - 1
        cmds.cutKey(time=(0, previous_frame))

        #DO THE FREAME OF ANIMATION
        cmds.currentTime(self.animation_start_val)
        cmds.select(self.ctrl_list)
        cmds.setKeyframe()

        cmds.currentTime(self.animation_rest_val)
        cmds.select(self.ctrl_list)
        cmds.setKeyframe()

        cmds.currentTime(self.tpose_frame_val)

        trans_list = ['translateX', 'translateY', 'translateZ']
        rotate_list = ['rotateX', 'rotateY', 'rotateZ']




        '''
        for each in value:
            for each_ctrl in self.ctrl_list:
                if each in each_ctrl:
                    for each_attr in value[each]:
                        try:
                            cmds.setAttr(each_ctrl + '.' + each_attr, value[each][each_attr])
                        except:
                            pass
        '''
        cmds.select(self.ctrl_list)
        cmds.setKeyframe()

        self.prePose = False
        self.pre_tpose_button.setVisible(False)
        self.post_tpose_button.setVisible(True)

    def post_tpose_button_def(self):
        '''

        :return:
        '''

        minTime = cmds.playbackOptions(q=True, minTime=True)
        maxTime = cmds.playbackOptions(q=True, maxTime=True)

        cmds.playbackOptions(minTime=self.tpose_frame_val, maxTime=self.animation_start_val)
        cmds.select(self.ctrl_list)
        mel.eval('doBakeSimulationArgList 8 { "1","0","10","1","0","0","1","1","0","1","animationList","0","0","0","0","0","1","0","1" };')

        cmds.playbackOptions(minTime=minTime, maxTime=maxTime)















'''
from spark.widget.Animation import TPose_Create_Widget
reload(TPose_Create_Widget)
from spark.widget.Animation.TPose_Create_Widget import TPOSECREATE
tpose = TPOSECREATE()
tpose.show()
'''