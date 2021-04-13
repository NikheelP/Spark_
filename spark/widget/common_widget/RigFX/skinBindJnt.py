from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.common import rename
from spark.department.CFX.cfx_tools.rigFX import rigFX_
from spark.department.common import Outliner
from spark.widget import widget_help
for each in [sample_color_variable, sample_widget_template, style_sheet_template, rename, rigFX_, widget_help, Outliner]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.widget_help import WIDGET_HELP

from spark.widget.common_widget import rigFX_icon
rigFxIconPath = os.path.abspath(rigFX_icon.__file__).replace('\\', '/')
last_obj = rigFxIconPath.split('/')[-1]
rigfxIconPath_ = rigFxIconPath.split(last_obj)[0]


class SKINBINDJNT(SAMPLE_WIDGET):
    def __init__(self, title='skinBindJnt'):
        super(SKINBINDJNT, self).__init__(title=title)


        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        get_mainWidget = self.get_main_widget()
        grid_Layout = self.sample_widget_template.grid_layout(parent_self=get_mainWidget,
                                                              set_spacing=3)

        new_value = 0
        vertical_val = 0

        # JOINT LIST WIDGET
        grid_Layout.addWidget(self.joint_list_widget(), vertical_val, new_value, 1, 1)
        new_value += 1

        # GEO LIST WIDGET
        grid_Layout.addWidget(self.geo_list_widget(), vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        grid_Layout.addWidget(self.create_update_widet(), vertical_val, new_value, 1, 2)




    def joint_list_widget(self):
        '''

        :return:
        '''

        joint_list_widget = self.sample_widget_template.widget_def()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=joint_list_widget,
                                                                      set_spacing=3)

        #LIST WIDGET
        self.joint_list = self.sample_widget_template.list_widget()
        self.joint_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.joint_list.itemSelectionChanged.connect(self.joint_list_def)
        vertical_layout.addWidget(self.joint_list)


        #ADD JOINT TO LIST
        add_joint_to_list_text = 'Add Joint to List'
        add_joint_to_list_button = self.sample_widget_template.pushButton(set_text=add_joint_to_list_text,
                                                                          connect=self.add_joint_to_list_button_def)
        vertical_layout.addWidget(add_joint_to_list_button)

        #CLEAR JOINT LIST
        clear_joint_list_text = 'Clear Joint List'
        clear_joint_list_button = self.sample_widget_template.pushButton(set_text=clear_joint_list_text,
                                                                         connect=self.clear_joint_list_button_def)
        vertical_layout.addWidget(clear_joint_list_button)


        #vertical_layout.addItem(self.sample_widget_template.spaceItem())

        return joint_list_widget

    def geo_list_widget(self):
        '''

        :return:
        '''

        geo_list_widget = self.sample_widget_template.widget_def()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=geo_list_widget,
                                                                      set_spacing=3)

        # LIST WIDGET
        self.geo_list = self.sample_widget_template.list_widget()
        self.geo_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.geo_list.itemSelectionChanged.connect(self.obj_list_def)

        vertical_layout.addWidget(self.geo_list)

        # ADD JOINT TO LIST
        add_geo_to_list_text = 'Add Geo to List'
        add_geo_to_list_button = self.sample_widget_template.pushButton(set_text=add_geo_to_list_text,
                                                                       connect=self.add_geo_to_list_button_def)
        vertical_layout.addWidget(add_geo_to_list_button)

        # CLEAR JOINT LIST
        clear_geo_listt_ext = 'Clear Geo List'
        clear_geo_list_button = self.sample_widget_template.pushButton(set_text=clear_geo_listt_ext,
                                                                       connect=self.clear_geo_list_button_def)
        vertical_layout.addWidget(clear_geo_list_button)

        #vertical_layout.addItem(self.sample_widget_template.spaceItem())

        return geo_list_widget


    def create_update_widet(self):
        '''

        :return:
        '''

        create_update_widget = self.sample_widget_template.widget_def()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=create_update_widget,
                                                                      set_spacing=3)

        #COMBOBOX
        itmes = ['Hierarchy', 'SelectedJoint']
        self.hierarchy_selected_joint_combobox = self.sample_widget_template.comboBox(addItems=itmes)
        vertical_layout.addWidget(self.hierarchy_selected_joint_combobox)


        #BIND JNT BUTTON
        bind_jnt_text = 'Bind Jnt'
        bind_jnt_button = self.sample_widget_template.pushButton(set_text=bind_jnt_text,
                                                                 connect=self.bind_jnt_button_def)
        vertical_layout.addWidget(bind_jnt_button)

        '''
        #GET LIST OF THE JOINT CONNECTED WITH THE SELECTED GEO
        get_list_of_joint_connected_with_selected_geo_text = 'get List Of the Joint Connected With The Selected Geo'
        get_list_of_joint_connected_with_selected_geo_button = self.sample_widget_template.pushButton(set_text=get_list_of_joint_connected_with_selected_geo_text)
        vertical_layout.addWidget(get_list_of_joint_connected_with_selected_geo_button)

        #GET LIST OF THE GEO CONNECTED WITH THE SELECTED JOINT
        get_list_of_geo_connected_with_selected_joint_text = 'get List Of the Joint Connected With The Selected Geo'
        get_list_of_geo_connected_with_selected_joint_button = self.sample_widget_template.pushButton(set_text=get_list_of_geo_connected_with_selected_joint_text)
        vertical_layout.addWidget(get_list_of_geo_connected_with_selected_joint_button)
        '''
        return create_update_widget




    def add_joint_to_list_button_def(self):
        '''
        ADD JOINT LIST TO THE LIST OBJECT
        :return:
        '''

        self.joint_list.clear()

        sel_obj = cmds.ls(sl=True)
        for each_obj in sel_obj:
            if cmds.objectType(each_obj) == 'joint':
                self.joint_list.addItem(each_obj)

    def clear_joint_list_button_def(self):
        '''
        CLEAR THE LIST OF THE JOINT
        :return:
        '''
        self.joint_list.clear()

    def joint_list_def(self):
        '''

        :return:
        '''
        items = self.joint_list.selectedItems()
        obj = []
        for i in range(len(items)):
            obj.append(str(self.joint_list.selectedItems()[i].text()))
        if obj:
            cmds.select(obj)

    def add_geo_to_list_button_def(self):
        '''
        ADD GEO TO THE LIST
        :return:
        '''
        self.geo_list.clear()

        sel_obj = cmds.ls(sl=True)
        print(sel_obj)
        for each_obj in sel_obj:
            shape_name = cmds.listRelatives(each_obj, s=True)
            if shape_name != None:
                if cmds.objectType(shape_name[0]) == 'mesh' or cmds.objectType(shape_name[0]) == 'nurbsCurve' or cmds.objectType(shape_name[0]) == 'nurbsSurface':
                    self.geo_list.addItem(each_obj)


    def clear_geo_list_button_def(self):
        '''
        CLEAR THE GEO LIST
        :return:
        '''
        self.geo_list.clear()

    def obj_list_def(self):
        '''

        :return:
        '''
        items = self.geo_list.selectedItems()
        obj = []
        for i in range(len(items)):
            obj.append(str(self.geo_list.selectedItems()[i].text()))
        if obj:
            cmds.select(obj)


    def bind_jnt_button_def(self):
        '''

        :return:
        '''
        #CHECK IF IT HAS WHAT WE NEED
        #1 -  IF JOINT HAS SELECTED AND MULTIPLE OBJ WILL BE FINE
        #2 - IF LEFT AND RIGHT HAS SAME SELECTION
        print('this is start')

        #1
        joint_list = self.joint_list.selectedItems()
        geo_list = self.geo_list.selectedItems()

        #CHECK HIERACHY AND SELECTED
        #itmes = ['Hierarchy', 'SelectedJoint']
        current_text = self.hierarchy_selected_joint_combobox.currentText()

        if current_text == 'Hierarchy':
            Hierarchy = True
            SelectedJoint = False
        else:
            SelectedJoint = True
            Hierarchy = False
        print()
        if len(joint_list) == len(geo_list):
            print('this is sa,')
            a = 0
            for each in joint_list:
                print(each)

                if Hierarchy:
                    jnt_name = self.joint_list.selectedItems()[a].text()
                    jnt_list = cmds.listRelatives(jnt_name, c=True, ad=True, fullPath=True)
                    jnt_list.append(jnt_name)
                else:
                    jnt_list = self.joint_list.selectedItems()[a].text()
                print(jnt_list)
                print(geo_list)
                cmds.select(jnt_list, self.geo_list.selectedItems()[a].text())
                cmds.SmoothBindSkin()

                a+=1

        else:
            a = 0
            jnt_all_list = []
            for each in joint_list:
                if Hierarchy:
                    jnt_name = self.joint_list.selectedItems()[a].text()
                    jnt_list = cmds.listRelatives(jnt_name, c=True, ad=True, fullPath=True)
                    jnt_all_list.extend(jnt_list)
                else:
                    jnt_all_list = self.joint_list.selectedItems()[a].text()

                a+=1
            geo_all_list = []
            a =0
            for each in geo_list:
                geo_all_list.append(self.geo_list.selectedItems()[a].text())
                a+=1

            print('thi sis eslsssssss')
            cmds.select(jnt_all_list, geo_all_list)
            cmds.SmoothBindSkin()
            print('it wil bind randomly')








