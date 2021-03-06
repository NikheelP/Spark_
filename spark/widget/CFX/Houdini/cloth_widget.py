from spark.widget.sample import sample_color_variable, sample_widget_template, style_sheet_template
from spark.widget.import_module import *
from spark.department.Help.Houdini import nodes, help
import hou

for each in [sample_color_variable, sample_widget_template, style_sheet_template, help, nodes]:
    reload(each)

from spark.widget.sample.sample_widget_template import SAMPLE_WIDGET_TEMPLATE
from spark.department.Help.Houdini.help import HELP
from spark.department.Help.Houdini.nodes import NODES


class CLOTH_WIDGET():
    def __init__(self):
        self.sample_widget_template = SAMPLE_WIDGET_TEMPLATE()
        self.help_class = HELP()
        self.node_class = NODES()

    def ui(self, widget):
        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=widget)

        # SEARCH WIDGET
        search_widget = self.search_widget_ui()
        vertical_layout.addWidget(search_widget)

        # BUTTON WIDGET
        button_widget = self.button_def()
        vertical_layout.addWidget(button_widget)

    def search_widget_ui(self):
        search_widget = self.sample_widget_template.widget_def(min_size=[0, 26],
                                                               max_size=[self.sample_widget_template.max_size, 26])

        vertical_layout = self.sample_widget_template.vertical_layout(parent_self=search_widget)

        self.filter_linedit = self.sample_widget_template.line_edit(set_PlaceholderText='Filter with Name')
        self.filter_linedit.textChanged.connect(self.filter_linedit_def)

        vertical_layout.addWidget(self.filter_linedit)

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

        # SMOOTH
        smooth_text = 'SmoothNode'
        smooth_button = self.sample_widget_template.pushButton(set_text=smooth_text,
                                                               min_size=[button_size, button_size])
        smooth_button.clicked.connect(self.smooth_button_def)
        grid_layout.addWidget(smooth_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # CORRECTIVE BLENDSHAPE
        corrective_text = 'CorrectiveBlendshape'
        corrective_button = self.sample_widget_template.pushButton(set_text=corrective_text,
                                                                   min_size=[button_size, button_size])
        corrective_button.clicked.connect(self.corrective_button_def)
        grid_layout.addWidget(corrective_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # NORMAL PUSH
        normal_push_text = 'normalPush'
        normal_push_button = self.sample_widget_template.pushButton(set_text=normal_push_text,
                                                                    min_size=[button_size, button_size])
        normal_push_button.clicked.connect(self.normal_push_def)
        grid_layout.addWidget(normal_push_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # SOFT MOD
        softmod_text = 'SoftMod'
        self.softmod_push_button = self.sample_widget_template.pushButton(set_text=softmod_text,
                                                                          min_size=[button_size, button_size])
        self.softmod_push_button.clicked.connect(self.softmod_push_def)
        grid_layout.addWidget(self.softmod_push_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # SOFT MOD
        addsoftmod_set_text = 'Add SoftMod to Set'
        addsoftmod_set_toolTip = 'Select a softModHandle first, then toggle select all geo to add to its set'
        self.add_softmod_set_button = self.sample_widget_template.pushButton(set_text=addsoftmod_set_text,
                                                                             min_size=[button_size, button_size],
                                                                             set_tool_tip=addsoftmod_set_toolTip,
                                                                             connect=self.add_softmod_set_button_def)
        grid_layout.addWidget(self.add_softmod_set_button, vertical_val, new_value, 1, 1)

        vertical_val += 1
        new_value = 0

        # CLUSTER TWEAK
        cluster_tweak_text = 'Cluster_Tweak'
        cluster_tweak_push_button = self.sample_widget_template.pushButton(set_text=cluster_tweak_text,
                                                                           min_size=[button_size, button_size])
        cluster_tweak_push_button.clicked.connect(self.cluster_tweak_push_button_def)
        grid_layout.addWidget(cluster_tweak_push_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # BLEND WRAP
        blendWrap_text = 'BlendWrap'
        blendWrap_push_button = self.sample_widget_template.pushButton(set_text=blendWrap_text,
                                                                       min_size=[button_size, button_size])
        blendWrap_push_button.clicked.connect(self.blendWrap_push_button_def)
        grid_layout.addWidget(blendWrap_push_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # NOISE DEFORMER
        noiseDeform_text = 'NoiseDeform'
        noiseDeform_push_button = self.sample_widget_template.pushButton(set_text=noiseDeform_text,
                                                                         min_size=[button_size, button_size])
        noiseDeform_push_button.clicked.connect(self.noiseDeform_push_button_def)
        grid_layout.addWidget(noiseDeform_push_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # MESH COLLUTION
        meshCollution_text = 'meshCollution'
        meshCollution_push_button = self.sample_widget_template.pushButton(set_text=meshCollution_text,
                                                                           min_size=[button_size, button_size])
        meshCollution_push_button.clicked.connect(self.meshCollution_push_button_def)
        grid_layout.addWidget(meshCollution_push_button, vertical_val, new_value, 1, 1)
        new_value += 1

        # CFX TWEAK LIKE SONY

        # RigFx

        #
        vertical_val += 1
        grid_layout.addItem(self.sample_widget_template.spaceItem(), vertical_val, new_value, 1, 1)

        return main_widget

    def filter_linedit_def(self):
        '''

        :return:
        '''

        text = self.filter_linedit.text()


    def smooth_button_def(self):
        '''
        CREATE A SMOOTH NODE
        :return:
        '''
        node_type = 'smooth::2.0'
        selected_nodes = list(hou.selectedNodes())
        if selected_nodes:
            selected_nodes = selected_nodes[0]
            parent_obj = selected_nodes.parent()
            #CREATE NODE
            #GET THE NO OF THE NODE TYOE
            val = int(self.help_class.get_no_of_node_type(parent_obj, node_type))
            node_name = 'Smooth_' + str(val)
            node_name = self.node_class.smoothNode(obj_path=parent_obj, node_name=node_name, setInput=True, parent_obj=selected_nodes)
            self.help_class.setFlag(node=node_name,
                                    displayFlag=True,
                                    templateFlag=True,
                                    renderFlag=True)
            #set the position

            self.help_class.set_node_new_position(node_name, previousNode=selected_nodes)
            node_name.setColor(self.help_class.get_random_color())

        pass


    def corrective_button_def(self):
        pass

    def normal_push_def(self):
        pass

    def softmod_push_def(self):
        '''

        :return:
        '''
        pass

    def add_softmod_set_button_def(self):
        pass

    def cluster_tweak_push_button_def(self):
        '''

        :return:
        '''
        pass

    def blendWrap_push_button_def(self):
        pass

    def noiseDeform_push_button_def(self):
        '''

        :return:
        '''
        pass

    def meshCollution_push_button_def(self):
        '''

        :return:
        '''
        pass




