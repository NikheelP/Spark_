from spark.widget.import_module import *

from spark.widget.sample.sample_maya_widget import SAMPLE_WIDGET



class PLAYBLAST_SETTING(SAMPLE_WIDGET):
    def __init__(self, cacheManger_name= 'CacheManagerData', title='Playblast Setting', width=500, height=400):
        super(PLAYBLAST_SETTING, self).__init__(title=title, width=width, height=height)

        self.int_validator = QIntValidator()

        self.cache_manager_data = cacheManger_name

        # PLABLAST
        self.playblast_format_list = ['qt', 'avi', 'image']
        self.playblast_format = self.playblast_format_list[0]
        self.encodeing_list = ['Planer RGB', 'Sorenson Video', 'Sorenson Video 3', 'BMP', 'H.264', 'Cinepak',
                               'DV/DVCPRO-NTSC', 'DV-PAL']
        self.encodeing = self.encodeing_list[4]
        self.quality = 100
        self.frame_padding = 4
        self.percent = 100

        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        main_widget = self.get_main_widget()

        grid_layout = self.sample_widget_template.grid_layout(parent_self=main_widget,
                                                              set_spacing=5)

        new_value = 0
        vertical_val = 0

        #PLAYBLAST FORMART
        playblast_format_label = self.sample_widget_template.label(set_text='PlayBlast Format')
        grid_layout.addWidget(playblast_format_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.playblast_format_comboBox = self.sample_widget_template.comboBox(addItems=self.playblast_format_list)
        grid_layout.addWidget(self.playblast_format_comboBox, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        #ENCODING
        encoding_label = self.sample_widget_template.label(set_text='Encoding')
        grid_layout.addWidget(encoding_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.encodeing_comboBox = self.sample_widget_template.comboBox(addItems=self.encodeing_list)
        self.encodeing_comboBox.setCurrentIndex(4)
        grid_layout.addWidget(self.encodeing_comboBox, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        # ENCODING
        quality_label = self.sample_widget_template.label(set_text='Encoding')
        grid_layout.addWidget(quality_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.quality_lineedit = self.sample_widget_template.line_edit(set_text='100')
        grid_layout.addWidget(self.quality_lineedit, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        # ENCODING
        frame_padding_label = self.sample_widget_template.label(set_text='Frame Padding')
        grid_layout.addWidget(frame_padding_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.frame_padding_lineedit = self.sample_widget_template.line_edit(set_text='4')
        self.frame_padding_lineedit.setValidator(self.int_validator)
        grid_layout.addWidget(self.frame_padding_lineedit, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        # ENCODING
        percent_label = self.sample_widget_template.label(set_text='Percent')
        grid_layout.addWidget(percent_label, vertical_val, new_value, 1, 1)
        new_value += 1

        self.percent_lineedit = self.sample_widget_template.line_edit(set_text='100')
        self.percent_lineedit.setValidator(self.int_validator)
        grid_layout.addWidget(self.percent_lineedit, vertical_val, new_value, 1, 1)
        vertical_val += 1
        new_value = 0

        add_playblast_setting = self.sample_widget_template.pushButton(set_text='Add Playblast Setting')
        grid_layout.addWidget(add_playblast_setting, vertical_val, new_value, 1, 2)
        vertical_val += 1
        new_value = 0

        grid_layout.addItem(self.sample_widget_template.spaceItem(), vertical_val, new_value, 1, 2)


        '''
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
        '''

