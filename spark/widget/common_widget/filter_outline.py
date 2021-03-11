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


class FILTER_OUTLINE(SAMPLE_WIDGET):
    def __init__(self, title='Filter Object', width=300):
        super(FILTER_OUTLINE, self).__init__(title=title, width=width)
        self.sample_widget_template = SAMPLE_WIDGET_TEMPLATE()
        self.sample_color_variable = COLOR_VARIABLE()

        '''
        geometry
        light
        camera
        curve
        locator
        Deformer
        ncloth
        constraint
        nuclus
        hairsystem
        
        
        '''


        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        get_widget = self.get_main_widget()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=get_widget)

        #SEARCH LINEEDIT
        search_lineedit = self.sample_widget_template.line_edit(set_PlaceholderText='Filter Object')
        verticalLayout.addWidget(search_lineedit)


        #TREE WIDGET
        self.treeWidget = self.sample_widget_template.treeWidget(setHeaderHidden=True)
        self.treeWidget.itemSelectionChanged.connect(self.treeWidget_def)
        self.add_tree_widget()
        '''
        l1 = QTreeWidgetItem(["String A"])
        for i in range(3):
            l1_child = QTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
            l1.addChild(l1_child)
        treeWidget.addTopLevelItem(l1)
        '''
        verticalLayout.addWidget(self.treeWidget)


        #REFRESH BUTTON
        button_name = 'Rrefresh'
        refresh_button = self.sample_widget_template.pushButton(set_text=button_name, connect=self.refresh_button_def)
        verticalLayout.addWidget(refresh_button)

    def refresh_button_def(self):
        self.add_tree_widget()
        print('this is the refresh button')


    def add_tree_widget(self):
        #clear the tree widget
        self.treeWidget.clear()

        obj = cmds.ls(transforms=True)
        list_obj_type = []
        for each in obj:
            shape = cmds.listRelatives(each, s=True)
            if shape:
                obj_type = cmds.objectType(shape[0])
                list_obj_type.append(obj_type)
            else:
                obj_type = cmds.objectType(each)
                list_obj_type.append(obj_type)

        filter_list_obj_tye = list(set(list_obj_type))

        for each in filter_list_obj_tye:
            print(each)
            l1 = QTreeWidgetItem([each.upper()])
            if each == 'camera':
                color = self.sample_color_variable.camera_color.get_value()
            elif each == 'mesh':
                color = self.sample_color_variable.mesh_color.get_value()
            elif each == 'locator':
                color = self.sample_color_variable.locator_color.get_value()
            elif each == 'nurbsCurve':
                color = self.sample_color_variable.nurbsCurve_color.get_value()
            elif 'light' in each.lower():
                color = self.sample_color_variable.light_color.get_value()
            else:
                color = self.sample_color_variable.violet_color.get_value()


            l1.setForeground(0, QBrush(QColor(color[0], color[1], color[2], 255)))
            #QColor(255, 255, 255, 127)



            self.treeWidget.addTopLevelItem(l1)

            obj = cmds.ls(type=each)
            parent_obj = cmds.listRelatives(obj, parent=True)
            if parent_obj == None:
                parent_obj = obj

            for each_obj in parent_obj:
                l2 = QTreeWidgetItem([each_obj])
                l1.addChild(l2)

    def treeWidget_def(self):
        cmds.select(cl=True)
        selected = list(self.treeWidget.selectedItems())
        if selected:
            for each in selected:
                obj = each.text(0)
                if cmds.objExists(obj):
                    cmds.select(obj, add=True)





####################
def soft_select_to_cluster_def(self):
    sel_vert = cmds.ls(sl=True)
    soft_selcetion = om.MGlobal.getRichSelection()
    rich_selection = om.MRichSelection(soft_selcetion)
    selection_list = rich_selection.getSelection()
    component = selection_list.getComponent(0)
    component_index = om.MFnSingleIndexedComponent(component[1])
    vertex_list = component_index.getElements()
    weight_list = {}
    for loop in range(len(vertex_list)):
        weight = component_index.weight(loop)
        influence = weight.influence
        weight_list.setdefault(vertex_list[loop],influence)


    obj_name = sel_vert[0].split(".vtx")[0]
    cmds.select(obj_name)
    #get the object name
    if cmds.objExists('Soft_Selection_to_Cluster*Handle'):
        cmds.select('Soft_Selection_to_Cluster*')
        sel_cluster = cmds.ls(sl=True)
        len_sel_cluster = len(sel_cluster)
        cluster_name = 'Soft_Selection_to_Cluster' + str(len_sel_cluster + 1)
    else:
        cluster_name = 'Soft_Selection_to_Cluster1'
    cmds.cluster(n=cluster_name)
    cluster_handle_name = cluster_name + 'Handle'
    cluster_shape_name = cmds.listRelatives(cluster_handle_name,s=True)[0]
    cmds.percent(cluster_name, (obj_name + '.vtx[0:]'), v=0)
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    cmds.progressBar( gMainProgressBar,
                      edit=True,
                      beginProgress=True,
                      isInterruptable=True,
                      status='Creating a soft Selection....',
                      maxValue=len(weight_list) )
    equal_value = len(weight_list)/100
    add_value = 0
    for each_weight in weight_list:
        current_vertex = obj_name + '.vtx[%s]' % each_weight
        weight_value = weight_list[each_weight]
        cmds.percent(cluster_name, current_vertex, v=weight_value)
        add_value = add_value + equal_value
        cmds.progressBar(gMainProgressBar, edit=True, step=add_value)
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)


    point_position  = cmds.pointPosition(sel_vert[0])
    cmds.setAttr((cluster_handle_name + '.rotatePivotX'),point_position[0])
    cmds.setAttr((cluster_handle_name + '.rotatePivotY'),point_position[1])
    cmds.setAttr((cluster_handle_name + '.rotatePivotZ'),point_position[2])
    cmds.setAttr((cluster_handle_name + '.scalePivotX'),point_position[0])
    cmds.setAttr((cluster_handle_name + '.scalePivotY'),point_position[1])
    cmds.setAttr((cluster_handle_name + '.scalePivotZ'),point_position[2])

    cmds.setAttr((cluster_shape_name + '.originX'),point_position[0])
    cmds.setAttr((cluster_shape_name + '.originY'),point_position[1])
    cmds.setAttr((cluster_shape_name + '.originZ'),point_position[2])

    cmds.select(cluster_handle_name)







