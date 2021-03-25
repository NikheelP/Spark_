'''
this is the connection editor to make a simplify version
'''


from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template

for each in [sample_color_variable, sample_widget_template, style_sheet_template]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.sample_color_variable import COLOR_VARIABLE


class CONNECTION_EDITOR(SAMPLE_WIDGET):
    def __init__(self, title='Connection Editor', width=600):
        super(CONNECTION_EDITOR, self).__init__(title=title, width=width)

        self.left_to_right = 'LeftToRight'
        self.right_to_left = 'RightToLeft'

        self.output_input_switch_value = self.left_to_right

        self.initUI()





    def initUI(self):
        '''

        :return:
        '''
        main_widget = self.get_main_widget()

        verticalLyout = self.sample_widget_template.vertical_layout(main_widget)

        #COMBOBOX
        verticalLyout.addWidget(self.combobox_widget_def())

        #RELOAD LEFT AND RELOAD RIGHT
        verticalLyout.addWidget(self.reload_left_reload_right_def())

        #OUTPUT INPUT SWITCH
        verticalLyout.addWidget(self.output_input_switch())

        #OBJECT LIST
        verticalLyout.addWidget(self.treewidget_list())

        #CLEAR WIDGET
        verticalLyout.addWidget(self.clear_widget_def())

        verticalLyout.addItem(self.sample_widget_template.spaceItem())

    def combobox_widget_def(self):
        '''

        :return:
        '''

        combobox_widget = self.sample_widget_template.widget_def()

        verticalLayout = self.sample_widget_template.vertical_layout(combobox_widget)

        additems = ['Direct', 'MultiplyDivide', 'Reverse', 'Negative',
                    'Direct Connect base on left select(will get connection from based on right selection)',
                    'Direct Connect base in right select(will get connection from based on right selection)',
                    'Reverse Connect base on left select(will get connection from based on right selection)',
                    'Reverse Connect base in right select(will get connection from based on right selection)',
                    'Negarive Connect base on left select(will get connection from based on right selection)',
                    'Negative Connect base in right select(will get connection from based on right selection)']
        comboxBox = self.sample_widget_template.comboBox(addItems=additems,
                                                         setEditable=True)
        verticalLayout.addWidget(comboxBox)

        return combobox_widget

    def reload_left_reload_right_def(self):
        '''

        :return:
        '''
        reload_widget = self.sample_widget_template.widget_def()

        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=reload_widget, set_contents_margins=[2,2,2,2], set_spacing=2)

        #RELOAD LEFT
        reload_left_text = 'Reload Left'
        reload_left_button = self.sample_widget_template.pushButton(set_text=reload_left_text, connect=self.reload_left_button_def)
        horizontal_layout.addWidget(reload_left_button)

        #RELOAD RIGHT
        reload_right_text = 'Relod Right'
        reload_right_button = self.sample_widget_template.pushButton(set_text=reload_right_text)
        horizontal_layout.addWidget(reload_right_button)

        return reload_widget

    def output_input_switch(self):
        '''

        :return:
        '''
        output_input_switch_widget = self.sample_widget_template.widget_def()

        self.output_input_horizontalLayout = self.sample_widget_template.horizontal_layout(parent_self=output_input_switch_widget)

        output_text = 'Output'
        output_label = self.sample_widget_template.label(set_text=output_text, set_alighment='center')
        self.output_input_horizontalLayout.addWidget(output_label)

        input_text = 'Input'
        input_label = self.sample_widget_template.label(set_text=input_text, set_alighment='center')
        self.output_input_horizontalLayout.addWidget(input_label)


        return output_input_switch_widget

    def treewidget_list(self):
        '''

        :return:
        '''
        treewidget_widget = self.sample_widget_template.widget_def(min_size=[0, 600])

        grid_layout = self.sample_widget_template.grid_layout(parent_self=treewidget_widget)

        new_value = 0
        vertical_val = 0

        #OUTPUT LINEEDIT
        output_linedit = self.sample_widget_template.line_edit()
        grid_layout.addWidget(output_linedit, vertical_val, new_value, 1, 1)
        new_value += 1

        # INPUT LINEEDIT
        input_linedit = self.sample_widget_template.line_edit()
        grid_layout.addWidget(input_linedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        #OUTPUT TREEWIDGET
        output_treeWidget = self.sample_widget_template.treeWidget(setHeaderHidden=True)
        grid_layout.addWidget(output_treeWidget, vertical_val, new_value, 1, 1)
        new_value += 1

        #INPUT TREEWIDGET
        input_treeWidget = self.sample_widget_template.treeWidget(setHeaderHidden=True)
        grid_layout.addWidget(input_treeWidget, vertical_val, new_value, 1, 1)

        return treewidget_widget

    def clear_widget_def(self):
        '''

        :return:
        '''
        clear_widget = self.sample_widget_template.widget_def()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=clear_widget)
        new_value = 0
        vertical_val = 0

        input_name = self.sample_widget_template.label(set_text='Input', set_alighment='center')
        grid_layout.addWidget(input_name, vertical_val, new_value, 1, 1)
        new_value += 1

        output_name = self.sample_widget_template.label(set_text='Output', set_alighment='center')
        grid_layout.addWidget(output_name, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        input_clear_button = self.sample_widget_template.pushButton(set_text='Clear Input')
        grid_layout.addWidget(input_clear_button, vertical_val, new_value, 1, 1)
        new_value += 1

        output_clear_button = self.sample_widget_template.pushButton(set_text='Clear Output')
        grid_layout.addWidget(output_clear_button, vertical_val, new_value, 1, 1)

        return clear_widget

    def reload_left_button_def(self):
        '''

        :return:
        '''
        pass