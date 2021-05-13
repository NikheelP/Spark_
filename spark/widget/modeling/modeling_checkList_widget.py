from spark.department.Modeling import modeling_checklist

for each in [modeling_checklist]:
    reload(each)



from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET
from collections import OrderedDict

from spark.department.Modeling.modeling_checklist import MODELING_CHECKLIST

class MODELING_CHECKLIST_WIDGET(SAMPLE_WIDGET):
    def __init__(self, title='Modeling Checklist', width=500, height=600):
        super(MODELING_CHECKLIST_WIDGET, self).__init__(title=title, width=width, height=height)
        self.modeling_checklist_class = MODELING_CHECKLIST()

        self.checkbox_list = OrderedDict()
        self.checkbox_button_list = OrderedDict()
        self.progressBar_list = OrderedDict()



        self.initUI()


    def initUI(self):
        '''

        :return:
        '''

        main_widget = self.get_main_widget()

        verticalLayout = self.sample_widget_template.vertical_layout(parent_self=main_widget)

        verticalLayout.addWidget(self.upper_widget())

        verticalLayout.addWidget(self.lower_listWidget())



    def upper_widget(self):
        '''

        :return:
        '''
        upper_widget = self.sample_widget_template.widget_def()

        gridLayout = self.sample_widget_template.grid_layout(parent_self=upper_widget)

        new_value = 0
        vertical_val = 0

        # SELECT ALL
        select_all_text = 'Select All : '
        self.select_all_checkbox = self.sample_widget_template.checkbox(set_text=select_all_text,
                                                                stateChanged=self.select_all_checkbox_def)
        gridLayout.addWidget(self.select_all_checkbox, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0


        #DELETE HISTORY
        delete_history_text = ' Delete History: '
        self.checkbox_list['delete_history'] = self.sample_widget_template.checkbox(set_text=delete_history_text)
        gridLayout.addWidget(self.checkbox_list['delete_history'], vertical_val, new_value, 1, 1)
        new_value += 1

        self.progressBar_list['delete_history'] = self.sample_widget_template.progressBar()
        gridLayout.addWidget(self.progressBar_list['delete_history'], vertical_val, new_value, 1, 1)
        new_value += 1

        delete_history_button_text = 'Delete History'
        self.checkbox_button_list['delete_history'] =  self.sample_widget_template.pushButton(set_text=delete_history_button_text,
                                                                                              connect=self.deleteHistory_def)
        gridLayout.addWidget(self.checkbox_button_list['delete_history'], vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0


        #FREEZ TRABSFORM
        freez_transform_text = 'Freez Transform : '
        self.checkbox_list['freez_transform'] = self.sample_widget_template.checkbox(set_text=freez_transform_text)
        gridLayout.addWidget(self.checkbox_list['freez_transform'], vertical_val, new_value, 1, 1)
        new_value += 1

        freez_transform_button_text = 'Freez Transform'
        self.checkbox_button_list['freez_transform'] = self.sample_widget_template.pushButton(set_text=freez_transform_button_text,
                                                                                              set_object_name='Freez_Transform')
        gridLayout.addWidget(self.checkbox_button_list['freez_transform'], vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        #DELETE NAMESPACE
        delete_namespace_text = 'Delete Namespace : '
        self.checkbox_list['delete_namespace'] = self.sample_widget_template.checkbox(set_text=delete_namespace_text)
        gridLayout.addWidget(self.checkbox_list['delete_namespace'], vertical_val, new_value, 1, 1)
        new_value += 1

        delete_namespace_button_text = 'Delete Namespace'
        self.checkbox_button_list['delete_namespace'] = self.sample_widget_template.pushButton(set_text=delete_namespace_button_text,
                                                                                              set_object_name='Delete_Namespace')
        gridLayout.addWidget(self.checkbox_button_list['delete_namespace'], vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        #DELETE UNUSEDNODE
        delete_unusednode_text = 'Delete UnUsedNode : '
        self.checkbox_list['delete_unusedNode'] = self.sample_widget_template.checkbox(set_text=delete_unusednode_text)
        gridLayout.addWidget(self.checkbox_list['delete_unusedNode'], vertical_val, new_value, 1, 1)
        new_value += 1

        delete_unusednode_button_text = 'Delete unUsedNode'
        self.checkbox_button_list['delete_unusedNode'] = self.sample_widget_template.pushButton(set_text=delete_unusednode_button_text,
                                                                                                set_object_name='Delete_unUsedNode')
        gridLayout.addWidget(self.checkbox_button_list['delete_unusedNode'], vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        # MAKE A PIVOT ON CENTER ORIGINE
        make_pivot_center_origin_text = 'Make Pivot Center Origin : '
        self.checkbox_list['make_pivot_center'] = self.sample_widget_template.checkbox(set_text=make_pivot_center_origin_text)
        gridLayout.addWidget(self.checkbox_list['make_pivot_center'], vertical_val, new_value, 1, 1)
        new_value += 1


        pivot_center_button_text = 'Pivot Center'
        self.checkbox_button_list['make_pivot_center'] = self.sample_widget_template.pushButton(set_text=pivot_center_button_text,
                                                                                                set_object_name='Pivot_Center')
        gridLayout.addWidget(self.checkbox_button_list['make_pivot_center'], vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        create_modeling_checklist_button_text = 'Create Modeling Checklist'
        create_modeling_checklist_button = self.sample_widget_template.pushButton(set_text=create_modeling_checklist_button_text,
                                                                                  connect=self.create_modeling_checklist_button_def)
        gridLayout.addWidget(create_modeling_checklist_button, vertical_val, new_value, 1, 2)



        return upper_widget



    def lower_listWidget(self):
        '''

        :return:
        '''
        lower_listWidget = self.sample_widget_template.list_widget()

        return lower_listWidget


    def select_all_checkbox_def(self):
        '''

        :return:
        '''


        if self.select_all_checkbox.isChecked():
            for each in self.checkbox_list:
                self.checkbox_list[each].setChecked(True)
        else:
            for each in self.checkbox_list:
                self.checkbox_list[each].setChecked(False)


    def create_modeling_checklist_button_def(self):
        '''

        :return:
        '''


        for each in self.checkbox_list:
            a = 0
            if self.checkbox_list[each].isChecked():
                if each == 'delete_history':
                    self.modeling_checklist_class.deleteHistory()
                    green_styleSheet = self.green_styleSheet(self.checkbox_button_list[each].objectName())
                    self.checkbox_button_list[each].setStyleSheet(green_styleSheet)

                elif each == 'freez_transform':
                    self.modeling_checklist_class.freez_transform()
                    green_styleSheet = self.green_styleSheet(self.checkbox_button_list[each].objectName())
                    self.checkbox_button_list[each].setStyleSheet(green_styleSheet)

                elif each == 'delete_namespace':
                    self.modeling_checklist_class.delete_namespace()
                    green_styleSheet = self.green_styleSheet(self.checkbox_button_list[each].objectName())
                    self.checkbox_button_list[each].setStyleSheet(green_styleSheet)

                elif each == 'delete_unusedNode':
                    self.modeling_checklist_class.delUnusedNodes()
                    green_styleSheet = self.green_styleSheet(self.checkbox_button_list[each].objectName())
                    self.checkbox_button_list[each].setStyleSheet(green_styleSheet)

                a+=1


    def red_styleSheet(self, obj_name):
        '''

        :param obj_name:
        :return:
        '''
        return self.sample_widget_template.styleSheet_def(obj_name=obj_name, background_color=self.color_variable_class.red_color.get_value())

    def green_styleSheet(self, obj_name):
        '''

        :param obj_name:
        :return:
        '''
        return self.sample_widget_template.styleSheet_def(obj_name=obj_name,
                                                          background_color=self.color_variable_class.green_color.get_value())

    def deleteHistory_def(self):
        '''

        :return:
        '''
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.0001
            self.progressBar_list['delete_history'].setValue(self.completed)

'''
from spark.widget.modeling import modeling_checkList_widget
reload(modeling_checkList_widget)
modeling = modeling_checkList_widget.MODELING_CHECKLIST()
modeling.show()
'''