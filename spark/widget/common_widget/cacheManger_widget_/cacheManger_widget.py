from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os, glob, json
import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import time
from os import listdir
from os.path import isfile, join
import webbrowser

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.Help import help
from spark.department.Help import geoCache
from spark.department.CFX.cfx_tools import cacheManager
from spark.department.common import rename
from spark.department.Help import attribute
from spark.department.CFX.cfx_tools.rigFX import rigFX_
from spark.widget import widget_help
from spark.widget.common_widget.cacheManger_widget_ import playblast_setting
for each in [sample_color_variable, sample_widget_template, style_sheet_template, rename, cacheManager, geoCache, help, attribute, rigFX_, widget_help,
             playblast_setting]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.department.CFX.cfx_tools.cacheManager import CACHEMANAGER
from spark.department.Help.geoCache import GEOCACHE
from spark.department.Help.help import HELP
from spark.department.Help.attribute import ATTRIBUTE
from spark.department.CFX.cfx_tools.rigFX.rigFX_ import RIGFX
from spark.widget.widget_help import WIDGET_HELP
from spark.widget.common_widget.cacheManger_widget_.playblast_setting import PLAYBLAST_SETTING

from spark.widget.common_widget import cacheManager_icon
cacheManagerIconPath = os.path.abspath(cacheManager_icon.__file__).replace('\\', '/')
last_obj = cacheManagerIconPath.split('/')[-1]
cacheManagerIconPath = cacheManagerIconPath.split(last_obj)[0]

from spark.widget.common_widget import rigFX_icon
rigFxIconPath = os.path.abspath(rigFX_icon.__file__).replace('\\', '/')
last_obj = rigFxIconPath.split('/')[-1]
rigfxIconPath_ = rigFxIconPath.split(last_obj)[0]

