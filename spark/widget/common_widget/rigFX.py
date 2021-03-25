from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
from functools import partial

from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.department.common import rename
from spark.department.CFX.cfx_tools.rigFX import rigFX_
for each in [sample_color_variable, sample_widget_template, style_sheet_template, rename, rigFX_]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.widget.sample.sample_color_variable import COLOR_VARIABLE
from spark.department.CFX.cfx_tools.rigFX.rigFX_ import RIGFX

from spark.widget.common_widget import rigFX_icon
rigfxIconPath = os.path.abspath(rigFX_icon.__file__).replace('\\', '/')




class RIGFX_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='RigFx'):
        super(RIGFX_WIDGET, self).__init__(title=title)

        self.spacing = 3
        self.icon_size = 20

        self.rig_fx_class = RIGFX()

        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        widget = self.get_main_widget()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=widget)

        self.spliter_val = self.sample_widget_template.splitter_def(parent_self=widget, set_orientation=self.sample_widget_template.horizonatal)
        verticalLayout.addWidget(self.spliter_val)

        self.splitter_left_def()

        self.splitter_right_def()

    def splitter_left_def(self):
        '''

        :return:
        '''
        tree_widget_out = self.sample_widget_template.widget_def(parent_self=self.spliter_val)

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=tree_widget_out)

        tree_widget = self.sample_widget_template.treeWidget(setHeaderHidden=True)
        verticalLayout.addWidget(tree_widget)

        return tree_widget_out

    def splitter_right_def(self):
        '''

        :return:
        '''
        right_main_widget = self.sample_widget_template.widget_def(parent_self=self.spliter_val)

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=right_main_widget, set_contents_margins=[10, 10, 10, 10], set_spacing=self.spacing)


        #create main widget
        verticalLayout.addWidget(self.create_main_widget_def())

        #create group widget
        verticalLayout.addWidget(self.create_group_widget_def())

        #tab widget
        verticalLayout.addWidget(self.tab_widget_def())

    def create_main_widget_def(self):
        '''

        :return:
        '''

        create_main_widget = self.sample_widget_template.widget_def()
        grid_Layout = self.sample_widget_template.grid_layout(parent_self=create_main_widget)

        new_value = 0
        vertical_val = 0

        # CREATE NAME LABEL
        create_name_label_text = 'Name'
        create_name_label = self.sample_widget_template.label(set_text=create_name_label_text)
        grid_Layout.addWidget(create_name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        #CREATE NAME LINEEDIT'
        create_name_lineedit = self.sample_widget_template.line_edit()
        grid_Layout.addWidget(create_name_lineedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        #CREATE NAME BUTTON
        crete_name_button_text = 'Create RigFx Group'
        create_name_button = self.sample_widget_template.pushButton(set_text=crete_name_button_text)
        grid_Layout.addWidget(create_name_button, vertical_val, new_value, 1, 2)

        return create_main_widget

    def create_group_widget_def(self):
        '''

        :return:
        '''

        create_main_widget = self.sample_widget_template.widget_def()
        grid_Layout = self.sample_widget_template.grid_layout(parent_self=create_main_widget)

        new_value = 0
        vertical_val = 0

        # CREATE NAME LABEL
        create_name_label_text = 'Group Name'
        create_name_label = self.sample_widget_template.label(set_text=create_name_label_text)
        grid_Layout.addWidget(create_name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        #CREATE NAME LINEEDIT'
        create_name_lineedit = self.sample_widget_template.line_edit()
        grid_Layout.addWidget(create_name_lineedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        #CREATE NAME BUTTON
        create_grp_name_button_text = 'Create Cloth/Hair Group'
        create_grp_name_button = self.sample_widget_template.pushButton(set_text=create_grp_name_button_text)
        grid_Layout.addWidget(create_grp_name_button, vertical_val, new_value, 1, 2)

        return create_main_widget

    def tab_widget_def(self):
        '''

        :return:
        '''
        tab_main_widget = self.sample_widget_template.widget_def()

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=tab_main_widget)



        tab_widget = self.sample_widget_template.tab_widget(tab_main_widget)
        vertical_layout.addWidget(tab_widget)

        #CLOTH TAB
        self.cloth_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.cloth_widget_def()
        tab_widget.addTab(self.cloth_tab_widget, 'Cloth')

        #HAIR TAB
        self.hair_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.hair_widget_def()
        tab_widget.addTab(self.hair_tab_widget, 'Hair')

        #CONSTRAINT TAB
        self.constraint_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.constraint_field_def()
        tab_widget.addTab(self.constraint_tab_widget, 'Constraint/Field')

        #EXTRA TAB
        self.extra_tab_widget = self.sample_widget_template.widget_def(parent_self=tab_widget)
        self.extra_def()
        tab_widget.addTab(self.extra_tab_widget, 'Extra')


        return tab_main_widget

    def cloth_widget_def(self):
        '''

        :return:
        '''
        cloth_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.cloth_tab_widget,
                                                                            set_spacing=self.spacing)

        #NCLOTH
        ncloth_button_text = 'nCloth'
        icon_ = 'ncloth.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        ncloth_button = self.sample_widget_template.pushButton(set_text=ncloth_button_text,
                                                               set_icon=icon_path,
                                                               set_icon_size=[self.icon_size, self.icon_size],
                                                               connect=self.ncloth_def)
        cloth_vertical_layout.addWidget(ncloth_button)

        #PASSIVE COLLIDER
        passive_collider_button_text = 'Passive Collider'
        icon_ = 'create_passive_collider.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        passive_collider_button = self.sample_widget_template.pushButton(set_text=passive_collider_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])

        #"E:\PythonScript\Script\Script_Dir\Maya\Department\CFX\ClothHairFx\icon\create_passive_collider.png"
        cloth_vertical_layout.addWidget(passive_collider_button)

        #DELETE HISTORY
        delete_history_button_text = 'Delete History'

        delete_history_button = self.sample_widget_template.pushButton(set_text=delete_history_button_text)
        cloth_vertical_layout.addWidget(delete_history_button)

        #DISPLAY CURRENT MESH
        display_current_mesh_button_text = 'Display Current Mesh'
        icon_ = 'ncltoh_current_mesh.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        display_current_mesh_button = self.sample_widget_template.pushButton(set_text=display_current_mesh_button_text,
                                                                             set_icon=icon_path,
                                                                             set_icon_size=[self.icon_size, self.icon_size])
        cloth_vertical_layout.addWidget(display_current_mesh_button)

        #DISPLAY INPUT MESH
        display_input_mesh_button_text = 'Display Input Mesh'
        icon_ = 'input_mesh.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        display_input_mesh_button = self.sample_widget_template.pushButton(set_text=display_input_mesh_button_text,
                                                                           set_icon=icon_path,
                                                                           set_icon_size=[self.icon_size, self.icon_size])
        cloth_vertical_layout.addWidget(display_input_mesh_button)

        #REMOVE CLOTH
        remove_cloth_button_text = 'Remove Cloth'
        icon_ = 'remove_cloth.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        remove_cloth_button = self.sample_widget_template.pushButton(set_text=remove_cloth_button_text,
                                                                     set_icon=icon_path,
                                                                     set_icon_size=[self.icon_size, self.icon_size])
        cloth_vertical_layout.addWidget(remove_cloth_button)

        cloth_vertical_layout.addItem(self.sample_widget_template.spaceItem())

    def hair_widget_def(self):
        '''

        :return:
        '''
        hair_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.hair_tab_widget,
                                                                           set_spacing=self.spacing)

        # GET HAIR EXAMPLE
        get_hair_example_button_text = 'Get Hair Example'
        icon_ = 'get_hair_example.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        get_hair_example_button = self.sample_widget_template.pushButton(set_text=get_hair_example_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(get_hair_example_button)

        # PAINT HAIR FOLICAL
        paint_hair_folical_button_text = 'Paint Hair'
        icon_ = 'paint_hair_folical.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        paint_hair_folical_button = self.sample_widget_template.pushButton(set_text=paint_hair_folical_button_text,
                                                                           set_icon=icon_path,
                                                                           set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(paint_hair_folical_button)

        # MAKE SELECTION CURVE DYNAMICS
        make_selection_curve_to_dynamics_button_text = 'Make Selection curve to Dynamics'
        icon_ = 'make_selected_curve_dynamic.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        make_selection_curve_to_dynamics_button = self.sample_widget_template.pushButton(set_text=make_selection_curve_to_dynamics_button_text,
                                                                                         set_icon=icon_path,
                                                                                         set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(make_selection_curve_to_dynamics_button)

        # ADD OUTPUT CURVE TO HAIR
        add_output_curve_to_hair_button_text = 'Add Output Curve to Hair'
        icon_ = 'assign_paint_effects_brush_to_hair.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        add_output_curve_to_hair_button = self.sample_widget_template.pushButton(set_text=add_output_curve_to_hair_button_text,
                                                                                 set_icon=icon_path,
                                                                                 set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(add_output_curve_to_hair_button)


        # ASSIGN PAINT EFFECTS BRUSH TO HAIR
        assign_paint_efftes_bush_to_hair_button_text = 'Assign Paint Effect Brush'
        icon_ = 'assign_paint_effects_brush_to_hair.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        assign_paint_efftes_bush_to_hair_button = self.sample_widget_template.pushButton(set_text=assign_paint_efftes_bush_to_hair_button_text,
                                                                                         set_icon=icon_path,
                                                                                         set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(assign_paint_efftes_bush_to_hair_button)

        # ADD PAINT EFFECTS OUTPUT TO HAIR
        assign_paint_efftes_output_to_hair_button_text = 'Assign Paint Effects Output to Hair'

        assign_paint_efftes_output_to_hair_button = self.sample_widget_template.pushButton(set_text=assign_paint_efftes_output_to_hair_button_text)
        hair_vertical_layout.addWidget(assign_paint_efftes_output_to_hair_button)

        # SCALE HAIR TOOL
        scale_hair_button_text = 'Scale Hair'
        icon_ = 'scale_hair_tool.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        scale_hair_button = self.sample_widget_template.pushButton(set_text=scale_hair_button_text,
                                                                   set_icon=icon_path,
                                                                   set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(scale_hair_button)

        # TRANSPLANT HAIR
        transplant_hair_button_text = 'Transplant Hair'
        icon_ = 'transplant_hair.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        transplant_hair_button = self.sample_widget_template.pushButton(set_text=transplant_hair_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(transplant_hair_button)

        # DELETE HAIR
        delete_hair_button_text = 'Delete Hair'
        icon_ = 'delete_hair.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        delete_hair_button = self.sample_widget_template.pushButton(set_text=delete_hair_button_text,
                                                                    set_icon=icon_path,
                                                                    set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(delete_hair_button)

        hair_vertical_layout.addItem(self.sample_widget_template.spaceItem())

    def constraint_field_def(self):
        '''

        self.component = icon_path + "/component.png"
        self.force_field = icon_path + "/force_field.png"
        self.point_to_surface = icon_path + "/point_to_surface.png"
        self.slide_on_surface = icon_path + "/slide_on_surface.png"
        self.tearable_surface = icon_path + "/tearable_surface.png"
        self.transform_constraint = icon_path + "/transform_constraint.png"


        :return:
        '''

        vericalLayout = self.sample_widget_template.vertical_layout(parent_self=self.constraint_tab_widget)

        # COMPONENT
        component_button_text = 'Component'
        icon_ = 'component.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        component_button = self.sample_widget_template.pushButton(set_text=component_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(component_button)

        # COMPONENT TO COMPONENT
        component_to_component_button_text = 'Component to Component'
        component_to_component_button = self.sample_widget_template.pushButton(set_text=component_to_component_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(component_to_component_button)

        # FORCE FIELD
        force_field_button_text = 'Force Field'
        icon_ = 'force_field.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        force_field_button = self.sample_widget_template.pushButton(set_text=force_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(force_field_button)

        # POINT TO SURFACE
        point_to_surface_button_text = 'Point to Surface'
        icon_ = 'point_to_surface.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        point_to_surface_button = self.sample_widget_template.pushButton(set_text=point_to_surface_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(point_to_surface_button)

        # SLIDE TO SURFACE
        slide_to_surface_button_text = 'Slide to Surface'
        icon_ = 'slide_on_surface.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        slide_to_surface_button = self.sample_widget_template.pushButton(set_text=slide_to_surface_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(slide_to_surface_button)

        # TEARABLE SURFACE
        tearable_surface_button_text = 'tearable Surface'
        icon_ = 'tearable_surface.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        tearable_surface_button = self.sample_widget_template.pushButton(set_text=tearable_surface_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(tearable_surface_button)

        # TRANSFORM CONSTRAINT
        transform_constraint_button_text = 'Transform Constraint'
        icon_ = 'transform_constraint.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        transform_constraint_button = self.sample_widget_template.pushButton(set_text=transform_constraint_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(transform_constraint_button)

        # AIR FIELD
        air_field_button_text = 'Air Field'
        icon_ = 'delete_hair.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        air_field_button = self.sample_widget_template.pushButton(set_text=air_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(air_field_button)

        # DRAG FILED
        drag_field_button_text = 'Drag Field'
        icon_ = 'air_field.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        drag_field_button = self.sample_widget_template.pushButton(set_text=drag_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(drag_field_button)

        # GRAVITY FIELD
        gravity_field_button_text = 'Gravity Field'
        icon_ = 'gravity.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        gravity_field_button = self.sample_widget_template.pushButton(set_text=gravity_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(gravity_field_button)

        # NEWTON FIELD
        newton_field_button_text = 'Newton Field'
        icon_ = 'newton_field.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        newton_field_button = self.sample_widget_template.pushButton(set_text=newton_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(newton_field_button)

        # RADIUS FILED
        radius_field_button_text = 'Radius Field'
        icon_ = 'radial_field.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        radius_field_button = self.sample_widget_template.pushButton(set_text=radius_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(radius_field_button)

        # TURBULANCE FILED
        turbulance_field_button_text = 'Turbulance Field'
        icon_ = 'turbulance_field.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        turbulance_field_button = self.sample_widget_template.pushButton(set_text=turbulance_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(turbulance_field_button)

        # UNIFORM FIELD
        uniform_field_button_text = 'Uniform Field'
        icon_ = 'duniform.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        uniform_field_button = self.sample_widget_template.pushButton(set_text=uniform_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(uniform_field_button)

        # VORTEX FIELD
        vortex_field_button_text = 'Vortex Field'
        icon_ = 'vortex_field.svg'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        vortex_field_button = self.sample_widget_template.pushButton(set_text=vortex_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(vortex_field_button)

        # VOLUME FIELD
        volume_field_button_text = 'Volume Field'
        icon_ = 'volume_axis.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        volume_field_button = self.sample_widget_template.pushButton(set_text=volume_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(volume_field_button)

        # VOLUME CURVE
        volume_curve_button_text = 'Volume Curve'
        icon_ = 'volume_axis.png'
        icon_path = rigfxIconPath.replace('__init__.py', icon_)
        volume_curve_button = self.sample_widget_template.pushButton(set_text=volume_curve_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        vericalLayout.addWidget(volume_curve_button)

    def extra_def(self):
        '''

        :return:
        '''

        vericalLayout = self.sample_widget_template.vertical_layout(parent_self=self.extra_tab_widget,
                                                                    set_spacing=self.spacing)


        #IMPORT CLOTH RIG
        import_cloth_rig_button_text = 'Improt Cloth Rig'
        import_cloth_rig_button = self.sample_widget_template.pushButton(set_text=import_cloth_rig_button_text)
        vericalLayout.addWidget(import_cloth_rig_button)

        #COMBINE CLOTH RIG
        combine_cloth_rig_button_text = 'Combine Cloth Rig'
        combine_cloth_rig_button = self.sample_widget_template.pushButton(set_text=combine_cloth_rig_button_text)
        vericalLayout.addWidget(combine_cloth_rig_button)

        vericalLayout.addItem(self.sample_widget_template.spaceItem())

    def ncloth_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        for each in sel_obj:
            cloth_name, input_name, rest_name, ncloth_name, nucleus_name = self.rig_fx_class.create_Cloth(each)
            print('this is the cloth Name: ', cloth_name)
            print('this is the input Name: ', input_name)
            print('this is the rest Name: ', rest_name)
            print('this is the ncloth Name: ', ncloth_name)
            print('this is the nucleus Name: ', nucleus_name)


    def create_techanim_grp(self):
        '''

        :return:
        '''

        pass

    def basic_folder_structure(self):
        '''

        :return:
        '''
        rigFx_list = ['ClothRigFX', 'Input_Grp', 'TechAnim_Grp', 'Sim_Grp', 'TechAnimCloth_Grp', 'TechAnimClothFinal_Grp', 'Final_Grp']