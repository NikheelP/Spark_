from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os, glob, json
import maya.cmds as cmds
from functools import partial
from os import listdir
from os.path import isfile, join
import webbrowser

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.Help import help
from spark.department.Help import geoCache
from spark.department.CFX.cfx_tools import cacheManager
from spark.department.common import rename
from spark.department.Help import attribute
for each in [sample_color_variable, sample_widget_template, style_sheet_template, rename, cacheManager, geoCache, help, attribute]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.sample_color_variable import COLOR_VARIABLE
from spark.department.common.rename import RENAME
from spark.department.CFX.cfx_tools.cacheManager import CACHEMANAGER
from spark.department.Help.geoCache import GEOCACHE
from spark.department.Help.help import HELP
from spark.department.Help.attribute import ATTRIBUTE

from spark.widget.common_widget import cacheManager_icon
cacheManagerIconPath = os.path.abspath(cacheManager_icon.__file__).replace('\\', '/')
last_obj = cacheManagerIconPath.split('/')[-1]
cacheManagerIconPath = cacheManagerIconPath.split(last_obj)[0]

from spark.widget.common_widget import rigFX_icon
rigFxIconPath = os.path.abspath(rigFX_icon.__file__).replace('\\', '/')
last_obj = rigFxIconPath.split('/')[-1]
rigfxIconPath_ = rigFxIconPath.split(last_obj)[0]