class CACHEMANGER_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='Cache Manger', width=1200):
        super(CACHEMANGER_WIDGET, self).__init__(title=title, width=width)
        self.cache_manager_class = CACHEMANAGER()
        self.geo_cache_class = GEOCACHE()
        self.help_class = HELP()
        self.attribute_class = ATTRIBUTE()
        self.rig_fx_class = RIGFX()
        self.widget_help_class = WIDGET_HELP()


        self.end_time_val = cmds.playbackOptions(q=True, maxTime=True)
        self.start_time_val = cmds.playbackOptions(q=True, minTime=True)
        self.buffer_val = 10
        self.icon_size = 50
        on_icon = 'onIcon.png'
        off_icon = 'offIcon.png'
        self.on_icon_path = cacheManagerIconPath + on_icon
        self.off_icon_path = cacheManagerIconPath + off_icon

        self.ncloth_tree_vis = True
        self.nRigit_tree_vis = False
        self.nConstraint_tree_vis = False
        self.nhair_tree_vis = False
        self.follicle1_tree_vis = False
        self.ncloth_tree_widget_item = []
        self.sim_tree_widget_item = {}
        self.cam_list = []
        cam_shape_list = cmds.ls(type='camera')
        for each in cam_shape_list:
            self.cam_list.append(cmds.listRelatives(each, p=True)[0])

        self.float_validator = QDoubleValidator()


        #CACHE MANAER NODE
        self.cache_manager_data = 'CacheManagerData'
        self.sim_start = 'sim_start'
        self.sim_start_val = 0.0
        self.sim_end = 'sim_end'
        self.sim_end_val = 0.0
        self.sim_path = 'sim_path'

        self.geo_cache_start = 'geo_cache_start'
        self.geo_cache_start_val = 0.0
        self.geo_cache_end = 'geo_cache_end'
        self.geo_cache_end_val = 0.0
        self.geo_path = 'geo_cache_path'

        self.playblast_start = 'playblast_start'
        self.playblast_start_val = 1001.0
        self.playblast_end = 'playblast_end'
        self.playblast_end_val = 0.0
        self.playblast_path = 'playblast_path'

        self.final_start = 'final_start'
        self.final_start_val = 0.0
        self.final_end = 'final_end'
        self.final_end_val = 0.0
        self.final_path = 'final_path'

        self.manual_start = 'manual_start'
        self.manual_start_val = 0.0
        self.manual_end = 'manual_end'
        self.manual_end_val = 0.0
        self.manual_path = 'manual_path'

        self.camera = 'Camera'
        self.camera_name = self.cam_list[0]

        self.ncloth_val = True
        self.nrigid_val = False
        self.nconstraint_val = False
        self.nhair_val = False
        self.folical_val = False

        self.ncloth_text = 'nCloth'
        self.nrigit_text = 'nRigit'
        self.nconstraint_text = 'nConstraint'
        self.nhair_text = 'nHair'
        self.folical_text = 'follicle'

        # GET THE SIM CACHE PATH
        self.sim_cache_path, self.geo_cache_path, self.playblast_cache_path, self.final_cache_path, self.manual_cache_path = self.cache_manager_class.initcheck()
        self.cache_manager_data_def()

        self.get_cache_manager_data()

        self.ui()

        self.tree_checkbox_def()


    def ui(self):
        '''

        :return:
        '''
        self.main_widget = self.get_main_widget()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.main_widget)


        #CACHE MANAGER UPPER WIDGET
        cache_manager_upper_widget = self.sample_widget_template.widget_def(parent_self=self.main_widget)
        vertical_layout.addWidget(cache_manager_upper_widget)

        cache_manager_upper_widget_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=cache_manager_upper_widget)

        #GET THE MAIN SPLITTER
        main_horizonatal_splitter = self.sample_widget_template.splitter_def(parent_self=cache_manager_upper_widget,
                                                                             set_orientation=self.sample_widget_template.vertical)
        cache_manager_upper_widget_vertical_layout.addWidget(main_horizonatal_splitter)

        #CREATE A TWO WIDGET
        self.upper_widget = self.sample_widget_template.widget_def(parent_self=main_horizonatal_splitter,
                                                              min_size=[0, 500])
        upper_widget_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.upper_widget)
        self.upper_widget_splitter = self.sample_widget_template.splitter_def(parent_self=self.upper_widget,
                                                                              set_orientation=self.sample_widget_template.horizonatal)
        upper_widget_vertical_layout.addWidget(self.upper_widget_splitter)
        self.cloth_input_output_widget()
        self.cloth_button_widget()
        self.cache_playblast_history_widget()

        self.lower_widget = self.sample_widget_template.widget_def(parent_self=main_horizonatal_splitter,
                                                              min_size=[0, 100])
        lower_widget_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.lower_widget)
        self.lower_widget_splitter = self.sample_widget_template.splitter_def(parent_self=self.lower_widget,
                                                                              set_orientation=self.sample_widget_template.horizonatal)
        lower_widget_vertical_layout.addWidget(self.lower_widget_splitter)

        self.comment_widget()
        self.file_status_widget()

        #CacheManagerData
        #DELETE CacheManagerData
        button_min_height = 60
        delete_cacheManager_button_widget = self.sample_widget_template.widget_def(parent_self=self.main_widget,
                                                                                   min_size=[0, button_min_height],
                                                                                   max_size=[self.sample_widget_template.max_size,
                                                                                             button_min_height])
        vertical_layout.addWidget(delete_cacheManager_button_widget)

        refresh_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=delete_cacheManager_button_widget)

        #DELETE CACHEMANAGER
        refresh_button = self.sample_widget_template.pushButton(set_text='Delete CacheManager And RefreshUI',
                                                                connect=self.delete_cacheManager_def)
        refresh_vertical_layout.addWidget(refresh_button)

        #REFRESH UI
        refresh_button = self.sample_widget_template.pushButton(set_text='Refresh UI',
                                                                connect=self.window_show_def)
        refresh_vertical_layout.addWidget(refresh_button)


        '''

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=main_widget)

        main_horizonatal_splitter = self.sample_widget_template.splitter_def(parent_self=main_widget,
                                                                             set_orientation=self.sample_widget_template.vertical)
        vertical_layout.addWidget(main_horizonatal_splitter)


        #CLOTH INPUT BUTTON HISTORY SPLITTER
        self.cloth_input_button_history_splitter = self.sample_widget_template.splitter_def(parent_self=main_horizonatal_splitter,
                                                                                            set_orientation=self.sample_widget_template.horizonatal)


        cache_manager_upper_widget = self.sample_widget_template.widget_def(parent_self=self.cloth_input_button_history_splitter)

        new_vertical = self.sample_widget_template.vertical_layout(parent_self=cache_manager_upper_widget)
        pus = self.sample_widget_template.pushButton(set_text='test')
        new_vertical.addWidget(pus)

        cache_manager_lower_widget = self.sample_widget_template.widget_def(parent_self=self.cloth_input_button_history_splitter)

        new_add_vertical = self.sample_widget_template.vertical_layout(parent_self=cache_manager_lower_widget)
        pus = self.sample_widget_template.pushButton(set_text='anothertest')
        new_add_vertical.addWidget(pus)


        
        self.cloth_input_output_widget()
        self.cloth_button_widget()
        self.cache_playblast_history_widget()
        
        #COMMENT AND FILE STATUS SPLIT
        self.comment_file_status_splitter = self.sample_widget_template.splitter_def(parent_self=main_horizonatal_splitter,
                                                                                     set_orientation=self.sample_widget_template.horizonatal)
        
        self.comment_widget()
        self.file_status_widget()
        

        #REFRESH EVERYTHING PUSHBUTTON
        refresh_everything_text = 'Refresh Everything'
        refresh_everything_pushbutton = self.sample_widget_template.pushButton(set_text=refresh_everything_text)
        vertical_layout.addWidget(refresh_everything_pushbutton)
        '''

    def delete_cacheManager_def(self):
        '''

        :return:
        '''
        name = 'CacheManagerData'
        if cmds.objExists(name):
            cmds.delete(name)
        self.window_show_def()

    def window_show_def(self):
        '''

        :return:
        '''
        self.close()
        #from spark.widget.common_widget.cacheManger_widget_ import cacheManger_widget
        #reload(cacheManger_widget)
        #from spark.widget.common_widget.cacheManger_widget_.cacheManger_widget import CACHEMANGER_WIDGET
        cache_mager_class = CACHEMANGER_WIDGET()
        cache_mager_class.show()

        return cache_mager_class


    def cloth_input_output_widget(self):
        '''

        :return:
        '''
        cloth_input_output_widget = self.sample_widget_template.widget_def(self.upper_widget_splitter,
                                                                           max_size=[350, self.sample_widget_template.max_size])

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=cloth_input_output_widget)

        #DO THE TAB WIDGET
        tab_widget = self.sample_widget_template.tab_widget(parent_self=cloth_input_output_widget)
        stylesheet = """ 
                    QTabBar::tab:selected {background: green;}
                    QTabWidget>QWidget>QWidget{background: gray;}
                    """
        tab_widget.setStyleSheet(stylesheet)
        vertical_layout.addWidget(tab_widget)

        # SIM TAB
        self.sim_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        sim_tab_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.sim_tab_widget)

        self.sim_tree_widget = self.sample_widget_template.treeWidget()
        # sim_tree_widget.setHeaderHidden(True)
        header = QTreeWidgetItem(["Node", "Visibility"])
        self.sim_tree_widget.setColumnWidth(0, 200)
        self.sim_tree_widget.setColumnWidth(1, 10)
        self.sim_tree_widget.setHeaderItem(header)
        self.sim_tree_widget.itemSelectionChanged.connect(self.sim_tree_widget_def)

        self.sim_tree_def()
        sim_tab_vertical_layout.addWidget(self.sim_tree_widget)
        tab_widget.addTab(self.sim_tab_widget, 'Sim'.upper())


        # INPUT TAB
        self.input_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        input_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.input_tab_widget)
        input_vertical_layout.addWidget(self.input_list_def())
        tab_widget.addTab(self.input_tab_widget, 'Input'.upper())

        # OUTPUT TAB
        self.output_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        output_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.output_tab_widget)
        output_vertical_layout.addWidget(self.output_list_def())
        tab_widget.addTab(self.output_tab_widget, 'Output'.upper())

        vertical_layout.addWidget(self.cloth_nrigit_switch_widget())


        return cloth_input_output_widget

    def cloth_nrigit_switch_widget(self):
        '''

        :return:
        '''
        cloth_nrigit_switch_widget = self.sample_widget_template.widget_def()


        grid_layout = self.sample_widget_template.grid_layout(parent_self=cloth_nrigit_switch_widget,
                                                              set_spacing=5)

        new_value = 0
        vertical_val = 0

        # SHOW LABEL
        show_text = 'Show : '
        show_object = self.sample_widget_template.setObjectName('Show_Object')
        show_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=show_object,
                                                                     color=self.color_variable_class.gold_color.get_value())
        show_label = self.sample_widget_template.label(set_text=show_text,
                                                       set_object_name=show_object,
                                                       set_styleSheet=show_styleSheet)
        grid_layout.addWidget(show_label, vertical_val, new_value, 1, 1)
        new_value += 1

        # NCLOTH CHECKBOX
        self.ncloth_text = 'nCloth'
        ncloth_obj_name = self.sample_widget_template.setObjectName(self.ncloth_text)
        ncloth_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=ncloth_obj_name,
                                                                       color=self.color_variable_class.nCloth_color.get_value())
        self.ncloth_checkbox = self.sample_widget_template.checkbox(set_text=self.ncloth_text,
                                                                    set_object_name=ncloth_obj_name,
                                                                    set_styleSheet=ncloth_styleSheet, stateChanged=self.tree_checkbox_def)
        self.ncloth_checkbox.setChecked(self.ncloth_val)
        grid_layout.addWidget(self.ncloth_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NRIGIT CHECKBOX
        self.nrigit_text = 'nRigit'
        nrigit_obj_name = self.sample_widget_template.setObjectName(self.nrigit_text)
        nrigit_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nrigit_obj_name, color=self.color_variable_class.nRigit_color.get_value())
        self.nrigit_chekbox = self.sample_widget_template.checkbox(set_text=self.nrigit_text,
                                                              set_object_name=nrigit_obj_name,
                                                              set_styleSheet=nrigit_styleSheet, stateChanged=self.tree_checkbox_def)
        self.nrigit_chekbox.setChecked(self.nrigid_val)
        grid_layout.addWidget(self.nrigit_chekbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NCONSTRAINT CHECKBOX
        self.nconstraint_text = 'nConstraint'
        nconstraint_obj_name = self.sample_widget_template.setObjectName(self.nconstraint_text)
        nconstraint_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nconstraint_obj_name,
                                                                            color=self.color_variable_class.nConstraint_color.get_value())
        self.nconstraint_checkbox = self.sample_widget_template.checkbox(set_text=self.nconstraint_text,
                                                                    set_object_name=nconstraint_obj_name,
                                                                    set_styleSheet=nconstraint_styleSheet, stateChanged=self.tree_checkbox_def)
        self.nconstraint_checkbox.setChecked(self.nconstraint_val)
        grid_layout.addWidget(self.nconstraint_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NHAIR CHECKBOX

        self.nhair_text = 'nHair'
        nhair_obj_name = self.sample_widget_template.setObjectName(self.nhair_text)
        nhair_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nhair_obj_name, color=self.color_variable_class.nHair_color.get_value())
        self.nhair_checkbox = self.sample_widget_template.checkbox(set_text=self.nhair_text,
                                                              set_object_name=nhair_obj_name,
                                                              set_styleSheet=nhair_styleSheet, stateChanged=self.tree_checkbox_def)
        self.nhair_checkbox.setChecked(self.nhair_val)
        grid_layout.addWidget(self.nhair_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NHAIR CHECKBOX
        self.folical_text = 'follicle'
        folical_obj_name = self.sample_widget_template.setObjectName(self.folical_text)
        folical_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=folical_obj_name,
                                                                      color=self.color_variable_class.folical_color.get_value())
        self.folicle_checkbox = self.sample_widget_template.checkbox(set_text=self.folical_text,
                                                                   set_object_name=folical_obj_name,
                                                                   set_styleSheet=folical_styleSheet,
                                                                   stateChanged=self.tree_checkbox_def)
        self.folicle_checkbox.setChecked(self.folical_val)
        self.nhair_checkbox.setChecked(self.nhair_tree_vis)
        grid_layout.addWidget(self.folicle_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1




        '''
        # SELECT LABEL
        select_text = 'Select : '
        select_object = self.sample_widget_template.setObjectName('Select_Object')
        select_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=select_object,
                                                                       color=self.color_variable_class.gold_color.get_value())
        select_label = self.sample_widget_template.label(set_text=select_text,
                                                         set_object_name=select_object,
                                                         set_styleSheet=select_styleSheet)
        grid_layout.addWidget(select_label, vertical_val, new_value, 1, 1)
        new_value += 1

        # NCLOTH NODE CHECKBOX
        ncloth_node_text = 'nCloth Node'
        ncloth_node_object = self.sample_widget_template.setObjectName(ncloth_node_text)
        ncloth_node_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=ncloth_node_object,
                                                                            color = self.color_variable_class.nCloth_color.get_value())
        ncloth_node_pushButton = self.sample_widget_template.pushButton(set_text=ncloth_node_text,
                                                                        set_object_name=ncloth_node_object,
                                                                        set_styleSheet=ncloth_node_styleSheet,
                                                                        connect=self.ncloth_node_pushButton_def)
        grid_layout.addWidget(ncloth_node_pushButton, vertical_val, new_value, 1, 1)
        new_value += 1

        # NCLLOTH MESH CHECKBOX
        ncloth_mesh_text = 'nCloth Mesh'
        ncloth_mesh_object = self.sample_widget_template.setObjectName(ncloth_mesh_text)
        ncloth_mesh_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=ncloth_mesh_object, color=self.color_variable_class.nCloth_color.get_value())
        ncloth_mesh_pushButton = self.sample_widget_template.pushButton(set_text=ncloth_mesh_text,
                                                                        set_object_name=ncloth_mesh_object,
                                                                        set_styleSheet=ncloth_mesh_styleSheet)
        grid_layout.addWidget(ncloth_mesh_pushButton, vertical_val, new_value, 1, 1)
        new_value += 1

        # NHAIR NODE CHCKBOXn
        nhair_node_text = 'nHair Node'
        nhair_node_object = self.sample_widget_template.setObjectName(nhair_node_text)
        nhair_node_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nhair_node_object,
                                                                           color=self.color_variable_class.nHair_color.get_value())
        nhair_node_checkbox = self.sample_widget_template.pushButton(set_text=nhair_node_text,
                                                                   set_object_name=nhair_node_object,
                                                                   set_styleSheet=nhair_node_styleSheet)
        grid_layout.addWidget(nhair_node_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1
        '''
        return cloth_nrigit_switch_widget

    def cloth_button_widget(self):
        '''

        :return:
        '''

        cloth_button_widget = self.sample_widget_template.widget_def(self.upper_widget_splitter,
                                                                     max_size=[180, self.sample_widget_template.max_size])

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=cloth_button_widget,
                                                                      set_spacing=5)

        #SELECT NCLOTH NODE CHECKBOX
        select_ncloth_node_text = 'Select all nCloth Node'
        select_ncloth_node_object = self.sample_widget_template.setObjectName(select_ncloth_node_text)
        select_ncloth_node_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=select_ncloth_node_object,
                                                                                   color=self.color_variable_class.yellow_color.get_value())
        self.select_ncloth_node_checkbox = self.sample_widget_template.checkbox(set_text=select_ncloth_node_text,
                                                                           set_object_name=select_ncloth_node_object,
                                                                           set_styleSheet=select_ncloth_node_styleSheet)
        self.select_ncloth_node_checkbox.setChecked(True)
        vertical_layout.addWidget(self.select_ncloth_node_checkbox)

        button_width = 150
        button_height = 75


        #NCLOTH CACHE BUTTON
        ncloth_cache_text = 'nCloth Cache'
        icon_ = 'nClothCache.webp'
        icon_path = cacheManagerIconPath + icon_
        ncloth_cache_button = self.sample_widget_template.pushButton(set_text=ncloth_cache_text,
                                                                      max_size=[self.sample_widget_template.max_size, button_height],
                                                                      set_icon=icon_path,
                                                                      set_icon_size=[self.icon_size, self.icon_size],
                                                                      connect=self.ncloth_cache_def)
        vertical_layout.addWidget(ncloth_cache_button)

        #DISCONNECT THE NCLOTH CACHE BUTTON
        disconnect_nCloth_cache_text = 'Disconnect nCloth Cache'
        icon_ = 'disConnectnClothCache.webp'
        icon_path = cacheManagerIconPath + icon_
        disconnect_the_ncloth_cache_button = self.sample_widget_template.pushButton(set_text=disconnect_nCloth_cache_text,
                                                                                    max_size=[self.sample_widget_template.max_size, button_height],
                                                                                    set_icon=icon_path,
                                                                                    set_icon_size=[self.icon_size, self.icon_size],
                                                                                    connect=self.disconnect_the_ncloth_cache_button_def)
        vertical_layout.addWidget(disconnect_the_ncloth_cache_button)

        #GEO CACHE BUTTON
        geo_cache_text = 'Geo Cache'
        icon_ = 'geometry_Cache.png'
        icon_path = cacheManagerIconPath + icon_
        geo_cache_button = self.sample_widget_template.pushButton(set_text=geo_cache_text,
                                                                  max_size=[self.sample_widget_template.max_size, button_height],
                                                                  set_icon=icon_path,
                                                                  set_icon_size=[self.icon_size, self.icon_size],
                                                                  connect=self.geo_cache_button_def)
        vertical_layout.addWidget(geo_cache_button)

        #DISCONNECT THE GEO CACHE BUTTON
        disconnect_geo_cache_text = 'Disconnect Geo Cache'
        icon_ = 'disConnectnGeoCache.png'
        icon_path = cacheManagerIconPath + icon_
        diconnect_the_geo_cache_button = self.sample_widget_template.pushButton(set_text=disconnect_geo_cache_text,
                                                                                max_size=[self.sample_widget_template.max_size, button_height],
                                                                      set_icon=icon_path,
                                                                      set_icon_size=[self.icon_size, self.icon_size])
        vertical_layout.addWidget(diconnect_the_geo_cache_button)

        #PLABLAST BUTTON
        playblast_button_text = 'Playblast'
        icon_ = 'PlayBlast.png'
        icon_path = cacheManagerIconPath + icon_
        playblast_button = self.sample_widget_template.pushButton(set_text=playblast_button_text,
                                                                  max_size=[self.sample_widget_template.max_size, button_height],
                                                                  set_icon=icon_path,
                                                                  set_icon_size=[self.icon_size, self.icon_size],
                                                                  connect=self.playblast_button_def)
        vertical_layout.addWidget(playblast_button)

        # FINCAL CACHE BUTTON
        final_cache_button_text = 'Final Cache'
        icon_ = 'Final.png'
        icon_path = cacheManagerIconPath + icon_
        final_cache_button = self.sample_widget_template.pushButton(set_text=final_cache_button_text,
                                                                    max_size=[self.sample_widget_template.max_size, button_height],
                                                                      set_icon=icon_path,
                                                                      set_icon_size=[self.icon_size, self.icon_size],
                                                                    connect=self.final_cache_button_def)
        vertical_layout.addWidget(final_cache_button)

        # MANUAL CACHE BUTTON
        manual_cache_button_text = 'Manual Cache'


        manual_cache_button = self.sample_widget_template.pushButton(set_text=manual_cache_button_text,
                                                                    max_size=[self.sample_widget_template.max_size,button_height],
                                                                     connect=self.manual_cache_button_def)
        vertical_layout.addWidget(manual_cache_button)


        return cloth_button_widget

    def cache_manager_data_def(self):
        '''
        CREATE A CACHE MANAGER NODE TO SAVE ALL THE UI DATA
        :return:
        '''

        if not cmds.objExists(self.cache_manager_data):
            cmds.createNode('transform', n=self.cache_manager_data)
            cmds.setAttr(self.cache_manager_data + ".hideOnPlayback", 1)

            #NOW CREATEA A ATTRIBUTE
            for each in [self.sim_start, self.sim_end, self.geo_cache_start, self.geo_cache_end,
                         self.playblast_start, self.playblast_end, self.final_start, self.final_end,
                         self.manual_start, self.manual_end]:
                self.attribute_class.add_attr(self.cache_manager_data, attribute_name=each, attribute_type=self.attribute_class.float)


            for each in [self.sim_path, self.geo_path, self.playblast_path, self.final_path, self.manual_path, self.camera]:
                self.attribute_class.add_attr(obj=self.cache_manager_data, attribute_name=each, attribute_type=self.attribute_class.string)


            for each in [self.ncloth_text, self.nrigit_text, self.nconstraint_text, self.nhair_text, self.folical_text]:
                self.attribute_class.add_attr(obj=self.cache_manager_data, attribute_name=each, attribute_type=self.attribute_class.boolean)

            cmds.setAttr((self.cache_manager_data + '.hideOnPlayback'), 1)
            cmds.setAttr((self.cache_manager_data + '.hiddenInOutliner'), 1)

            #


            #SET THE ATTRIBUTE
            self.set_cache_manger_data()



    def get_cache_manager_data(self):
        '''

        :return:
        '''

        if cmds.objExists(self.cache_manager_data):
            self.sim_start_val = cmds.getAttr(self.cache_manager_data + '.' + self.sim_start)
            self.sim_end_val = cmds.getAttr(self.cache_manager_data + '.' + self.sim_end)
            self.sim_cache_path = cmds.getAttr(self.cache_manager_data + '.' + self.sim_path)
            self.geo_cache_start_val = cmds.getAttr(self.cache_manager_data + '.' + self.geo_cache_start)
            self.geo_cache_end_val = cmds.getAttr(self.cache_manager_data + '.' + self.geo_cache_end)
            self.geo_cache_path = cmds.getAttr(self.cache_manager_data + '.' + self.geo_path)
            self.playblast_start_val = cmds.getAttr(self.cache_manager_data + '.' + self.playblast_start)
            self.playblast_end_val = cmds.getAttr(self.cache_manager_data + '.' + self.playblast_end)
            self.playblast_cache_path = cmds.getAttr(self.cache_manager_data + '.' + self.playblast_path)
            self.final_start_val = cmds.getAttr(self.cache_manager_data + '.' + self.final_start)
            self.final_end_val = cmds.getAttr(self.cache_manager_data + '.' + self.final_end)
            self.final_cache_path = cmds.getAttr(self.cache_manager_data + '.' + self.final_path)
            self.camera_name = cmds.getAttr(self.cache_manager_data + '.' + self.camera)
            self.ncloth_val = cmds.getAttr(self.cache_manager_data + '.' + self.ncloth_text)
            self.nrigid_val = cmds.getAttr(self.cache_manager_data + '.' + self.nrigit_text)
            self.nconstraint_val = cmds.getAttr(self.cache_manager_data + '.' + self.nconstraint_text)
            self.nhair_val = cmds.getAttr(self.cache_manager_data + '.' + self.nhair_text)
            self.folical_val = cmds.getAttr(self.cache_manager_data + '.' + self.folical_text)


    def set_cache_manger_data(self):
        '''
        SET THE CACHE MANAGER DATA FROM THE NODE WHICH IS THERE IN THE FILE
        :return:
        '''

        if cmds.objExists(self.cache_manager_data):

            cmds.setAttr(self.cache_manager_data + '.' + self.sim_start, self.sim_start_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.sim_end, self.sim_end_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.sim_path, self.sim_cache_path, type='string')
            cmds.setAttr(self.cache_manager_data + '.' + self.geo_cache_start, self.geo_cache_start_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.geo_cache_end, self.geo_cache_end_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.geo_path, self.geo_cache_path, type='string')
            cmds.setAttr(self.cache_manager_data + '.' + self.playblast_start, self.playblast_start_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.playblast_end, self.playblast_end_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.playblast_path, self.playblast_cache_path, type='string')
            cmds.setAttr(self.cache_manager_data + '.' + self.final_start, self.final_start_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.final_end, self.final_end_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.final_path, self.final_cache_path, type='string')
            cmds.setAttr(self.cache_manager_data + '.' + self.camera, self.camera_name, type='string')
            cmds.setAttr(self.cache_manager_data + '.' + self.manual_start, self.manual_start_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.manual_end, self.manual_end_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.manual_path, self.manual_cache_path, type='string')
            cmds.setAttr(self.cache_manager_data + '.' + self.ncloth_text, self.ncloth_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.nrigit_text, self.nrigid_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.nconstraint_text, self.nconstraint_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.nhair_text, self.nhair_val)
            cmds.setAttr(self.cache_manager_data + '.' + self.folical_text, self.folical_val)


    def cache_playblast_history_widget(self):
        '''

        :return:
        '''

        cache_playblast_history_widget = self.sample_widget_template.widget_def(self.upper_widget_splitter)

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=cache_playblast_history_widget)

        tab_widget = self.sample_widget_template.tab_widget(parent_self=cache_playblast_history_widget)
        vertical_layout.addWidget(tab_widget)

        # SIMCACHE TAB
        self.sim_cache_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        sim_cache_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.sim_cache_tab_widget)
        sim_cache_verticalLayout.addWidget(self.sim_cache_history_def())
        tab_widget.addTab(self.sim_cache_tab_widget, 'SimCache')

        # GEOCACHE TAB
        self.geo_cache_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        geo_cache_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.geo_cache_tab_widget)
        geo_cache_verticalLayout.addWidget(self.geo_cache_history_def())
        tab_widget.addTab(self.geo_cache_tab_widget, 'GeoCache')

        # PLAYBLAST TAB
        self.playblast_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        playblast_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.playblast_tab_widget)
        playblast_verticalLayout.addWidget(self.playblast_history_def())
        tab_widget.addTab(self.playblast_tab_widget, 'PlayBlast')

        #FINAL CACHE TAB
        self.final_cache_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        final_cache_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.final_cache_tab_widget)
        final_cache_verticalLayout.addWidget(self.final_cache_history_def())
        tab_widget.addTab(self.final_cache_tab_widget, 'Final Cache')

        # FINAL CACHE TAB
        self.manual_cache_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        manual_cache_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.manual_cache_tab_widget)
        manual_cache_verticalLayout.addWidget(self.manual_cache_history_def())
        tab_widget.addTab(self.manual_cache_tab_widget, 'Manual Cache')


        return cache_playblast_history_widget

    def comment_widget(self):
        '''

        :return:
        '''
        self.min_height = 0
        comments_widget = self.sample_widget_template.widget_def(self.lower_widget_splitter)
        comments_widget.resize(self.min_height, self.min_height)


        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=comments_widget)

        #COMMENTS PLAIN TEXT EDIT
        self.comments_plain_text_edit = self.sample_widget_template.plainTextEdit()
        self.comments_plain_text_edit.setPlaceholderText('Please Write and Comments on the cache or the playblast you Want')
        vertical_layout.addWidget(self.comments_plain_text_edit)

        return comments_widget

    def file_status_widget(self):
        '''

        :return:
        '''

        file_status_widget = self.sample_widget_template.widget_def(self.lower_widget_splitter)
        file_status_widget.resize(self.min_height, self.min_height)

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=file_status_widget)

        #TAB WIDGET
        tab_widget = self.sample_widget_template.tab_widget(parent_self=file_status_widget)
        vertical_layout.addWidget(tab_widget)

        # NOTES TAB
        self.notes_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        note_tab_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.notes_tab)
        note_tab_verticalLayout.addWidget(self.notes_tab_widget())
        tab_widget.addTab(self.notes_tab, 'Comments')

        # INFO
        self.info_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        info_tab_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.info_tab)
        info_tab_verticalLayout.addWidget(self.info_tab_widget())
        tab_widget.addTab(self.info_tab, 'Info')

        # PARAMETER
        self.parameter_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        param_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.parameter_tab)
        self.parameter_tree_widget = self.sample_widget_template.treeWidget()
        header = QTreeWidgetItem(["Object", "Value"])
        self.parameter_tree_widget.setHeaderItem(header)
        param_verticalLayout.addWidget(self.parameter_tree_widget)
        tab_widget.addTab(self.parameter_tab, 'Parm')

        return file_status_widget

    def notes_tab_widget(self):
        '''

        :return:
        '''
        notes_widget = self.sample_widget_template.widget_def()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=notes_widget)

        self.notes_plainTextEdit = self.sample_widget_template.plainTextEdit()
        self.notes_plainTextEdit.setReadOnly(True)
        verticalLayout.addWidget(self.notes_plainTextEdit)

        return notes_widget

    def info_tab_widget(self):
        '''

        :return:
        '''
        info_widget = self.sample_widget_template.widget_def()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=info_widget)

        new_value = 0
        vertical_val = 0

        # NAME LABEL
        name_text = 'Name : '.upper()
        name_label = self.sample_widget_template.label(set_text=name_text,
                                                       set_alighment='right')
        grid_layout.addWidget(name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        name_val_text = 'Name : '.upper()
        self.info_name_val_label = self.sample_widget_template.label()
        grid_layout.addWidget(self.info_name_val_label, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        file_path_text = 'FilePath : '.upper()
        file_path_label = self.sample_widget_template.label(set_text=file_path_text,
                                                            set_alighment='right')
        grid_layout.addWidget(file_path_label, vertical_val, new_value, 1, 1)
        new_value += 1

        file_path_val_text = 'FilePath : '.upper()
        self.info_file_path_val_label = self.sample_widget_template.label()
        grid_layout.addWidget(self.info_file_path_val_label, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        date_time_text = 'Date & Time : '.upper()
        date_time_label = self.sample_widget_template.label(set_text=date_time_text,
                                                            set_alighment='right')
        grid_layout.addWidget(date_time_label, vertical_val, new_value, 1, 1)
        new_value += 1

        date_time_val_text = 'FilePath : '.upper()
        self.info_date_time_val_label = self.sample_widget_template.label()
        grid_layout.addWidget(self.info_date_time_val_label, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        grid_layout.addItem(self.sample_widget_template.spaceItem(), vertical_val, new_value, 1, 1)

        return info_widget



    def sim_cache_history_def(self):
        '''

        :return:
        '''

        widget = self.sample_widget_template.widget_def()

        vertical_laout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #####################################
        #TIME RANGE WIDGET
        time_range_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(time_range_widget)

        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=time_range_widget)

        #TIME RANGE LABEL
        time_range_label = 'Time Range'
        time_range_label = self.sample_widget_template.label(set_text=time_range_label)
        horizontal_layout.addWidget(time_range_label)

        #START TIME
        self.sim_start_val = self.cache_manager_class.get_nucleus_start_frame()
        self.sim_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.sim_start_val),
                                                                             set_PlaceholderText='Set Start Time')
        self.sim_start_time_lineedit.setValidator(self.float_validator)
        self.sim_start_time_lineedit.textChanged.connect(self.sim_start_time_lineedit_def)

        horizontal_layout.addWidget(self.sim_start_time_lineedit)

        #END TIME
        if self.end_time_val > self.start_time_val:
            self.sim_end_val = self.end_time_val + 10
        else:
            self.sim_end_val = self.start_time_val + 10
        self.sim_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.sim_end_val), set_PlaceholderText='Set End Time')
        self.sim_end_time_lineedit.setValidator(self.float_validator)
        self.sim_end_time_lineedit.textChanged.connect(self.sim_end_time_lineedit_def)
        horizontal_layout.addWidget(self.sim_end_time_lineedit)

        self.sim_cache_path_checkbox = self.sample_widget_template.checkbox(set_text='Cache Path Lock',
                                                                            set_checked=True,
                                                                            stateChanged=self.sim_cache_path_checkbox_def)
        vertical_laout.addWidget(self.sim_cache_path_checkbox)

        ####################################
        #CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        #CACHE PATH LABEL
        cache_path_label_text = 'Cache Path'
        cache_path_label = self.sample_widget_template.label(set_text=cache_path_label_text)
        horizontal_layout.addWidget(cache_path_label)

        self.cache_path_lineedit = self.sample_widget_template.line_edit(set_text=self.sim_cache_path)

        self.cache_path_lineedit.textChanged.connect(self.cache_path_lineedit_def)
        self.cache_path_lineedit.setDisabled(True)
        horizontal_layout.addWidget(self.cache_path_lineedit)

        cache_path_button = self.sample_widget_template.pushButton(set_text='...',
                                                                   connect=self.cache_path_button_def)
        horizontal_layout.addWidget(cache_path_button)

        self.set_cache_manger_data()

        #####################################
        #REPLAVE CACHE
        replace_cache_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(replace_cache_widget)
        replace_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=replace_cache_widget)

        ####################################
        #LIST WIDGET
        self.sim_cache_list_widget = self.sample_widget_template.list_widget()
        self.sim_cache_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sim_cache_list_widget.customContextMenuRequested.connect(self.sim_cache_list_widget_contexMenu)
        self.sim_cache_list_widget.itemSelectionChanged.connect(self.sim_cache_list_widget_def)
        vertical_laout.addWidget(self.sim_cache_list_widget)
        self.update_sim_cache_listwidget()

        return widget

    def sim_cache_path_checkbox_def(self):
        '''

        :return:
        '''
        if self.sim_cache_path_checkbox.isChecked():
            self.cache_path_lineedit.setDisabled(True)
        else:
            self.cache_path_lineedit.setDisabled(False)

    def geo_cache_path_checkbox_def(self):
        '''

        :return:
        '''
        if self.geo_cache_path_checkbox.isChecked():
            self.geo_cache_lineedit.setDisabled(True)
        else:
            self.geo_cache_lineedit.setDisabled(False)

    def playblast_path_checkbox_def(self):
        '''

        :return:
        '''
        if self.playblast_path_checkbox.isChecked():
            self.playblast_path_lineedit.setDisabled(True)
        else:
            self.playblast_path_lineedit.setDisabled(False)

    def final_cache_path_checkbox_def(self):
        '''

        :return:
        '''
        if self.final_cache_path_checkbox.isChecked():
            self.final_cache_path_lineedit.setDisabled(True)
        else:
            self.final_cache_path_lineedit.setDisabled(False)

    def manual_cache_path_checkbox_def(self):
        '''

        :return:
        '''
        if self.manual_cache_path_checkbox.isChecked():
            self.manual_cache_path_lineedit.setDisabled(True)
        else:
            self.manual_cache_path_lineedit.setDisabled(False)


    def geo_cache_history_def(self):
        '''

        :return:
        '''

        widget = self.sample_widget_template.widget_def()

        vertical_laout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #####################################
        #TIME RANGE WIDGET
        time_range_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(time_range_widget)

        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=time_range_widget)

        #TIME RANGE LABEL
        time_range_label = 'Time Range'
        time_range_label = self.sample_widget_template.label(set_text=time_range_label)
        horizontal_layout.addWidget(time_range_label)

        #START TIME
        self.geo_cache_start_val = self.start_time_val - self.buffer_val
        self.geo_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.geo_cache_start_val),
                                                                             set_PlaceholderText='Set Start Time')
        self.geo_start_time_lineedit.setValidator(self.float_validator)
        self.geo_start_time_lineedit.textChanged.connect(self.geo_start_time_lineedit_def)
        horizontal_layout.addWidget(self.geo_start_time_lineedit)

        #END TIME
        if self.end_time_val > self.geo_cache_start_val:
            self.geo_cache_end_val = self.end_time_val + self.buffer_val
        else:
            self.geo_cache_end_val = self.geo_cache_start_val + self.buffer_val

        self.geo_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.geo_cache_end_val),
                                                                      set_PlaceholderText='Set End Time')
        self.geo_end_time_lineedit.setValidator(self.float_validator)
        self.geo_end_time_lineedit.textChanged.connect(self.geo_end_time_lineedit_def)
        horizontal_layout.addWidget(self.geo_end_time_lineedit)

        self.geo_cache_path_checkbox = self.sample_widget_template.checkbox(set_text='Cache Path Lock',
                                                                            set_checked=True,
                                                                            stateChanged=self.geo_cache_path_checkbox_def)
        vertical_laout.addWidget(self.geo_cache_path_checkbox)

        ####################################
        #CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        #CACHE PATH LABEL
        cache_path_label_text = 'Cache Path'
        cache_path_label = self.sample_widget_template.label(set_text=cache_path_label_text)
        horizontal_layout.addWidget(cache_path_label)

        self.geo_cache_lineedit = self.sample_widget_template.line_edit(set_text=self.geo_cache_path)
        self.geo_cache_lineedit.textChanged.connect(self.geo_cache_lineedit_def)
        self.geo_cache_lineedit.setDisabled(True)
        horizontal_layout.addWidget(self.geo_cache_lineedit)

        #GEO CACH BROWSE
        geo_cache_path_browse_button = self.sample_widget_template.pushButton(set_text='...',
                                                                              connect=self.geo_cache_path_browse_button_def)
        horizontal_layout.addWidget(geo_cache_path_browse_button)


        ####################################
        #LIST WIDGET
        self.geo_cache_list_widget = self.sample_widget_template.list_widget()
        self.geo_cache_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.geo_cache_list_widget.customContextMenuRequested.connect(self.geo_cache_list_widget_contexMenu)
        self.geo_cache_list_widget.itemSelectionChanged.connect(self.geo_cache_list_widget_def)

        vertical_laout.addWidget(self.geo_cache_list_widget)
        self.update_geo_cache_listwidget()
        self.set_cache_manger_data()

        return widget

    def geo_cache_list_widget_def(self):
        '''

        :return:
        '''
        item = self.geo_cache_list_widget.selectedItems()[0]
        json_path = self.geo_cache_path + '/' + item.text() + '.json'

        file_path = json_path.replace('json', 'mcx')

        with open(json_path) as f:
            data = json.load(f)
            self.update_ui_json_read(data, file_name=item.text(), file_path=file_path, param=False)


    def playblast_list_widget_def(self):
        '''

        :return:
        '''
        item = self.playblast_list_widget.selectedItems()[0]
        json_path = self.playblast_cache_path + '/' + item.text() + '.json'

        file_path = json_path.replace('json', 'mov')

        with open(json_path) as f:
            data = json.load(f)
            self.update_ui_json_read(data, file_name=item.text(), file_path=file_path, param=False)

    def playblast_list_widget_doubleclicked_def(self):
        print('Double Clicked ')

    def final_cache_list_widget_def(self):
        '''

        :return:
        '''
        item = self.final_cache_list_widget.selectedItems()[0]
        json_path = self.final_cache_path + '/' + item.text() + '/' + item.text() + '.json'

        file_path = json_path.replace('json', 'abc')

        with open(json_path) as f:
            data = json.load(f)
            self.update_ui_json_read(data, file_name=item.text(), file_path=file_path, param=False)

    def manual_cache_list_widget_def(self):
        '''

        :return:
        '''
        item = self.manual_cache_list_widget.selectedItems()[0]
        json_path = self.manual_cache_path + '/' + item.text() + '/' + item.text() + '.json'

        file_path = json_path.replace('json', 'abc')

        with open(json_path) as f:
            data = json.load(f)
            self.update_ui_json_read(data, file_name=item.text(), file_path=file_path, param=False)


    def playblast_history_def(self):
        '''

        :return:
        '''

        widget = self.sample_widget_template.widget_def()

        vertical_laout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #####################################
        #TIME RANGE WIDGET
        time_range_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(time_range_widget)

        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=time_range_widget)

        #TIME RANGE LABEL
        time_range_label = 'Time Range'
        time_range_label = self.sample_widget_template.label(set_text=time_range_label)
        horizontal_layout.addWidget(time_range_label)

        #START TIME
        self.playblast_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.playblast_start_val),
                                                                        set_PlaceholderText='Set Start Time')

        self.playblast_start_time_lineedit.setValidator(self.float_validator)
        self.playblast_start_time_lineedit.textChanged.connect(self.playblast_start_time_lineedit_def)
        horizontal_layout.addWidget(self.playblast_start_time_lineedit)

        # END TIME
        if self.end_time_val > self.playblast_start_val:
            self.playblast_end_val = self.end_time_val + self.buffer_val
        else:
            self.playblast_end_val = self.playblast_start_val + self.buffer_val


        self.playblast_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.playblast_end_val), set_PlaceholderText='Set End Time')
        self.playblast_end_time_lineedit.setValidator(self.float_validator)
        self.playblast_end_time_lineedit.textChanged.connect(self.playblast_end_time_lineedit_def)
        horizontal_layout.addWidget(self.playblast_end_time_lineedit)

        self.playblast_path_checkbox = self.sample_widget_template.checkbox(set_text='Playblast Path Lock',
                                                                            set_checked=True,
                                                                            stateChanged=self.playblast_path_checkbox_def)
        vertical_laout.addWidget(self.playblast_path_checkbox)

        ####################################
        #CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        #CACHE PATH LABEL
        playblast_path_label_text = 'Playblast Path'
        playblast_path_label = self.sample_widget_template.label(set_text=playblast_path_label_text)
        horizontal_layout.addWidget(playblast_path_label)

        self.playblast_path_lineedit = self.sample_widget_template.line_edit(set_text=self.playblast_cache_path)
        self.playblast_path_lineedit.textChanged.connect(self.playblast_path_lineedit_def)
        self.playblast_path_lineedit.setDisabled(True)
        horizontal_layout.addWidget(self.playblast_path_lineedit)

        # PLAYBLAST BROWSE
        playblast_path_browse_button = self.sample_widget_template.pushButton(set_text='...',
                                                                              connect=self.playblast_path_browse_button_def)
        horizontal_layout.addWidget(playblast_path_browse_button)


        #CAM WIDGET
        cam_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cam_widget)

        grid_layout = self.sample_widget_template.grid_layout(parent_self=cam_widget)
        new_value = 0
        vertical_val = 0

        #CAMERA LABEL
        camera_label_text = 'Camera'
        camera_label = self.sample_widget_template.label(set_text=camera_label_text)
        grid_layout.addWidget(camera_label, vertical_val, new_value, 1, 1)
        new_value += 1

        #CAMERA COMBOXBOX
        self.camera_combobox = self.sample_widget_template.comboBox(addItems=self.cam_list)

        self.camera_combobox.currentIndexChanged.connect(self.camera_combobox_def)
        grid_layout.addWidget(self.camera_combobox, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        #PLAUBLAST SETTING BUTTON
        playblast_setting_button_text = 'Playblast Setting'
        playblast_setting_button = self.sample_widget_template.pushButton(set_text=playblast_setting_button_text,
                                                                          connect=self.playblast_setting_button_def)
        grid_layout.addWidget(playblast_setting_button, vertical_val, new_value, 1, 2)
        new_value += 1


        ####################################
        #LIST WIDGET
        self.playblast_list_widget = self.sample_widget_template.list_widget()
        self.update_playblast_list_widget()
        self.playblast_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playblast_list_widget.customContextMenuRequested.connect(self.playblast_list_widget_contexMenu)
        self.playblast_list_widget.itemSelectionChanged.connect(self.playblast_list_widget_def)
        self.playblast_list_widget.doubleClicked.connect(self.playblast_openFile_def)
        vertical_laout.addWidget(self.playblast_list_widget)

        self.set_cache_manger_data()

        return widget

    def camera_combobox_def(self, index):
        '''

        :param index:
        :return:
        '''
        self.camera_name = self.camera_combobox.currentText()
        self.set_cache_manger_data()


    def final_cache_history_def(self):
        '''

        :return:
        '''

        widget = self.sample_widget_template.widget_def()

        vertical_laout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #####################################
        #TIME RANGE WIDGET
        time_range_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(time_range_widget)

        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=time_range_widget)

        #TIME RANGE LABEL
        time_range_label = 'Time Range'
        time_range_label = self.sample_widget_template.label(set_text=time_range_label)
        horizontal_layout.addWidget(time_range_label)

        #START TIME
        self.final_start_val = self.start_time_val - self.buffer_val
        self.final_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.final_start_val), set_PlaceholderText='Set Start Time')
        self.final_start_time_lineedit.setValidator(self.float_validator)
        self.final_start_time_lineedit.textChanged.connect(self.final_start_time_lineedit_def)
        horizontal_layout.addWidget(self.final_start_time_lineedit)

        # END TIME
        if self.end_time_val > self.final_start_val:
            self.final_end_val = self.end_time_val + self.buffer_val
        else:
            self.final_end_val = self.final_start_val + self.buffer_val

        self.final_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.final_end_val), set_PlaceholderText='Set End Time')
        self.final_end_time_lineedit.setValidator(self.float_validator)
        self.final_end_time_lineedit.textChanged.connect(self.final_end_time_lineedit_def)
        horizontal_layout.addWidget(self.final_end_time_lineedit)

        self.final_cache_path_checkbox = self.sample_widget_template.checkbox(set_text='Final Cache Path Lock',
                                                                            set_checked=True,
                                                                            stateChanged=self.final_cache_path_checkbox_def)
        vertical_laout.addWidget(self.final_cache_path_checkbox)

        ####################################
        #CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        #CACHE PATH LABEL
        cache_path_label_text = 'Final Cache Path'
        cache_path_label = self.sample_widget_template.label(set_text=cache_path_label_text)
        horizontal_layout.addWidget(cache_path_label)

        self.final_cache_path_lineedit = self.sample_widget_template.line_edit(set_text=self.final_cache_path)
        self.final_cache_path_lineedit.textChanged.connect(self.final_cache_path_lineedit_def)
        self.final_cache_path_lineedit.setDisabled(True)
        horizontal_layout.addWidget(self.final_cache_path_lineedit)

        #FINAL CACHE BROWSE
        final_cache_browse_button = self.sample_widget_template.pushButton(set_text='...',
                                                                           connect=self.final_cache_browse_button_def)
        horizontal_layout.addWidget(final_cache_browse_button)


        ####################################
        #LIST WIDGET
        self.final_cache_list_widget = self.sample_widget_template.list_widget()
        self.final_cache_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.final_cache_list_widget.customContextMenuRequested.connect(self.final_cache_list_widget_contexMenu)
        self.final_cache_list_widget.itemSelectionChanged.connect(self.final_cache_list_widget_def)
        self.update_final_list_widget()
        vertical_laout.addWidget(self.final_cache_list_widget)

        self.set_cache_manger_data()

        return widget


    def manual_cache_history_def(self):
        '''

        :return:
        '''
        widget = self.sample_widget_template.widget_def()

        vertical_laout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #####################################
        # TIME RANGE WIDGET
        time_range_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(time_range_widget)

        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=time_range_widget)

        # TIME RANGE LABEL
        time_range_label = 'Time Range'
        time_range_label = self.sample_widget_template.label(set_text=time_range_label)
        horizontal_layout.addWidget(time_range_label)

        # START TIME
        self.manual_start_val = self.start_time_val - self.buffer_val
        self.manual_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.manual_start_val),
                                                                          set_PlaceholderText='Set Start Time')
        self.manual_start_time_lineedit.setValidator(self.float_validator)
        self.manual_start_time_lineedit.textChanged.connect(self.manual_start_time_lineedit_def)
        horizontal_layout.addWidget(self.manual_start_time_lineedit)

        # END TIME
        if self.end_time_val > self.final_start_val:
            self.manual_end_val = self.end_time_val + self.buffer_val
        else:
            self.manual_end_val = self.final_start_val + self.buffer_val

        self.manual_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.final_end_val),
                                                                        set_PlaceholderText='Set End Time')
        self.manual_end_time_lineedit.setValidator(self.float_validator)
        self.manual_end_time_lineedit.textChanged.connect(self.manual_end_time_lineedit_def)
        horizontal_layout.addWidget(self.manual_end_time_lineedit)

        self.manual_cache_path_checkbox = self.sample_widget_template.checkbox(set_text='Final Cache Path Lock',
                                                                              set_checked=True,
                                                                              stateChanged=self.manual_cache_path_checkbox_def)
        vertical_laout.addWidget(self.manual_cache_path_checkbox)


        ####################################
        # CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        # CACHE PATH LABEL
        cache_path_label_text = 'Final Cache Path'
        cache_path_label = self.sample_widget_template.label(set_text=cache_path_label_text)
        horizontal_layout.addWidget(cache_path_label)

        self.manual_cache_path_lineedit = self.sample_widget_template.line_edit(set_text=self.manual_cache_path)
        self.manual_cache_path_lineedit.textChanged.connect(self.manual_cache_path_lineedit_def)
        self.manual_cache_path_lineedit.setDisabled(True)
        horizontal_layout.addWidget(self.manual_cache_path_lineedit)

        # MANUAL CACHE BROWSE
        manual_cache_browse_button = self.sample_widget_template.pushButton(set_text='...',
                                                                           connect=self.manaul_cache_browse_button_def)
        horizontal_layout.addWidget(manual_cache_browse_button)

        ####################################
        # LIST WIDGET
        self.manual_cache_list_widget = self.sample_widget_template.list_widget()
        self.manual_cache_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.manual_cache_list_widget.customContextMenuRequested.connect(self.manual_cache_list_widget_contexMenu)
        self.manual_cache_list_widget.itemSelectionChanged.connect(self.manual_cache_list_widget_def)
        self.update_manual_list_widget()
        vertical_laout.addWidget(self.manual_cache_list_widget)

        self.set_cache_manger_data()

        return widget



    def tree_on_off_icon_color(self, value):
        if value == 0:
            icon_path = self.off_icon_path
            styleSheet_color = self.color_variable_class.red_color.get_value()
        else:
            icon_path = self.on_icon_path
            styleSheet_color = self.color_variable_class.green_color.get_value()

        return icon_path, styleSheet_color

    def sim_tree_def(self):
        '''

        :return:
        '''
        self.sim_tree_widget_item['nCloth'] = []
        cfx_list = self.cache_manager_class.get_cfx_list()

        for each_cfx_list in cfx_list:

            nucleus = QTreeWidgetItem(self.sim_tree_widget)
            nucleus.setText(0, each_cfx_list)
            #setForeground(0, QtGui.QBrush(Qt.green))
            nucleus.setForeground(0, QBrush(QColor(self.color_variable_class.green_color.get_value()[0],
                                                   self.color_variable_class.green_color.get_value()[1],
                                                   self.color_variable_class.green_color.get_value()[2])))


            nucleus_set_obj = each_cfx_list + '_Object'

            icon_path, styleSheet_color = self.tree_on_off_icon_color(cmds.getAttr(each_cfx_list + '.enable'))

            styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nucleus_set_obj,
                                                                    background_color=styleSheet_color)
            
            nucleus_button = self.sample_widget_template.pushButton(parent_self=self.sim_tree_widget,
                                                                    set_icon=icon_path,
                                                                    set_icon_size=[20, 20],
                                                                    set_styleSheet=styleSheet,
                                                                    set_object_name=nucleus_set_obj)

            nucleus_button.clicked.connect(partial(self.nucleus_button, each_cfx_list,  nucleus_button))

            self.sim_tree_widget.setItemWidget(nucleus, 1, nucleus_button)


            #CHECK THE NCLOTH
            if self.ncloth_tree_vis:
                if cfx_list[each_cfx_list]['nCloth']:
                    for each_nCloth in cfx_list[each_cfx_list]['nCloth']:

                        ncloth_item = QTreeWidgetItem(nucleus)
                        ncloth_item.setText(0, each_nCloth)
                        ncloth_item.setForeground(0, QBrush(QColor(self.color_variable_class.nCloth_color.get_value()[0],
                                                                   self.color_variable_class.nCloth_color.get_value()[1],
                                                                   self.color_variable_class.nCloth_color.get_value()[2])))
                        self.ncloth_tree_widget_item.append(ncloth_item)

                        icon_ = 'ncloth.svg'
                        icon_path = rigfxIconPath_ + icon_
                        icon = QIcon()
                        icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
                        ncloth_item.setIcon(0, icon)

                        ncloth_set_obj = each_nCloth + '_Object'
                        icon_path, styleSheet_color = self.tree_on_off_icon_color(cmds.getAttr(each_nCloth + '.isDynamic'))
                        styleSheet = self.sample_widget_template.styleSheet_def(obj_name=ncloth_set_obj,
                                                                                background_color=styleSheet_color)
                        ncloth_button = self.sample_widget_template.pushButton(parent_self=self.sim_tree_widget,
                                                                               set_icon=icon_path,
                                                                               set_icon_size=[20, 20],
                                                                               set_styleSheet=styleSheet,
                                                                               set_object_name=ncloth_set_obj)
                        ncloth_button.clicked.connect(partial(self.nucleus_button, each_nCloth, ncloth_button))
                        self.sim_tree_widget.setItemWidget(ncloth_item, 1, ncloth_button)

            if self.nConstraint_tree_vis:
                if cfx_list[each_cfx_list]['dynamicConstraint']:
                    for each_dynamicConstraint in cfx_list[each_cfx_list]['dynamicConstraint']:
                        shape = cmds.listRelatives(each_dynamicConstraint, s=True)[0]
                        dynamicConstraint_item = QTreeWidgetItem(nucleus)
                        dynamicConstraint_item.setForeground(0, QBrush(QColor(self.color_variable_class.nConstraint_color.get_value()[0],
                                                                              self.color_variable_class.nConstraint_color.get_value()[1],
                                                                              self.color_variable_class.nConstraint_color.get_value()[2])))
                        icon_ = 'out_dynamicConstraint.png'
                        icon_path = rigfxIconPath_ + icon_
                        icon = QIcon()
                        icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
                        dynamicConstraint_item.setIcon(0, icon)

                        dynamicConstraint_item.setText(0, each_dynamicConstraint)
                        dynamicConstraint_set_obj = each_dynamicConstraint + '_Object'
                        icon_path, styleSheet_color = self.tree_on_off_icon_color(cmds.getAttr(each_dynamicConstraint + '.enable'))
                        styleSheet = self.sample_widget_template.styleSheet_def(obj_name=dynamicConstraint_set_obj,
                                                                                background_color=styleSheet_color)
                        dynamicConstraint_button = self.sample_widget_template.pushButton(parent_self=self.sim_tree_widget, set_icon=icon_path,
                                                                                          set_icon_size=[20, 20],
                                                                                          set_styleSheet=styleSheet,
                                                                                          set_object_name=dynamicConstraint_set_obj)
                        dynamicConstraint_button.clicked.connect(partial(self.nucleus_button, each_dynamicConstraint, dynamicConstraint_button))
                        self.sim_tree_widget.setItemWidget(dynamicConstraint_item, 1, dynamicConstraint_button)

            if self.nRigit_tree_vis:
                if cfx_list[each_cfx_list]['nRigid']:
                    for each_nRigid in cfx_list[each_cfx_list]['nRigid']:
                        nRigid_item = QTreeWidgetItem(nucleus)
                        nRigid_item.setText(0, each_nRigid)
                        nRigid_item.setForeground(0, QBrush(QColor(self.color_variable_class.nRigit_color.get_value()[0],
                                                                   self.color_variable_class.nRigit_color.get_value()[1],
                                                                   self.color_variable_class.nRigit_color.get_value()[2])))
                        icon_ = 'nRigid1.svg'
                        icon_path = rigfxIconPath_ + icon_
                        icon = QIcon()
                        icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
                        nRigid_item.setIcon(0, icon)


                        nRigid_set_obj = each_nRigid + '_Object'
                        icon_path, styleSheet_color = self.tree_on_off_icon_color(cmds.getAttr(each_nRigid + '.isDynamic'))
                        styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nRigid_set_obj,
                                                                                background_color=styleSheet_color)
                        nRigid_button = self.sample_widget_template.pushButton(parent_self=self.sim_tree_widget,set_icon=icon_path,
                                                                                set_icon_size=[20, 20],
                                                                                set_styleSheet=styleSheet,
                                                                                set_object_name=nRigid_set_obj)
                        nRigid_button.clicked.connect(partial(self.nucleus_button, each_nRigid, nRigid_button))
                        self.sim_tree_widget.setItemWidget(nRigid_item, 1, nRigid_button)

            if self.nhair_tree_vis:
                if cfx_list[each_cfx_list]['hairSystem']:
                    for each_hairSystem in cfx_list[each_cfx_list]['hairSystem']:
                        hairSystem_item = QTreeWidgetItem(nucleus)
                        hairSystem_item.setText(0, each_hairSystem)
                        hairSystem_item.setForeground(0, QBrush(QColor(self.color_variable_class.nHair_color.get_value()[0],
                                                                   self.color_variable_class.nHair_color.get_value()[1],
                                                                   self.color_variable_class.nHair_color.get_value()[2])))
                        icon_ = 'hairSystem1.svg'
                        icon_path = rigfxIconPath_ + icon_
                        icon = QIcon()
                        icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
                        hairSystem_item.setIcon(0, icon)


                        if cmds.getAttr(each_hairSystem + '.simulationMethod') == 0:
                            value = 0
                        else:
                            value = 1

                        hairSystem_set_obj = each_hairSystem + '_Object'
                        icon_path, styleSheet_color = self.tree_on_off_icon_color(value)
                        styleSheet = self.sample_widget_template.styleSheet_def(obj_name=hairSystem_set_obj,
                                                                                background_color=styleSheet_color)
                        hairSystem_button = self.sample_widget_template.pushButton(parent_self=self.sim_tree_widget, set_icon=icon_path,
                                                                                set_icon_size=[20, 20],
                                                                                set_styleSheet=styleSheet,
                                                                                set_object_name=hairSystem_set_obj)
                        self.sim_tree_widget.setItemWidget(hairSystem_item, 1, hairSystem_button)

                        #SET THE FOLLICLE
                        if self.follicle1_tree_vis:
                            hairsystem_shape = cmds.listRelatives(each_hairSystem, s=True)[0]
                            follicle_list = list(set(cmds.listConnections(hairsystem_shape, type='follicle')))
                            for each_follicle in follicle_list:
                                follicle_item = QTreeWidgetItem(hairSystem_item)
                                follicle_item.setText(0, each_follicle)
                                follicle_item.setForeground(0, QBrush(QColor(self.color_variable_class.folical_color.get_value()[0],
                                                                             self.color_variable_class.folical_color.get_value()[1],
                                                                         self.color_variable_class.folical_color.get_value()[2])))
                        hairSystem_item.setExpanded(True)

            nucleus.setExpanded(True)
            
    def nucleus_button(self, nucleus_name, nucleus_button):
        '''

        :param nucleus_name:
        :return:
        '''

        rgbcolor = nucleus_button.palette().button().color().getRgb()
        color = [rgbcolor[0], rgbcolor[1], rgbcolor[2]]
        if color == self.color_variable_class.green_color.get_value():
            try:
                cmds.setAttr(nucleus_name + '.enable', 0)
                val = cmds.getAttr(nucleus_name + '.enable')
            except:
                cmds.setAttr(nucleus_name + '.isDynamic', 0)
                val = cmds.getAttr(nucleus_name + '.isDynamic')
            #CHANGE THE COLOR




            icon_path, styleSheet_color = self.tree_on_off_icon_color(val)
            styleSheet = self.sample_widget_template.styleSheet_def(obj_name =nucleus_button.objectName(),
                                                                    background_color=styleSheet_color)
            nucleus_button.setStyleSheet(styleSheet)
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
            nucleus_button.setIcon(icon)


        else:
            try:
                cmds.setAttr(nucleus_name + '.enable', 1)
                val = cmds.getAttr(nucleus_name + '.enable')
            except:
                cmds.setAttr(nucleus_name + '.isDynamic', 1)
                val = cmds.getAttr(nucleus_name + '.isDynamic')

            icon_path, styleSheet_color = self.tree_on_off_icon_color(val)
            styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nucleus_button.objectName(),
                                                                    background_color=styleSheet_color)
            nucleus_button.setStyleSheet(styleSheet)
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
            nucleus_button.setIcon(icon)




    def sim_tree_widget_def(self):
        '''
        select the object
        :return:
        '''
        getSelected = self.sim_tree_widget.selectedItems()
        obj = []
        if getSelected:
            a = 0
            for each in getSelected:
                baseNode = getSelected[a]
                getChildNode = baseNode.text(0)
                if cmds.objExists(getChildNode):
                    obj.append(getChildNode)
                a+=1
        if obj:
            cmds.select(obj)



    def input_list_def(self):
        '''

        :return:
        '''
        self.input_list_widget = self.sample_widget_template.list_widget()
        self.input_list_widget.itemSelectionChanged.connect(self.input_list_widget_def)
        self.input_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        input_list = self.rig_fx_class.get_obj_type('Input')
        if input_list:
            for each_input in input_list:
                shape = cmds.listRelatives(each_input, s=True)
                if shape:
                    self.input_list_widget.addItem(each_input)

            '''
            print('thi sis input list: ', input_list)
            grp_name = input_list[0]
            print('this is the grpname: ', grp_name)
            all_input_child = cmds.listRelatives(grp_name, c=True, ad=True, fullPath=True)
            print('this is inputs: ', all_input_child)
            if all_input_child:
                for each in all_input_child:
                    if cmds.objectType(each) != 'transform':
                        parent_obj = cmds.listRelatives(each, p=True, fullPath=True)[0]
                        self.input_list_widget.addItem(parent_obj)

            '''
        return self.input_list_widget

    def input_list_widget_def(self):
        '''

        :return:
        '''
        items = self.input_list_widget.selectedItems()
        item_list = []
        for each in items:
            item_text = each.text()
            if cmds.objExists(item_text):
                item_list.append(item_text)

        cmds.select(item_list)


    def output_list_def(self):
        '''

        :return:
        '''

        self.output_list_widget = self.sample_widget_template.list_widget()
        self.output_list_widget.itemSelectionChanged.connect(self.output_list_widget_def)
        self.output_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        output_list = self.rig_fx_class.get_obj_type('Final')
        if output_list:
            for each_input in output_list:
                shape = cmds.listRelatives(each_input, s=True)
                if shape:
                    self.output_list_widget.addItem(each_input)

        return self.output_list_widget

    def output_list_widget_def(self):
        '''

        :return:
        '''
        items = self.output_list_widget.selectedItems()
        item_list = []
        for each in items:
            item_text = each.text()
            if cmds.objExists(item_text):
                item_list.append(item_text)

        cmds.select(item_list)


    def ncloth_cache_def(self):
        '''

        :return:
        '''
        #GET ALL THE CLOTH
        # GET CACHE IS GOING TO REPLACE OR NOT
        if self.select_ncloth_node_checkbox.isChecked():

            nHair = cmds.ls(type='hairSystem')
            nCloth = cmds.ls(type='nCloth')
            #nCloth.extend(nHair)
            sel_ncloth = []
            for each in [nCloth, nHair]:
                if each:
                    for each_obj in each:
                        sel_ncloth.append(cmds.listRelatives(each_obj, p=True)[0])

        else:
            selected_val = True
            sel_ncloth = cmds.ls(sl=True)
            for each in sel_ncloth:
                shape = cmds.listRelatives(each, s=True)
                if cmds.objectType(shape) != 'nCloth' or cmds.objectType(shape) != 'hairSystem':
                    sel_ncloth.remove(each)

        attr_list = {}
        start_val = float(self.sim_start_time_lineedit.text())
        end_val = float(self.sim_end_time_lineedit.text())
        attr_list['Comments'] = self.comments_plain_text_edit.toPlainText()
        sim_path = self.cache_path_lineedit.text()

        nucleus = cmds.ls(type='nucleus')

        #NCLOTH
        nCloth = cmds.ls(type='nCloth')

        #NRIGIT
        nRigid = cmds.ls(type='nRigid')

        #NCONSTRAINT
        dynamicConstraint = cmds.ls(type='dynamicConstraint')

        #nHair
        hairSystem = cmds.ls(type='hairSystem')

        #folicle
        follicle = cmds.ls(type='follicle')

        for each_object in [nucleus, nCloth, nRigid, dynamicConstraint, hairSystem, follicle]:
            if each_object:
                for each_subObject in each_object:
                    attr_list[each_subObject] = self.attribute_class.get_all_attr_val(each_subObject)


        self.cache_manager_class.ncloth_cache_def(ncloth_list=sel_ncloth,
                                                  start_val=start_val,
                                                  end_val=end_val,
                                                  sim_path=sim_path,
                                                  attr_list=attr_list)

        self.update_sim_cache_listwidget()
        self.comments_plain_text_edit.clear()


        '''
        #GET CACHE IS GOING TO REPLACE OR NOT
        if self.replace_checkbox.isChecked():
            replace_val = True
        else:
            replace_val = False

        if self.select_ncloth_node_checkbox.isChecked():
            selected_val = False
        else:
            selected_val = True


        sim_start_time_val = float(self.sim_start_time_lineedit.text())
        sim_end_time_val = float(self.sim_end_time_lineedit.text())
        comments = self.comments_plain_text_edit.toPlainText()
        self.cache_manager_class.ncloth_cache_def(replace=replace_val,
                                                  selected=selected_val,
                                                  sim_start_frame=sim_start_time_val,
                                                  sim_end_frame=sim_end_time_val,
                                                  notes=comments)


        self.update_sim_cache_listwidget()
        '''

    def playblast_button_def(self):
        '''

        :return:
        '''
        current_start_frame, current_end_frame = self.cache_manager_class.set_frames(new_start_frame=self.playblast_start_val,
                                                                 new_end_frame=self.playblast_end_val)

        all_panel = cmds.getPanel(type='modelPanel')
        for each_panel in all_panel:
            try:
                cmds.modelEditor(each_panel, e=True, alo=False)
                cmds.modelEditor(each_panel, e=True, pm=True, nurbsCurves=True)
                if cmds.ls(type='hairSystem'):
                    cmds.modelEditor(each_panel, e=True, nurbsCurves=True)
                mel.eval('lookThroughModelPanel %s %s;' % (self.camera_name, each_panel))
            except:
                pass
        # playblast  -format qt -filename "movies/clothOne.mov" -forceOverwrite  -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 100 -compression "H.264" -quality 100;
        #file_name = self.get_file_name() + '_' + str(len(file_path_list)) + '_Sim_Cache'
        onlyfiles = [f for f in listdir(self.playblast_cache_path) if isfile(join(self.playblast_cache_path, f))]
        file_path_list = []

        for each in onlyfiles:
            if '.mov' in each:
                if self.cache_manager_class.get_file_name() in each:
                    file_path_list.append(each)
        name = self.playblast_cache_path + '/' + self.cache_manager_class.get_file_name() + '_' + str(len(file_path_list)) + '_PlayBlast'
        file_name = name + '.mov'
        json_name = name + '.json'

        self.playblast_format_list = ['qt', 'avi', 'image']
        self.playblast_format = self.playblast_format_list[0]
        self.encodeing_list = ['Planer RGB', 'Sorenson Video', 'Sorenson Video 3', 'BMP', 'H.264', 'Cinepak',
                               'DV/DVCPRO-NTSC', 'DV-PAL']
        self.encodeing = self.encodeing_list[4]
        self.quality = 100
        self.frame_padding = 4
        self.percent = 100

        cmds.playblast(format=self.playblast_format, forceOverwrite=True, p=self.percent, sequenceTime=0, clearCache=True, viewer=True, showOrnaments=True, s="ohNo",
                       compression=self.encodeing, quality=self.quality, f=file_name, framePadding=self.frame_padding)

        for each_panel in all_panel:
            cmds.modelEditor(each_panel, e=True, alo=True)

        self.update_playblast_list_widget()

        #UPDATE THE JSON PATH
        attr_list= {}
        attr_list['Comments'] = self.comments_plain_text_edit.toPlainText()
        with open(json_name, 'w') as f:
            json.dump(attr_list, f)

        cmds.playbackOptions(minTime=current_start_frame, maxTime=current_end_frame)
        self.comments_plain_text_edit.clear()

    def final_cache_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if not sel_obj:
            raise Exception('Please select object to export the final cache')

        current_start_frame, current_end_frame = self.cache_manager_class.set_frames(new_start_frame=self.final_start_val,
                                                                                     new_end_frame=self.final_end_val)

        #CREATE A FOLDER AND EXPORT ABC FILE IN THAT
        list_dir = os.listdir(self.final_cache_path)
        final_cache_name = 'Final_Cache_' + str(len(list_dir) + 1)
        folder_path = self.final_cache_path + '/' + final_cache_name
        os.mkdir(folder_path)

        name = folder_path + '/' + final_cache_name
        file_path = name + '.abc'
        json_name = name + '.json'

        self.geo_cache_class.export_abc_file(start_frame=self.final_start_val,
                                             end_frame=self.final_end_val,
                                             char_list=sel_obj,
                                             abc_file_path=file_path)

        self.update_final_list_widget()

        # UPDATE THE JSON PATH
        attr_list = {}
        attr_list['Comments'] = self.comments_plain_text_edit.toPlainText()
        with open(json_name, 'w') as f:
            json.dump(attr_list, f)

        self.comments_plain_text_edit.clear()

        cmds.playbackOptions(minTime=current_start_frame, maxTime=current_end_frame)

    def manual_cache_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if not sel_obj:
            raise Exception('Please select object to export the final cache')

        current_start_frame, current_end_frame = self.cache_manager_class.set_frames(new_start_frame=self.manual_start_val,
                                                                                     new_end_frame=self.manual_end_val)


        # CREATE A FOLDER AND EXPORT ABC FILE IN THAT
        list_dir = os.listdir(self.manual_cache_path)
        manual_cache_name = 'Manual_Cache_' + str(len(list_dir) + 1)
        folder_path = self.manual_cache_path + '/' + manual_cache_name
        os.mkdir(folder_path)

        name = folder_path + '/' + manual_cache_name
        file_path = name + '.abc'
        json_name = name + '.json'

        self.geo_cache_class.export_abc_file(start_frame=self.final_start_val,
                                             end_frame=self.final_end_val,
                                             char_list=sel_obj,
                                             abc_file_path=file_path)

        self.update_manual_list_widget()

        # UPDATE THE JSON PATH
        attr_list = {}
        attr_list['Comments'] = self.comments_plain_text_edit.toPlainText()
        with open(json_name, 'w') as f:
            json.dump(attr_list, f)

        self.comments_plain_text_edit.clear()

        cmds.playbackOptions(minTime=current_start_frame, maxTime=current_end_frame)

    def sim_cache_list_widget_def(self):
        '''

        :return:
        '''
        item = self.sim_cache_list_widget.selectedItems()
        if item:
            json_path = self.sim_cache_path + '/' + item[0].text() + '.json'

            file_path = json_path.replace('json', 'mcx')

            with open(json_path) as f:
                data = json.load(f)
                self.update_ui_json_read(data, file_name=item[0].text(), file_path=file_path)

    def sim_cache_list_widget_contexMenu(self, position):
        # Popup menu
        popMenu = QMenu()
        replace_attr = QAction("Replace With this setting", self)
        replace_attr.triggered.connect(self.replace_attr_def)
        explore_folder = QAction("Explore to folder", self)
        explore_folder.triggered.connect(self.explore_folder_def)

        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        popMenu.addAction(replace_attr)
        popMenu.addAction(explore_folder)

        popMenu.exec_(self.sim_cache_list_widget.mapToGlobal(position))

    def geo_cache_list_widget_contexMenu(self, position):
        '''

        :return:
        '''
        popMenu = QMenu()
        explore_folder = QAction("Explore to folder", self)
        select_geo = QAction("Select Geo Connected with Cache", self)
        explore_folder.triggered.connect(self.geo_explore_folder_def)
        select_geo.triggered.connect(self.select_geo_def)

        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        popMenu.addAction(explore_folder)
        popMenu.addAction(select_geo)

        popMenu.exec_(self.sim_cache_list_widget.mapToGlobal(position))

    def playblast_list_widget_contexMenu(self, position):
        '''

        :return:
        '''
        popMenu = QMenu()
        explore_folder = QAction("Explore to folder", self)
        openFile = QAction("OpenFile", self)
        explore_folder.triggered.connect(self.playblast_explore_folder_def)
        openFile.triggered.connect(self.playblast_openFile_def)

        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        popMenu.addAction(explore_folder)
        popMenu.addAction(openFile)

        popMenu.exec_(self.playblast_list_widget.mapToGlobal(position))

    def final_cache_list_widget_contexMenu(self, position):
        '''

        :return:
        '''
        popMenu = QMenu()
        explore_folder = QAction("Explore to folder", self)
        import_file = QAction("Import File", self)
        explore_folder.triggered.connect(self.final_cache_explore_folder_def)
        import_file.triggered.connect(self.final_cache_import_file_def)

        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        popMenu.addAction(explore_folder)
        popMenu.addAction(import_file)

        popMenu.exec_(self.final_cache_list_widget.mapToGlobal(position))

    def manual_cache_list_widget_contexMenu(self, position):
        '''

        :return:
        '''
        popMenu = QMenu()
        explore_folder = QAction("Explore to folder", self)
        import_file = QAction("Import File", self)
        explore_folder.triggered.connect(self.manual_cache_explore_folder_def)
        import_file.triggered.connect(self.manual_cache_import_file_def)

        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        popMenu.addAction(explore_folder)
        popMenu.addAction(import_file)

        popMenu.exec_(self.manual_cache_list_widget.mapToGlobal(position))



    def replace_attr_def(self):
        '''

        :return:
        '''
        item = self.sim_cache_list_widget.selectedItems()[0]
        json_path = self.sim_cache_path + '/' + item.text() + '.json'

        with open(json_path) as f:
            data = json.load(f)
            for each in data:
                if each != 'Comments':
                    if cmds.objExists(each):
                        for each_data in data[each]:
                            try:
                                cmds.setAttr(each + '.' + each_data, data[each][each_data])
                            except:
                                pass

    def explore_folder_def(self):
        '''
        exporing the folder
        :return:
        '''
        webbrowser.open(self.sim_cache_path)

    def geo_explore_folder_def(self):
        '''
        exporing the folder
        :return:
        '''
        webbrowser.open(self.geo_cache_path)

    def select_geo_def(self):
        '''

        :return:
        '''
        item = self.geo_cache_list_widget.selectedItems()[0]
        json_path = self.geo_cache_path + '/' + item.text() + '.json'

        with open(json_path) as f:
            data = json.load(f)
            for each in data:
                if each != 'Comments':
                    if each == 'GeoList':
                        cmds.select(data[each])

    def playblast_explore_folder_def(self):
        '''
        exporing the folder
        :return:
        '''
        webbrowser.open(self.playblast_cache_path)

    def final_cache_explore_folder_def(self):
        '''
        exporing the folder
        :return:
        '''
        webbrowser.open(self.final_cache_path)

    def final_cache_import_file_def(self):
        '''

        :return:
        '''
        item = self.final_cache_list_widget.selectedItems()[0]
        file_path = self.final_cache_path + '/' + item.text() + '/' + item.text() + '.abc'
        cmds.AbcImport(file_path, mode='import')

    def manual_cache_import_file_def(self):
        '''

        :return:
        '''
        item = self.manual_cache_list_widget.selectedItems()[0]
        file_path = self.manual_cache_path + '/' + item.text() + '/' + item.text() + '.abc'
        cmds.AbcImport(file_path, mode='import')


    def manual_cache_explore_folder_def(self):
        '''

        :return:
        '''
        webbrowser.open(self.manual_cache_path)

    def playblast_openFile_def(self):
        '''

        :return:
        '''
        item = self.playblast_list_widget.selectedItems()[0]
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',item.text())
        file_path = self.playblast_cache_path + '/' + str(item.text()) + '.mov'
        print('tis is the file path: ', file_path)
        os.startfile(file_path)

    def update_ui_json_read(self, json_data, file_name='', file_path='', param=True):
        '''

        :param json_data:
        :return:
        '''
        #UPDATE THE TEXT EDIT FILE
        self.notes_plainTextEdit.setPlainText(json_data['Comments'])

        #UPDATE THE INFOR TAB
        self.info_name_val_label.setText(file_name)
        self.info_file_path_val_label.setText(file_path)
        time_val = time.ctime(os.path.getmtime(file_path))
        self.info_date_time_val_label.setText(time_val)

        #CREATE A TREE WIDGET
        self.parameter_tree_widget.clear()
        if param:

            for each in json_data:
                if each != 'Comments':
                    each_name = QTreeWidgetItem(self.parameter_tree_widget)
                    each_name.setText(0, each)
                    for each_attr in json_data[each]:
                        each_attr_name = QTreeWidgetItem(each_name)
                        each_attr_name.setText(0, each_attr)
                        val = str(json_data[each][each_attr])
                        each_attr_name.setText(1, val)

        '''
        nucleus = QTreeWidgetItem(self.parameter_tree_widget)
        nucleus.setText(0, each_cfx_list)
        '''

    def cache_path_lineedit_def(self):
        '''

        :return:
        '''
        self.sim_cache_path = self.cache_path_lineedit.text()

        self.update_sim_cache_listwidget()
        self.set_cache_manger_data()

    def update_sim_cache_listwidget(self):
        '''

        :return:
        '''
        # UPDATE THE UI PART
        self.sim_cache_list_widget.clear()
        # now add all the object into the list
        mc_file_list = []
        files = list(filter(os.path.isfile, glob.glob(self.sim_cache_path + "/*")))
        files.sort(key=lambda x: os.path.getmtime(x))

        for each in files:
            if 'mc' in each:
                split_ = each.split('\\')[1]
                item = QListWidgetItem(split_.split('.')[0])
                self.sim_cache_list_widget.addItem(item)


    def disconnect_the_ncloth_cache_button_def(self):
        '''

        :return:
        '''

        # GET CACHE IS GOING TO REPLACE OR NOT
        if self.select_ncloth_node_checkbox.isChecked():
            self.cache_manager_class.delete_ncloth_cache(selected=False)
        else:
            self.cache_manager_class.delete_ncloth_cache(selected=True)

    def geo_cache_button_def(self):
        '''
        #create a geo cache on the gep cache directory
        :return:
        '''
        sel_geo = cmds.ls(sl=True)
        if sel_geo:
            for each in sel_geo:
                if cmds.objectType(each) == 'transform':
                    child_obj = cmds.listRelatives(each, s=True)
                    if type(child_obj) == list:
                        if not cmds.objectType(child_obj[0]) == 'mesh':
                            raise Exception('Please Select Mesh Geo TO do a cache')
                    else:
                        if not cmds.objectType(child_obj) == 'mesh':
                            raise Exception('Please Select Mesh Geo TO do a cache')
                else:
                    if not cmds.objectType(each) == 'mesh':
                        raise Exception('Please Select Mesh Geo TO do a cache')
        else:
            raise Exception('Please Select Geometry Transformation node to do a cache')

        current_start_frame, current_end_frame = self.cache_manager_class.set_frames(new_start_frame=self.geo_cache_start_val,
                                                                                     new_end_frame=self.geo_cache_end_val)

        start_frame = float(self.geo_start_time_lineedit.text())
        end_frame = float(self.geo_end_time_lineedit.text())

        #get the cache name
        file_name = self.cache_manager_class.get_file_name()
        onlyfiles = [f for f in listdir(self.geo_cache_path) if isfile(join(self.geo_cache_path, f))]
        file_path_list = []

        for each in onlyfiles:
            if 'mc' in each:
                if self.cache_manager_class.get_file_name() in each:
                    file_path_list.append(each)
        cache_name = file_name + '_Geo_' + str(len(file_path_list))

        self.geo_cache_class.exportMCCache(geo=sel_geo,
                                           cacheFile=self.geo_cache_path,cache_name=cache_name,
                                           startFrame=start_frame, endFrame=end_frame)

        #UPDATE THE LIST WIDGET
        self.update_geo_cache_listwidget()

        #UPDATE JSON FILE
        self.geo_json_file_create(geo_list=sel_geo, name=cache_name)

        cmds.playbackOptions(minTime=current_start_frame, maxTime=current_end_frame)


        #doCreateGeometryCache 5 {"0", "1.0", "1210.0", "OneFile", "1", "C:/Users/Admin/Desktop/test/data/geoCache", "1", "clothOne_Geo_7", "0", "export", "0", "1", "1", "0", "0", "mcc" };'
        #doCreateGeometryCache 6 {"2", "1.0", "1210.0", "OneFile", "1", "C:/Users/Admin/Desktop/test/data/geoCache", "0", "clothOne_Geo_7", "0", "export", "0", "1", "1", "0", "1", "mcx", "0" } ;
        #('this is the cacha path: ', u'doCreateGeometryCache 5 {"2", -19.0, 220.0, "OneFile", "1", C:/Users/Admin/Desktop/test/data/geoCache, "0", clothOne_Geo_0, "0", "export", "0", "1", "1", "0", "1", "mcx", "0" }')


    def update_geo_cache_listwidget(self):
        '''

        :return:
        '''
        # UPDATE THE UI PART
        self.geo_cache_list_widget.clear()
        # now add all the object into the list
        files = list(filter(os.path.isfile, glob.glob(self.geo_cache_path + "/*")))
        files.sort(key=lambda x: os.path.getmtime(x))

        for each in files:
            if 'mc' in each:
                split_ = each.split('\\')[1]
                item = QListWidgetItem(split_.split('.')[0])
                self.geo_cache_list_widget.addItem(item)

    def update_playblast_list_widget(self):
        '''

        :return:
        '''
        self.playblast_list_widget.clear()
        # now add all the object into the list
        files = list(filter(os.path.isfile, glob.glob(self.playblast_cache_path + "/*")))
        files.sort(key=lambda x: os.path.getmtime(x))

        for each in files:
            split_ = each.split('\\')[1]
            if '.mov' in split_:
                item = QListWidgetItem(split_.split('.')[0])
                self.playblast_list_widget.addItem(item)

    def update_final_list_widget(self):
        '''

        :return:
        '''
        self.final_cache_list_widget.clear()
        # now add all the object into the list

        folder = os.listdir(self.final_cache_path)
        for each in folder:
            item = QListWidgetItem(each)
            self.final_cache_list_widget.addItem(item)
        '''
        for each in folder:
            split_ = each.split('\\')[1]
            item = QListWidgetItem(split_.split('.')[0])
            self.final_cache_list_widget.addItem(item)
        '''
    def update_manual_list_widget(self):
        '''

        :return:
        '''
        self.manual_cache_list_widget.clear()
        # now add all the object into the list
        folder = os.listdir(self.manual_cache_path)
        for each in folder:
            item = QListWidgetItem(each)
            self.manual_cache_list_widget.addItem(item)

    def geo_json_file_create(self, geo_list, name):
        '''

        :return:
        '''
        attr_list_val = {}
        attr_list_val['GeoList'] = geo_list
        attr_list_val['Comments'] = self.comments_plain_text_edit.toPlainText()

        json_path = self.geo_cache_path + '/' + name + '.json'
        with open(json_path, 'w') as f:
            json.dump(attr_list_val, f)

        self.comments_plain_text_edit.clear()

    def tree_checkbox_def(self):
        '''

        :return:
        '''
        self.ncloth_tree_vis = self.ncloth_checkbox.isChecked()
        self.nRigit_tree_vis = self.nrigit_chekbox.isChecked()
        self.nConstraint_tree_vis = self.nconstraint_checkbox.isChecked()
        self.nhair_tree_vis = self.nhair_checkbox.isChecked()
        self.follicle1_tree_vis = self.folicle_checkbox.isChecked()
        if self.ncloth_tree_vis == False:
            self.ncloth_val = 0
        else:
            self.ncloth_val = 1

        if self.nConstraint_tree_vis == False:
            self.nconstraint_val = 0
        else:
            self.nconstraint_val = 1

        if self.nRigit_tree_vis == False:
            self.nrigid_val = 0
        else:
            self.nrigid_val = 1

        if self.nhair_tree_vis == False:
            self.nhair_val = 0
        else:
            self.nhair_val = 1

        if self.follicle1_tree_vis == False:
            self.folical_val = 0
        else:
            self.folical_val = 1


        self.sim_tree_widget.clear()
        self.sim_tree_def()
        self.set_cache_manger_data()




    def cache_path_button_def(self):
        '''

        :return:
        '''
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.sim_cache_path))
        if folder:
            self.cache_path_lineedit.setText(folder)


    def geo_start_time_lineedit_def(self):
        '''

        :return:
        '''
        self.geo_cache_start_val = float(self.geo_start_time_lineedit.text())
        self.set_cache_manger_data()

    def geo_end_time_lineedit_def(self):
        '''

        :return:
        '''
        self.geo_cache_end_val = float(self.geo_end_time_lineedit.text())
        self.set_cache_manger_data()

    def geo_cache_path_browse_button_def(self):
        '''

        :return:
        '''
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.geo_cache_path))
        if folder:
            self.geo_cache_lineedit.setText(folder)

    def playblast_path_browse_button_def(self):
        '''

        :return:
        '''
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.playblast_cache_path))
        if folder != '':
            self.playblast_path_lineedit.setText(folder)

    def final_cache_browse_button_def(self):
        '''

        :return:
        '''
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.final_cache_path))
        if folder != '':
            self.final_cache_path_lineedit.setText(folder)

    def manaul_cache_browse_button_def(self):
        '''

        :return:
        '''
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.manual_cache_path))
        if folder != '':
            self.manual_cache_path_lineedit.setText(folder)

    def playblast_path_lineedit_def(self):
        '''

        :return:
        '''
        self.playblast_cache_path = self.playblast_path_lineedit.text()
        self.update_playblast_list_widget()
        self.set_cache_manger_data()

    def final_cache_path_lineedit_def(self):
        '''

        :return:
        '''
        self.final_cache_path = self.final_cache_path_lineedit.text()
        self.update_final_list_widget()
        self.set_cache_manger_data()

    def manual_cache_path_lineedit_def(self):
        '''

        :return:
        '''
        self.manual_cache_path = self.manual_cache_path_lineedit.text()
        self.update_manual_list_widget()
        self.set_cache_manger_data()

    def geo_cache_lineedit_def(self):
        '''

        :return:
        '''
        self.geo_cache_path = self.geo_cache_lineedit.text()
        self.update_geo_cache_listwidget()
        self.set_cache_manger_data()

    def playblast_start_time_lineedit_def(self):
        '''

        :return:
        '''
        self.playblast_start_val = float(self.playblast_start_time_lineedit.text())
        self.set_cache_manger_data()

    def playblast_end_time_lineedit_def(self):
        '''

        :return:
        '''
        self.playblast_end_val = float(self.playblast_end_time_lineedit.text())
        self.set_cache_manger_data()

    def final_start_time_lineedit_def(self):
        '''

        :return:
        '''
        self.final_start_val = float(self.final_start_time_lineedit.text())
        self.set_cache_manger_data()

    def final_end_time_lineedit_def(self):
        '''

        :return:
        '''
        self.final_end_val = float(self.final_end_time_lineedit.text())
        self.set_cache_manger_data()

    def manual_start_time_lineedit_def(self):
        '''

        :return:
        '''
        self.manual_start_val = float(self.manual_start_time_lineedit.text())
        self.set_cache_manger_data()

    def manual_end_time_lineedit_def(self):
        '''

        :return:
        '''
        self.manual_end_val = float(self.manual_end_time_lineedit.text())
        self.set_cache_manger_data()


    def sim_start_time_lineedit_def(self):
        '''

        :return:
        '''
        sim_start_val = self.sim_start_time_lineedit.text()
        self.sim_start_val = float(sim_start_val)

        for each in cmds.ls(type='nucleus'):
            cmds.setAttr(each + '.startFrame', self.sim_start_val)

        self.set_cache_manger_data()


    def sim_end_time_lineedit_def(self):
        '''

        :return:
        '''
        sim_start_val = self.sim_end_time_lineedit.text()
        self.sim_end_val = float(sim_start_val)

        self.set_cache_manger_data()

    def playblast_setting_button_def(self):
        '''

        :return:
        '''
        self.playblast_setting = PLAYBLAST_SETTING()
        #self.playblast_setting.show()
        pass


