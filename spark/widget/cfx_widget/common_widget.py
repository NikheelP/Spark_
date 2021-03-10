from spark.widget.import_module import *

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
        # TRANSFORM CACHE NODE
        # RENAME TOOL
        # WEDGE TOOL
        # CONNECTION EDITOR
        # ASSIGN RANDOM SHADER
        # MAKE A TECHANIM SCENE
        # RIVET


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











