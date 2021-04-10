from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template

for each in [sample_color_variable, sample_widget_template, style_sheet_template]:
    reload(each)

from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE

class COMMON_WIDGET():
    def __init__(self):
        self.sample_widget_template = SAMPLE_WIDGET_TEMPLATE()

    def ui(self, widget):
        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=widget)

        #SEARCH WIDGET
        search_widget = self.search_widget_ui()
        vertical_layout.addWidget(search_widget)

        #BUTTON WIDGET
        button_widget = self.button_def()
        vertical_layout.addWidget(button_widget)
        pass

    def search_widget_ui(self):
        search_widget = self.sample_widget_template.widget_def(min_size=[0, 26], max_size=[self.sample_widget_template.max_size, 26])

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=search_widget)

        linedit = self.sample_widget_template.line_edit(set_PlaceholderText='Filter with Name')
        vertical_layout.addWidget(linedit)

        return search_widget

    def button_def(self):
        main_widget = self.sample_widget_template.widget_def()

        main_widget_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=main_widget)

        scroll_area = self.sample_widget_template.scrollArea(parent_self=main_widget)

        scroll_widget = self.sample_widget_template.widget_def()
        scroll_area.setWidget(scroll_widget)
        main_widget_vertical_layout.addWidget(scroll_area)

        # button_widget = self.sample_widget_template.widget_def()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=scroll_widget, set_spacing=3)

        button_size = 150

        a = 0
        new_value = 0
        vertical_val = 0

        # FILTER SELECTION OUTLINER
        filter_outline = 'Filter Outline'
        filter_outline_button = self.sample_widget_template.pushButton(set_text=filter_outline,
                                                               min_size=[button_size, button_size])
        filter_outline_button.clicked.connect(self.filter_outline_button_def)
        grid_layout.addWidget(filter_outline_button, vertical_val, new_value, 1, 1)
        new_value += 1
        # PLAYBLAST MANAGER
        # MOTION MULT NODE
        # FILTER SELECTION OUTLINER
        motionMultNode_text = 'MotionMult'
        motionMultNode_toolTip = 'Load Motion Mult plugin'
        motionMultNode_button = self.sample_widget_template.pushButton(set_text=motionMultNode_text,
                                                                       min_size=[button_size, button_size],
                                                                       set_tool_tip=motionMultNode_toolTip)
        motionMultNode_button.clicked.connect(self.motionMultNode_button_def)
        grid_layout.addWidget(motionMultNode_button, vertical_val, new_value, 1, 1)
        new_value += 1


        # TRANSFORM CACHE NODE
        # RENAME TOOL
        rename_text = 'Rename'
        rename_toolTip = 'Open Rename Window'
        rename_button = self.sample_widget_template.pushButton(set_text=rename_text,
                                                               min_size=[button_size, button_size],
                                                               set_tool_tip=rename_toolTip)
        rename_button.clicked.connect(self.rename_button_def)
        grid_layout.addWidget(rename_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # WEDGE TOOL
        # CONNECTION EDITOR
        connection_editor_text = 'Connection Editor'
        connection_editor_toolTip = 'Open customize connection editor window'
        connection_editor_button = self.sample_widget_template.pushButton(set_text=connection_editor_text,
                                                                          set_tool_tip=connection_editor_toolTip,
                                                                          min_size=[button_size, button_size])
        connection_editor_button.clicked.connect(self.connection_editor_button_def)
        grid_layout.addWidget(connection_editor_button, vertical_val, new_value, 1, 1)
        new_value +=1


        # ASSIGN RANDOM SHADER
        random_shader_text = 'Assign Random Shader'
        random_shader_toolTip = 'Assign Random shader to selected object'
        random_shader_button = self.sample_widget_template.pushButton(set_text=random_shader_text,
                                                                      min_size=[button_size, button_size],
                                                                      set_tool_tip=random_shader_toolTip,
                                                                      connect=self.random_shader_button_def)
        grid_layout.addWidget(random_shader_button, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        # MAKE A TECHANIM SCENE
        # RIVET

        #RIGFX
        rigFx_text = 'RigFX'
        rigFx_toolTip = 'Assign Random shader to selected object'
        rigFx_button = self.sample_widget_template.pushButton(set_text=rigFx_text,
                                                              min_size=[button_size, button_size],
                                                              set_tool_tip=rigFx_toolTip,
                                                              connect=self.rigFx_toolTip_def)
        grid_layout.addWidget(rigFx_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # SORTLIST
        sortlist_text = 'SortList'
        sortlist_toolTip = 'Sort Out the Object\n Select all the object and run this button\n will Sort out the selected object'
        sortlist_button = self.sample_widget_template.pushButton(set_text=sortlist_text,
                                                              min_size=[button_size, button_size],
                                                              set_tool_tip=sortlist_toolTip,
                                                              connect=self.sort_def)
        grid_layout.addWidget(sortlist_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # RIVET
        rivet_text = 'Rivet'
        rivet_toolTip = 'Create a Rivet\n Select Two Edge and Click this Button'
        rivet_button = self.sample_widget_template.pushButton(set_text=rivet_text,
                                                                 min_size=[button_size, button_size],
                                                                 set_tool_tip=rivet_toolTip,
                                                                 connect=self.rivet_def)
        grid_layout.addWidget(rivet_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # CACHE MANAGER
        cache_manger_text = 'Cache Manger'
        cache_manger_toolTip = 'Manage your cache and Playblast'
        cache_manger_button = self.sample_widget_template.pushButton(set_text=cache_manger_text,
                                                              min_size=[button_size, button_size],
                                                              set_tool_tip=cache_manger_toolTip,
                                                              connect=self.cache_manger_def)
        grid_layout.addWidget(cache_manger_button, vertical_val, new_value, 1, 1)
        new_value += 1


        '''
        side_val = 4
        while a < 50:
            button_text = 'Sample_' + str(a)
            button_name = self.sample_widget_template.pushButton(set_text=button_text,
                                                                 min_size=[button_size, button_size])
            grid_layout.addWidget(button_name, vertical_val, new_value, 1, 1)
            new_value += 1
            if new_value > side_val:
                new_value = 0
                vertical_val += 1

            a += 1
        '''
        vertical_val += 1
        grid_layout.addItem(self.sample_widget_template.spaceItem(), vertical_val, new_value, 1, 1)

        return main_widget

    def filter_outline_button_def(self):
        from spark.widget.common_widget import filter_outline
        reload(filter_outline)
        from spark.widget.common_widget.filter_outline import FILTER_OUTLINE

        filter_window = FILTER_OUTLINE()
        filter_window.show()


    def motionMultNode_button_def(self):
        '''

        :return:
        '''
        from spark.department.CFX import node_create
        reload(node_create)
        node_create.motionMult()

        #OPEN THE UI
        from spark.widget.common_widget import motionMult_widget
        reload(motionMult_widget)
        from spark.widget.common_widget.motionMult_widget import MOTIONMULT_WIDGET

        motion_mult = MOTIONMULT_WIDGET()
        motion_mult.show()



    def rename_button_def(self):
        '''

        :return:
        '''
        from spark.widget.common_widget import rename_widget
        reload(rename_widget)
        from spark.widget.common_widget.rename_widget import RENAME_WIDGET
        rename_widget_ = RENAME_WIDGET()
        rename_widget_.show()

    def connection_editor_button_def(self):
        '''

        :return:
        '''
        from spark.widget.common_widget import connection_editor_widget
        reload(connection_editor_widget)
        from spark.widget.common_widget.connection_editor_widget import CONNECTION_EDITOR
        connection = CONNECTION_EDITOR()
        connection.show()

    def random_shader_button_def(self):
        '''

        :return:
        '''
        from spark.department.common import random_shader
        reload(random_shader)
        from spark.department.common.random_shader import RANDOMSHADER
        random_shader_ = RANDOMSHADER()
        random_shader_.random_shader()


    def rigFx_toolTip_def(self):
        '''

        :return:
        '''
        from spark.widget.common_widget.RigFX import rigFX_widget
        reload(rigFX_widget)
        from spark.widget.common_widget.RigFX.rigFX_widget import RIGFX_WIDGET
        rigfx_class = RIGFX_WIDGET()

        rigfx_class.show()


    def sort_def(self):
        '''

        :return:
        '''
        from spark.department.common import sortList
        reload(sortList)
        from spark.department.common.sortList import SORTLIST

        sort_class = SORTLIST()
        sort_class.sort_selected()

    def rivet_def(self):
        '''

        :return:
        '''
        from spark.department.common import rivet
        reload(rivet)
        from spark.department.common.rivet import RIVET
        rivet_class = RIVET()
        rivet_class.create()

    def cache_manger_def(self):
        '''

        :return:
        '''
        from spark.widget.common_widget import cacheManger_widget
        reload(cacheManger_widget)
        from spark.widget.common_widget.cacheManger_widget import CACHEMANGER_WIDGET
        cache_mager_class = CACHEMANGER_WIDGET()
        cache_mager_class.show()




