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


class RENAME_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='Rename'):
        super(RENAME_WIDGET, self).__init__(title=title)
        self.rename_class = RENAME()
        self.onlyInt = QIntValidator()

        self.prefix_name = 'prefix'
        self.suffix_name = 'suffix'

        self.widget_help_class = WIDGET_HELP()

        self.initUI()


    def initUI(self):
        get_main_widget = self.get_main_widget()

        # Vertical Layout
        self.rig_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=get_main_widget)


        # OPTION FOR HELP AND RESET BUTTON
        option_for_help_gridWidget = self.option_for_help_reset_widet()
        self.rig_vertical_layout.addLayout(option_for_help_gridWidget)


        # SEARCH AND REPLACE GRID WIDGET
        search_layout = self.search_replace_def()
        self.rig_vertical_layout.addLayout(search_layout)

        #add_sammple_button
        prefix_sample_button_layout = self.sample_button_widget(val=self.prefix_name)
        self.rig_vertical_layout.addLayout(prefix_sample_button_layout)

        # PREFIX
        prefix_layout = self.prefix_def()
        self.rig_vertical_layout.addLayout(prefix_layout)

        # add_sammple_button
        prefix_sample_button_layout = self.sample_button_widget(val=self.suffix_name)
        self.rig_vertical_layout.addLayout(prefix_sample_button_layout)

        # SUFFIX
        suffix_layout = self.suffix_def()
        self.rig_vertical_layout.addLayout(suffix_layout)

        # RENAME OBJECT
        rename_layout = self.rename_def()
        self.rig_vertical_layout.addLayout(rename_layout)

        remove_layout = self.remove_last_first_character()
        self.rig_vertical_layout.addLayout(remove_layout)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.rig_vertical_layout.addItem(spacerItem)

    def option_for_help_reset_widet(self):
        self.option_for_help_gridWidget = self.sample_widget_template.grid_layout()

        a = 0
        new_value = 0
        vertical_val = 0

        # RELOAD BUTTON
        reset_button_name = 'Reset'
        reset_button = self.sample_widget_template.pushButton(min_size=[20, 20], max_size=[20, 20],
                                                              set_object_name=reset_button_name,
                                                              set_tool_tip=reset_button_name,
                                                              set_status=reset_button_name)
        self.option_for_help_gridWidget.addWidget(reset_button, vertical_val, new_value, 1, 1)
        new_value += 1
        a += 1

        # HELP BUTTON
        help_button_name = 'Help'
        help_button = self.sample_widget_template.pushButton(min_size=[20, 20], max_size=[20, 20],
                                                             set_object_name=help_button_name,
                                                             set_tool_tip=help_button_name, set_status=help_button_name)
        self.option_for_help_gridWidget.addWidget(help_button, vertical_val, new_value, 1, 1)
        new_value += 1
        a += 1

        self.add_spaceItem(vertical_val, self.option_for_help_gridWidget)

        return self.option_for_help_gridWidget

    def add_spaceItem(self, val, widget):
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        widget.addItem(spacerItem, val + 1, 0, 1, 5)

    def search_replace_def(self):
        self.search_replace_grid_layout = self.sample_widget_template.grid_layout()

        a = 0
        new_value = 0
        vertical_val = 0

        # SEARCH LABEL
        search_label = self.sample_widget_template.label(set_text='Search')
        self.search_replace_grid_layout.addWidget(search_label, vertical_val, new_value, 1, 1)
        new_value += 1
        a += 1

        # SEARCH LINEDIT
        self.search_lineedit = self.sample_widget_template.line_edit()
        self.search_lineedit.textChanged.connect(self.search_lineedit_def)
        self.search_replace_grid_layout.addWidget(self.search_lineedit, vertical_val, new_value, 1, 1)
        new_value += 1
        a += 1

        vertical_val += 1
        new_value = 0

        # REPLACE LABEL
        replace_label = self.sample_widget_template.label(set_text='Replace')
        self.search_replace_grid_layout.addWidget(replace_label, vertical_val, new_value, 1, 1)
        new_value += 1
        a += 1

        # REPLACE LINEDIT
        self.replace_lineedit = self.sample_widget_template.line_edit()
        self.replace_lineedit.textChanged.connect(self.replace_lineedit_def)
        self.search_replace_grid_layout.addWidget(self.replace_lineedit, vertical_val, new_value, 1, 1)
        new_value += 1
        a += 1

        vertical_val += 1
        new_value = 0
        # SEARCH AND REPLACE BUTTON
        search_replace_button = self.sample_widget_template.pushButton(set_text='Search and Replace')
        search_replace_button.clicked.connect(self.search_replace_button_def)
        self.search_replace_grid_layout.addWidget(search_replace_button, vertical_val, new_value, 1, 2)

        self.add_spaceItem(vertical_val, self.search_replace_grid_layout)

        return self.search_replace_grid_layout

    def sample_button_widget(self, val='Prefix'):
        sample_button_gridLayout = self.sample_widget_template.grid_layout()

        sample_name_list = ['_Obj', '_Grp', '_LOC', '_Jnt', 'CluHandle', '_Cloth', '_Hair', '_Const', '_SkinBind_Jnt',
                            '_SkinBind_Const_LOC',
                            '_First_Ctrl', '_Secound_Ctrl', '_Third_Ctrl', '_Ctrl']
        new_value = 0
        vertical_val = 0
        a = 0
        new_val = 0
        for each in sample_name_list:
            object_name = 'Prefix_' + each
            prefix_button = self.sample_widget_template.pushButton(set_text=each,
                                                                   set_object_name=object_name)
            prefix_button.clicked.connect(partial(self.prefix_suffix_sample, val, each))
            sample_button_gridLayout.addWidget(prefix_button, vertical_val, new_value, 1, 1)
            new_value += 1
            a += 1
            if a > 6:
                a = 0
                vertical_val += 1
                new_value = 0

        self.add_spaceItem(vertical_val, sample_button_gridLayout)

        return sample_button_gridLayout

    def prefix_suffix_sample(self, prefix_or_suffix, text):
        if prefix_or_suffix.lower() == self.prefix_name:
            self.prefix_linedit.setText(text)
        elif prefix_or_suffix.lower() == self.suffix_name:
            self.suffix_linedit.setText(text)

    def prefix_def(self):
        prefix_gridlayout = self.sample_widget_template.grid_layout()

        new_value = 0
        vertical_val = 0

        # prefix LABEL
        prefix_label = self.sample_widget_template.label(set_text='Prefix')
        prefix_gridlayout.addWidget(prefix_label, vertical_val, new_value, 1, 1)
        new_value += 1

        # PREFIX LINEEDIT
        self.prefix_linedit = self.sample_widget_template.line_edit(set_PlaceholderText='Prefix_')
        self.prefix_linedit.textChanged.connect(self.prefix_lineedit_def)
        prefix_gridlayout.addWidget(self.prefix_linedit, vertical_val, new_value, 1, 1)
        new_value += 1

        # PREFIX BUTTON
        prefix_button = self.sample_widget_template.pushButton(set_text='Add Prefix')
        prefix_button.clicked.connect(self.prefix_button_def)
        prefix_gridlayout.addWidget(prefix_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # self.add_spaceItem(vertical_val, prefix_gridlayout)

        return prefix_gridlayout

    def suffix_def(self):
        suffix_gridlayout = self.sample_widget_template.grid_layout()

        new_value = 0
        vertical_val = 0

        # suffix LABEL
        suffix_label = self.sample_widget_template.label(set_text='suffix')
        suffix_gridlayout.addWidget(suffix_label, vertical_val, new_value, 1, 1)
        new_value += 1

        # suffix LINEEDIT
        self.suffix_linedit = self.sample_widget_template.line_edit(set_PlaceholderText='_Suffix')
        self.suffix_linedit.textChanged.connect(self.suffix_lineedit_def)
        suffix_gridlayout.addWidget(self.suffix_linedit, vertical_val, new_value, 1, 1)
        new_value += 1

        # suffix BUTTON
        suffix_button = self.sample_widget_template.pushButton(set_text='Add Suffix')
        suffix_button.clicked.connect(self.suffix_button_def)
        suffix_gridlayout.addWidget(suffix_button, vertical_val, new_value, 1, 1)
        new_value += 1

        self.add_spaceItem(vertical_val, suffix_gridlayout)
        return suffix_gridlayout

    def rename_def(self):
        rename_gridlayout = self.sample_widget_template.grid_layout()

        new_value = 0
        vertical_val = 0

        # RENMAE LABEL
        rename_label = self.sample_widget_template.label(set_text='Rename: ')
        rename_gridlayout.addWidget(rename_label, vertical_val, new_value, 1, 1)
        new_value += 1

        # RENMAE LINEDIT
        self.rename_linedit = self.sample_widget_template.line_edit(set_PlaceholderText='Rename object')
        self.rename_linedit.textChanged.connect(self.rename_lineedit_def)
        rename_gridlayout.addWidget(self.rename_linedit, vertical_val, new_value, 1, 1)

        new_value = 0
        vertical_val += 1
        # START
        start_label = self.sample_widget_template.label(set_text='Start: ')
        rename_gridlayout.addWidget(start_label, vertical_val, new_value, 1, 1)
        new_value += 1

        # START LINEDIT
        self.start_linedit = self.sample_widget_template.line_edit()
        self.start_linedit.setValidator(self.onlyInt)
        self.start_linedit.setText(str(1))
        rename_gridlayout.addWidget(self.start_linedit, vertical_val, new_value, 1, 1)

        # PADDING
        new_value = 0
        vertical_val += 1
        # START
        padding_label = self.sample_widget_template.label(set_text='padding: ')
        rename_gridlayout.addWidget(padding_label, vertical_val, new_value, 1, 1)
        new_value += 1
        # PADDING LINEDIT
        self.padding_lineedit = self.sample_widget_template.line_edit()
        self.padding_lineedit.setValidator(self.onlyInt)
        self.padding_lineedit.setText(str(3))
        rename_gridlayout.addWidget(self.padding_lineedit, vertical_val, new_value, 1, 1)

        vertical_val += 1
        new_value = 0
        # RENAME OBJECT
        rename_pushButton = self.sample_widget_template.pushButton(set_text='Rename')
        rename_pushButton.clicked.connect(self.rename_pushButton_def)
        rename_gridlayout.addWidget(rename_pushButton, vertical_val, new_value, 1, 2)

        self.add_spaceItem(vertical_val, rename_gridlayout)
        return rename_gridlayout

    def remove_last_first_character(self):
        remove_last_first_gridlayout = self.sample_widget_template.grid_layout()

        new_value = 0
        vertical_val = 0

        remove_last_charcter_button = self.sample_widget_template.pushButton(set_text='Remove Last Character')
        remove_last_charcter_button.clicked.connect(self.remove_last_charcter_button_def)
        remove_last_first_gridlayout.addWidget(remove_last_charcter_button, vertical_val, new_value, 1, 2)

        new_value = 0
        vertical_val += 1

        remove_first_charcter_button = self.sample_widget_template.pushButton(set_text='Remove First Character')
        remove_first_charcter_button.clicked.connect(self.remove_first_charcter_button_def)
        remove_last_first_gridlayout.addWidget(remove_first_charcter_button, vertical_val, new_value, 1, 2)

        return remove_last_first_gridlayout

    def search_replace_button_def(self):
        # get the val
        list_object = cmds.ls(sl=True)
        search_val = self.search_lineedit.text()
        replace_val = self.replace_lineedit.text()
        self.rename_class.search_replace(list_object=list_object,
                                         search_name=search_val,
                                         replace_name=replace_val)
        print('Object Name has been replaced')

    def prefix_button_def(self):
        list_object = cmds.ls(sl=True)
        prefix_val = self.prefix_linedit.text()
        self.rename_class.add_prefix(list_object=list_object, prefix_name=prefix_val)

    def suffix_button_def(self):
        list_object = cmds.ls(sl=True)
        suffix_val = self.suffix_linedit.text()
        self.rename_class.add_suffix(list_object=list_object, suffix_name=suffix_val)

    def rename_pushButton_def(self):
        list_object = cmds.ls(sl=True)
        start_val = self.start_linedit.text()
        padding_val = self.padding_lineedit.text()
        object_name = self.rename_linedit.text()
        self.rename_class.rename(list_object=list_object, object_name=object_name, start_val=start_val,
                                 padding=padding_val)

    def remove_last_charcter_button_def(self):
        list_object = cmds.ls(sl=True)
        self.rename_class.remove_lastword(list_object=list_object)

    def remove_first_charcter_button_def(self):
        list_object = cmds.ls(sl=True)
        self.rename_class.remove_firstword(list_object=list_object)


    def search_lineedit_def(self):
        '''
        set the tex what we need remove all the punctuation in the lineedit
        :return:
        '''
        text = self.search_lineedit.text()
        self.search_lineedit.setText(self.widget_help_class.make_simple_text(text))

    def replace_lineedit_def(self):
        '''
        set the tex what we need remove all the punctuation in the lineedit
        :return:
        '''
        text = self.replace_lineedit.text()
        self.replace_lineedit.setText(self.widget_help_class.make_simple_text(text))

    def prefix_lineedit_def(self):
        '''
        set the tex what we need remove all the punctuation in the lineedit
        :return:
        '''
        text = self.prefix_linedit.text()
        self.prefix_linedit.setText(self.widget_help_class.make_simple_text(text))

    def suffix_lineedit_def(self):
        '''
        set the tex what we need remove all the punctuation in the lineedit
        :return:
        '''
        text = self.suffix_linedit.text()
        self.suffix_linedit.setText(self.widget_help_class.make_simple_text(text))

    def rename_lineedit_def(self):
        '''
        set the tex what we need remove all the punctuation in the lineedit
        :return:
        '''
        text = self.rename_linedit.text()
        self.rename_linedit.setText(self.widget_help_class.make_simple_text(text))
