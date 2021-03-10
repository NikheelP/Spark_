from spark.widget.import_module import *
#from spark.widget.sample.sample_widget import SAMPLE_WIDGET
import os
import maya.cmds as cmds
from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template

for each in [sample_color_variable, sample_widget_template, style_sheet_template]:
    reload(each)

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE


class FILTER_OUTLINE(SAMPLE_WIDGET):
    def __init__(self, title='Filter Window'):
        super(FILTER_OUTLINE, self).__init__(title=title)
        self.sample_widget_template = SAMPLE_WIDGET_TEMPLATE()

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
            l1.setForeground(0, QBrush(Qt.green))


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