class CACHEMANGER_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='Cache Manger'):
        super(CACHEMANGER_WIDGET, self).__init__(title=title)
        self.cache_manager_class = CACHEMANAGER()
        self.geo_cache_class = GEOCACHE()
        self.help_class = HELP()
        self.attribute_class = ATTRIBUTE()

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

        #CACHE MANAER NODE
        self.cache_manager_data = 'CacheManagerData'
        self.sim_start = 'sim_start'
        self.sim_start_val = 0.0
        self.sim_end = 'sim_end'
        self.sim_end_val = 0.0
        self.sim_path = 'sim_path'
        self.sim_path_val = ''

        self.geo_cache_start = 'geo_cache_start'
        self.geo_cache_start_val = 0.0
        self.geo_cache_end = 'geo_cache_end'
        self.geo_cache_end_val = 0.0
        self.geo_cache_path = 'geo_cache_path'
        self.geo_cache_path_val = ''

        self.playblast_start = 'playblast_start'
        self.playblast_start_val = 0.0
        self.playblast_end = 'playblast_end'
        self.playblast_end_val = 0.0
        self.playblast_path = 'playblast_path'
        self.playblast_path_val = ''

        self.final_start = 'final_start'
        self.final_start_val = 0.0
        self.final_end = 'final_end'
        self.final_end_val = 0.0
        self.final_path = 'final_path'
        self.final_path_val = ''



        # GET THE SIM CACHE PATH
        self.sim_cache_path, self.geo_cache_path, self.playblast_cache_path, self.final_cache_path = self.cache_manager_class.initcheck()

        self.ui()


    def ui(self):
        '''

        :return:
        '''
        main_widget = self.get_main_widget()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=main_widget)

        main_horizonatal_splitter = self.sample_widget_template.splitter_def(parent_self=main_widget,
                                                                             set_orientation=self.sample_widget_template.vertical)
        vertical_layout.addWidget(main_horizonatal_splitter)


        #CLOTH INPUT BUTTON HISTORY SPLITTER
        self.cloth_input_button_history_splitter = self.sample_widget_template.splitter_def(parent_self=main_horizonatal_splitter, set_orientation=self.sample_widget_template.horizonatal)

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

    def cloth_input_output_widget(self):
        '''

        :return:
        '''

        cloth_input_output_widget = self.sample_widget_template.widget_def(self.cloth_input_button_history_splitter)

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
        ncloth_text = 'nCloth'
        ncloth_obj_name = self.sample_widget_template.setObjectName(ncloth_text)
        ncloth_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=ncloth_obj_name,
                                                                       color=self.color_variable_class.nCloth_color.get_value())
        self.ncloth_checkbox = self.sample_widget_template.checkbox(set_text=ncloth_text,
                                                               set_object_name=ncloth_obj_name,
                                                               set_styleSheet=ncloth_styleSheet, stateChanged=self.tree_checkbox_def)
        self.ncloth_checkbox.setChecked(self.ncloth_tree_vis)
        grid_layout.addWidget(self.ncloth_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NRIGIT CHECKBOX
        nrigit_text = 'nRigit'
        nrigit_obj_name = self.sample_widget_template.setObjectName(nrigit_text)
        nrigit_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nrigit_obj_name, color=self.color_variable_class.nRigit_color.get_value())
        self.nrigit_chekbox = self.sample_widget_template.checkbox(set_text=nrigit_text,
                                                              set_object_name=nrigit_obj_name,
                                                              set_styleSheet=nrigit_styleSheet, stateChanged=self.tree_checkbox_def)
        self.nrigit_chekbox.setChecked(self.nRigit_tree_vis)
        grid_layout.addWidget(self.nrigit_chekbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NCONSTRAINT CHECKBOX
        nconstraint_text = 'nConstraint'
        nconstraint_obj_name = self.sample_widget_template.setObjectName(nconstraint_text)
        nconstraint_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nconstraint_obj_name,
                                                                            color=self.color_variable_class.nConstraint_color.get_value())
        self.nconstraint_checkbox = self.sample_widget_template.checkbox(set_text=nconstraint_text,
                                                                    set_object_name=nconstraint_obj_name,
                                                                    set_styleSheet=nconstraint_styleSheet, stateChanged=self.tree_checkbox_def)
        self.nconstraint_checkbox.setChecked(self.nConstraint_tree_vis)
        grid_layout.addWidget(self.nconstraint_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NHAIR CHECKBOX
        nhair_text = 'nHair'
        nhair_obj_name = self.sample_widget_template.setObjectName(nhair_text)
        nhair_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=nhair_obj_name, color=self.color_variable_class.nHair_color.get_value())
        self.nhair_checkbox = self.sample_widget_template.checkbox(set_text=nhair_text,
                                                              set_object_name=nhair_obj_name,
                                                              set_styleSheet=nhair_styleSheet, stateChanged=self.tree_checkbox_def)
        self.nhair_checkbox.setChecked(self.nhair_tree_vis)
        grid_layout.addWidget(self.nhair_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1

        # NHAIR CHECKBOX
        folical_text = 'follicle'
        folical_obj_name = self.sample_widget_template.setObjectName(folical_text)
        folical_styleSheet = self.sample_widget_template.styleSheet_def(obj_name=folical_obj_name,
                                                                      color=self.color_variable_class.folical_color.get_value())
        self.folicle_checkbox = self.sample_widget_template.checkbox(set_text=folical_text,
                                                                   set_object_name=folical_obj_name,
                                                                   set_styleSheet=folical_styleSheet,
                                                                   stateChanged=self.tree_checkbox_def)
        self.folicle_checkbox.setChecked(self.follicle1_tree_vis)
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

        cloth_button_widget = self.sample_widget_template.widget_def(self.cloth_input_button_history_splitter)

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
                                                                      set_icon_size=[self.icon_size, self.icon_size])
        vertical_layout.addWidget(playblast_button)

        # FINCAL CACHE BUTTON
        final_cache_button_text = 'Final Cache'
        icon_ = 'Final.png'
        icon_path = cacheManagerIconPath + icon_
        final_cache_button = self.sample_widget_template.pushButton(set_text=final_cache_button_text,
                                                                    max_size=[self.sample_widget_template.max_size, button_height],
                                                                      set_icon=icon_path,
                                                                      set_icon_size=[self.icon_size, self.icon_size])
        vertical_layout.addWidget(final_cache_button)


        return cloth_button_widget

    def cache_manager_data(self):
        self.cache_manager_data = 'CacheManagerData'
        self.sim_start = 'sim_start'
        self.sim_start_val = 0.0
        self.sim_end = 'sim_end'
        self.sim_end_val = 0.0
        self.sim_path = 'sim_path'
        self.sim_path_val = ''

        self.geo_cache_start = 'geo_cache_start'
        self.geo_cache_start_val = 0.0
        self.geo_cache_end = 'geo_cache_end'
        self.geo_cache_end_val = 0.0
        self.geo_cache_path = 'geo_cache_path'
        self.geo_cache_path_val = ''

        self.playblast_start = 'playblast_start'
        self.playblast_start_val = 0.0
        self.playblast_end = 'playblast_end'
        self.playblast_end_val = 0.0
        self.playblast_path = 'playblast_path'
        self.playblast_path_val = ''

        self.final_start = 'final_start'
        self.final_start_val = 0.0
        self.final_end = 'final_end'
        self.final_end_val = 0.0
        self.final_path = 'final_path'
        self.final_path_val = ''

        if not cmds.objExists(self.cache_manager_data):
            cmds.createNode('transform', n=self.cache_manager_data)
            cmds.setAttr(self.cache_manager_data + ".hideOnPlayback", 1)

            #NOW CREATEA A ATTRIBUTE
            self.attribute_class.add_attr()



    def cache_playblast_history_widget(self):
        '''

        :return:
        '''

        cache_playblast_history_widget = self.sample_widget_template.widget_def(self.cloth_input_button_history_splitter)

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

        return cache_playblast_history_widget

    def comment_widget(self):
        '''

        :return:
        '''

        comments_widget = self.sample_widget_template.widget_def(self.comment_file_status_splitter)

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=comments_widget)

        #COMMENTS PLAIN TEXT EDIT
        self.comments_plain_text_edit = self.sample_widget_template.plainTextEdit()
        vertical_layout.addWidget(self.comments_plain_text_edit)

        return comments_widget

    def file_status_widget(self):
        '''

        :return:
        '''

        file_status_widget = self.sample_widget_template.widget_def(self.comment_file_status_splitter)

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=file_status_widget)

        #TAB WIDGET
        tab_widget = self.sample_widget_template.tab_widget(parent_self=file_status_widget)
        vertical_layout.addWidget(tab_widget)

        # NOTES TAB
        self.notes_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        note_tab_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.notes_tab)
        note_tab_verticalLayout.addWidget(self.notes_tab_widget())
        tab_widget.addTab(self.notes_tab, 'Notes')

        # INFO
        self.info_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        info_tab_verticalLayout = self.sample_widget_template.vertical_layout(parent_self=self.info_tab)
        info_tab_verticalLayout.addWidget(self.info_tab_widget())
        tab_widget.addTab(self.info_tab, 'Info')

        # PARAMETER
        self.parameter_tab = self.sample_widget_template.widget_def(parent_self=tab_widget)
        tab_widget.addTab(self.parameter_tab, 'Parm')

        return file_status_widget

    def notes_tab_widget(self):
        '''

        :return:
        '''
        notes_widget = self.sample_widget_template.widget_def()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=notes_widget)

        self.notes_plainTextEdit = self.sample_widget_template.plainTextEdit()
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
        name_label = self.sample_widget_template.label(set_text=name_text)
        grid_layout.addWidget(name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        name_val_text = 'Name : '.upper()
        name_val_label = self.sample_widget_template.label(set_text=name_val_text)
        grid_layout.addWidget(name_val_label, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        file_path_text = 'FilePath : '.upper()
        file_path_label = self.sample_widget_template.label(set_text=file_path_text)
        grid_layout.addWidget(file_path_label, vertical_val, new_value, 1, 1)
        new_value += 1

        file_path_val_text = 'FilePath : '.upper()
        file_path_val_label = self.sample_widget_template.label(set_text=file_path_val_text)
        grid_layout.addWidget(file_path_val_label, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        date_time_text = 'Date & Time : '.upper()
        date_time_label = self.sample_widget_template.label(set_text=date_time_text)
        grid_layout.addWidget(date_time_label, vertical_val, new_value, 1, 1)
        new_value += 1

        date_time_val_text = 'FilePath : '.upper()
        date_time_val_label = self.sample_widget_template.label(set_text=date_time_val_text)
        grid_layout.addWidget(date_time_val_label, vertical_val, new_value, 1, 1)
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
        self.sim_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.cache_manager_class.get_nucleus_start_frame()),
                                                                        set_PlaceholderText='Set Start Time')
        horizontal_layout.addWidget(self.sim_start_time_lineedit)

        #END TIME
        self.sim_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.end_time_val + 10), set_PlaceholderText='Set End Time')
        horizontal_layout.addWidget(self.sim_end_time_lineedit)


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
        horizontal_layout.addWidget(self.cache_path_lineedit)

        cache_path_button = self.sample_widget_template.pushButton(set_text='...',
                                                                   connect=self.cache_path_button_def)
        horizontal_layout.addWidget(cache_path_button)

        #####################################
        #REPLAVE CACHE
        replace_cache_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(replace_cache_widget)
        replace_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=replace_cache_widget)

        '''
        replace_chekbox_text = 'Replace Cache'
        replace_chekbox_object = self.sample_widget_template.setObjectName(replace_chekbox_text)
        replace_checkbox_setStyleSheet = self.sample_widget_template.styleSheet_def(obj_name=replace_chekbox_object,
                                                                                    color=self.color_variable_class.yellow_color.get_value())
        self.replace_checkbox = self.sample_widget_template.checkbox(set_text=replace_chekbox_object,
                                                                set_object_name=replace_chekbox_object,
                                                                set_styleSheet=replace_checkbox_setStyleSheet)
        self.replace_checkbox.setChecked(True)
        replace_vertical_layout.addWidget(self.replace_checkbox)
        '''
        ####################################
        #LIST WIDGET
        self.sim_cache_list_widget = self.sample_widget_template.list_widget()
        self.sim_cache_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sim_cache_list_widget.customContextMenuRequested.connect(self.sim_cache_list_widget_contexMenu)
        self.sim_cache_list_widget.itemSelectionChanged.connect(self.sim_cache_list_widget_def)
        vertical_laout.addWidget(self.sim_cache_list_widget)
        self.update_sim_cache_listwidget()

        return widget

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
        self.geo_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.start_time_val - self.buffer_val),
                                                                        set_PlaceholderText='Set Start Time')
        horizontal_layout.addWidget(self.geo_start_time_lineedit)

        #END TIME

        self.geo_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.end_time_val + self.buffer_val),
                                                                      set_PlaceholderText='Set End Time')
        horizontal_layout.addWidget(self.geo_end_time_lineedit)


        ####################################
        #CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        #CACHE PATH LABEL
        cache_path_label_text = 'Cache Path'
        cache_path_label = self.sample_widget_template.label(set_text=cache_path_label_text)
        horizontal_layout.addWidget(cache_path_label)

        cache_path_lineedit = self.sample_widget_template.line_edit(set_text=self.geo_cache_path)
        horizontal_layout.addWidget(cache_path_lineedit)


        ####################################
        #LIST WIDGET
        self.geo_cache_list_widget = self.sample_widget_template.list_widget()
        vertical_laout.addWidget(self.geo_cache_list_widget)
        self.update_geo_cache_listwidget()

        return widget

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
        geo_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(1001),
                                                                        set_PlaceholderText='Set Start Time')
        horizontal_layout.addWidget(geo_start_time_lineedit)

        #END TIME
        geo_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.end_time_val + self.buffer_val), set_PlaceholderText='Set End Time')
        horizontal_layout.addWidget(geo_end_time_lineedit)

        ####################################
        #CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        #CACHE PATH LABEL
        playblast_path_label_text = 'Playblast Path'
        playblast_path_label = self.sample_widget_template.label(set_text=playblast_path_label_text)
        horizontal_layout.addWidget(playblast_path_label)

        cache_path_lineedit = self.sample_widget_template.line_edit(set_text=self.playblast_cache_path)
        horizontal_layout.addWidget(cache_path_lineedit)


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
        camera_combobox = self.sample_widget_template.comboBox()
        grid_layout.addWidget(camera_combobox, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        #PLAUBLAST SETTING BUTTON
        playblast_setting_button_text = 'Playblast Setting'
        playblast_setting_button = self.sample_widget_template.pushButton(set_text=playblast_setting_button_text)
        grid_layout.addWidget(playblast_setting_button, vertical_val, new_value, 1, 2)
        new_value += 1


        ####################################
        #LIST WIDGET
        sim_cache_list_widget = self.sample_widget_template.list_widget()
        vertical_laout.addWidget(sim_cache_list_widget)

        return widget

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
        final_start_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.start_time_val - self.buffer_val), set_PlaceholderText='Set Start Time')
        horizontal_layout.addWidget(final_start_time_lineedit)

        #END TIME
        final_end_time_lineedit = self.sample_widget_template.line_edit(set_text=str(self.end_time_val + self.buffer_val), set_PlaceholderText='Set End Time')
        horizontal_layout.addWidget(final_end_time_lineedit)


        ####################################
        #CACHE PATH WIDGET
        cache_path_widget = self.sample_widget_template.widget_def()
        vertical_laout.addWidget(cache_path_widget)
        horizontal_layout = self.sample_widget_template.horizontal_layout(parent_self=cache_path_widget)

        #CACHE PATH LABEL
        cache_path_label_text = 'Final Cache Path'
        cache_path_label = self.sample_widget_template.label(set_text=cache_path_label_text)
        horizontal_layout.addWidget(cache_path_label)

        cache_path_lineedit = self.sample_widget_template.line_edit(set_text=self.final_cache_path)
        horizontal_layout.addWidget(cache_path_lineedit)


        ####################################
        #LIST WIDGET
        final_cache_list_widget = self.sample_widget_template.list_widget()
        vertical_laout.addWidget(final_cache_list_widget)

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
            nucleus_button = self.sample_widget_template.pushButton(set_icon=icon_path,
                                                                    set_icon_size=[20, 20],
                                                                    set_styleSheet=styleSheet,
                                                                    set_object_name=nucleus_set_obj)
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
                        ncloth_button = self.sample_widget_template.pushButton(set_icon=icon_path,
                                                                                set_icon_size=[20, 20],
                                                                                set_styleSheet=styleSheet,
                                                                                set_object_name=ncloth_set_obj)
                        self.sim_tree_widget.setItemWidget(ncloth_item, 1, ncloth_button)

            if self.nConstraint_tree_vis:
                if cfx_list[each_cfx_list]['dynamicConstraint']:
                    for each_dynamicConstraint in cfx_list[each_cfx_list]['dynamicConstraint']:
                        shape = cmds.listRelatives(each_dynamicConstraint, s=True)[0]
                        dynamicConstraint_item = QTreeWidgetItem(nucleus)
                        dynamicConstraint_item.setForeground(0, QBrush(QColor(self.color_variable_class.nConstraint_color.get_value()[0],
                                                                              self.color_variable_class.nConstraint_color.get_value()[1],
                                                                              self.color_variable_class.nConstraint_color.get_value()[2])))
                        #"C:\Users\Admin\Desktop\Nikheel\Spark_Project\Spark_\spark\widget\common_widget\rigFX_icon\out_dynamicConstraint.png"
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
                        dynamicConstraint_button = self.sample_widget_template.pushButton(set_icon=icon_path,
                                                                                set_icon_size=[20, 20],
                                                                                set_styleSheet=styleSheet,
                                                                                set_object_name=dynamicConstraint_set_obj)
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
                        nRigid_button = self.sample_widget_template.pushButton(set_icon=icon_path,
                                                                                set_icon_size=[20, 20],
                                                                                set_styleSheet=styleSheet,
                                                                                set_object_name=nRigid_set_obj)
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
                        hairSystem_button = self.sample_widget_template.pushButton(set_icon=icon_path,
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
        input_list_widget = self.sample_widget_template.list_widget()


        return input_list_widget

    def output_list_def(self):
        '''

        :return:
        '''

        output_list_widget = self.sample_widget_template.list_widget()

        return output_list_widget

    def ncloth_cache_def(self):
        '''

        :return:
        '''
        print('nCloth will cache')
        #GET ALL THE CLOTH
        # GET CACHE IS GOING TO REPLACE OR NOT
        if self.select_ncloth_node_checkbox.isChecked():
            nCloth = cmds.ls(type='nCloth')
            sel_ncloth = []
            for each in nCloth:
                sel_ncloth.append(cmds.listRelatives(each, p=True)[0])

        else:
            selected_val = True
            sel_ncloth = cmds.ls(sl=True)
            for each in sel_ncloth:
                shape = cmds.listRelatives(each, s=True)
                if cmds.objectType(shape) != 'nCloth':
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

        print('this is the ncloth: ', sel_ncloth)
        print('this is the Start Frame: ', start_val)
        print('this is the end Frame: ', end_val)
        print('this is the simPath: ', sim_path)
        print('this is the attr_list: ', attr_list)


        self.cache_manager_class.ncloth_cache_def(ncloth_list=sel_ncloth,
                                                  start_val=start_val,
                                                  end_val=end_val,
                                                  sim_path=sim_path,
                                                  attr_list=attr_list)

        self.update_sim_cache_listwidget()


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

    def sim_cache_list_widget_def(self):
        '''

        :return:
        '''
        item = self.sim_cache_list_widget.selectedItems()[0]
        json_path = self.sim_cache_path + '/' + item.text() + '.json'
        with open(json_path) as f:
            data = json.load(f)
            self.update_ui_json_read(data)

    def sim_cache_list_widget_contexMenu(self, position):
        # Popup menu
        popMenu = QMenu()
        replace_attr = QAction("Replace With this setting", self)
        addPercentage = QAction("add Percentage value", self)
        explore_folder = QAction("Explore to folder", self)
        explore_folder.triggered.connect(self.explore_folder_def)

        # Check if it is on the item when you right-click, if it is not, delete and modify will not be displayed.
        popMenu.addAction(replace_attr)
        popMenu.addAction(addPercentage)
        popMenu.addAction(explore_folder)
        #if self.sim_cache_list_widget.itemAt(position):
            #popMenu.addAction(delAct)


        popMenu.exec_(self.sim_cache_list_widget.mapToGlobal(position))

    def explore_folder_def(self):
        '''
        exporing the folder
        :return:
        '''
        webbrowser.open(self.sim_cache_path)

    def update_ui_json_read(self, json_data):
        '''

        :param json_data:
        :return:
        '''
        #UPDATE THE TEXT EDIT FILE
        self.notes_plainTextEdit.setPlainText(json_data['Comments'])


    def cache_path_lineedit_def(self):
        '''

        :return:
        '''
        self.sim_cache_path = self.cache_path_lineedit.text()
        self.update_sim_cache_listwidget()



    def update_sim_cache_listwidget(self):
        '''

        :return:
        '''
        # UPDATE THE UI PART
        self.sim_cache_list_widget.clear()
        # now add all the object into the list
        mc_file_list = []
        onlyfiles = [f for f in listdir(self.sim_cache_path) if isfile(join(self.sim_cache_path, f))]
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
            self.cache_manager_class.delete_ncloth_cache(selected=True)
        else:
            self.cache_manager_class.delete_ncloth_cache(selected=False)



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


    def geo_json_file_create(self, geo_list, name):
        '''

        :return:
        '''
        attr_list_val = {}
        attr_list_val['GeoList'] = geo_list
        attr_list_val['Notes'] = self.comments_plain_text_edit.toPlainText()

        json_path = self.geo_cache_path + '/' + name + '.json'
        with open(json_path, 'w') as f:
            json.dump(attr_list_val, f)

    def tree_checkbox_def(self):
        '''

        :return:
        '''
        self.ncloth_tree_vis = self.ncloth_checkbox.isChecked()
        self.nRigit_tree_vis = self.nrigit_chekbox.isChecked()
        self.nConstraint_tree_vis = self.nconstraint_checkbox.isChecked()
        self.nhair_tree_vis = self.nhair_checkbox.isChecked()
        self.follicle1_tree_vis = self.folicle_checkbox.isChecked()

        self.sim_tree_widget.clear()
        self.sim_tree_def()

    def cache_path_button_def(self):
        '''

        :return:
        '''
        get_lineedit = self.sim_cache_path
        new_path = 'C:\Users\Admin\Documents\maya\projects\default\data\simCache'
        _audio_file = QFileDialog.getOpenFileName(self, "Audio File",
                                                             get_lineedit, '*')
        #folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        print(_audio_file)





