from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
from functools import partial

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.common import rename
from spark.widget import widget_help

for each in [sample_color_variable, sample_widget_template, style_sheet_template, rename, widget_help]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.sample_color_variable import COLOR_VARIABLE
from spark.department.common.rename import RENAME
from spark.widget.widget_help import WIDGET_HELP


class MOTIONMULT_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='MotionMult', height=150):
        super(MOTIONMULT_WIDGET, self).__init__(title=title, height=height)

        self.anim_obj = ''
        self.input_list = []
        self.output_list = []

        self.initUI()

    def initUI(self):
        '''

        :return:
        '''

        get_widget = self.get_main_widget()

        grid_layput = self.sample_widget_template.grid_layout(parent_self=get_widget,
                                                              set_spacing=5)

        new_value = 0
        vertical_val = 0

        #ANIM POS BUTTON
        anim_pos_button = self.sample_widget_template.pushButton(set_text='Anim Pos >>>',
                                                                 connect=self.anim_pos_button_def)
        grid_layput.addWidget(anim_pos_button, vertical_val, new_value, 1, 1)
        new_value += 1

        self.anim_pos_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Please Specify the Anim Center Joint Postion')
        self.anim_pos_lineedit.textChanged.connect(self.anim_pos_lineedit_def)
        grid_layput.addWidget(self.anim_pos_lineedit, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        #INPUT LIST
        input_list_button = self.sample_widget_template.pushButton(set_text='Input List >>>',
                                                                   connect=self.input_list_button_def)
        grid_layput.addWidget(input_list_button, vertical_val, new_value, 1, 1)
        new_value += 1

        self.input_list_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Please Specify List of the input Geo')
        self.input_list_lineedit.textChanged.connect(self.input_list_lineedit_def)
        grid_layput.addWidget(self.input_list_lineedit, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        #OUTPUT LIST
        output_list_button = self.sample_widget_template.pushButton(set_text='Output List >>>',
                                                                    connect=self.output_list_button_def)
        grid_layput.addWidget(output_list_button, vertical_val, new_value, 1, 1)
        new_value += 1

        self.output_list_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Please Specify List of the Output Geo')
        self.output_list_lineedit.textChanged.connect(self.output_list_lineedit_def)
        grid_layput.addWidget(self.output_list_lineedit, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        create_motionMult_button = self.sample_widget_template.pushButton(set_text='>>> Create MotionMult <<<',
                                                                          connect=self.create_motionMult_button_def)
        grid_layput.addWidget(create_motionMult_button, vertical_val, new_value, 1, 2)
        vertical_val += 1
        new_value = 0

        grid_layput.addItem(self.sample_widget_template.spaceItem(), vertical_val, new_value, 1, 2)


    def anim_pos_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            self.anim_pos_lineedit.setText(sel_obj[0])
            self.anim_obj = sel_obj[0]

    def anim_pos_lineedit_def(self):
        '''

        :return:
        '''
        self.anim_obj = self.anim_pos_lineedit.text()

    def input_list_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.input_list = sel_obj
        obj_str = ''
        for each in sel_obj:
            obj_str += each + ' '
        self.input_list_lineedit.setText(obj_str)
        if '' in self.input_list:
            self.input_list.remove('')

    def input_list_lineedit_def(self):
        '''

        :return:
        '''
        text = self.input_list_lineedit.text()
        self.input_list = text.split(' ')
        if '' in self.input_list:
            self.input_list.remove('')

    def output_list_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.output_list = sel_obj
        obj_str = ''
        for each in sel_obj:
            obj_str += each + ' '

        self.output_list_lineedit.setText(obj_str)
        if '' in self.output_list:
            self.output_list.remove('')

    def output_list_lineedit_def(self):
        '''

        :return:
        '''
        text = self.output_list_lineedit.text()
        self.output_list = text.split(' ')
        if '' in self.output_list:
            self.output_list.remove('')


    def create_motionMult_button_def(self):
        '''

        :return:
        '''
        print('this is the Anim Obj Pos: ', self.anim_obj)
        print('this is the Input List: ', self.input_list)
        print('this is the Output List: ', self.output_list)
        #LOAD PLUGIN
        from spark.department.CFX import node_create
        reload(node_create)
        node_create.motionMult()

        '''
        disconnectAttr rivet.translate motionMult1.inputOneTrans;
        // Result: Disconnect rivet.translate from motionMult1.inputOneTrans. // 
        connectAttr -f rivet.translate motionMult1.inputOneTrans;
        // Result: Connected rivet.translate to motionMult1.inputOneTrans. // 
        disconnectAttr motionMult1.outputTrans output_cluHandle.translate;
        // Result: Disconnect motionMult1.outputTrans from output_cluHandle.translate. // 
        disconnectAttr motionMult1.inputTrans input_cluHandle.translate;
        // Result: Disconnect motionMult1.inputTrans from input_cluHandle.translate. // 
        connectAttr -f motionMult1.inputTrans input_cluHandle.translate;
        // Result: Connected motionMult1.inputTrans to input_cluHandle.translate. // 
        connectAttr -f motionMult1.outputTrans output_cluHandle.translate;
        // Result: Connected motionMult1.outputTrans to output_cluHandle.translate. // 
        // Warning: Panel size cannot accommodate all requested Heads Up Display elements. // 
        
        '''
        name = 'MotionMult_' + str(len(cmds.ls('motionMult')) + 1)
        cmds.createNode('motionMult', n=name)
        cmds.connectAttr((self.anim_obj + '.t'), (name + '.inputOneTrans' ), f=True)

        #CREATE A CLUSTER ON THE INPUT LIST
        cmds.select(self.input_list)
        input_cluster_name = name + '_InputCluster'
        input_cluset_handle_name = input_cluster_name + 'Handle'
        cmds.cluster(n=input_cluster_name)

        #CREATE CLUSTER ON THE OUTPUT LIST
        cmds.select(self.output_list)
        output_cluster_name = name + '_OutputCluster'
        output_cluset_handle_name = output_cluster_name + 'Handle'
        cmds.cluster(n=output_cluster_name)

        for each in [input_cluset_handle_name, output_cluset_handle_name]:
            cmds.setAttr(each + '.v', 0)



        cmds.connectAttr((name + '.inputTrans'), (input_cluset_handle_name + '.t'), f=True)
        cmds.connectAttr((name + '.outputTrans'), (output_cluset_handle_name + '.t'), f=True)












