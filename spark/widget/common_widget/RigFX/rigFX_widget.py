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
from spark.department.CFX.cfx_tools.rigFX.rigFX_ import RIGFX
from spark.widget.widget_help import WIDGET_HELP
from spark.department.common.Outliner import outlinerWidget

from spark.widget.common_widget import rigFX_icon
rigFxIconPath = os.path.abspath(rigFX_icon.__file__).replace('\\', '/')
last_obj = rigFxIconPath.split('/')[-1]
rigfxIconPath_ = rigFxIconPath.split(last_obj)[0]


class RIGFX_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='RigFx'):
        super(RIGFX_WIDGET, self).__init__(title=title)

        self.spacing = 3
        self.icon_size = 30

        self.no_techanim_lineedit_lock = False
        self.no_techanimCloth_lineedit_lock = False
        self.rigfxname_lock = False


        self.validator = QDoubleValidator()

        self.rig_fx_class = RIGFX()
        self.widget_help_class = WIDGET_HELP()

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
        tree_widget_out = self.sample_widget_template.widget_def(parent_self=self.spliter_val,
                                                                 min_size=[350, 200])
        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=tree_widget_out)

        self.rigfx_tree_widget = outlinerWidget(outlinerName='Sample')
        self.rigfx_tree_widget.setWindowFlags(self.rigfx_tree_widget.windowFlags() | Qt.WindowStaysOnTopHint)
        self.rigfx_tree_widget.resize(600, 350)
        verticalLayout.addWidget(self.rigfx_tree_widget)

        return tree_widget_out

    def splitter_right_def(self):
        '''

        :return:
        '''
        right_main_widget = self.sample_widget_template.widget_def(parent_self=self.spliter_val)

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=right_main_widget, set_contents_margins=[10, 10, 10, 10], set_spacing=self.spacing)


        #create main widget
        main_widget = self.create_main_widget_def()
        verticalLayout.addWidget(main_widget)

        #create group widget
        group_widget = self.create_group_widget_def()
        verticalLayout.addWidget(group_widget)

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

        #NO OF THE TECHANIM FILE
        no_of_techanim_file_label_text = 'No Techanim File'
        no_of_techanim_file_label = self.sample_widget_template.label(set_text=no_of_techanim_file_label_text)
        grid_Layout.addWidget(no_of_techanim_file_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.no_of_techanim_file_lineedit = self.sample_widget_template.line_edit(set_text=str(3))
        self.no_of_techanim_file_lineedit.setValidator(self.validator)
        if self.no_techanim_lineedit_lock == True:
            self.no_of_techanim_file_lineedit.setDisabled(True)
        else:
            self.no_of_techanim_file_lineedit.setDisabled(False)

        grid_Layout.addWidget(self.no_of_techanim_file_lineedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        self.no_techanim_lineedit_lock = False
        self.no_techanimCloth_lineedit_lock = False
        self.rigfxname_lock = False


        #NO OF THE TECHANIM CLOTH FILE
        no_of_techanim_cloth_file_label_text = 'No TechanimCloth File'
        no_of_techanimcloth_file_label = self.sample_widget_template.label(set_text=no_of_techanim_cloth_file_label_text)
        grid_Layout.addWidget(no_of_techanimcloth_file_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.no_of_techanimcloth_file_lineedit = self.sample_widget_template.line_edit(set_text=str(3))
        self.no_of_techanimcloth_file_lineedit.setValidator(self.validator)
        if self.no_techanimCloth_lineedit_lock == True:
            self.no_of_techanimcloth_file_lineedit.setDisabled(True)
        else:
            self.no_of_techanimcloth_file_lineedit.setDisabled(False)
        grid_Layout.addWidget(self.no_of_techanimcloth_file_lineedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1



        # CREATE NAME LABEL
        create_name_label_text = 'Name'
        create_name_label = self.sample_widget_template.label(set_text=create_name_label_text)
        grid_Layout.addWidget(create_name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        #CREATE NAME LINEEDIT
        self.create_rigFx_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Specify the RigFx Name')
        self.create_rigFx_lineedit.textChanged.connect(self.create_rigFx_lineedit_def)
        if self.rigfxname_lock == True:
            self.create_rigFx_lineedit.setDisabled(True)
        else:
            self.create_rigFx_lineedit.setDisabled(False)
        grid_Layout.addWidget(self.create_rigFx_lineedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        #CREATE NAME BUTTON
        crete_rigfx_button_text = 'Create RigFx Group'
        crete_rigfx_button = self.sample_widget_template.pushButton(set_text=crete_rigfx_button_text,
                                                                    connect=self.crete_rigfx_button_def)
        grid_Layout.addWidget(crete_rigfx_button, vertical_val, new_value, 1, 2)

        return create_main_widget


    def create_group_widget_def(self):
        '''

        :return:
        '''

        create_main_widget = self.sample_widget_template.widget_def()
        grid_Layout = self.sample_widget_template.grid_layout(parent_self=create_main_widget)

        new_value = 0
        vertical_val = 0

        #CLOTH CHECKBOX
        self.cloth_checkbox = self.sample_widget_template.checkbox(set_text='Cloth', set_checked=True)
        self.cloth_checkbox.stateChanged.connect(self.cloth_checkbox_def)
        grid_Layout.addWidget(self.cloth_checkbox, vertical_val, new_value, 1, 1)
        new_value += 1

        #HAIR CHECKBOX
        self.hair_checkbox = self.sample_widget_template.checkbox(set_text='Hair')
        self.hair_checkbox.stateChanged.connect(self.hair_checkbox_def)
        grid_Layout.addWidget(self.hair_checkbox, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        # CREATE NAME LABEL
        create_name_label_text = 'Group Name'
        create_name_label = self.sample_widget_template.label(set_text=create_name_label_text)
        grid_Layout.addWidget(create_name_label, vertical_val, new_value, 1, 1)
        new_value += 1

        #CREATE NAME LINEEDIT'
        self.create_grp_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Select Clot_Grp or Hair_Grp and Create name under it')
        self.create_grp_lineedit.textChanged.connect(self.create_grp_lineedit_def)
        grid_Layout.addWidget(self.create_grp_lineedit, vertical_val, new_value, 1, 1)
        new_value = 0
        vertical_val += 1

        #CREATE NAME BUTTON
        create_grp_name_button_text = 'Create Cloth/Hair Group'
        create_grp_name_button = self.sample_widget_template.pushButton(set_text=create_grp_name_button_text,
                                                                        connect=self.create_grp_name_button_def)
        grid_Layout.addWidget(create_grp_name_button, vertical_val, new_value, 1, 2)

        return create_main_widget

    def cloth_checkbox_def(self):
        '''

        :return:
        '''
        if self.cloth_checkbox.isChecked():
            self.hair_checkbox.setChecked(False)
            self.cloth_checkbox.setChecked(True)
        else:
            self.hair_checkbox.setChecked(True)
            self.cloth_checkbox.setChecked(False)

    def hair_checkbox_def(self):
        '''

        :return:
        '''
        if self.hair_checkbox.isChecked():
            self.hair_checkbox.setChecked(True)
            self.cloth_checkbox.setChecked(False)
        else:
            self.cloth_checkbox.setChecked(True)
            self.hair_checkbox.setChecked(False)

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
        scroll_area = self.sample_widget_template.scrollArea(parent_self=self.cloth_tab_widget)
        main_widget_vertical_layout = self.sample_widget_template.vertical_layout(
            parent_self=self.cloth_tab_widget)
        scroll_widget = self.sample_widget_template.widget_def()
        scroll_area.setWidget(scroll_widget)
        main_widget_vertical_layout.addWidget(scroll_area)


        cloth_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=scroll_widget,
                                                                            set_spacing=self.spacing)

        #NCLOTH
        ncloth_button_text = 'nCloth'
        icon_ = 'ncloth.svg'
        icon_path = rigfxIconPath_ + icon_
        ncloth_toolTip = 'Create nCloh \nSelect geo and Select ClothGrp and run the command to create nCloth'
        ncloth_button = self.sample_widget_template.pushButton(set_text=ncloth_button_text,
                                                               set_icon=icon_path,
                                                               set_icon_size=[self.icon_size, self.icon_size],
                                                               connect=self.ncloth_def,
                                                               set_tool_tip=ncloth_toolTip)
        cloth_vertical_layout.addWidget(ncloth_button)

        #PASSIVE COLLIDER
        passive_collider_button_text = 'Passive Collider'
        icon_ = 'create_passive_collider.png'
        icon_path = rigfxIconPath_ + icon_
        passive_collider_button_setToolTip = 'Create Passive Collider\n Select geo and Click the button to Create Collution\n' \
                                             'if you are selecting secound object as *_Collider_Grp then collider will parent to that Grp or else\n' \
                                             'will parent to helper_Collider_Grp'
        passive_collider_button = self.sample_widget_template.pushButton(set_text=passive_collider_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                         set_tool_tip=passive_collider_button_setToolTip,
                                                                         connect=self.passive_collider_button_def)

        #"E:\PythonScript\Script\Script_Dir\Maya\Department\CFX\ClothHairFx\icon\create_passive_collider.png"
        cloth_vertical_layout.addWidget(passive_collider_button)

        #DELETE HISTORY
        delete_history_button_text = 'Delete History'
        delete_history_button_setToolTip = 'Delete History from the nCloth'
        delete_history_button = self.sample_widget_template.pushButton(set_text=delete_history_button_text,
                                                                       set_tool_tip=delete_history_button_setToolTip,
                                                                       connect=self.rig_fx_class.ncloth_DeleteHistory)
        cloth_vertical_layout.addWidget(delete_history_button)

        #DISPLAY CURRENT MESH
        display_current_mesh_button_text = 'Display Current Mesh'
        icon_ = 'ncltoh_current_mesh.png'
        icon_path = rigfxIconPath_ + icon_
        display_current_mesh_button_setToolTip = 'Display Current Mesh'
        display_current_mesh_button = self.sample_widget_template.pushButton(set_text=display_current_mesh_button_text,
                                                                             set_icon=icon_path,
                                                                             set_icon_size=[self.icon_size, self.icon_size],
                                                                             set_tool_tip=display_current_mesh_button_setToolTip,
                                                                             connect=self.rig_fx_class.displayCurrentMesh)
        cloth_vertical_layout.addWidget(display_current_mesh_button)

        #DISPLAY INPUT MESH
        display_input_mesh_button_text = 'Display Input Mesh'
        icon_ = 'input_mesh.png'
        icon_path = rigfxIconPath_ + icon_
        display_input_mesh_button_setToolTip = 'Display Input Mesh'
        display_input_mesh_button = self.sample_widget_template.pushButton(set_text=display_input_mesh_button_text,
                                                                           set_icon=icon_path,
                                                                           set_icon_size=[self.icon_size, self.icon_size],
                                                                             set_tool_tip=display_input_mesh_button_setToolTip,
                                                                             connect=self.rig_fx_class.displayInputMesh)
        cloth_vertical_layout.addWidget(display_input_mesh_button)

        #REMOVE CLOTH
        remove_cloth_button_text = 'Remove Cloth'
        icon_ = 'remove_cloth.png'
        icon_path = rigfxIconPath_ + icon_
        remove_cloth_button_setToolTip = 'Display Input Mesh'
        remove_cloth_button = self.sample_widget_template.pushButton(set_text=remove_cloth_button_text,
                                                                     set_icon=icon_path,
                                                                     set_icon_size=[self.icon_size, self.icon_size],
                                                                     set_tool_tip=remove_cloth_button_setToolTip,
                                                                     connect=self.rig_fx_class.removenCloth)
        cloth_vertical_layout.addWidget(remove_cloth_button)

        cloth_vertical_layout.addItem(self.sample_widget_template.spaceItem())

    def hair_widget_def(self):
        '''

        :return:
        '''

        scroll_area = self.sample_widget_template.scrollArea(parent_self=self.hair_tab_widget)
        main_widget_vertical_layout = self.sample_widget_template.vertical_layout(
            parent_self=self.hair_tab_widget)
        scroll_widget = self.sample_widget_template.widget_def()
        scroll_area.setWidget(scroll_widget)
        main_widget_vertical_layout.addWidget(scroll_area)

        hair_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=scroll_widget,
                                                                           set_spacing=self.spacing)

        # GET HAIR EXAMPLE
        get_hair_example_button_text = 'Get Hair Example'
        icon_ = 'get_hair_example.png'
        icon_path = rigfxIconPath_ + icon_
        get_hair_example_button = self.sample_widget_template.pushButton(set_text=get_hair_example_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                         connect=self.rig_fx_class.getHairExample)
        hair_vertical_layout.addWidget(get_hair_example_button)

        # PAINT HAIR FOLICAL
        paint_hair_folical_button_text = 'Paint Hair'
        icon_ = 'paint_hair_folical.png'
        icon_path = rigfxIconPath_ + icon_
        paint_hair_folical_button = self.sample_widget_template.pushButton(set_text=paint_hair_folical_button_text,
                                                                           set_icon=icon_path,
                                                                           set_icon_size=[self.icon_size, self.icon_size],
                                                                           connect=self.rig_fx_class.paintHairFolical)
        hair_vertical_layout.addWidget(paint_hair_folical_button)

        # MAKE SELECTION CURVE DYNAMICS
        make_selection_curve_to_dynamics_button_text = 'Make Selection curve to Dynamics'
        icon_ = 'make_selected_curve_dynamic.png'
        icon_path = rigfxIconPath_ + icon_
        nhair_toolTip = 'Create nHair \nSelect curve list and Select HairGrp and run the command to create HairSystem'
        make_selection_curve_to_dynamics_button = self.sample_widget_template.pushButton(set_text=make_selection_curve_to_dynamics_button_text,
                                                                                         set_icon=icon_path,
                                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                                         connect=self.nhair_def,
                                                                                         set_tool_tip=nhair_toolTip)
        hair_vertical_layout.addWidget(make_selection_curve_to_dynamics_button)

        # ADD OUTPUT CURVE TO HAIR
        add_output_curve_to_hair_button_text = 'Add Output Curve to Hair'
        icon_ = 'assign_paint_effects_brush_to_hair.png'
        icon_path = rigfxIconPath_ + icon_
        add_output_curve_to_hair_button = self.sample_widget_template.pushButton(set_text=add_output_curve_to_hair_button_text,
                                                                                 set_icon=icon_path,
                                                                                 set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(add_output_curve_to_hair_button)


        # ASSIGN PAINT EFFECTS BRUSH TO HAIR
        assign_paint_efftes_bush_to_hair_button_text = 'Assign Paint Effect Brush'
        icon_ = 'assign_paint_effects_brush_to_hair.png'
        icon_path = rigfxIconPath_ + icon_
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
        icon_path = rigfxIconPath_ + icon_
        scale_hair_button = self.sample_widget_template.pushButton(set_text=scale_hair_button_text,
                                                                   set_icon=icon_path,
                                                                   set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(scale_hair_button)

        # TRANSPLANT HAIR
        transplant_hair_button_text = 'Transplant Hair'
        icon_ = 'transplant_hair.png'
        icon_path = rigfxIconPath_ + icon_
        transplant_hair_button = self.sample_widget_template.pushButton(set_text=transplant_hair_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size])
        hair_vertical_layout.addWidget(transplant_hair_button)

        # DELETE HAIR
        delete_hair_button_text = 'Delete Hair'
        icon_ = 'delete_hair.png'
        icon_path = rigfxIconPath_ + icon_
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

        scroll_area = self.sample_widget_template.scrollArea(parent_self=self.constraint_tab_widget)
        main_widget_vertical_layout = self.sample_widget_template.vertical_layout(parent_self=self.constraint_tab_widget)
        scroll_widget = self.sample_widget_template.widget_def()
        scroll_area.setWidget(scroll_widget)
        main_widget_vertical_layout.addWidget(scroll_area)



        vericalLayout = self.sample_widget_template.vertical_layout(parent_self=scroll_widget,
                                                                    set_spacing=self.spacing)

        # COMPONENT
        component_button_text = 'Component'
        icon_ = 'component.png'
        icon_path = rigfxIconPath_ + icon_
        component_button_setToolTip = 'Select Vertex and Shift Select the Group name to Constraint Group and Clicke the button\n' \
                                      'NOTE: if you are not selecting the any Constraint button at the last it will move Constraint to helper_Constraint_Grp'
        component_button = self.sample_widget_template.pushButton(set_text=component_button_text,
                                                                  set_icon=icon_path,
                                                                  set_icon_size=[self.icon_size, self.icon_size],
                                                                  set_tool_tip=component_button_setToolTip,
                                                                  connect=self.component_button_def)
        vericalLayout.addWidget(component_button)

        # COMPONENT TO COMPONENT
        component_to_component_button_text = 'Component to Component'
        component_to_component_button_setToolTip = 'Select Vertex and Shift Select the Group name to Constraint Group and Clicke the button\n' \
                                      'NOTE: if you are not selecting the any Constraint button at the last it will move Constraint to helper_Constraint_Grp'
        component_to_component_button = self.sample_widget_template.pushButton(set_text=component_to_component_button_text,
                                                                               set_icon=icon_path,
                                                                               set_icon_size=[self.icon_size, self.icon_size],
                                                                               set_tool_tip=component_to_component_button_setToolTip,
                                                                               connect=self.component_to_component_button_def)
        vericalLayout.addWidget(component_to_component_button)

        # FORCE FIELD
        force_field_button_text = 'Force Field'
        icon_ = 'force_field.png'
        icon_path = rigfxIconPath_ + icon_
        force_field_button_setToolTip = 'Select Vertex and Shift Select the Group name to Constraint Group and Clicke the button\n' \
                                      'NOTE: if you are not selecting the any Constraint button at the last it will move Constraint to helper_Constraint_Grp'
        force_field_button = self.sample_widget_template.pushButton(set_text=force_field_button_text,
                                                                    set_icon=icon_path,
                                                                    set_icon_size=[self.icon_size, self.icon_size],
                                                                    set_tool_tip=force_field_button_setToolTip,
                                                                    connect=self.force_field_button_def)
        vericalLayout.addWidget(force_field_button)

        # POINT TO SURFACE
        point_to_surface_button_text = 'Point to Surface'
        icon_ = 'point_to_surface.png'
        icon_path = rigfxIconPath_ + icon_
        point_to_surface_button_toolTip = 'Select Vertex list + select Object to Create Point to Surface and if needed Select the COnstraint Group to parent COnstraint' \
                                          'to that Group \n' \
                                          'if you do not Select any Group at last will parent to helper_Constraint_Grp'
        point_to_surface_button = self.sample_widget_template.pushButton(set_text=point_to_surface_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                         set_tool_tip=point_to_surface_button_toolTip,
                                                                         connect=self.point_to_surface_button_def)
        vericalLayout.addWidget(point_to_surface_button)

        # SLIDE TO SURFACE
        slide_to_surface_button_text = 'Slide to Surface'
        icon_ = 'slide_on_surface.png'
        icon_path = rigfxIconPath_ + icon_
        slide_to_surface_button_toolTip = 'Select Vertex list + select Object to Create Slide to Surface and if needed Select the COnstraint Group to parent COnstraint' \
                                          'to that Group \n' \
                                          'if you do not Select any Group at last will parent to helper_Constraint_Grp'
        slide_to_surface_button = self.sample_widget_template.pushButton(set_text=slide_to_surface_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                         set_tool_tip=slide_to_surface_button_toolTip,
                                                                         connect=self.slide_to_surface_button_def)
        vericalLayout.addWidget(slide_to_surface_button)

        # TEARABLE SURFACE
        tearable_surface_button_text = 'tearable Surface'
        icon_ = 'tearable_surface.png'
        icon_path = rigfxIconPath_ + icon_
        tearable_surface_button = self.sample_widget_template.pushButton(set_text=tearable_surface_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                         connect=self.tearable_button_def)
        vericalLayout.addWidget(tearable_surface_button)

        # TRANSFORM CONSTRAINT
        transform_constraint_button_text = 'Transform Constraint'
        icon_ = 'transform_constraint.png'
        icon_path = rigfxIconPath_ + icon_
        transform_constraint_button = self.sample_widget_template.pushButton(set_text=transform_constraint_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                             connect=self.transform_button_def)
        vericalLayout.addWidget(transform_constraint_button)

        # AIR FIELD
        air_field_button_text = 'Air Field'
        icon_ = 'delete_hair.png'
        icon_path = rigfxIconPath_ + icon_
        air_field_button = self.sample_widget_template.pushButton(set_text=air_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                  connect=self.air_field_def)
        vericalLayout.addWidget(air_field_button)

        # DRAG FILED
        drag_field_button_text = 'Drag Field'
        icon_ = 'air_field.svg'
        icon_path = rigfxIconPath_ + icon_
        drag_field_button = self.sample_widget_template.pushButton(set_text=drag_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                   connect=self.drag_field_def)
        vericalLayout.addWidget(drag_field_button)

        # GRAVITY FIELD
        gravity_field_button_text = 'Gravity Field'
        icon_ = 'gravity.svg'
        icon_path = rigfxIconPath_ + icon_
        gravity_field_button = self.sample_widget_template.pushButton(set_text=gravity_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                      connect=self.gravity_field_def)
        vericalLayout.addWidget(gravity_field_button)

        # NEWTON FIELD
        newton_field_button_text = 'Newton Field'
        icon_ = 'newton_field.svg'
        icon_path = rigfxIconPath_ + icon_
        newton_field_button = self.sample_widget_template.pushButton(set_text=newton_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                     connect=self.newton_field_def)
        vericalLayout.addWidget(newton_field_button)

        # RADIUS FILED
        #"C:\Users\Admin\Desktop\Nikheel\Spark_Project\Spark_\spark\widget\common_widget\rigFX_icon\"
        radius_field_button_text = 'Radius Field'
        icon_ = 'radial_field.svg'
        icon_path = rigfxIconPath_ + icon_
        radius_field_button = self.sample_widget_template.pushButton(set_text=radius_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                     connect=self.radius_field_def)
        vericalLayout.addWidget(radius_field_button)

        # TURBULANCE FILED
        turbulance_field_button_text = 'Turbulance Field'
        icon_ = 'turbulance_field.svg'
        icon_path = rigfxIconPath_ + icon_
        turbulance_field_button = self.sample_widget_template.pushButton(set_text=turbulance_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                         connect=self.turbulance_field_def)
        vericalLayout.addWidget(turbulance_field_button)

        # UNIFORM FIELD
        uniform_field_button_text = 'Uniform Field'
        icon_ = 'duniform.svg'
        icon_path = rigfxIconPath_ + icon_
        uniform_field_button = self.sample_widget_template.pushButton(set_text=uniform_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                      connect=self.uniform_field_def)
        vericalLayout.addWidget(uniform_field_button)

        # VORTEX FIELD
        vortex_field_button_text = 'Vortex Field'
        icon_ = 'vortex_field.svg'
        icon_path = rigfxIconPath_ + icon_
        vortex_field_button = self.sample_widget_template.pushButton(set_text=vortex_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                     connect=self.vortex_field_def)
        vericalLayout.addWidget(vortex_field_button)

        # VOLUME FIELD
        volume_field_button_text = 'Volume Field'
        icon_ = 'volume_axis.png'
        icon_path = rigfxIconPath_ + icon_
        volume_field_button = self.sample_widget_template.pushButton(set_text=volume_field_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                     connect=self.volume_field_def)
        vericalLayout.addWidget(volume_field_button)

        # VOLUME CURVE
        volume_curve_button_text = 'Volume Curve'
        icon_ = 'volume_axis.png'
        icon_path = rigfxIconPath_ + icon_
        volume_curve_button = self.sample_widget_template.pushButton(set_text=volume_curve_button_text,
                                                                         set_icon=icon_path,
                                                                         set_icon_size=[self.icon_size, self.icon_size],
                                                                     connect=self.volume_curve_def)
        vericalLayout.addWidget(volume_curve_button)

    def extra_def(self):
        '''

        :return:
        '''

        scroll_area = self.sample_widget_template.scrollArea(parent_self=self.extra_tab_widget)
        main_widget_vertical_layout = self.sample_widget_template.vertical_layout(
            parent_self=self.extra_tab_widget)
        scroll_widget = self.sample_widget_template.widget_def()
        scroll_area.setWidget(scroll_widget)
        main_widget_vertical_layout.addWidget(scroll_area)


        vericalLayout = self.sample_widget_template.vertical_layout(parent_self=scroll_widget,
                                                                    set_spacing=self.spacing)

        # UPDATE OR CREATE LAYER
        update_or_create_layer_text = 'Update or Create Layer system'
        update_or_create_layer_tooolTip = 'Update the Layer System with the Name and if it not exists will creat that '
        update_or_create_layer = self.sample_widget_template.pushButton(set_text=update_or_create_layer_text,
                                                                        set_tool_tip=update_or_create_layer_tooolTip,
                                                                        connect=self.rig_fx_class.update_sets_layer)
        vericalLayout.addWidget(update_or_create_layer)

        '''
        #IMPORT CLOTH RIG
        import_cloth_rig_button_text = 'Improt Cloth Rig'
        import_cloth_rig_button = self.sample_widget_template.pushButton(set_text=import_cloth_rig_button_text)
        vericalLayout.addWidget(import_cloth_rig_button)

        #COMBINE CLOTH RIG
        combine_cloth_rig_button_text = 'Combine Cloth Rig'
        combine_cloth_rig_button = self.sample_widget_template.pushButton(set_text=combine_cloth_rig_button_text)
        vericalLayout.addWidget(combine_cloth_rig_button)

        #ADD INPUT GEO TO INPUT SET
        add_input_geo_to_input_set_text = 'Add Input Geo to InputGeo Set'
        add_input_geo_to_input_set = self.sample_widget_template.pushButton(set_text=add_input_geo_to_input_set_text)
        vericalLayout.addWidget(add_input_geo_to_input_set)

        #ADD TECHANIM TO TECHANIM SET
        add_techanim_geo_to_techanim_set_text = 'Add TechAnim Geo to TechAnim Set'
        add_techanim_geo_to_techanim_set = self.sample_widget_template.pushButton(set_text=add_techanim_geo_to_techanim_set_text)
        vericalLayout.addWidget(add_techanim_geo_to_techanim_set)

        #ADD TECHANIM CLOTH TO TECHANIMCLOTH SET
        add_techanim_cloth_geo_to_techanimcloth_set_text = 'Add TechAnimCloth Geo to TechAnimCloth Set'
        add_techanim_cloth_geo_to_techanimcloth_set = self.sample_widget_template.pushButton(set_text=add_techanim_cloth_geo_to_techanimcloth_set_text)
        vericalLayout.addWidget(add_techanim_cloth_geo_to_techanimcloth_set)

        #ADD FINAL GEO TO FINALGEO SET
        add_final_geo_to_final_set_text = 'Add Final Geo to Final Set'
        add_final_geo_to_final_set = self.sample_widget_template.pushButton(set_text=add_final_geo_to_final_set_text)
        vericalLayout.addWidget(add_final_geo_to_final_set)

       

        #MAKE RIGFX ORGANIZED
        make_rigfx_organized_text = 'Make RigFx Organized'
        make_rigfx_organized_tooolTip = 'Make a RigFx Organized'
        make_rigfx_organized = self.sample_widget_template.pushButton(set_text=make_rigfx_organized_text,
                                                                        set_tool_tip=make_rigfx_organized_tooolTip,
                                                                      connect=self.rig_fx_class.update_set)
        vericalLayout.addWidget(make_rigfx_organized)

        # ADD TAG
        add_rigfx_tag_text = 'Add RigFx Tag'
        add_rigfx_tag_tooolTip = 'Add Manually Tag'
        add_rigfx_tag = self.sample_widget_template.pushButton(set_text=add_rigfx_tag_text,
                                                                      set_tool_tip=add_rigfx_tag_tooolTip,
                                                                      connect=self.add_rigfx_tag_def)
        vericalLayout.addWidget(add_rigfx_tag)

        # Skin Bind Jnt
        skinBin_jnt_text = 'skinBind Jnt'
        skinBin_jnt_tooolTip = 'Bind the Skin with the specific Joint'
        skinBin_jnt = self.sample_widget_template.pushButton(set_text=skinBin_jnt_text,
                                                             set_tool_tip=skinBin_jnt_tooolTip,
                                                             connect=self.skinBin_jnt_def)
        vericalLayout.addWidget(skinBin_jnt)

        '''




        vericalLayout.addItem(self.sample_widget_template.spaceItem())






    def create_rigFx_lineedit_def(self):
        '''
        set the tex what we need remove all the punctuation in the lineedit
        :return:
        '''
        text = self.create_rigFx_lineedit.text()
        self.create_rigFx_lineedit.setText(self.widget_help_class.make_simple_text(text))

    def create_grp_lineedit_def(self):
        '''
        set the tex what we need remove all the punctuation in the lineedit
        :return:
        '''
        text = self.create_grp_lineedit.text()
        self.create_grp_lineedit.setText(self.widget_help_class.make_simple_text(text))


    def ncloth_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)

        #CREATE A TECHANIM FILE
        self.rig_fx_class.create_cloth_rigfx_def(sel_obj[0], cloth_grp_name=sel_obj[1])


    def nhair_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        hair_grp = sel_obj[-1]
        curve_list = sel_obj.remove(hair_grp)

        self.rig_fx_class.create_hair_rigfx_def(hair_list=sel_obj, grp_name=hair_grp)


    def passive_collider_button_def(self):
        '''
        CREATE A PASSIVE COLLIDER
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        if len(sel_obj) > 2:
            raise RuntimeError('Please Select one ot Two Object to Create Passive Collider')

        if len(sel_obj) == 2:
            self.rig_fx_class.passive_collider_def(obj_name=sel_obj[0], grp_name=sel_obj[1])
        else:
            self.rig_fx_class.passive_collider_def(obj_name=sel_obj[0])

    def delete_history_button_def(self):
        '''

        :return:
        '''
        self.rig_fx_class.ncloth_DeleteHistory()

    def update_rigfx_tree_widget(self):
        '''
        update the tree widget
        :return:
        '''
        pass

    def create_grp_name_button_def(self):
        '''
        CREATE A CLOTH AND HAIR GROUP
        :return:
        '''

        #GET THE CHECKBOX
        self.hair_checkbox_query = self.hair_checkbox.isChecked()
        grp_name = self.create_grp_lineedit.text()

        if self.hair_checkbox_query == True:
            self.rig_fx_class.create_hair_folder_structure(hair_name=grp_name)
        else:
            self.rig_fx_class.create_cloth_folder_structure(cloth_name=grp_name)

        self.create_grp_lineedit.setText('')


        '''
        #GET THE NAME OF THE OBJECT
        grp_name = self.create_grp_lineedit.text()

        sel_obj = cmds.ls(sl=True)
        if len(sel_obj) == 1:
            if cmds.getAttr(sel_obj[0] + '.obj_type') == 'Cloth':
                self.rig_fx_class.create_cloth_folder_structure(cloth_name=grp_name)
            elif cmds.getAttr(sel_obj[0] + '.obj_type') == 'Hair':
                self.rig_fx_class.create_hair_folder_structure(hair_name=grp_name)
                print('Hair basic Setup is going to create')
            else:
                raise RuntimeError('Please Atlease Select Cloth_Grp or Hair_Grp to Run the command')
        '''

    def create_techanim_grp(self):
        '''

        :return:
        '''

        pass

    def crete_rigfx_button_def(self):
        '''

        :return:
        '''
        rigFx_name = self.create_rigFx_lineedit.text()
        no_techanim_file = int(self.no_of_techanim_file_lineedit.text())
        no_techanimcloth_file = int(self.no_of_techanimcloth_file_lineedit.text())
        if rigFx_name != '':
            self.rig_fx_class.rigFx_grp_def(rigFx_name, noTechAnimGrp=no_techanim_file, noTechAnimCloth=no_techanimcloth_file)
        self.create_rigFx_lineedit.setText('')

        self.no_techanim_lineedit_lock = True
        self.no_techanimCloth_lineedit_lock = True
        self.rigfxname_lock = True

        self.no_of_techanim_file_lineedit.setDisabled(True)
        self.no_of_techanimcloth_file_lineedit.setDisabled(True)
        self.create_rigFx_lineedit.setDisabled(True)


    def component_button_def(self):
        '''
        #CREATE A COMPONENT BUTTON
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.component_constraint(sel_obj, type=self.rig_fx_class.component_type)


    def component_to_component_button_def(self):
        '''
                #CREATE A COMPONENT BUTTON
                :return:
                '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.component_constraint(sel_obj, type=self.rig_fx_class.component_to_component_type)

    def force_field_button_def(self):
        '''
        #CREATE A COMPONENT BUTTON
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.component_constraint(sel_obj, type=self.rig_fx_class.forcefield_type)

    def point_to_surface_button_def(self):
        '''
        CREATE A POINT TO SURFACE
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.point_to_surface_constriant(sel_obj, type=self.rig_fx_class.pointtosurface_type)


    def slide_to_surface_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.point_to_surface_constriant(sel_obj, type=self.rig_fx_class.slidetosurface_type)

    def tearable_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.tearable_transform_constriant(sel_obj, type=self.rig_fx_class.tearablesurface_type)

    def transform_button_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.tearable_transform_constriant(sel_obj, type=self.rig_fx_class.transoformconstraint_type)

    def air_field_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.airfield_type)


    def drag_field_def(self):
        '''

                :return:
                '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.dragfield_type)


    def gravity_field_def(self):
        '''

        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.gravityfield_type)

    def newton_field_def(self):
        '''
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.newtonfield_type)

    def radius_field_def(self):
        '''
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.radiusfield_type)

    def turbulance_field_def(self):
        '''
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.turbulancefield_type)

    def uniform_field_def(self):
        '''
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.uniformfield_type)

    def vortex_field_def(self):
        '''
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.vortexfield_type)


    def volume_field_def(self):
        '''
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.volumefield_type)

    def volume_curve_def(self):
        '''
        :return:
        '''
        sel_obj = cmds.ls(sl=True)
        self.rig_fx_class.field_def(sel_obj=sel_obj, type=self.rig_fx_class.volumecurve_type)


    def add_rigfx_tag_def(self):
        '''

        :return:
        '''
        from spark.widget.common_widget.RigFX import rigfxAddTag
        reload(rigfxAddTag)
        from spark.widget.common_widget.RigFX.rigfxAddTag import RIGFXADDTAG
        rigfxAddTag_class = RIGFXADDTAG()
        rigfxAddTag_class.show()

    def skinBin_jnt_def(self):
        '''

        :return:
        '''
        from spark.widget.common_widget.RigFX import skinBindJnt
        reload(skinBindJnt)
        from spark.widget.common_widget.RigFX.skinBindJnt import SKINBINDJNT
        skinBindJnt_class = SKINBINDJNT()
        skinBindJnt_class.show()










